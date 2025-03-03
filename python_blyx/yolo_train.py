from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data="yolo_train_yaml.yaml", epochs=100, imgsz=640,name="blyx")