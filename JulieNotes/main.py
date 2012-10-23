from PySide.QtCore import QUrl
from PySide.QtGui import QTabBar
from JulieNotes.design.output import Ui_MainWindow
from PySide import QtCore, QtGui

import sys
from JulieNotes.core.restructedText import reST_to_html

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__handle_events()

        # Debug:
        with open('../EXAMPLE.rst', 'r') as f:
            text = f.read()
        self.ui.textEdit.setText(text)

    def __handle_events(self):
        """
        Event handlers
        """
        # Quit
        self.ui.action_Quit.triggered.connect(QtCore.QCoreApplication.instance().quit)
        # Open / Save
        self.ui.action_Open.triggered.connect(self._load_from_file)
        self.ui.action_Save.triggered.connect(self._save_to_file)
        self.ui.action_Save_As.triggered.connect(self._save_to_file)
        self.ui.actionAbout.triggered.connect(self._show_about)
        # Tabs change handle
        self.ui.View.findChild(QTabBar).currentChanged.connect(self._tab_pressed)

    def _render_text(self, text):
        render = reST_to_html(text)
        with open('./core/template/rendered_file.html', 'wb') as f:
            f.write(render)

    def show_in_browser(self, text):
        self._render_text(text)
        self.ui.qwebview.load(QUrl("./core/template/rendered_file.html"))
        self.ui.qwebview.show()

    def _tab_pressed(self):
        text = self.ui.textEdit.toPlainText()
        self.show_in_browser(text)

    def _save_to_file(self):
        print ('Trying to save')

    def _load_from_file(self):
        print ('Trying to load')

    def _show_about(self):
        print ('Trying to show about')

    def show(self, *args, **kwargs):
        self._tab_pressed()
        super().show()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Julie_app = MainWindow()
    Julie_app.show()
    sys.exit(app.exec_())

