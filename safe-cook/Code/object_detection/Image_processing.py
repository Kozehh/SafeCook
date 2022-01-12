import numpy as np
import cv2

class Yolo:

    def __init__(self, weightsFile, cfgFile, objNamesFile):
        self.weightsFile = weightsFile
        self.cfgFile = cfgFile
        self.objNamesFile = objNamesFile
        self.net = None
        self.classes = None
        self.colors = None
        self.output_layers = None


    def load(self):
        # Ici qu'on load le modèle
        # Utiliser OpenCV pour loader un modèle YOLOv5
        net = cv2.dnn.readNet(self.weightsFile, self.cfgFile)
        classes = []
        with open(self.objNamesFile, "r") as f:
            classes = [line.strip() for line in f.readlines()]

        layers_names = net.getLayerNames()
        output_layers = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        self.net, self.classes, self.colors, self.output_layers = net, classes, colors, output_layers

    def detect_objects(self, img, net, outputLayers):
        blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
        net.setInput(blob)
        outputs = net.forward(outputLayers)
        return blob, outputs

    def processImage(self, frame, text):
        height, width, channels = frame.shape
        blob, outputs = self.detect_objects(frame, self.net, self.output_layers)
        boxes, confs, class_ids = self.get_box_dimensions(outputs, height, width)

        # Add to a string, all the objects detected in the frame
        for i in range(len(boxes)):
                text.append("Detected {}".format(
                    str(self.classes[class_ids[i]])))
                
        # TODO remove this when the oven class will be implemented and calculated in the weights
        # This hardcode the detection of a stove object
        #boxes.append([115, 135, 100, 70])
        #confs.append(1)
        #class_ids.append(2)

        return self.draw_labels(boxes, confs, self.colors, class_ids, self.classes, frame), self.process_data(confs, boxes, class_ids), text

    def process_data(self, confs, boxes, class_ids):
        data = ''
        for i in range(len(class_ids)):
            data = "#".join((data, "|".join((str(class_ids[i]), str(confs[i]), str(boxes[i])))))
        print(data)
        return data

    def draw_labels(self, boxes, confs, colors, class_ids, classes, img):
        indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                print(x, y, w, h)
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y - 5), font, 1, color, 1)
        return img

    def get_box_dimensions(self, outputs, height, width):
        boxes = []
        confs = []
        class_ids = []
        for output in outputs:
            for detect in output:
                scores = detect[5:]
                class_id = np.argmax(scores)
                conf = scores[class_id]
                if conf > 0.5:
                    center_x = int(detect[0] * width)
                    center_y = int(detect[1] * height)
                    w = int(detect[2] * width)
                    h = int(detect[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confs.append(float(conf))
                    class_ids.append(class_id)
        return boxes, confs, class_ids
