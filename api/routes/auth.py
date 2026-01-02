from flask import Blueprint, request, jsonify
from bson import ObjectId
import time

from db.mongo import db
from core.auth import hash_password, verify_password, create_token

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.post("/signup")
def signup():
    body = request.get_json(force=True) or {}
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""

    if not email or "@" not in email:
        return jsonify({"error": "Valid email required"}), 400

    existing = db["users"].find_one({"email": email})
    if existing:
        return jsonify({"error": "Email already in use"}), 409
    
    try:
        password_hash = hash_password(password)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    doc = {
        "email": email,
        "password_hash": password_hash,
        "notify": True,
        "location": None,            
        "radius_km": 5,
        "item_filters": [], 
        "created_at": int(time.time())
    }

    res = db["users"].insert_one(doc)
    user_id = str(res.inserted_id)
    token = create_token(user_id)
    return jsonify({"token": token, "user_id": user_id})


@auth_bp.post("/login")
def login():
    body = request.get_json(force=True) or {}
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""

    user = db["users"].find_one({"email": email})
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not verify_password(password, user.get("password_hash", "")):
        return jsonify({"error": "Invalid credentials"}), 401

    user_id = str(user["_id"])
    token = create_token(user_id)
    return jsonify({"token": token, "user_id": user_id})