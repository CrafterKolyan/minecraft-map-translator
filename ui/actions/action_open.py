from PySide2 import QtGui
from PySide2 import QtWidgets

import ui.application


class ActionOpen(QtWidgets.QAction):
    def __init__(self, parent=None):
        super().__init__(parent=parent, text="Open...")
        self.setShortcut(QtGui.QKeySequence.Open)
        self.triggered.connect(self.action)

    def action(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(caption="Select folder with save")
        if directory:
            ui.application.MapTranslatorMainWindow.instance().open(directory)
