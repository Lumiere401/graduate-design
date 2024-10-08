from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from math import sqrt

DEFAULT_LINE_COLOR = QColor(0, 255, 0, 128)
DEFAULT_FILL_COLOR = QColor(255, 0, 0, 128)
DEFAULT_SELECT_LINE_COLOR = QColor(255, 255, 255)
DEFAULT_SELECT_FILL_COLOR = QColor(0, 128, 255, 155)
DEFAULT_VERTEX_FILL_COLOR = QColor(0, 255, 0, 255)
DEFAULT_HVERTEX_FILL_COLOR = QColor(255, 0, 0)
MIN_Y_LABEL = 10

# 点距离
def distance(p):
    return sqrt(p.x() * p.x() + p.y() * p.y())

class Shape(object):
    P_SQUARE, P_ROUND = range(2)

    MOVE_VERTEX, NEAR_VERTEX = range(2)

    # The following class variables influence the drawing
    # of _all_ shape objects.
    line_color = DEFAULT_LINE_COLOR
    fill_color = DEFAULT_FILL_COLOR
    select_line_color = DEFAULT_SELECT_LINE_COLOR
    select_fill_color = DEFAULT_SELECT_FILL_COLOR
    vertex_fill_color = DEFAULT_VERTEX_FILL_COLOR
    hvertex_fill_color = DEFAULT_HVERTEX_FILL_COLOR
    point_type = P_ROUND
    point_size = 8
    scale = 1.0
    angle = 0
    rotate_point = QPoint

    def __init__(self, label=None, line_color=DEFAULT_LINE_COLOR, difficult=False, paintLabel=False):
        self.label = label
        self.points = []
        self.fill = False
        self.selected = False
        self.difficult = difficult
        self.paintLabel = paintLabel

        self._highlightIndex = None
        self._highlightMode = self.NEAR_VERTEX
        self._highlightSettings = {
            self.NEAR_VERTEX: (4, self.P_ROUND),
            self.MOVE_VERTEX: (1.5, self.P_SQUARE),
        }

        self._closed = False

        if line_color is not None:
            # Override the class line_color attribute
            # with an object attribute. Currently this
            # is used for drawing the pending line a different color.
            self.line_color = line_color

    def close(self):
        self._closed = True

    def reachMaxPoints(self):
        if len(self.points) >= 5:
            return True
        return False

    def addPoint(self, point):
        if not self.reachMaxPoints():
            self.points.append(point)

    def popPoint(self):
        if self.points:
            return self.points.pop()
        return None

    def isClosed(self):
        return self._closed

    def setOpen(self):
        self._closed = False

    def toAnno(self):
        return {'label':self.label, 
                'xmin':str(int(self.points[0].x())), 
                'ymin':str(int(self.points[0].y())), 
                'xmax':str(int(self.points[2].x())), 
                'ymax':str(int(self.points[2].y()))}

    # 绘制形状
    def paint(self, painter):
        if self.points:
            color = self.select_line_color if self.selected else self.line_color
            pen = QPen(color)
            # Try using integer sizes for smoother drawing(?)
            pen.setWidth(max(1, int(round(2.0 / self.scale))))
            painter.setPen(pen)


            line_path = QPainterPath()
            vrtx_path = QPainterPath()
            line_path.moveTo(self.points[0])

            for i, p in enumerate(self.points[0:4]):
                line_path.lineTo(p)
                self.drawVertex(vrtx_path, i)  #画端点
            if self.isClosed():
                line_path.lineTo(self.points[0])

            if len(self.points) < 2:
                painter.drawPath(line_path)
                painter.drawPath(vrtx_path)
                painter.fillPath(vrtx_path, self.vertex_fill_color)
            else:
                width = self.points[2].x() - self.points[0].x()
                height = self.points[2].y() - self.points[0].y()
                rec = QRectF(self.points[0].x(), self.points[0].y(), int(width), int(height))
                d = self.point_size / self.scale
                self.rotate_point = QPointF(int((self.points[0].x() + self.points[2].x()) / 2), self.points[0].y() - 30)
                vrtx_path.addEllipse(self.rotate_point, d / 2.0, d / 2.0)
                # painter.translate(self.points[0].x() + width / 2, self.points[0].y() + height / 2)
                # painter.rotate(self.angle)
                painter.drawEllipse(rec)
                painter.drawPath(vrtx_path)
                # painter.resetTransform()
                painter.fillPath(vrtx_path, self.vertex_fill_color)


            # Draw text at the top-left
            if self.paintLabel:
                min_x = sys.maxsize
                min_y = sys.maxsize
                for point in self.points:
                    min_x = min(min_x, point.x())
                    min_y = min(min_y, point.y())
                if min_x != sys.maxsize and min_y != sys.maxsize:
                    font = QFont()
                    font.setPointSize(8)
                    font.setBold(True)
                    painter.setFont(font)
                    if(self.label == None):
                        self.label = ""
                    if(min_y < MIN_Y_LABEL):
                        min_y += MIN_Y_LABEL
                    painter.drawText(min_x, min_y, self.label)

            if self.fill:
                color = self.select_fill_color if self.selected else self.fill_color
                pen = QPen(self.line_color)
                pen.setStyle(Qt.DashDotLine)
                painter.setPen(pen)
                painter.drawPath(line_path)
                #painter.fillPath(line_path, color)


    def drawVertex(self, path, i):
        d = self.point_size / self.scale
        shape = self.point_type
        point = self.points[i]
        if i == self._highlightIndex:
            size, shape = self._highlightSettings[self._highlightMode]
            d *= size
        if self._highlightIndex is not None:
            self.vertex_fill_color = self.hvertex_fill_color
        else:
            self.vertex_fill_color = Shape.vertex_fill_color
        if shape == self.P_SQUARE:
            path.addRect(point.x() - d / 2, point.y() - d / 2, d, d)
        elif shape == self.P_ROUND:
            path.addEllipse(point, d / 2.0, d / 2.0)
        else:
            assert False, "unsupported vertex shape"

    def nearestVertex(self, point, epsilon):
        for i, p in enumerate(self.points):
            if distance(p - point) <= epsilon:
                return i
        return None

    def containsPoint(self, point):
        return self.makePath().contains(point)

    def makePath(self):
        path = QPainterPath(self.points[0])
        for p in self.points[1:3]:
            path.lineTo(p)
        return path

    def boundingRect(self):
        return self.makePath().boundingRect()

    def moveBy(self, offset):
        self.points = [p + offset for p in self.points]

    def moveVertexBy(self, i, offset):
        self.points[i] = self.points[i] + offset

    def highlightVertex(self, i, action):
        self._highlightIndex = i
        self._highlightMode = action

    def highlightClear(self):
        self._highlightIndex = None

    def copy(self):
        shape = Shape("%s" % self.label)
        shape.points = [p for p in self.points]
        shape.fill = self.fill
        shape.selected = self.selected
        shape._closed = self._closed
        if self.line_color != Shape.line_color:
            shape.line_color = self.line_color
        if self.fill_color != Shape.fill_color:
            shape.fill_color = self.fill_color
        shape.difficult = self.difficult
        return shape

    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = value
