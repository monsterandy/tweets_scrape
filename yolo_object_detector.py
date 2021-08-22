# ------------------------
#   USAGE
# ------------------------
# detector = ObjectDetector()
# detector.detect_object(image_path)

# ------------------------
#   IMPORTS
# ------------------------
# import the necessary packages
import numpy as np
import cv2
import os


class ObjectDetector:
    def __init__(self,
                 yolo_path='yolo-coco',     # base path to YOLO directory
                 confidence=0.5) -> None:   # minimum probability to filter weak detections
        self.conf = confidence

        # Load the COCO class labels that our YOLO model was trained on
        labelsPath = os.path.sep.join([yolo_path, "coco.names"])
        self.LABELS = open(labelsPath).read().strip().split("\n")

        # Derive the paths to the YOLO weights and model configuration
        weightsPath = os.path.sep.join([yolo_path, "yolov4.weights"])
        configPath = os.path.sep.join([yolo_path, "yolov4.cfg"])

        # Load the YOLO object detector trained on COCO dataset (80 classes)
        print("[INFO]  Loading YOLO from disk...")
        self.net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

        # Determine only the output layer names that we need from YOLO
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def detect_object(self, path):
        # Load the input image and grab its spatial dimensions
        img = cv2.imread(path)

        # Construct a blob from the input image, perform a forward pass of the YOLO object detector and that will give us
        # bounding boxes alongside its associated probabilities
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        layerOutputs = self.net.forward(self.ln)

        max_confidence = 0
        max_classID = -1
        # Loop over each one of the layer outputs
        for output in layerOutputs:
            # loop over each one of the detections
            for detection in output:
                # extract the class ID and confidence (i.e, probability) of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > max_confidence:
                    max_classID = classID
                    max_confidence = confidence

        if max_confidence > self.conf:
            # print('{} - {}'.format(self.LABELS[max_classID], path))
            return 1
        else:
            # print('0 - {}'.format(path))
            return 0

    def detect_objects_in_image(self, path):
        # Load the input image and grab its spatial dimensions
        img = cv2.imread(path)

        # Construct a blob from the input image, perform a forward pass of the YOLO object detector and that will give us
        # bounding boxes alongside its associated probabilities
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        layerOutputs = self.net.forward(self.ln)
        classIDs = []
        max_confidence = 0
        max_classID = -1
        # Loop over each one of the layer outputs
        for output in layerOutputs:
            # loop over each one of the detections
            for detection in output:
                # extract the class ID and confidence (i.e, probability) of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > 0.25:
                    # max_classID = classID
                    # max_confidence = confidence
                    classIDs.append(self.LABELS[classID])
        
        objectString = ','.join(classIDs)
        
        return objectString
        # if max_confidence > self.conf:
        #     # print('{} - {}'.format(self.LABELS[max_classID], path))
        #     return 1
        # else:
        #     # print('0 - {}'.format(path))
        #     return 0
