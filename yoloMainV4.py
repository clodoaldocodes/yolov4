import cv2
import numpy as np

# Load YOLO model
net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")

# Define classes of objects to detect
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Load image and prepare it for detection
img = cv2.imread("image.jpg")
height, width, channels = img.shape
blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), swapRB=True, crop=False)

# Set input to the YOLO network
net.setInput(blob)

# Make detections and get the confidence scores and class IDs
output_layers = net.getUnconnectedOutLayersNames()
layer_outputs = net.forward(output_layers)
confidences = []
class_ids = []
boxes = []
for output in layer_outputs:
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Apply non-max suppression to remove overlapping boxes
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# Print the detected objects
for i in range(len(boxes)):
    if i in indexes:
        label = str(classes[class_ids[i]])
        print(label)
