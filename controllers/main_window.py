from PySide6.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView, QHBoxLayout, QFrame, QPushButton,QFileDialog
from views.main_window import MainWindow
from views.general_custom_ui import GeneralCustomUi
from views import components
import pandas as pd
import sqlite3
import os

from database.database import get_connection, create_tables_if_not_exists,select_all


class MainWindowForm(QWidget, MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ui = GeneralCustomUi(self)

        self.config_table()
        self.set_table_data()

        # Crear tablas si no existen
        #create_tables_if_not_exists()
        self.operador_button.clicked.connect(self.abrir_selector_archivos)

    def mousePressEvent(self, event):
        self.ui.mouse_press_event(event)

    def abrir_selector_archivos(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo")
        if archivo:
            print(f"Archivo seleccionado:\n{archivo}")


    def config_table(self):
        column_label = ("ID","Articulo", "Nombre","Física disponíble", "Almacen", "Clase", "Marca", "Matriz", "Tipo de Producto","Precio anterior", "Precio actua", "") 
        self.infopedidos_table.setColumnCount(len(column_label))
        self.infopedidos_table.setHorizontalHeaderLabels(column_label)
        self.infopedidos_table.setColumnWidth(1,200) #articulo
        self.infopedidos_table.setColumnWidth(2,120) #Nombre
        self.infopedidos_table.setColumnWidth(3,120) #Física disponíble
        self.infopedidos_table.setColumnWidth(4,120) #Almacen
        self.infopedidos_table.setColumnWidth(5,120) #Clase
        self.infopedidos_table.setColumnWidth(6,120) #Marca
        self.infopedidos_table.setColumnWidth(7,120) #Matriz
        self.infopedidos_table.setColumnWidth(8,120) #Tipo de Producto
        self.infopedidos_table.setColumnWidth(9,120) #Precio anterior
        self.infopedidos_table.setColumnWidth(10,120) #Precio actua
        self.infopedidos_table.setColumnWidth(11,110) #Precio actua
        self.infopedidos_table.verticalHeader().setDefaultSectionSize(150)
        self.infopedidos_table.setColumnHidden(0, True)
        self.infopedidos_table.setSelectionBehavior(QAbstractItemView.SelectRows)

            
    def populate_table(self, data):
        #self.infopedidos_table.clearContents()  # Limpia el contenido de la tabla sin borrar las cabeceras
        #self.infopedidos_table.setRowCount(len(data) + 1)  # Actualiza el número correcto de filas

        for index_row, row in enumerate(data):
            for index_cell, cell in enumerate(row):
                item = QTableWidgetItem(str(cell))  # Crear un ítem con el contenido de la celda
                self.infopedidos_table.setItem(index_row, index_cell, item)

            # Agregar el botón de acción en la última columna
            self.infopedidos_table.setCellWidget(
                index_row, 11, self.build_action_button()
            )

        # Botón "Cargar más" en la última fila
        #last_row_index = len(data)
        #self.infopedidos_table.setSpan(
        #    last_row_index, 0, 1, self.infopedidos_table.columnCount()
        #)
        #load_more_button = QPushButton("Cargar más")
        #load_more_button.clicked.connect(self.load_more)
        #self.infopedidos_table.setCellWidget(last_row_index, 0, load_more_button)

    def build_action_button(self):
        view_button=components.Butonn("view","#17A288")
        edit_button=components.Butonn("edit","#007BFF")
        delete_button=components.Butonn("delete","#DC3545")

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(view_button)
        buttons_layout.addWidget(edit_button)
        buttons_layout.addWidget(delete_button)

        buttons_frame =QFrame()
        buttons_frame.setLayout(buttons_layout)

        view_button.clicked.connect(self.view_cita)
        edit_button.clicked.connect(self.edit_cita)
        delete_button.clicked.connect(self.delete_cita)

        return buttons_frame
    
    def set_table_data(self):
        data = select_all()
        self.populate_table(data)
    
    def remove_img(self, img_path):
        os.remove(img_path)

    def get_cita_id_from_table(self,table,button):
        row_index = table.indexAt(button.parent().pos()).row()
        cell_id_index= table.model().index(row_index,0)
        cita_id= table.model().data(cell_id_index)
        return cita_id
    