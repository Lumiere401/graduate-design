import os
import sys
import matplotlib.pyplot as plt
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
from tensorflow.python.client import device_lib
from log import LOG
print(device_lib.list_local_devices())
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from .Vnet2d.vnet_model import DSVnet2dModule
from .Vnet2d.vnet_model import Vnet2dModule
import numpy as np
import pandas as pd
import cv2
import tensorflow as tf
config = tf.compat.v1.ConfigProto()
sess = tf.compat.v1.Session(config=config)
#
# class prediction:
#     def __init__(self, path):
#         predict_test(path)

def canny_demo(image):
    t = 80
    canny_output = cv2.Canny(image, t, t * 2)
    cv2.imwrite("./canny_output.png", canny_output)
    return canny_output

def circumstance_cal(image):
    contours, hierarchy = cv2.findContours(image,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    perimeter = cv2.arcLength(contours[0], True)
    return perimeter

def predict_test(model, raw_path, mask_path, pixel_path, progress_signal):
    test_set_csv = pd.read_csv(pixel_path)
    raw_test_set = raw_path + '/'
    mask_test_set = mask_path + '/'
    imagedata = test_set_csv.iloc[:, 0].values
    total_images = len(imagedata)

    for i in range(total_images):
        src_image = cv2.imread(raw_test_set + imagedata[i], cv2.IMREAD_GRAYSCALE)
        resize_image = cv2.resize(src_image, (768, 512))
        mask_image = model.prediction(resize_image)
        new_mask_image = cv2.resize(mask_image, (src_image.shape[1], src_image.shape[0]))

        edge = canny_demo(new_mask_image)
        y, x = np.nonzero(edge)
        edge_list = np.array([[_x, _y] for _x, _y in zip(x, y)])
        _ellipse = cv2.fitEllipse(edge_list)

        minx = int(_ellipse[0][0] - _ellipse[1][1] / 2)
        miny = int(_ellipse[0][1] - _ellipse[1][0] / 2)
        maxx = int(_ellipse[0][0] + _ellipse[1][1] / 2)
        maxy = int(_ellipse[0][1] + _ellipse[1][0] / 2)
        file = mask_test_set + imagedata[i].split('.')[0] + '.txt'

        try:
            with open(file, 'w', encoding='utf-8') as fp:
                anno_str = '{} {} {} {} {}\n'.format('default', minx, miny, maxx, maxy)
                fp.write(anno_str)
        except:
            LOG.error("annotation file {} non-existent".format(file))

        edge_clone = edge.copy()
        src_image = np.zeros(src_image.shape, src_image.dtype)
        cv2.ellipse(src_image, _ellipse, (255, 255, 255), 2)
        cv2.imwrite(mask_test_set + imagedata[i], src_image)

        # Update the progress bar
        progress_signal.emit(int((i + 1) / total_images * 100))

def predict_validation(path):
    '''
    Preprocessing for dataset
    '''
    Vnet2d = Vnet2dModule(512, 768, channels=1, costname="dice coefficient", inference=True,
                          model_path="log\segmeation\model\\Vnet2d.pd")
    path = path + '/'
    for i in range(990, 999, 1):
        src_image = cv2.imread(path + str(i) + ".bmp", cv2.IMREAD_GRAYSCALE)
        resize_image = cv2.resize(src_image, (768, 512))
        mask_image = Vnet2d.prediction(resize_image)
        new_mask_image = cv2.resize(mask_image, (src_image.shape[1], src_image.shape[0]))
        cv2.imwrite(path + str(i) + "mask.bmp", new_mask_image)

def predict(image):

    src = "output/"
    Vnet2d = Vnet2dModule(512, 768, channels=1, costname="dice coefficient", inference=True,
                          model_path="/\\HC18Challege\\Model\\vnet2d\\Vnet2d.pd")
    resize_image = cv2.resize(image, (768, 512))
    mask_image = Vnet2d.prediction(resize_image)
    new_mask_image = cv2.resize(mask_image, (image.shape[1], image.shape[0]))
    cv2.imwrite(src + 'output.png', new_mask_image)



#predict_test('E:/graduation_project/Medical_image_segment/HC18Challege/dataset/test_set/src', 'E:/graduation_project/Medical_image_segment/HC18Challege/dataset/test_set/new')