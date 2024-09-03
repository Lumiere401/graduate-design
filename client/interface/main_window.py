from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ctypes.wintypes import *
from .annotation import Annotation
from .training import Training
from .library import Library
from .about import About
from res.res import *
from log import LOG
from .shadow import RoundShadow

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        # 无窗体窗口
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 初始化窗口大小
        self.resize(1024,800)
        # 窗口最小大小
        self.setMinimumSize(1024,800)
        
        self.top_bts = []
        self.buildLayout()

        self.pages = []
        self.pages.append(Annotation())
        self.pages.append(Training())
        self.pages.append(Library())
        self.pages.append(About())
        self.centre_layout.addWidget(self.pages[0])
        self.centre_layout.addWidget(self.pages[1])
        self.centre_layout.addWidget(self.pages[2])
        self.centre_layout.addWidget(self.pages[3])
        
        # 默认显示标注界面
        self.current = 0
        self.centre_layout.setCurrentIndex(self.current)
        self.anno_bt.setChecked(True)

    def mousePressEvent(self, event):
        ''' 重写鼠标按下事件，以实现窗口的移动 '''
        if event.buttons() == Qt.LeftButton:
            self.last_position = event.globalPos()-self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        ''' 重写鼠标移动事件，以实现窗口的移动 '''
        try:
            if event.buttons() and Qt.LeftButton:
                # move相对于鼠标按下时窗口位置的偏移大小
                self.move(event.globalPos()-self.last_position)
                event.accept()
        except AttributeError:
            pass

    def nativeEvent(self, eventType, message):
        ''' 重写native事件，以实现窗口的放缩 '''
        result = 0
        msg2 = ctypes.wintypes.MSG.from_address(message.__int__())
        # 捕获改变窗口大小标志的范围，即鼠标在边框向内的第1-5个像素出现改变窗口大小标志
        minV,maxV = 1,5
        if msg2.message == 0x0084:
            xPos = (msg2.lParam & 0xffff) - self.frameGeometry().x()
            yPos = (msg2.lParam >> 16) - self.frameGeometry().y()

            if(xPos > minV and xPos < maxV):
                result = 10
            elif(xPos > (self.width() - maxV) and xPos < (self.width() - minV)):
                result = 11
            elif(yPos > minV and yPos < maxV):
                result = 12
            elif(yPos > (self.height() - maxV) and yPos < (self.height() - minV)):
                result = 15
            elif(xPos > minV and xPos < maxV and yPos > minV and yPos < maxV):
                result = 13
            elif(xPos > (self.width() - maxV) and xPos < (self.width() - minV) and yPos > minV and yPos < maxV):
                result = 14
            elif(xPos > minV and xPos < maxV and yPos > (self.height() - maxV) and yPos < (self.height() - minV)):
                result = 16
            elif(xPos > (self.width() - maxV) and xPos < (self.width() - minV) and yPos > (self.height() - maxV) and yPos < (self.height() - minV)):
                result = 17
            else:
                return (False,2)
            return (True,result)
        ret= QWidget.nativeEvent(self,eventType,message)
        return ret

    def buildLayout(self):
        wid_h = 40
        wid_w = 80
        # 顶部容器，使用顶部水平布局对象布局
        top_back_widget = QWidget()
        # logo
        logo_img = QPixmap('./res/icons/icon.png')

        logo_label = QLabel()
        logo_label.setFixedSize(wid_h,wid_h)
        logo_label.setPixmap(logo_img)
        logo_label.setScaledContents(True)
        # title
        app_title = QLabel()
        app_title.setText("医学图像分割标注系统")
        app_title.setStyleSheet('font-size:20px;padding-left:1px;')
        app_title.setFixedSize(250,wid_h)
        # 数据标注button
        self.anno_bt = QPushButton("数据标注", top_back_widget)
        self.anno_bt.setFlat(True)
        self.anno_bt.setFixedSize(wid_w,wid_h)
        self.anno_bt.clicked.connect(lambda:self.switchPage(0))
        self.anno_bt.setCheckable(True)
        self.anno_bt.setAutoExclusive(True)
        self.top_bts.append(self.anno_bt)
        # 模型训练button
        train_bt = QPushButton("可视化训练", top_back_widget)
        train_bt.setFlat(True)
        train_bt.setFixedSize(wid_w,wid_h)
        train_bt.clicked.connect(lambda:self.switchPage(1))
        train_bt.setCheckable(True)
        train_bt.setAutoExclusive(True)
        self.top_bts.append(train_bt)

        about_bt = QPushButton("关于", top_back_widget)
        about_bt.setFlat(True)
        about_bt.setFixedSize(wid_w,wid_h)
        about_bt.clicked.connect(lambda:self.switchPage(3))
        about_bt.setCheckable(True)
        about_bt.setAutoExclusive(True)
        self.top_bts.append(about_bt)

        # 最小化button
        min_bt = QPushButton(self)
        min_bt.setStyleSheet('''QPushButton{
    background:#6C6C6C;
    color:white;
    box-shadow: 1px 1px 3px rgba(0,0,0,0.3);font-size:16px;border-radius: 8px;font-family: 微软雅黑;
}
QPushButton:hover{                    
    background:#9D9D9D;
}
QPushButton:pressed{
    border: 1px solid #3C3C3C!important;
}''')
        #min_bt.setFlat(True)
        min_bt.setFixedSize(16,16)
        min_bt.clicked.connect(self.showMinimized)
        # 最大化button
        max_bt = QPushButton(self)
        max_bt.setStyleSheet('''QPushButton{
                                            background:#4AC44E;
                                            color:white;
                                            box-shadow: 1px 1px 3px rgba(0,0,0,0.3);
                                            font-size:16px;
                                            border-radius: 8px;
                                            font-family: 微软雅黑;}
                                        QPushButton:hover{                    
                                            background:#FF2D2D;
                                        }
                                        QPushButton:pressed{
                                            border: 1px solid #3C3C3C!important;
                                            background:#AE0000;
                                        }''')
        max_bt.setFixedSize(16, 16)
        max_bt.clicked.connect(lambda: self.showNormal() if self.isMaximized()  else self.showMaximized())
        # 关闭button
        close_bt = QPushButton(self)
        close_bt.setStyleSheet('''QPushButton{
                                    background:#CE0000;
                                    color:white;
                                    box-shadow: 1px 1px 3px rgba(0,0,0,0.3);
                                    font-size:16px;
                                    border-radius: 8px;
                                    font-family: 微软雅黑;}
                                QPushButton:hover{                    
                                    background:#FF2D2D;
                                }
                                QPushButton:pressed{
                                    border: 1px solid #3C3C3C!important;
                                    background:#AE0000;
                                }''')
        close_bt.setFixedSize(16, 16)
        close_bt.clicked.connect(self.close)
        # 顶部水平布局
        top_hBox = QHBoxLayout()
        top_hBox.setContentsMargins(0,0,0,0)
        top_hBox.setSpacing(0)
        top_hBox.addWidget(logo_label)
        top_hBox.addWidget(app_title)
        top_hBox.addWidget(self.anno_bt)
        top_hBox.addWidget(train_bt)
        # top_hBox.addWidget(lib_bt)
        top_hBox.addWidget(about_bt)
        top_hBox.addStretch(20)
        top_hBox.addWidget(min_bt)
        top_hBox.addStretch(1)
        top_hBox.addWidget(max_bt)
        top_hBox.addStretch(1)
        top_hBox.addWidget(close_bt)
        top_hBox.addStretch(1)

        top_back_widget.setStyleSheet('QWidget{background-color: rgb(169,169,169);font-weight: bold;font-family:"宋体";font-size:15px;color:black;}'
                                 "QPushButton:hover{background-color:rgb(160,200,240)}" #光标移动到上面后的前景色
                                 "QPushButton{ border-top-left-radius:3px;border-top-right-radius:3px}"  #圆角半径
                                 "QPushButton:pressed{background-color:rgb(160,200,240);color: red;}" #按下时的样式
                                 "QPushButton:checked{background-color:rgb(160,200,240);color: red;}" #按下时的样式
                                 )
        top_back_widget.setFixedHeight(wid_h)
        top_back_widget.setLayout(top_hBox)

        # 中心容器
        self.centre_layout = QStackedWidget()
        #self.centre_widget = QStackedWidget()
        #centre_widget.setLayout(self.centre_layout)
        #self.centre_widget.setStyleSheet('background-color: rgb(227,244,244)')
        #self.centre_widget.setStyleSheet('border:1px solid red;background-color: rgb(227,244,244)')

        #状态栏
        self.state_label1 = QLabel("")
        self.state_label1.setFixedHeight(20)

        self.state_label2 = QLabel("")
        self.state_label2.setFixedHeight(20)
        #self.state_label2.setAlignment(Qt.AlignVCenter)
        state_layout = QHBoxLayout()
        state_layout.setContentsMargins(0,0,0,0)
        state_layout.setSpacing(0)
        state_layout.addWidget(QLabel("  "))
        state_layout.addWidget(self.state_label1)
        state_layout.addStretch(1)
        state_layout.addWidget(self.state_label2)
        state_layout.addWidget(QLabel("  "))


        # 整个界面是一个垂直布局
        self.all_vbox = QVBoxLayout()
        # 外边距为0，内间距为0
        self.all_vbox.setContentsMargins(0,0,0,0)
        self.all_vbox.setSpacing(0)
        self.all_vbox.addWidget(top_back_widget)
        self.all_vbox.addWidget(self.centre_layout)
        self.all_vbox.addLayout(state_layout)
        self.setLayout(self.all_vbox)


    def switchPage(self, id):
        if self.current == id:
            return
        if id < 0 or id > 4:
            LOG.warning('the page id:', id)
            return
        self.state_label1.setText("")
        self.state_label2.setText("")
        self.current = id
        self.centre_layout.setCurrentIndex(self.current)


