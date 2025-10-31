from PyQt5.QtWidgets import QApplication
from ui.mainwindow import Ui_MainWindow 
import sys
from PyQt5.QtWidgets import QMainWindow
from function import Learining

learner = Learining()

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.lineEdit1.setPlaceholderText("Write training human's name")
        self.pushButton1.clicked.connect(self.click1)
        self.pushButton2.clicked.connect(self.click2)
    def click1(self):
        learner.capture(name=self.lineEdit1.text(), max_count=10)
    def click2(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
