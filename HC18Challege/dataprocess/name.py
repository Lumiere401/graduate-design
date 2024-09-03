import os
import pandas
import cv2
import csv

def read_image(directory_name, type):
    i = 0  # 计数器
    if type == 'x':
        for filename in os.listdir(directory_name):
            address = directory_name + filename
            csv_writerx.writerow([address])
    else:
        for filename in os.listdir(directory_name):
            address = directory_name + filename
            csv_writery.writerow([address])


fx = open('train_src_aug.csv', 'w', encoding= 'utf-8', newline="")
fy = open('train_mask_aug.csv', 'w', encoding= 'utf-8', newline="")
csv_writerx = csv.writer(fx)
csv_writery = csv.writer(fy)
csv_writerx.writerow(["filename"])
csv_writery.writerow(["filename"])

read_image("E:\\graduation_project\\Medical_image_segment\\HC18Challege\\dataset\\training_set\\process\\Aug\\src\\", 'x')
read_image("E:\\graduation_project\\Medical_image_segment\\HC18Challege\\dataset\\training_set\\process\\Aug\\mask\\", 'y')
