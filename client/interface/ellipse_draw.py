# ifndef DRAWQWIDGET_H
# define DRAWQWIDGET_H
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# include <QKeyEvent>
# include <qpoint.h>
# include <qpen.h>

DRAW_SHAP_E = ['DRAW_RECT','DRAW_ELLIPSE','DRAW_NO']

class Ellipse_draw(QWidget):
    def __init__(self):
        super(Ellipse_draw, self).__init__()

        # 椭圆区域相关变量和函数
        # 注意: drawEllipse(20, 20, 210, 160);第1，2个参数表示圆 / 椭圆距屏幕左上角的像素数，第3, 4个参数表示圆 / 椭圆的宽度和高度。
        # 更加确切地表述，这个圆或椭圆是在矩形中，这个矩形的左上角的顶点在坐标轴中的位置为（20，20），这个圆或椭圆的中心为这个矩形的中心

        self.ellipse_mouse_pos = 'ELLIPSE_OUTSIDE' #上顶角#下顶角#左顶角#右顶角#区域内部 # 区域外部
        self.ellipse_left = 0# 表示椭圆右上角的X坐标
        self.ellipse_top = 0# 表示椭圆右上角的Y坐标
        self.ellipse_width = 0# 表示椭圆的宽(即水平长度)
        self.ellipse_height = 0# 表示椭圆的高(即垂直长度)
        self.ellipse_middle_x = 0
        self.ellipse_middle_y = 0
        self.ellipse_polygon = []
        self._cursor = Qt.ArrowCursor


        self.picture_image = QImage
        self.picture_image_w = 0
        self.picture_image_h = 0

        self.setMouseTracking(True)



        self.new_mouse_pos = QPoint
        self.old_mouse_pos = QPoint
        self.m_difference_x = 0
        self.m_difference_y = 0
        self.painter = QPainter
        self.frame_pen = QPen(QColor(0,174,255),2)
        self.red_point_pen = QPen(QColor(255,0,0),4)
        self.is_mouse_pressed = False
        self.timer_id = self.startTimer(20)   #开启定时器，每隔20ms 执行一次timerEvent
        self.setMouseTracking(True)

        self.BoundaryRange = 6 #触发范围


        self.ellipse_init_region()


    def timerEvent(self, event):
        self.update()  #刷新

    def paintEvent(self, event):
        self.painter.begin()
        self.painter.drawImage(QRectF(0, 0, self.width(), self.height()), self.picture_image)
        self.painter.setPen(self.frame_pen)#绘制边框线
        self.painter.drawEllipse(QRect(self.ellipse_left, self.ellipse_top, self.ellipse_width, self.ellipse_height))
        self.painter.drawPoints(QPolygon(self.ellipse_polygon))
        self.painter.end()


    def mousePressEvent(self, event):
        # if not event.is_start_draw:
        #     return
        self.is_mouse_pressed = True


    def mouseMoveEvent(self, event):
        # if not event.is_start_draw:
        #     return
        self.new_mouse_pos = event.pos()
        if event.is_mouse_pressed:
            self.m_difference_x = self.new_mouse_pos.x() - self.old_mouse_pos.x();
            self.m_difference_y = self.new_mouse_pos.y() - self.old_mouse_pos.y();
            self.ellipse_change_region()
        else:
            self.ellipse_mouse_pos = self.ellipse_get_mouse_pos(self.new_mouse_pos.x(), self.new_mouse_pos.y());

        self.old_mouse_pos = self.new_mouse_pos;

    def mouseReleaseEvent(self, event):
        event.is_mouse_pressed = False

    def ellipse_init_region(self):

        self.ellipse_left = 100
        self.ellipse_top = 200
        self.ellipse_width = 101
        self.ellipse_height = 101
        self.ellipse_mouse_pos = 'ELLIPSE_OUTSIDE'
        self.ellipse_update_region()


    def ellipse_update_region(self): #点更新
        self.ellipse_middle_x = self.ellipse_left + (self.ellipse_width / 2)
        self.ellipse_middle_y = self.ellipse_top + (self.ellipse_height / 2)
        self.ellipse_polygon = []
        self.ellipse_polygon.append(QPoint(self.ellipse_middle_x, self.ellipse_top)) #上顶角 \
        self.ellipse_polygon.append(QPoint(self.ellipse_left + self.ellipse_width, self.ellipse_middle_y))#右顶角 \
        self.ellipse_polygon.append(QPoint(self.ellipse_middle_x, self.ellipse_top + self.ellipse_height)) #下顶角 \
        self.ellipse_polygon.append(QPoint(self.ellipse_left, self.ellipse_middle_y)) #左顶角



    def ellipse_change_region(self):
        if self.ellipse_mouse_pos == 'ELLIPSE_UPPER':
            self.ellipse_top += self.m_difference_y
            self.ellipse_height -= self.m_difference_y
        elif self.ellipse_mouse_pos == 'ELLIPSE_LOWER':
            self.ellipse_height += self.m_difference_y
        elif self.ellipse_mouse_pos == 'ELLIPSE_LEFT':
            self.ellipse_left += self.m_difference_x
            self.ellipse_width -= self.m_difference_x
        elif self.ellipse_mouse_pos == 'ELLIPSE_RIGHT':
            self.ellipse_width += self.m_difference_x
        elif self.ellipse_mouse_pos == 'ELLIPSE_INSIDE':
            self.ellipse_top += self.m_difference_y
            self.ellipse_left += self.m_difference_x
        elif self.ellipse_mouse_pos == 'ELLIPSE_OUTSIDE':
            return
        self.ellipse_update_region()


    def ellipse_get_mouse_pos(self, pos_x, pos_y):  #确定鼠标改变形状位置

        if (pos_x < self.ellipse_left or pos_x > (self.ellipse_left + self.ellipse_width) or pos_y < self.ellipse_top or pos_y > (self.ellipse_top + self.ellipse_height)):
            self.overrideCursor(Qt.ArrowCursor)
            return 'ELLIPSE_OUTSIDE'
        elif (pos_y <= self.ellipse_top + self.BoundaryRange): #上顶角
            if (pos_x >= (self.ellipse_middle_x - 3) and pos_x <= (self.ellipse_middle_x + 3)):
                self.overrideCursor(Qt.SizeVerCursor)
                return 'ELLIPSE_UPPER'
            else:
                self.overrideCursor(Qt.SizeAllCursor)
                return 'ELLIPSE_INSIDE'
        elif (pos_y >= self.ellipse_top + self.ellipse_height - self.BoundaryRange): #下顶角
            if (pos_x >= (self.ellipse_middle_x-3) and pos_x <= (self.ellipse_middle_x+3)):
                self.overrideCursor(Qt.SizeVerCursor)
                return 'ELLIPSE_LOWER'
            else:
                self.overrideCursor(Qt.SizeAllCursor)
                return 'ELLIPSE_INSIDE'
        elif (pos_x <= self.ellipse_left + self.BoundaryRange): # 左顶角
            if (pos_y >= (self.ellipse_middle_y-3) and pos_y <= (self.ellipse_middle_y+3)):
                self.overrideCursor(Qt.SizeHorCursor) # <-->
                return 'ELLIPSE_LEFT'
            else:
                self.overrideCursor(Qt.SizeAllCursor)
                return 'ELLIPSE_INSIDE'
        elif (pos_x >= self.ellipse_left + self.ellipse_width - self.BoundaryRange): # 右顶角
            if (pos_y >= (self.ellipse_middle_y-3) and pos_y <= (self.ellipse_middle_y+3)):
                self.overrideCursor(Qt.SizeHorCursor)  # <-->
                return 'ELLIPSE_RIGHT'
            else:
                self.overrideCursor(Qt.SizeAllCursor)
                return 'ELLIPSE_INSIDE'
        else:
            self.overrideCursor(Qt.SizeAllCursor)
            return 'ELLIPSE_INSIDE'



    def set_picture_image(self, file_name):
        image_tmp = QImage
        image_tmp.load(file_name)
        if not image_tmp.isNull():
            self.picture_image = image_tmp
            self.picture_image_w = image_tmp.width()
            self.picture_image_h = image_tmp.height()

    def currentCursor(self):
        cursor = QApplication.overrideCursor()
        if cursor is not None:
            cursor = cursor.shape()
        return cursor

    def overrideCursor(self, cursor):
        self._cursor = cursor
        if self.currentCursor() is None:
            QApplication.setOverrideCursor(cursor)
        else:
            QApplication.changeOverrideCursor(cursor)

