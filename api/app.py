from flask import Flask, jsonify
from api.db.mongo import db
from api.core.redis_client import redis_client

def create_app():
    app = Flask(__name__)

    @app.get('/health')
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

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)