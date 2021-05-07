import sys

from PySide2.QtWidgets import QApplication

from ui.application import MapTranslatorMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MapTranslatorMainWindow()
    main_window.show()
    sys.exit(app.exec_())
