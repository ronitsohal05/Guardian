from flask import Flask, jsonify

app = Flask(__name__)

@app.get('/health')
def health():
    return {"ok": True}


@app.post('/infer')
def infer():
    return jsonify(
        {
            "items": [
                {"label": "bread", "confidence": 0.998},
                {"label": "cake", "confidence": 0.87},
            ],
            "source": "stub",
            "model_version": "v0",
        }
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)