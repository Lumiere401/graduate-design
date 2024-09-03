from  dataprocess.Augmentation.ImageAugmentation import DataAug
import csv
import os

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





aug = DataAug(rotation=20, width_shift=0.01, height_shift=0.01, rescale=1.1)
aug.DataAugmentation('data\\Train_X.csv', 'data\\Train_Y.csv', 10, path="E:\\graduation project\\Medical_image_segment\\HC18Challege\dataset\\training_set\\process\\Aug\\")

read_image("E:\\graduation_project\\Medical_image_segment\\HC18Challege\\dataset\\training_set\\process\\Aug\\src\\", 'x')
read_image("E:\\graduation_project\\Medical_image_segment\\HC18Challege\\dataset\\training_set\\process\\Aug\\mask\\", 'y')
fx = open('train_src_aug.csv', 'w', encoding= 'utf-8', newline="")
fy = open('train_mask_aug.csv', 'w', encoding= 'utf-8', newline="")
csv_writerx = csv.writer(fx)
csv_writery = csv.writer(fy)
csv_writerx.writerow(["filename"])
csv_writery.writerow(["filename"])