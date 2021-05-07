from PySide2 import QtGui
from PySide2 import QtWidgets

import ui.application


class ActionSave(QtWidgets.QAction):
    def __init__(self, parent=None):
        super().__init__(parent=parent, text="Save")
        self.setShortcut(QtGui.QKeySequence.Save)
        self.triggered.connect(self.action)

    def action(self):
        ui.application.MapTranslatorMainWindow.instance().save()
