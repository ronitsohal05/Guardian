from flask import Blueprint, request, jsonify
from bson import ObjectId

from db.mongo import db
from core.auth import require_auth

prefs_bp = Blueprint("prefs", __name__)


@prefs_bp.post("/prefs")
@require_auth
def set_prefs():
    body = request.get_json(force=True) or {}

    notify = body.get("notify", True)
    radius_km = body.get("radius_km", 5)
    location = body.get("location")  # {"lat":..., "lng":...}
    item_filters = body.get("item_filters", [])

    # Validate basics
    if radius_km is not None:
        try:
            radius_km = float(radius_km)
            if radius_km <= 0 or radius_km > 100:
                return jsonify({"error": "radius_km must be between 0 and 100"}), 400
        except Exception:
            return jsonify({"error": "radius_km must be a number"}), 400

    if location is not None:
        if not isinstance(location, dict) or "lat" not in location or "lng" not in location:
            return jsonify({"error": "location must be {lat, lng}"}), 400
        try:
            lat = float(location["lat"])
            lng = float(location["lng"])
        except Exception:
            return jsonify({"error": "lat/lng must be numbers"}), 400
        if lat < -90 or lat > 90 or lng < -180 or lng > 180:
            return jsonify({"error": "lat/lng out of range"}), 400
        location = {"lat": lat, "lng": lng}

    if item_filters is None:
        item_filters = []
    if not isinstance(item_filters, list):
        return jsonify({"error": "item_filters must be a list"}), 400
    item_filters = [str(x).strip().lower() for x in item_filters if str(x).strip()]

    update = {
        "notify": bool(notify),
        "radius_km": radius_km,
        "location": location,
        "item_filters": item_filters
    }

    db["users"].update_one({"_id": ObjectId(request.user_id)}, {"$set": update})

    user = db["users"].find_one({"_id": ObjectId(request.user_id)}, {"password_hash": 0})
    user["_id"] = str(user["_id"])
    return jsonify({"ok": True, "user": user})
