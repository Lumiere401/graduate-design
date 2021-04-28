import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def canny_demo(image):
    t = 80
    canny_output = cv.Canny(image, t, t * 2)
    cv.imwrite("./canny_output.png", canny_output)
    return canny_output


src = cv.imread("E:\\graduation project\\HC18-Automated-measurement-of-fetal-head-circumference-master\\HC18Challege\dataset\\test_set\\mask\\000_HC.png")
bg = cv.imread("E:\\graduation project\\HC18-Automated-measurement-of-fetal-head-circumference-master\\HC18Challege\dataset\\test_set\\src\\000_HC.png")
edge = canny_demo(src)
y, x = np.nonzero(edge)  # 注：矩阵的坐标系表示和绘图用的坐标系不同，故需要做坐标转换
edge_list = np.array([[_x, _y] for _x, _y in zip(x, y)])  # 边界点坐标

_ellipse = cv.fitEllipse(edge_list)  # 椭圆拟合
print(_ellipse)  # 这儿包含 椭圆的中心坐标，长短轴长度（2a，2b），旋转角度
# 如第一排图得出的参数((407.63262939453125, 425.8587341308594), (361.6327209472656, 416.6160583496094), 170.43588256835938)
edge_clone = edge.copy()
cv.ellipse(bg, _ellipse, (255, 0, 0), 5)
plt.figure(figsize=(20,20))
plt.subplot(1,4,1)
cv.imwrite("./output.png", bg)

