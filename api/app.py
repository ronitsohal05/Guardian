import os
import json
import time
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

from db.mongo import db
from core.redis_client import redis_client

from routes.auth import auth_bp
from routes.me import me_bp
from routes.prefs import prefs_bp
from routes.stores import stores_bp
from routes.email import email_bp

CV_URL = os.getenv("CV_URL", "http://cv:8002")


def create_app():
    app = Flask(__name__)

    CORS(
        app,
        resources={r"/*": {"origins": ["http://localhost:3000", "http://localhost:5173", "http://localhost"]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/redis-test")
    def redis_test():
        redis_client.set("guardian:test", "hello")
        return jsonify({"value": redis_client.get("guardian:test")})

    @app.get("/mongo-test")
    def mongo_test():
        db["test"].insert_one({"hello": "mongo"})
        doc = db["test"].find_one(sort=[("_id", -1)])
        return jsonify({"last_doc": {"hello": doc.get("hello")}})

    @app.post("/upload-test")
    def upload_test():
        store_id = None
        items = []

        if request.form and request.form.get("store_id"):
            store_id = request.form.get("store_id")

        body = {}
        try:
            body = request.get_json(force=False) or {}
        except Exception:
            body = {}

        if not store_id:
            store_id = body.get("store_id", "store_123")

        if "image" in request.files:
            img = request.files["image"]
            files = {"image": (img.filename or "image.jpg", img.stream, img.content_type or "application/octet-stream")}
            cv_resp = requests.post(f"{CV_URL}/infer", files=files, timeout=30)
        else:
            cv_resp = requests.post(f"{CV_URL}/infer", timeout=10)

        if cv_resp.status_code != 200:
            print(f"CV error: {cv_resp.status_code} - {cv_resp.text}")
            return jsonify({"error": f"CV service error: {cv_resp.text}"}), 500

        cv_resp.raise_for_status()
        detections = cv_resp.json()
        items = [x["label"] for x in detections.get("items", [])]

        redis_client.xadd("events:surplus", {
            "store_id": store_id,
            "items": json.dumps(items),
            "timestamp": int(time.time())
        })

        return jsonify({"ok": True, "store_id": store_id, "items": items})

    app.register_blueprint(auth_bp)
    app.register_blueprint(me_bp)
    app.register_blueprint(prefs_bp)
    app.register_blueprint(stores_bp)
    app.register_blueprint(email_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
