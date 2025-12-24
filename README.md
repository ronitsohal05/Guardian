# Guardian

## System Diagram
```mermaid
flowchart TD

%% Lanes keep the diagram readable
subgraph Clients
  U["Users (Mobile/Web App)"]
  S["Shop Staff (Phone Upload)"]
end

subgraph Services
  API["Backend API (FastAPI/Flask)"]
  CV["CV Inference Service (YOLO/CLIP)"]
  W["Worker (Matcher + Notifier)"]
end

subgraph Data
  R[("Redis")]
  DB[("Primary DB (Postgres/Mongo)")]
end

subgraph External
  N["Push/SMS/Email Provider"]
end

%% Main flow
S -->|"1) Upload image + store_id"| API
API -->|"2) Send image"| CV
CV -->|"3) Detections"| API

API -->|"4a) Save long-term"| DB
API -->|"4b) Cache surplus (TTL)"| R
API -->|"4c) Enqueue event"| R

R -->|"5) Event"| W
W -->|"6) Pref + Geo lookup"| R
W -->|"7) Dedup key"| R
W -->|"8) Notify"| N
N -->|"9) Alert"| U

U -->|"10) Refresh feed"| API
API -->|"11) Read live surplus"| R
API -->|"12) Read profile/history (optional)"| DB
API -->|"13) Return feed"| U
```

## Architecture Diagram

```mermaid
flowchart LR
  %% =========================
  %% Guardian MVP Architecture
  %% =========================

  subgraph Client["Client Layer"]
    U["Web/Mobile App"]
    S["Shop Portal (Upload)"]
  end

  subgraph Edge["Edge / API Layer"]
    LB["HTTPS / Reverse Proxy (NGINX)"]
    API["FastAPI Backend\n(Auth • Feed • Upload)"]
  end

  subgraph Compute["Compute Layer"]
    W["Worker Service\n(Match + Notify)"]
    CV["CV Service\n(Detect items)\n(MVP: stub)"]
  end

  subgraph Data["Data Layer"]
    R[("Redis\nCache • Queue • Dedup • Geo/Prefs")]
    DB[("Postgres\nUsers • Stores • Notification history")]
    OBJ[("Object Storage\n(Optional)\nImages")]
  end

  subgraph External["External Providers (Optional)"]
    PUSH["Push/SMS/Email\n(FCM/Twilio/SendGrid)"]
  end

  %% Client -> API
  U -->|"HTTPS"| LB --> API
  S -->|"HTTPS (image upload)"| LB --> API

  %% API -> CV + storage
  API -->|"Invoke inference"| CV
  API -->|"Store image (optional)"| OBJ

  %% API -> Data
  API -->|"Read/Write"| DB
  API -->|"Cache live surplus (TTL)\nEnqueue events"| R

  %% Worker -> Data + Providers
  R -->|"Pop events (BRPOP/Streams)"| W
  W -->|"Geo + Pref lookup\nDedup key (NX+TTL)"| R
  W -->|"Persist notification (optional)"| DB
  W -->|"Send alerts"| PUSH

  %% Alerts to users
  PUSH -->|"Notification"| U
```
