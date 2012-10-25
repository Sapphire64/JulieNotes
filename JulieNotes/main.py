from PySide.QtCore import QUrl, QAbstractTableModel, Qt
from PySide.QtGui import QTabBar, QFileDialog
from JulieNotes.design.output import Ui_MainWindow
from PySide import QtCore, QtGui

import sys
from JulieNotes.core.restructedText import reST_to_html

class MainWindow(QtGui.QMainWindow):

    __last_key = None
    __opened_file = ''

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__handle_events()

        # keep header/title list separate
        header = ['Test', 'Test']
        # a list of (name, age, weight) tuples
        data_list = [
            ('Test Test', '362'),
            ('Test Test1', '212'),
        ]

        table_model = MyTableModel(self, data_list, header)
        self.ui.TableView.setModel(table_model)

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
        self.ui.action_Save.triggered.connect(self._save_current)
        self.ui.action_Save_As.triggered.connect(self._save_to_file)
        self.ui.actionAbout.triggered.connect(self._show_about)
        # Tabs change handle
        self.ui.View.findChild(QTabBar).currentChanged.connect(self._tab_pressed)

    def __open_file(self, path):
        try:
            with open(path, 'r') as f:
                text = f.read()
        except Exception as e:
            print (e)
        else:
            try:
                self.ui.textEdit.setText(text)
            except Exception as e:
                print (e)
            else:
                self.__opened_file = path

    def __save_to_file(self, path=None):
        if path is None:
            path = self.__opened_file
        if not path:
            return # save nothing or any other case

        text = self.ui.textEdit.toPlainText()

        try:
            with open(path, 'w') as f:
                f.write(text)
        except Exception as e:
            print (e)
        else:
            self.__opened_file = path

    def _render_text(self, text):
        render = reST_to_html(text)
        with open('./core/template/rendered_file.html', 'wb') as f:
            f.write(render)

    def show_in_browser(self, text):
        self._render_text(text)
        self.ui.qwebview.load(QUrl("./core/template/rendered_file.html"))
        self.ui.qwebview.show()

    def keyPressEvent(self, event):

        key = event.key()

        if key == 16777249:
            self.__last_key = key
        elif key == 83 and self.__last_key == 16777249:
            self._save_current()
        else:
            QtGui.QWidget.keyPressEvent(self, event)

        """ This code does not work, but should:
        if key == QtCore.Qt.Key_Save:
            self._save_to_file()
        elif key == QtCore.Qt.Key_Open:
            self._load_from_file()
        else:
            QtGui.QWidget.keyPressEvent(self, event)
        """

    def _tab_pressed(self):
        text = self.ui.textEdit.toPlainText()
        self.show_in_browser(text)

    def _save_current(self):
        self.__save_to_file()

    def _save_to_file(self):
        if not self.__opened_file:
            return
        filepath = QFileDialog.getOpenFileName(self, "New file name", '~', "All files (*.*)")
        self.__save_to_file(path=filepath[0])

    def _load_from_file(self):
        filepath = QFileDialog.getOpenFileName(self, "Open rst file", '~', "All files (*.*)")
        self.__open_file(filepath[0])
        self._tab_pressed()

    def _show_about(self):
        print ('Trying to show about')

    def show(self, *args, **kwargs):
        self._tab_pressed()
        super().show()


class MyTableModel(QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        return len(self.mylist[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Julie_app = MainWindow()
    Julie_app.show()
    sys.exit(app.exec_())

