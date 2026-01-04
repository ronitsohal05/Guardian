import fiftyone as fo
import fiftyone.zoo as foz

CLASSES = [
    "Apple", "Banana", "Orange", "Grape", "Strawberry",
    "Tomato", "Potato", "Bell pepper", "Cucumber", "Carrot", "Broccoli",
    "Bread", "Cake", "Pastry", "Croissant", "Doughnut", "Muffin", "Cookie",
]

MAX_SAMPLES_TRAIN = 6000
MAX_SAMPLES_VAL = 1200
EXPORT_DIR = "./cv/model/data/openimages_produce_bakery_yolo"

print("Downloading TRAIN split...")
train = foz.load_zoo_dataset(
    "open-images-v7",
    split="train",
    label_types=["detections"],
    classes=CLASSES,
    max_samples=MAX_SAMPLES_TRAIN,
    shuffle=True,
)

print("Downloading VALIDATION split...")
val = foz.load_zoo_dataset(
    "open-images-v7",
    split="validation",
    label_types=["detections"],
    classes=CLASSES,
    max_samples=MAX_SAMPLES_VAL,
    shuffle=True,
)

print("Train fields:", list(train.get_field_schema().keys()))

# Your dataset shows this field exists:
label_field = "ground_truth"
print("Using label_field:", label_field)

print("Exporting TRAIN dataset to YOLO format...")
train.export(
    export_dir=f"{EXPORT_DIR}/train",
    dataset_type=fo.types.YOLOv5Dataset,
    label_field=label_field,
    classes=CLASSES,
)

print("Exporting VAL dataset to YOLO format...")
val.export(
    export_dir=f"{EXPORT_DIR}/val",
    dataset_type=fo.types.YOLOv5Dataset,
    label_field=label_field,
    classes=CLASSES,
)

print("\n✅ DONE!")
print(f"YOLO dataset written to: {EXPORT_DIR}/")
