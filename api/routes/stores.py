from flask import Blueprint, request, jsonify

from db.mongo import db

stores_bp = Blueprint("stores", __name__)

@stores_bp.post("/stores")
def create_store():
    body = request.get_json(force=True) or {}
    store_id = (body.get("store_id") or "").strip()
    name = (body.get("name") or "").strip()
    location = body.get("location")

    if not store_id:
        return jsonify({"error": "store_id required"}), 400
    if not name:
        return jsonify({"error": "name required"}), 400
    if not isinstance(location, dict) or "lat" not in location or "lng" not in location:
        return jsonify({"error": "location must be {lat, lng}"}), 400

    try:
        lat = float(location["lat"])
        lng = float(location["lng"])
    except Exception:
        return jsonify({"error": "lat/lng must be numbers"}), 400

    doc = {
        "_id": store_id,  # use store_id as Mongo _id
        "name": name,
        "location": {"lat": lat, "lng": lng}
    }

    existing = db["stores"].find_one({"_id": store_id})
    if existing:
        db["stores"].update_one({"_id": store_id}, {"$set": doc})
        return jsonify({"ok": True, "store_id": store_id, "updated": True})

    db["stores"].insert_one(doc)
    return jsonify({"ok": True, "store_id": store_id, "created": True})


@stores_bp.get("/stores")
def list_stores():
    stores = list(db["stores"].find({}))
    out = []
    for s in stores:
        out.append({
            "store_id": s["_id"],
            "name": s.get("name"),
            "location": s.get("location")
        })
    return jsonify({"stores": out})
