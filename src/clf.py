
import cv2
import numpy as np
from collections import defaultdict
import math
from pyzbar import pyzbar


modelConfiguration = "power-tiny.cfg"
modelWeights = "power-tiny_20000.weights"
rd = lambda x: round(math.log(x))


class Parser:
    def __init__(self):
        self.net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        # 缩放后的图像大小
        self.new_size = (416, 416)
        self.scale = 0.0054154

    def make_blob_from_file(self, image):
        image = cv2.resize(image, self.new_size)
        blob = cv2.dnn.blobFromImage(image, self.scale, self.new_size, [0,0,0], 1, crop=False)
        return blob

    def make_blob_from_files(self, images):
        blob = cv2.dnn.blobFromImages(images, self.scale, self.new_size, [0,0,0], 1, crop=False)
        return blob

    def extract(self, image_path):
        # if not multiple:
        img = cv2.imread(image_path)
        blob = self.make_blob_from_file(img)
        self.net.setInput(blob)
        out = self.net.forward(self.get_output_layers(self.net))
        outs = (image_path, out, img)
        return outs

    def do(self, outs_container):
        """根据比例切换到图像的真是边框位置"""
        fn, outs, img = outs_container
        # for fn, outs, img in outs_container:
        result = self.process_out(outs, img, fn)
        return result

    def process_out(self, outs, img, fn):
        conf_threshold = 0.5
        nms_threshold = 0.4
        class_ids = []
        confidences = []
        boxes = []
        results = []
        cutter = []
        height, width = self.new_size
        xm, ym = height / img.shape[1], width / img.shape[0]

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
            cutter.append([round(x / xm), round(x / xm + w / xm), round(y / ym), round(y / ym + h / ym)])

        for side in cutter:
            _side = []
            for i in side:
                if i < 0:
                    _side.append(0)
                else:
                    _side.append(i)

            sid_img = img[_side[2]:_side[3], _side[0]:_side[1]]
            results.append((sid_img, ((_side[2] + _side[3]) / 2, (_side[0] + _side[1]) / 2)))
        return fn, results

    def parse(self, img_path):
        maps = defaultdict(list)
        outs = self.extract(img_path)
        fn, results = self.do(outs)
        for img, center in results:
            x, _ = center
            k = rd(x)
            maps[k].append(self.extract_barcode(img))
        return maps

    @staticmethod
    def get_output_layers(net):
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        return output_layers

    @staticmethod
    def extract_barcode(img):
        from uuid import uuid4
        uid = str(uuid4())
        barcodes = pyzbar.decode(img)
        result = []
        cv2.imwrite(uid+'.jpg', img)

        for barcode in barcodes:
            code = barcode.data.decode('utf-8')
            result.append(str(code))
        return ",".join(result)

    def get_data_array(self, img_path):
        try:
            maps = self.parse(img_path)
            data = [v for _, v in maps.items()]
        except Exception as e:
            data = [['']]
        return data

    @staticmethod
    def show_img(img_path):
        cv2.namedWindow("output", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions
        im = cv2.imread(img_path)                        # Read image
        # imS = cv2.resize(im, (960, 540))                    # Resize image
        cv2.imshow("output", im)
