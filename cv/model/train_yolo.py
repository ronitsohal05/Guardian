from pathlib import Path
import torch
from ultralytics import YOLO

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR / "runs_guardian"

DATA_YAML = SCRIPT_DIR / "data" / "openimages_produce_bakery_yolo" / "data.yaml"
BASE_MODEL = "yolov8n.pt"

# Training parameters
EPOCHS = 40
IMGSZ = 640
VAL_IMGSZ = 512
BATCH = 8
DEVICE = "mps"


def main():
    if not DATA_YAML.exists():
        raise FileNotFoundError(
            f"Couldn't find {DATA_YAML}\n"
            "Make sure data.yaml exists relative to this script."
        )

    print("Torch:", torch.__version__)
    print("MPS available:", torch.backends.mps.is_available())
    print("Training device:", DEVICE)
    print("Dataset YAML:", DATA_YAML)

    last_checkpoint = PROJECT_DIR / "produce_bakery_yolov8n" / "weights" / "last.pt"

    if last_checkpoint.exists():
        print(f"Resuming training from: {last_checkpoint}")
        model = YOLO(str(last_checkpoint))
        model.train(resume=True)
    else:
        print("No last.pt found; starting fresh training run")
        model = YOLO(BASE_MODEL)
        model.train(
            data=str(DATA_YAML),
            epochs=EPOCHS,
            imgsz=IMGSZ,
            batch=BATCH,
            device=DEVICE,
            project=str(PROJECT_DIR),
            name="produce_bakery_yolov8n",
            patience=10,
            cache=True,
            amp=False,
        )

    # Validation
    metrics = model.val(
        data=str(DATA_YAML),
        imgsz=VAL_IMGSZ,
        batch=BATCH,
        device=DEVICE,
        max_det=100,
        conf=0.25,
    )

    print("\n Done")
    try:
        print("mAP50-95:", float(metrics.box.map))
        print("mAP50   :", float(metrics.box.map50))
        print("mAP75   :", float(metrics.box.map75))
    except Exception:
        print("Validation metrics object:", metrics)

    print("\nArtifacts saved under:")
    print(PROJECT_DIR / "produce_bakery_yolov8n")
    print("Best weights:")
    print(PROJECT_DIR / "produce_bakery_yolov8n" / "weights" / "best.pt")


if __name__ == "__main__":
    main()
