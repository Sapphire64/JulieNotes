from PySide.QtCore import QUrl
from JulieNotes.design.output import Ui_MainWindow
from PySide import QtCore, QtGui

import sys

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def run(self):
        self.ui.qwebview.load(QUrl("http://www.google.com"))
        self.ui.qwebview.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    myapp.run()
    sys.exit(app.exec_())

