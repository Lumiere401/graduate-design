from  dataprocess.Augmentation.ImageAugmentation import DataAug
import os
import pandas
import cv2
import csv

def read_image(directory_name):
    i = 0  # 计数器
    for filename in os.listdir(directory_name):
        img = cv2.imread(directory_name + "/" + filename)
        if filename.find('Annotation') > 0:

            src_path = 'E:\\graduation project\\Medical_image_segment\\HC18Challege\dataset\\training_set\\process\\mask\\'
            if not os.path.exists(src_path):
                os.makedirs(src_path)
            address = src_path + filename[:-4] + '.bmp'
            cv2.imwrite(address, img)
            csv_writery.writerow([address])
        else:
            src_path = 'E:\\graduation project\\Medical_image_segment\\HC18Challege\\dataset\\training_set\\process\\src\\'
            if not os.path.exists(src_path):
                os.makedirs(src_path)
            address = src_path + filename[:-4] + '.bmp'
            cv2.imwrite(address, img)
            csv_writerx.writerow([address])


fx = open('Train_X.csv', 'w', encoding= 'utf-8', newline="")
fy = open('Train_Y.csv', 'w', encoding= 'utf-8', newline="")
csv_writerx = csv.writer(fx)
csv_writery = csv.writer(fy)
csv_writerx.writerow(["filename"])
csv_writery.writerow(["filename"])


read_image("E:\\graduation project\\Medical_image_segment\\HC18Challege\\dataset\\src")
