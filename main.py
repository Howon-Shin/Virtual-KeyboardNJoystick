import sys

from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel
from PyQt5.QtGui import QDropEvent, QDragEnterEvent, QMouseEvent, QDrag, QMoveEvent

import pyautogui


# class DragButton(QPushButton):
#     def __init__(self, title):
#         super(DragButton, self).__init__(title, self)
#
#     def mousePressEvent(self, e: QMouseEvent):
#         self.position = e.globalPos() - self.pos()
#         e.accept()
#
#     def mouseMoveEvent(self, e: QMouseEvent):
#         se

class VirtualKeyboard(QWidget):

    def __init__(self):
        super(VirtualKeyboard, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setFocusPolicy(Qt.NoFocus)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAcceptDrops(True)

        self.title = '가상키보드 및 조이패드'
        self.setting = False
        self.currBtn = None
        self.allBtns = []
        self.keyBtns = []
        self.moveEn = False

        self.initUI()
        self.no_focus()

    def initUI(self):
        self.settingBackground = QLabel('', self)
        self.settingBackground.hide()
        self.settingBackground.setGeometry(0, 0, 1000, 1000)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 100)")

        self.settingBtn = QPushButton('설정', self)
        self.settingBtn.setStyleSheet("color: rgb(255, 255, 255);"
                                      "background-color: rgba(0, 0, 0, 5);"
                                      "border: 2px solid rgb(255, 255, 255);"
                                      "border-radius: 4px")
        self.settingBtn.setGeometry(600, 50, 60, 30)

        self.moveBtn = QLabel('---', self)
        self.moveBtn.setAlignment(Qt.AlignCenter)
        self.moveBtn.setStyleSheet("color: rgb(255, 255, 255);"
                                   "background-color: rgba(0, 0, 0, 5);"
                                   "border: 1px solid rgb(255, 255, 255);"
                                   )
        self.moveBtn.setGeometry(0, 0, 50, 25)

        self.addBtn = QPushButton('추가', self)
        self.addBtn.setStyleSheet("color: rgb(255, 255, 255);"
                                   "background-color: rgba(0, 0, 0, 5);"
                                   "border: 2px solid rgb(255, 255, 255);"
                                   "border-radius: 4px")
        self.addBtn.setGeometry(500, 50, 60, 30)
        self.addBtn.hide()


        self.btnLeft = QPushButton('Left', self)
        self.btnLeft.setStyleSheet("color: rgb(255, 255, 255);"
                                   "background-color: rgba(0, 0, 0, 5);"
                                   "border: 2px solid rgb(255, 255, 255);"
                                   "border-radius: 25px")
        self.btnLeft.setGeometry(600, 300, 50, 50)

        self.btnA = QPushButton('A', self)
        self.btnA.setStyleSheet("color: rgb(255, 255, 255);"
                                "background-color: rgba(0, 0, 0, 5);"
                                "border: 2px solid rgb(255, 255, 255);"
                                "border-radius: 25px")
        self.btnA.setGeometry(200, 200, 50, 50)

        self.keyBtns.append(self.btnLeft)
        self.keyBtns.append(self.btnA)

        self.allBtns.append(self.settingBtn)
        self.allBtns.append(self.addBtn)

        for btn in self.keyBtns:
            btn.setAutoRepeatInterval(5)
            btn.setAutoRepeat(True)

            self.btn_press_connect(btn)

            self.allBtns.append(btn)

        self.btn_press_connect(self.settingBtn)

        self.settingBtn.clicked.connect(self.setting_click)

        self.setWindowTitle(self.title)
        self.setGeometry(300, 300, 700, 400)
        self.show()

    def btn_press_connect(self, btn):
        btn.pressed.connect(lambda: self.key_click(btn))

    def key_click(self, btn):
        self.currBtn = btn
        self.moveEn = False

        if not self.setting and btn in self.keyBtns:
            pyautogui.press(btn.text())

    def setting_click(self):
        if self.setting:
            self.setting = False
            self.settingBtn.setStyleSheet("color: rgb(255, 255, 255);"
                                          "background-color: rgba(0, 0, 0, 5);"
                                          "border: 2px solid rgb(255, 255, 255);"
                                          "border-radius: 4px")
            self.currBtn = None
            self.settingBackground.hide()
            self.addBtn.hide()
        else:
            self.setting = True
            self.settingBtn.setStyleSheet("color: rgb(255, 255, 255);"
                                          "background-color: rgba(0, 0, 0, 100);"
                                          "border: 2px solid rgb(255, 255, 255);"
                                          "border-radius: 4px")
            self.settingBackground.show()
            self.addBtn.show()

    def dropEvent(self, e: QDropEvent):
        try:
            if self.setting:
                position = e.pos()
                self.currBtn.move(position)

                e.setDropAction(Qt.MoveAction)
            e.accept()
        except Exception as e:
            print(e)

    def dragEnterEvent(self, e: QMouseEvent):
        e.accept()

    def mouseMoveEvent(self, e: QMouseEvent):
        if e.buttons() == Qt.RightButton:
            return

        if self.setting:
            mime_data = QMimeData()
            drag = QDrag(self)
            drag.setMimeData(mime_data)

            drag.exec_(Qt.MoveAction)
        elif self.moveEn:
            self.move(e.globalPos() - self.mouse_position)

    def mousePressEvent(self, e: QMouseEvent):
        self.mouse_position = e.globalPos() - self.pos()
        self.moveEn = True
        e.accept()

    def no_focus(self):
        import ctypes
        import win32con

        user32 = ctypes.windll.user32
        dc = user32.FindWindowW(0, self.title)
        user32.SetWindowLongPtrW(dc, win32con.GWL_EXSTYLE, user32.GetWindowLongPtrW(dc, win32con.GWL_EXSTYLE)
                                 | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_APPWINDOW)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VirtualKeyboard()
    ex.show()
    sys.exit(app.exec_())
