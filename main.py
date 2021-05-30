from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from gui import*
from data import*
from PyQt5.QtCore import QThread, pyqtSlot
# https://www.youtube.com/watch?v=tRmrAtth8ls
class MyApp(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.thread = {}
        self.ui.pushButton.clicked.connect(self.connectClient)
        self.ui.pushButton_2.clicked.connect(self.startCrawlMessage)
        self.ui.pushButton_3.clicked.connect(self.stop)
        self.ui.pushButton_4.clicked.connect(self.commitComment)
        self.ui.toolButton.clicked.connect(self.openFile)
    def connectClient(self):
        self.thread[1] = YouTubeAPI(self,index=0)
        self.thread[1].start()
        self.ui.pushButton.setEnabled(False)
    def startCrawlMessage(self):
        self.thread[2] = YouTubeAPI(self,index=1)
        self.thread[2].updateListWidget.connect(self.updateList)
        self.thread[2].start()
        self.ui.pushButton_2.setEnabled(False)
    def commitComment(self):
        self.thread[3] = YouTubeAPI(self,index=2)
        self.thread[3].start()
    def stop(self):
        if self.thread[2].isRunning():
            self.thread[2].terminate()
        self.ui.pushButton_2.setEnabled(True)
    def updateList(self,value):
        self.ui.listWidget.addItem(value)
    def openFile(self):
        folder = QFileDialog.getOpenFileName(None, "Select a file","", filter="All files (*)")[0]
        self.ui.lineEdit.setText(str(folder))
        folder = open('options', 'w')
        folder.write(str(folder))
        folder.close()
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = MyApp()
    ui.show()
    sys.exit(app.exec_())
