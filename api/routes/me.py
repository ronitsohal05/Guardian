from flask import Blueprint, jsonify, request
from bson import ObjectId

from db.mongo import db
from core.auth import require_auth

me_bp = Blueprint("me", __name__)


@me_bp.get("/me")
@require_auth
def me():
    user = db["users"].find_one({"_id": ObjectId(request.user_id)}, {"password_hash": 0})
    if not user:
        return jsonify({"error": "User not found"}), 404
    user["_id"] = str(user["_id"])
    return jsonify({"user": user})
