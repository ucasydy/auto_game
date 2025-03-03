from ultralytics import YOLO

# Load a model
model = YOLO("./card_best.pt")  # load a custom model

# Predict with the model
results = model(r"C:\Users\Administrator\Desktop\python_blyx\dataset\data\1.png")  # predict on an image

# results[0].show()


# # Access the results
# for result in results:
#     xywh = result.boxes.xywh  # center-x, center-y, width, height
#     xywhn = result.boxes.xywhn  # normalized
#     xyxy = result.boxes.xyxy  # top-left-x, top-left-y, bottom-right-x, bottom-right-y
#     xyxyn = result.boxes.xyxyn  # normalized
#     names = [result.names[cls.item()] for cls in result.boxes.cls.int()]  # class name of each box
#     confs = result.boxes.conf  # confidence score of each box

for result in results:
    boxes = result.boxes
    for box in boxes:
        # 获取类别名称
        class_name = model.names[int(box.cls)]
        if class_name == 'fdj':
            # 获取置信度
            confidence = float(box.conf)
            # 获取边界框坐标
            bbox = box.xywh[0]
            
            # print(f"Class: {class_name}, Confidence: {confidence}, BBox: {bbox}")
            print(bbox[0], bbox[1])
