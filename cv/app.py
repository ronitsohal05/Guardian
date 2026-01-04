import os
from flask import Flask, jsonify, request
import numpy as np
import onnxruntime as ort
import cv2

app = Flask(__name__)

# Load Model
MODEL_PATH = os.environ.get("MODEL_PATH", "/app/models/best.onnx")

SESSION = ort.InferenceSession(
    MODEL_PATH,
    providers=["CPUExecutionProvider"],
)

INPUT_NAME = SESSION.get_inputs()[0].name


CLASS_NAMES = [
    "apple", "banana", "orange", "grape", "strawberry",
    "tomato", "potato", "bell_pepper", "cucumber", "carrot",
    "broccoli", "bread", "cake", "pastry", "croissant",
    "doughnut", "muffin", "cookie",
]


PRINT_SHAPE_ONCE = True


# Preprocessing
def preprocess(image_bytes: bytes) -> np.ndarray:
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image. Ensure you uploaded a valid JPG/PNG.")

    img = cv2.resize(img, (640, 640))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = img.astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))  # HWC -> CHW
    img = np.expand_dims(img, axis=0)   # (1, 3, 640, 640)
    return img

# Postprocessing
def postprocess(outputs):
    p = outputs[0][0].T          # (N, D)
    scores = p[:, 4:]            # assumes D = 4 + nc
    cls_id = int(np.argmax(scores.max(axis=0)))
    return [{"label": CLASS_NAMES[cls_id]}]



# Routes
@app.get("/health")
def health():
    return {"ok": True}


@app.post("/infer")
def infer():
    global PRINT_SHAPE_ONCE

    if "image" not in request.files:
        return jsonify({"error": "image file required (form field name: 'image')"}), 400

    image_bytes = request.files["image"].read()
    if not image_bytes:
        return jsonify({"error": "empty image upload"}), 400

    try:
        input_tensor = preprocess(image_bytes)
        outputs = SESSION.run(None, {INPUT_NAME: input_tensor})

        if PRINT_SHAPE_ONCE:
            print("ONNX output shapes:", [o.shape for o in outputs])
            PRINT_SHAPE_ONCE = False

        items = postprocess(outputs)

        return jsonify(
            {
                "items": items,
                "source": "onnx",
                "model_version": "produce_bakery_v1",
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)
