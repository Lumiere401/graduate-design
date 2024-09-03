import time

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from log import LOG
from .draw_area import DrawArea
from .label_dlg import LabelDialog
from .annotation_config_dialog import AnnotationConfigDialog
from .shape import Shape
from utils.anno_file_io import AnnoFileIo
from utils.simple_dialog import WaringDlg
from config import CONF
from .ellipse_draw import Ellipse_draw

import threading
import sys
import os
# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from HC18Challege.vnet2d_predict import predict_test
from HC18Challege.vnet2d_predict import predict_test
from HC18Challege.Vnet2d.vnet_model import Vnet2dModule
#线程类
class Worker(QThread):
    progressBarValue = pyqtSignal(int)  # Signal to communicate with the progress bar

    def __init__(self, model, img_path, save_path, pixel_path, num, parent=None):
        super(Worker, self).__init__(parent)
        self.img_path = img_path
        self.save_path = save_path
        self.pixel_path = pixel_path
        self.model = model
        self.num = num

    def run(self):
        predict_test(self.model, self.img_path, self.save_path, self.pixel_path, self.progressBarValue)  # Pass the signal to the function

# 自定义列表项
class HashableQListWidgetItem(QListWidgetItem):
    def __init__(self, *args):
        super(HashableQListWidgetItem, self).__init__(*args)

    def __hash__(self):
        return hash(id(self))

