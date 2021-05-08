import os
import re

import anvil
import anvil.errors
import nbt
from PySide2.QtCore import Qt
from PySide2.QtWidgets import *

from __version__ import __version__
from ui.actions.action_open import ActionOpen
from ui.actions.action_save import ActionSave


class MapTranslatorMainWindow(QMainWindow):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(MapTranslatorMainWindow, *args, **kwargs)
        return cls.__instance

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.init_ui()
        self.directory = None

    @classmethod
    def instance(cls):
        return cls.__instance

    def init_ui(self):
        self.setWindowTitle(f"Map Translator v{__version__}")
        self.add_menu()
        self.add_central_widget()
        self.show()

    def add_menu(self):
        menu_file = self.menuBar().addMenu("File")
        menu_file.addAction(ActionOpen(parent=menu_file))
        menu_file.addAction(ActionSave(parent=menu_file))

    def add_central_widget(self):
        table = QTableWidget(0, 2, parent=self)
        table.setHorizontalHeaderLabels(['Original', 'Translated'])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table = table
        self.setCentralWidget(self.table)

    def open(self, directory):
        base_path = os.path.join(directory, 'region')
        if not os.path.exists(base_path):
            return
        self.directory = directory

        directories = [self.directory, os.path.join(self.directory, 'DIM1'), os.path.join(self.directory, 'DIM-1')]
        base_paths = [os.path.join(x, 'region') for x in directories]

        all_strings = set()
        for base_path in base_paths:
            if not os.path.exists(base_path):
                continue
            for x in os.listdir(base_path):
                filename = os.path.join(base_path, x)
                region = anvil.Region.from_file(filename)
                for x in range(32):
                    for z in range(32):
                        try:
                            chunk = region.get_chunk(x, z)
                        except anvil.errors.ChunkNotFound:
                            continue
                        for te in chunk.tile_entities:
                            for y in te.tags:
                                if isinstance(y, nbt.nbt.TAG_String) and y.name != "id":
                                    if str(te[y.name]) in all_strings:
                                        continue
                                    all_strings.add(str(te[y.name]))
                                    row_n = self.table.rowCount()
                                    self.table.insertRow(row_n)
                                    item = QTableWidgetItem(str(te[y.name]))
                                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                                    self.table.setItem(row_n, 0, item)
                                    item = QTableWidgetItem(str(te[y.name]))
                                    self.table.setItem(row_n, 1, item)

    def save(self):
        if self.directory is None:
            return

        replacement = dict()
        for i in range(self.table.rowCount()):
            replacement[self.table.item(i, 0).text()] = self.table.item(i, 1).text()

        directories = [self.directory, os.path.join(self.directory, 'DIM1'), os.path.join(self.directory, 'DIM-1')]
        base_paths = [os.path.join(x, 'region') for x in directories]
        for base_path in base_paths:
            if not os.path.exists(base_path):
                continue
            for x in os.listdir(base_path):
                filename = os.path.join(base_path, x)
                region = anvil.Region.from_file(filename)
                match = re.fullmatch(r"r\.(-?\d+)\.(-?\d+)\.mca", x)

                new_region = anvil.EmptyRegion(int(match.group(1)), int(match.group(2)))
                for x in range(32):
                    for z in range(32):
                        try:
                            chunk = region.get_chunk(x, z)
                        except anvil.errors.ChunkNotFound:
                            continue
                        for te in chunk.tile_entities:
                            for y in te.tags:
                                if isinstance(y, nbt.nbt.TAG_String) and y.name != "id":
                                    te[y.name].value = replacement[str(te[y.name])]
                        new_region.add_chunk(chunk)
                new_region.save(filename)

        self.table.setRowCount(0)
        for value in set(replacement.values()):
            row_n = self.table.rowCount()
            self.table.insertRow(row_n)
            item = QTableWidgetItem(value)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_n, 0, item)
            item = QTableWidgetItem(value)
            self.table.setItem(row_n, 1, item)

