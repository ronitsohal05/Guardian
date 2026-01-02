import os, json, time, math
import redis
from pymongo import MongoClient

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://db:27017")
MONGO_DB = os.getenv("MONGO_DB", "guardian")

STREAM_KEY = os.getenv("EVENT_STREAM", "events:surplus")
GROUP = os.getenv("EVENT_GROUP", "worker-group")
CONSUMER = os.getenv("EVENT_CONSUMER", "worker-1")

DEDUP_TTL_SECONDS = int(os.getenv("DEDUP_TTL_SECONDS", "900"))
BLOCK_MS = int(os.getenv("BLOCK_MS", "5000"))

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
mongo = MongoClient(MONGO_URI)
db = mongo[MONGO_DB]

def ensure_group():
    try:
        r.xgroup_create(STREAM_KEY, GROUP, id="0", mkstream=True)
        print(f"[worker] Created group={GROUP} stream={STREAM_KEY}")
    except redis.exceptions.ResponseError as e:
        if "BUSYGROUP" not in str(e):
            raise


def haversine_km(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def process(event_id: str, fields: dict):
    store_id = fields.get("store_id")
    items = fields.get("items", "[]")
    ts = fields.get("timestamp") or int(time.time())

    if isinstance(items, str):
        try:
            items = json.loads(items)
        except Exception:
            items = []

    if not store_id or not isinstance(items, list):
        print(f"[worker] Bad event {event_id}: {fields}")
        return

    store = db["stores"].find_one({"_id": store_id})
    if not store or not store.get("location"):
        print(f"[worker] Store not found or missing location: {store_id}")
        return

    s_lat = float(store["location"]["lat"])
    s_lng = float(store["location"]["lng"])

    # Only users opted into notify and with a location set
    users = db["users"].find({"notify": True, "location": {"$ne": None}})

    for user in users:
        user_id = str(user["_id"])
        loc = user.get("location") or {}
        try:
            u_lat = float(loc["lat"])
            u_lng = float(loc["lng"])
        except Exception:
            continue

        radius_km = float(user.get("radius_km", 5) or 5)
        dist = haversine_km(u_lat, u_lng, s_lat, s_lng)
        if dist > radius_km:
            continue

        filters = user.get("item_filters", []) or []
        filters = [str(x).strip().lower() for x in filters if str(x).strip()]
        for item in items:
            item = str(item).strip().lower()
            if not item:
                continue
            if filters and item not in filters:
                continue

            # Dedup per user+store+item
            dedup_key = f"dedup:{user_id}:{store_id}:{item}"
            if not r.set(dedup_key, "1", nx=True, ex=DEDUP_TTL_SECONDS):
                print(f"[worker] Dedup hit {dedup_key}")
                continue

            notif = {
                "user_id": user_id,
                "store_id": store_id,
                "item": item,
                "event_id": event_id,
                "timestamp": int(ts),
                "distance_km": dist
            }
            db["notifications"].insert_one(notif)
            print(f"[worker] MATCH -> notify stub: {notif}")

def main():
    ensure_group()
    print("[worker] loop starting...")
    while True:
        resp = r.xreadgroup(GROUP, CONSUMER, {STREAM_KEY: ">"}, count=10, block=BLOCK_MS)
        if not resp:
            continue
        for _, messages in resp:
            for event_id, fields in messages:
                process(event_id, fields)
                r.xack(STREAM_KEY, GROUP, event_id)

if __name__ == "__main__":
    main()