class Annotation(QWidget):
    def __init__(self):
        super(Annotation, self).__init__()

        self.labels = CONF.anno_conf["labels"].split(',')
        self.curr_anno_io = None
        self.image = QImage()
        self.labelDialog = LabelDialog(parent=self, listItem=self.labels)
        self.items2shapes = {}
        self.shapes2items = {}
        self._noSelectionSlot = False
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.setStyleSheet("QPushButton:hover{background-color:rgb(160,200,240)}" #光标移动到上面后的前景色
                            "QPushButton:pressed{background-color:rgb(160,200,240);color: red;}" #按下时的样式
                            "QPushButton:checked{background-color:rgb(160,200,240);color: red;}" #按下时的样式
                            )
        tool_bt_w = 60
        tool_bt_h = 60
        list_w = 200
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # 工具按钮设置
        config_bt = QToolButton(self)
        config_bt.setFixedSize(tool_bt_w, tool_bt_h)
        config_bt.setStyleSheet(
            "QToolButton:hover{color:red}"  # 光标移动到上面后的前景色
            "QToolButton{border:none}"  # 圆角半径
            "QToolButton:pressed{background-color:rgb(180,180,180);border: None;}"  # 按下时的样式
        )
        config_bt.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        config_bt.setText('配置')
        config_bt.setIcon(QIcon(os.path.join(script_dir, '..', 'res', 'icons', 'open.png')))
        config_bt.setIconSize(QSize(30, 30))
        config_bt.setToolTip('配置')
        config_bt.clicked.connect(self.openConfigDlg)
        prev_bt = QToolButton(self)
        prev_bt.setToolTip('上一张图片')
        prev_bt.setStyleSheet(
            "QToolButton:hover{color:red}"  # 光标移动到上面后的前景色
            "QToolButton{border:none}"  # 圆角半径
            "QToolButton:pressed{background-color:rgb(180,180,180);border: None;}"  # 按下时的样式
        )
        prev_bt.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        prev_bt.setText('上一张图片')
        prev_bt.setFixedSize(tool_bt_w, tool_bt_h)
        prev_bt.setIcon(QIcon(os.path.join(script_dir, '..', 'res', 'icons', 'prev.png')))
        prev_bt.setIconSize(QSize(30, 30))
        prev_bt.clicked.connect(self.prevCB)
        next_bt = QToolButton(self)
        next_bt.setToolTip('下一张图片')
        next_bt.setStyleSheet(
            "QToolButton:hover{color:red}"  # 光标移动到上面后的前景色
            "QToolButton{border:none}"  # 圆角半径
            "QToolButton:pressed{background-color:rgb(180,180,180);border: None;}"  # 按下时的样式
        )
        next_bt.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        next_bt.setText('下一张图片')
        next_bt.setFixedSize(tool_bt_w, tool_bt_h)
        next_bt.setIcon(QIcon(os.path.join(script_dir, '..', 'res', 'icons', 'next.png')))
        next_bt.setIconSize(QSize(30, 30))
        next_bt.clicked.connect(self.nextCB)
        box_bt = QToolButton(self)
        box_bt.setStyleSheet(
            "QToolButton:hover{color:red}"  # 光标移动到上面后的前景色
            "QToolButton{border:none}"  # 圆角半径
            "QToolButton:pressed{background-color:rgb(180,180,180);border: None;}"  # 按下时的样式
        )
        box_bt.setToolTip('矩形框')
        box_bt.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        box_bt.setText('框选')
        box_bt.setIcon(QIcon(os.path.join(script_dir, '..', 'res', 'icons', 'objects.png')))
        box_bt.setIconSize(QSize(40, 40))
        box_bt.setFixedSize(tool_bt_w, tool_bt_h)
        box_bt.clicked.connect(self.newBoxCB)
        box_del_bt = QToolButton(self)
        box_del_bt.setStyleSheet(
            "QToolButton:hover{color:red}"  # 光标移动到上面后的前景色
            "QToolButton{border:none}"  # 圆角半径
            "QToolButton:pressed{background-color:rgb(180,180,180);border: None;}"  # 按下时的样式
        )
        box_del_bt.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        box_del_bt.setText('删除框')
        box_del_bt.setToolTip('删除框')
        box_del_bt.setIcon(QIcon(os.path.join(script_dir, '..', 'res', 'icons', 'cancel.png')))
        box_del_bt.setIconSize(QSize(30, 30))
        box_del_bt.setFixedSize(tool_bt_w, tool_bt_h)
        box_del_bt.clicked.connect(self.delSelShapeCB)

        del_action = QAction(self)
        #zoom_in_bt = QPushButton("放大", self)
        #zoom_in_bt.setFixedSize(tool_bt_w, tool_bt_h)
        self.zoom_value = QSpinBox()
        self.zoom_value.setRange(10, 500)
        self.zoom_value.setSingleStep(10)
        self.zoom_value.setSuffix(' %')
        self.zoom_value.setValue(100)
        self.zoom_value.setFixedSize(tool_bt_w, tool_bt_h)
        self.zoom_value.setStyleSheet("background-color:white")
        self.zoom_value.valueChanged.connect(self.zoomChange)

        #zoom_out_bt = QPushButton("缩小", self)
        #zoom_out_bt.setFixedSize(tool_bt_w, tool_bt_h)
        fin_win_bt = QToolButton(self)
        fin_win_bt.setStyleSheet(
            "QToolButton:hover{color:red}"  # 光标移动到上面后的前景色
            "QToolButton{border:none}"  # 圆角半径
            "QToolButton:pressed{background-color:rgb(180,180,180);border: None;}"  # 按下时的样式
        )
        fin_win_bt.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        fin_win_bt.setText('适应屏幕')
        fin_win_bt.setToolTip('适应屏幕')
        fin_win_bt.setIcon(QIcon(os.path.join(script_dir, '..', 'res', 'icons', 'fit-width.png')))
        fin_win_bt.setIconSize(QSize(30, 30))
        fin_win_bt.setFixedSize(tool_bt_w, tool_bt_h)
        fin_win_bt.clicked.connect(self.finWinCB)
        save_bt = QToolButton(self)
        save_bt.setStyleSheet(
            "QToolButton:hover{color:red}"  # 光标移动到上面后的前景色
            "QToolButton{border:none}"  # 圆角半径
            "QToolButton:pressed{background-color:rgb(180,180,180);border: None;}"  # 按下时的样式
        )
        save_bt.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        save_bt.setText('保存')
        save_bt.setToolTip('保存')
        save_bt.setIcon(QIcon('./res/icons/save.png'))
        save_bt.setIconSize(QSize(30, 30))
        save_bt.setFixedSize(tool_bt_w, tool_bt_h)
        save_bt.clicked.connect(self.saveCB)
        preAnnotation_start = QToolButton(self)
        preAnnotation_start.setStyleSheet(
            "QToolButton:hover{color:red}"  # 光标移动到上面后的前景色
            "QToolButton{border:none}"  # 圆角半径
            "QToolButton:pressed{background-color:rgb(180,180,180);border: None;}"  # 按下时的样式
        )
        preAnnotation_start.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        preAnnotation_start.setText('开始标注')
        preAnnotation_start.setToolTip('开始标注')
        preAnnotation_start.setIcon(QIcon(os.path.join(script_dir, '..', 'res', 'icons', 'labels.png')))
        preAnnotation_start.setIconSize(QSize(30, 30))
        preAnnotation_start.setFixedSize(tool_bt_w, tool_bt_h)
        preAnnotation_start.clicked.connect(self.StartPreAnnotation)
        self.defult_label_flg = QCheckBox("默认标签")
        self.defult_label_flg.setChecked(False)
        self.defult_label_flg.setFixedSize(60, 20)
        self.defult_label_value = QComboBox()
        self.defult_label_value.setFixedSize(60, 20)
        tool_layout = QVBoxLayout()


        tool_layout.addWidget(config_bt)
        tool_layout.addWidget(next_bt)
        tool_layout.addWidget(prev_bt)
        tool_layout.addWidget(box_bt)
        tool_layout.addWidget(box_del_bt)
        #tool_layout.addWidget(zoom_in_bt)
        tool_layout.addWidget(self.zoom_value)
        #tool_layout.addWidget(zoom_out_bt)
        tool_layout.addWidget(fin_win_bt)
        tool_layout.addWidget(save_bt)
        tool_layout.addWidget(preAnnotation_start)
        tool_layout.addWidget(QLabel(""))
        tool_layout.addWidget(self.defult_label_value)
        tool_layout.addWidget(QLabel(""))
        tool_layout.addWidget(self.defult_label_flg)
        tool_layout.addStretch(1)
        tool_layout.setContentsMargins(10,20,10,0)
        tool_layout.setSpacing(0)

        # 列表栏设置
        label_list_lab = QLabel("标签列表")
        self.label_list = QListWidget()
        self.label_list.setFixedWidth(list_w-3)
        self.label_list.itemDoubleClicked.connect(self.labelListItemDbClick)
        self.label_list.itemSelectionChanged.connect(self.labelListItemSelected)
        self.label_list.itemActivated.connect(self.labelListItemSelected)
        file_list_lab = QLabel("文件列表")
        self.file_list = QListWidget()
        self.file_list.setFixedWidth(list_w-3)
        self.file_list.itemDoubleClicked.connect(self.fileListItemDbClick)

        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(0,1,0,1)
        list_layout.setSpacing(2)
        list_layout.addWidget(label_list_lab)
        list_layout.addWidget(self.label_list)
        list_layout.addWidget(file_list_lab)
        list_layout.addWidget(self.file_list)

        list_frame = QFrame()
        list_frame.setFrameShape(QFrame.StyledPanel)
        list_frame.setLineWidth(1)
        list_frame.setFixedWidth(list_w)
        list_frame.setLayout(list_layout)

        # 绘图区域设置
        self.draw_area = DrawArea(parent=self)
        self.draw_area.zoomSignal.connect(self.zoomSignalCB)  # 缩放请求
        self.draw_area.scrollSignal.connect(self.scrollSignalCB) #滚动条
        self.draw_area.newShapeSignal.connect(self.newShapeSignalCB) #新框回调
        self.draw_area.selChangedSignal.connect(self.selChangedSignalCB)  # 绘图区域选中矩形信号
        self.draw_area.drawingSignal.connect(self.drawingSignalCB)   # 绘图区拖拽绘制信号

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.draw_area)
        self.scroll.setWidgetResizable(True)
        self.scrollBars = {
            Qt.Vertical: self.scroll.verticalScrollBar(),
            Qt.Horizontal: self.scroll.horizontalScrollBar()
        }

        win_layout = QHBoxLayout()
        win_layout.setContentsMargins(0,0,0,0)
        win_layout.setSpacing(0)
        win_layout.addWidget(list_frame)
        win_layout.addWidget(self.scroll)

        win_frame = QFrame()
        win_frame.setFrameShape(QFrame.StyledPanel)
        win_frame.setLineWidth(1)
        win_frame.setLayout(win_layout)

        vlayout = QHBoxLayout()
        vlayout.setContentsMargins(0,0,0,0)
        vlayout.setSpacing(0)
        vlayout.addLayout(tool_layout)
        vlayout.addWidget(win_frame)
        self.setLayout(vlayout)

        # 内容填充
        self.setDefultLabelItems()
        self.setFileListItems()

        # 快捷键
        del_shortcut = QShortcut(QKeySequence(Qt.Key_Delete), self)
        del_shortcut.activated.connect(self.delSelShapeCB)

        save_shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        save_shortcut.activated.connect(self.saveCB)

    # 缩放请求
    def zoomSignalCB(self, delta):
        # get the current scrollbar positions
        # calculate the percentages ~ coordinates
        h_bar = self.scrollBars[Qt.Horizontal]
        v_bar = self.scrollBars[Qt.Vertical]

        # get the current maximum, to know the difference after zooming
        h_bar_max = h_bar.maximum()
        v_bar_max = v_bar.maximum()

        # get the cursor position and draw_area size
        # calculate the desired movement from 0 to 1
        # where 0 = move left
        #       1 = move right
        # up and down analogous
        cursor = QCursor()
        pos = cursor.pos()
        relative_pos = QWidget.mapFromGlobal(self, pos)

        cursor_x = relative_pos.x()
        cursor_y = relative_pos.y()

        w = self.scroll.width()
        h = self.scroll.height()

        # the scaling from 0 to 1 has some padding
        # you don't have to hit the very leftmost pixel for a maximum-left movement
        margin = 0.1
        move_x = (cursor_x - margin * w) / (w - 2 * margin * w)
        move_y = (cursor_y - margin * h) / (h - 2 * margin * h)

        # clamp the values from 0 to 1
        move_x = min(max(move_x, 0), 1)
        move_y = min(max(move_y, 0), 1)

        # zoom in
        units = delta / (8 * 15)
        scale = 10
        self.addZoom(scale * units)

        # get the difference in scrollbar values
        # this is how far we can move
        d_h_bar_max = h_bar.maximum() - h_bar_max
        d_v_bar_max = v_bar.maximum() - v_bar_max

        # get the new scrollbar values
        new_h_bar_value = h_bar.value() + move_x * d_h_bar_max
        new_v_bar_value = v_bar.value() + move_y * d_v_bar_max

        h_bar.setValue(new_h_bar_value)
        v_bar.setValue(new_v_bar_value)

    def scrollSignalCB(self, delta, orientation):
        units = - delta / (8 * 15)
        bar = self.scrollBars[orientation]
        bar.setValue(bar.value() + bar.singleStep() * units)

    def newShapeSignalCB(self):
        """ 新框回调 """
        if not self.defult_label_flg.isChecked():
            text = self.labelDialog.popUp(labels = self.labels)
        else:
            text = self.defult_label_value.currentText()

        if text is not None:
            shape = self.draw_area.setLastLabel(text)
            self.addLabel(shape)
            self.draw_area.setEditing(True)
        else:
            self.draw_area.resetAllLines()

    # 绘图区域选中矩形信号
    def selChangedSignalCB(self, selected=False):
        if self._noSelectionSlot:
            self._noSelectionSlot = False
        else:
            shape = self.draw_area.selectedShape
            if shape:
                item = self.shapes2items[shape]
                item.setSelected(True)
            else:
                self.label_list.clearSelection()

    # 绘图区拖拽绘制信号
    def drawingSignalCB(self, drawing=True):
        if not drawing:
            self.draw_area.setEditing(True)
            self.draw_area.restoreCursor()

    def openConfigDlg(self):
        dlg = AnnotationConfigDialog(parent=self)
        if QDialog.Accepted == dlg.exec_():
            self.resetState()
            self.labels = dlg.label_list_te.toPlainText().split(',')
            self.setDefultLabelItems()
            self.setFileListItems()

    def prevCB(self):
        idx = self.file_list.row(self.file_list.currentItem())
        if idx < 0:
            return
        if idx == 0:
            WaringDlg(titile = '提示', text='已经是第一张图片', parent=self)
            return
        idx -= 1
        self.file_list.setCurrentRow(idx)
        file = self.file_list.currentItem().text()
        self.drawAreaLoadImg(file)

    def nextCB(self):
        idx = self.file_list.row(self.file_list.currentItem())
        if idx < 0:
            return
        if idx == self.file_list.count() - 1:
            WaringDlg(titile = '提示', text='已经是最后一张图片', parent=self)
            return
        idx += 1
        self.file_list.setCurrentRow(idx)
        file = self.file_list.currentItem().text()
        self.drawAreaLoadImg(file)

    def newBoxCB(self):
        self.draw_area.figure = 'rect'
        self.draw_area.setEditing(False)

    def newEllipseCB(self):
        self.ellipse = Ellipse_draw()

    def delSelShapeCB(self):
        shape = self.draw_area.deleteSelected()
        if shape is None:
            LOG.warning('rm empty label')
            return
        item = self.shapes2items[shape]
        self.label_list.takeItem(self.label_list.row(item))
        del self.shapes2items[shape]
        del self.items2shapes[item]

    def StartPreAnnotation(self):
        supports = ['.%s' % fmt.data().decode("ascii").lower() for fmt in QImageReader.supportedImageFormats()]
        images = []
        for root, dirs, files in os.walk(CONF.anno_conf["img_path"]):
            if not files:
                LOG.warning('dir empty')
                msgBox = QMessageBox(QMessageBox.Warning, 'Warning', '图片文件夹为空')
                msgBox.exec_()
                return
            for file in files:
                if not file.lower().endswith(tuple(supports)):
                    LOG.warning('no image')
                    msgBox = QMessageBox(QMessageBox.Warning, 'Warning', '图片文件夹含有非图像文件')
                    msgBox.exec_()
                    return

        files = os.listdir(CONF.anno_conf["img_path"])
        num = len(files)

        self.progressBar = QProgressDialog(self)
        self.progressBar.setWindowTitle("请稍等")
        self.progressBar.setLabelText("正在操作...")
        self.progressBar.setMinimumDuration(1000)
        self.progressBar.setCancelButtonText('用来取消按钮')
        self.progressBar.setRange(0, 100)
        self.progressBar.show()
        model = Vnet2dModule(512, 768, channels=1, costname="dice coefficient", inference=True,
                          model_path="./HC18Challege/Model/vnet2d/Vnet2d.pd")
        self.thread_1 = Worker(model, CONF.anno_conf["img_path"], CONF.anno_conf["save_path"], os.path.join(os.path.dirname(CONF.anno_conf["img_path"]), 'pixel_size.csv'), num)
        self.thread_1.progressBarValue.connect(self.progressBar.setValue)
        self.thread_1.start()

    def copy_file(self, i):
        self.progressBar.setValue(i)

    def setDefultLabelItems(self):
        self.defult_label_flg.setChecked(False)
        self.defult_label_value.clear()
        self.defult_label_value.addItems(self.labels)

    def setFileListItems(self):
        # 获取配置目录下支持的图片文件 和标签文件
        supports = ['.%s' % fmt.data().decode("ascii").lower() for fmt in QImageReader.supportedImageFormats()]
        images = []
        labels = []
        for root, dirs, files in os.walk(CONF.anno_conf["img_path"]):
            for file in files:
                if file.lower().endswith(tuple(supports)):
                    images.append(file)

        for root, dirs, files in os.walk(CONF.anno_conf["save_path"]):
            for file in files:
                if file.lower().endswith(tuple(supports)):
                    labels.append(file)

        self.file_list.clear()
        self.file_list.addItems(images)
        self.label_list.addItems(labels)


    def addLabel(self, shape):
        item = HashableQListWidgetItem(shape.label)
        self.items2shapes[item] = shape
        self.shapes2items[shape] = item
        self.label_list.addItem(item)

    def resetState(self):
        # 保存标注
        if self.curr_anno_io is not None:
            # 无论是否改变，这里都重置annos并保存
            self.curr_anno_io.clear()
            for shape in self.draw_area.shapes:
                anno = shape.toAnno()
                self.curr_anno_io.add(anno)
            self.curr_anno_io.save()
        # 状态重置
        self.draw_area.resetState()
        self.label_list.clear()
        self.zoom_value.setValue(100)
        self.items2shapes.clear()
        self.shapes2items.clear()

    def drawAreaLoadImg(self, file):
        img_file = CONF.anno_conf["img_path"] + '//' + file
        if not os.path.exists(img_file):
            LOG.error("{} non-existent".format(img_file))
            return

        # 重置状态
        self.resetState()
        self.draw_area.setEnabled(False)

        # 图片加载
        if not self.image.load(img_file):
            LOG.error("{} load failed.".format(img_file))
            return

        self.draw_area.loadPixmap(QPixmap.fromImage(self.image))
        zoom_v = self.scaleFitWindow()
        # self.setZoom(100*zoom_v)
        self.draw_area.setEnabled(True)
        self.draw_area.setFocus(True)

        # label 添加
        anno_file = CONF.anno_conf["save_path"] + '/' + file.split('.')[0] + '.txt'
        self.curr_anno_io = AnnoFileIo(anno_file)
        shapes = []
        for anno in self.curr_anno_io.annos:
            tmp_shape = Shape(label= anno['label'])
            tmp_shape.addPoint(QPoint(anno['xmin'], anno['ymin']))
            tmp_shape.addPoint(QPoint(anno['xmax'], anno['ymin']))
            tmp_shape.addPoint(QPoint(anno['xmax'], anno['ymax']))
            tmp_shape.addPoint(QPoint(anno['xmin'], anno['ymax']))
            tmp_shape.addPoint(QPoint(int((anno['xmin'] + anno['xmax']) / 2), anno['ymin'] - 30))
            tmp_shape.close()
            shapes.append(tmp_shape)
            self.addLabel(tmp_shape)
        self.draw_area.loadShapes(shapes)

        self.parent().window().state_label1.setText(file)

    def drawAreaLoadLabel(self, file):
        img_file = CONF.anno_conf["save_path"] + '//' + file
        if not os.path.exists(img_file):
            LOG.error("{} non-existent".format(img_file))
            return

        # 重置状态
        self.resetState()
        self.draw_area.setEnabled(False)

        # 图片加载
        if not self.image.load(img_file):
            LOG.error("{} load failed.".format(img_file))
            return

        self.draw_area.loadPixmap(QPixmap.fromImage(self.image))
        zoom_v = self.scaleFitWindow()
        self.setZoom(int(100 * zoom_v))
        self.draw_area.setEnabled(True)
        self.draw_area.setFocus(True)

    def fileListItemDbClick(self, item):
        file = item.text()
        self.drawAreaLoadImg(file)

    def labelListItemDbClick(self, item):
        file = item.text()
        self.drawAreaLoadLabel(file)

        if not self.draw_area.editing():
            return
        # 不支持多选，这里去选中的第一个
        items = self.label_list.selectedItems()
        item = items[0] if items else None
        if not item:
            return
        text = self.labelDialog.popUp(text=item.text(),labels = self.labels)
        if text is not None:
            item.setText(text)
            self.items2shapes[item].label = text

    def zoomChange(self):
        if self.image.isNull():
            LOG.warning('image is null.')
            return
        self.draw_area.scale = 0.01 * self.zoom_value.value()
        self.draw_area.adjustSize()
        self.draw_area.update()

    def setZoom(self, value):
        self.zoom_value.setValue(value)

    def addZoom(self, increment=10):
        self.setZoom(self.zoom_value.value() + increment)

    def scaleFitWindow(self):
        """计算最适窗口比例，注意调用前请确保image存在"""
        e = 2.0  # So that no scrollbars are generated.
        w1 = self.scroll.width() - e
        h1 = self.scroll.height() - e
        a1 = w1 / h1
        # Calculate a new scale value based on the pixmap's aspect ratio.
        w2 = self.draw_area.pixmap.width() - 0.0
        h2 = self.draw_area.pixmap.height() - 0.0
        a2 = w2 / h2
        return w1 / w2 if a2 >= a1 else h1 / h2

    def finWinCB(self):
        if self.image.isNull():
            LOG.warning('image is null.')
            return
        zoom_v = self.scaleFitWindow()
        self.setZoom(int(100*zoom_v))

    def saveCB(self):
        # 保存标注
        if self.curr_anno_io is not None:
            # 无论是否改变，这里都重置annos并保存
            self.curr_anno_io.clear()
            for shape in self.draw_area.shapes:
                anno = shape.toAnno()
                self.curr_anno_io.add(anno)
            self.curr_anno_io.save()

    # 标签列表项选中，关联到绘图区效果
    def labelListItemSelected(self):
        # 不支持多选，这里去选中的第一个
        print(self.items2shapes)
        items = self.label_list.selectedItems()
        item = items[0] if items else None
        # if item and self.draw_area.editing():
        #     self._noSelectionSlot = True
        #     self.draw_area.selectShape(self.items2shapes[item])

    # def labelListItemDbClick(self):
    #     if not self.draw_area.editing():
    #         return
    #     # 不支持多选，这里去选中的第一个
    #     items = self.label_list.selectedItems()
    #     item = items[0] if items else None
    #     if not item:
    #         return
    #     text = self.labelDialog.popUp(text=item.text(),labels = self.labels)
    #     if text is not None:
    #         item.setText(text)
    #         self.items2shapes[item].label = text

