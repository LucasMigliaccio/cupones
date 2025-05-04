from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QPixmap, QIcon, QColor
import os

class ImagenesTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data.reset_index(drop=True)
        self._columns = data.columns.tolist()

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._columns)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        
        row = index.row()
        col = index.column()
        column_name = self._columns[col]

        if role == Qt.DisplayRole:
            if column_name == "Imagen_Local":
                return ""
            return str(self._data.at[row, column_name])

        if role == Qt.DecorationRole and column_name == "Imagen_Local":
            filepath = self._data.at[row, column_name]
            if not filepath or not os.path.exists(filepath):
                filepath = "images/default.jpg"
            pixmap = QPixmap(filepath).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            return QIcon(pixmap)

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        if role == Qt.BackgroundRole:
            if "Precio anterior" in self._columns and "Precio actual" in self._columns:
                precio_anterior = self._data.at[row, "Precio anterior"]
                precio_actual = self._data.at[row, "Precio actual"]

                try:
                    precio_anterior = int(precio_anterior)
                    precio_actual = int(precio_actual)
                except ValueError:
                    return None

                if precio_actual > precio_anterior:
                    return QColor("#d4f4dd")  # VSuba
                elif precio_actual < precio_anterior:
                    return QColor("#f8d7da")  # Baja
    

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._columns[section]
            else:
                return section + 1
