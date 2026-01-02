import os, json, time
import redis
from pymongo import MongoClient

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://db:27017")
MONGO_DB = os.getenv("MONGO_DB", "guardian")

STREAM_KEY = os.getenv("EVENT_STREAM", "events:surplus")
GROUP = os.getenv("EVENT_GROUP", "worker-group")
CONSUMER = os.getenv("EVENT_CONSUMER", "worker-1")

DEDUP_TTL_SECONDS = int(os.getenv("DEDUP_TTL_SECONDS", "900"))
BLOCK_MS = int(os.getenv("BLOCK_MS", "5000"))

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
mongo = MongoClient(MONGO_URL)
db = mongo[MONGO_DB]

def ensure_group():
    try:
        r.xgroup_create(STREAM_KEY, GROUP, id="0", mkstream=True)
        print(f"[worker] Created group={GROUP} stream={STREAM_KEY}")
    except redis.exceptions.ResponseError as e:
        if "BUSYGROUP" not in str(e):
            raise

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

    for item in items:
        dedup_key = f"dedup:{store_id}:{item}"
        if not r.set(dedup_key, "1", nx=True, ex=DEDUP_TTL_SECONDS):
            print(f"[worker] Dedup hit {dedup_key}")
            continue

        notif = {"store_id": store_id, "item": item, "event_id": event_id, "timestamp": ts}
        db.notifications.insert_one(notif)
        print(f"[worker] NOTIFY(stub) {notif}")

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
