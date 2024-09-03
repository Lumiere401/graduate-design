import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def canny_demo(image):
    t = 80
    canny_output = cv.Canny(image, t, t * 2)
    cv.imwrite("./canny_output.png", canny_output)
    return canny_output


def circumstance_cal(image):
    contours, hierarchy = cv.findContours(image,cv.RETR_LIST,cv.CHAIN_APPROX_NONE)
    perimeter = cv.arcLength(contours[0], True)
    return perimeter


src = cv.imread("/\\HC18Challege\dataset\\test_set\\mask\\005_HC.png")
bg = cv.imread("/\\HC18Challege\dataset\\test_set\\src\\005_HC.png")
# src = cv.imread("E:\\graduation project\\Medical_image_segment\\HC18Challege\dataset\\training_set\\process\\mask\\001_HC_Annotation.bmp")
# bg = cv.imread("E:\\graduation project\\Medical_image_segment\\HC18Challege\dataset\\training_set\\process\\src\\001_HC.bmp")
edge = canny_demo(src)
y, x = np.nonzero(edge)  # 注：矩阵的坐标系表示和绘图用的坐标系不同，故需要做坐标转换
edge_list = np.array([[_x, _y] for _x, _y in zip(x, y)])  # 边界点坐标
_ellipse = cv.fitEllipse(edge_list)  # 椭圆拟合
print(_ellipse)  # 这儿包含 椭圆的中心坐标，长短轴长度（2a，2b），旋转角度
# 如第一排图得出的参数((407.63262939453125, 425.8587341308594), (361.6327209472656, 416.6160583496094), 170.43588256835938)
edge_clone = edge.copy()
cv.ellipse(bg, _ellipse, (0, 255, 0), 5)
cv.imwrite("./bg.png", bg)

img = np.zeros((540,800,3), np.uint8)
# img.fill(255)#fill the image with white
cv.ellipse(img, _ellipse, (255, 255, 255), 5)
img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imwrite("./img.png", img)
cum = int(circumstance_cal(img) * 0.116)
print(cum)

plt.figure(figsize=(20,20))
plt.subplot(1,4,1)
cv.putText(bg, 'HC:'+ str(cum) + 'mm', (int(_ellipse[0][0]),int(_ellipse[0][1])), cv.FONT_HERSHEY_COMPLEX, 2.0, (255, 0, 0), 2)
cv.imwrite("./output.png", bg)

