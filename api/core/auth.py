import os
import time
import bcrypt
import jwt
from functools import wraps
from flask import request, jsonify
from bson import ObjectId

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRES_SECONDS = int(os.getenv("JWT_EXPIRES_SECONDS", "604800"))

# Hash password using bcrypt
def hash_password(password: str) -> str:
    if not password or len(password) < 6:
        raise ValueError("Password must be at least 6 characters long.")
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

# Verify password against hash
def verify_password(password: str, password_hash: str) -> bool:
    if not password or not password_hash:
        return False
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except Exception:
        return False

# Create JWT token
def create_token(user_id: str) -> str:
    now = int(time.time())
    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + JWT_EXPIRES_SECONDS,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

# Decode and verify JWT token
def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

#Helper to extract Bearer token from Authorization header
def get_bearer_token() -> str | None:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    return auth.split(" ", 1)[1].strip()

#Validation decorator for routes that require authentication
def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = get_bearer_token()
        if not token:
            return jsonify({"error": "Missing Bearer token"}), 401
        try:
            claims = decode_token(token)
            request.user_id = claims.get("sub")
            if not request.user_id:
                return jsonify({"error": "Invalid token"}), 401
            ObjectId(request.user_id)
        except Exception:
            return jsonify({"error": "Invalid or expired token"}), 401
        return fn(*args, **kwargs)
    return wrapper