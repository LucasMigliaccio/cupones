from PySide6.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView, QHBoxLayout, QFrame, QPushButton,QFileDialog, QTableView,QDialog, QLabel,QVBoxLayout
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap

from views.main_window import MainWindow
from views.general_custom_ui import GeneralCustomUi
from views import components
from models.imagen_table import ImagenesTableModel
from database.database import get_connection, create_tables_if_not_exists,select_all,delete_all, return_dataframe
from database import database 

import pandas as pd
import sqlite3
import os
import requests
import sys

from bs4 import BeautifulSoup
from sqlalchemy import create_engine



class MainWindowForm(QWidget, MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ui = GeneralCustomUi(self)

        #self.config_table()
        #self.set_table_data()
        self.label_2.setText("No hay cupon seleccionado")
        self.label_tittle.setText("Cupones System")

        # Crear tablas si no existen
        #create_tables_if_not_exists()
        self.operador_button.clicked.connect(self.abrir_selector_archivos)
        self.ceo_button.clicked.connect(self.delete_table)
        self.recuento_button.clicked.connect(self.obtener_imagenes_y_datos)
        self.delete_table()

    def mousePressEvent(self, event):
        self.ui.mouse_press_event(event)

    def abrir_selector_archivos(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            "Archivos Excel (*.xlsx *.xls);;Archivos CSV (*.csv);;Todos los archivos (*)"
        )

        if archivo:
            print(f"📁 Archivo seleccionado:\n{archivo}")

            # Leer el archivo
            try:
                if archivo.endswith(".csv"):
                    df = pd.read_csv(archivo, skiprows=12)
                else:
                    df = pd.read_excel(archivo, skiprows=12)


                print (df)

                # Normalizar nombres de columnas para que coincidan con la tabla
                df.columns = [c.strip() for c in df.columns]
                columnas_esperadas = [
                    "Artículo", "Nombre", "Física disponible", "Almacen",
                    "Clase", "Marca", "Matriz", "Tipo de Producto",
                    "Precio anterior", "Precio actual"
                ]

                # Verifica que estén todas las columnas necesarias
                if not all(col in df.columns for col in columnas_esperadas):
                    self.label_2.setText("❌ Error: El archivo no contiene todas las columnas necesarias.")

                    print("❌ Error: El archivo no contiene todas las columnas necesarias.")
                    return

               
                conn = sqlite3.connect("database/cupon.sqlite3")
                cursor = conn.cursor()

                for _, row in df.iterrows():
                    cursor.execute("""
                        INSERT INTO cupon (
                            Artículo, Nombre, "Física disponíble", Almacen,
                            Clase, Marca, Matriz, "Tipo de Producto",
                            "Precio anterior", "Precio actual"
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row["Artículo"], row["Nombre"], row["Física disponible"], row["Almacen"],
                        row["Clase"], row["Marca"], row["Matriz"], row["Tipo de Producto"],
                        int(str(row["Precio anterior"]).replace(".", "").replace(",", "")),
                        int(str(row["Precio actual"]).replace(".", "").replace(",", ""))
                    ))

                conn.commit()
                conn.close()
                articulos = df['Artículo'].astype(str).tolist()
                self.label_2.setText("✅ Datos insertados correctamente en la tabla cupones.")
                print("✅ Datos insertados correctamente en la tabla cupones.")
            except Exception as e:
                print(f"❌ Error al procesar archivo: {e}")
                
    def analizar_archivo(self):
        print("llsss")
        columnas = ["ID", "Artículo", "Nombre", "Física disponible", "Almacen", "Clase", "Marca", "Matriz", "Tipo de Producto", "Precio anterior", "Precio actual"]
        data = select_all()
        df = pd.DataFrame(data, columns=columnas)

        lista = df['Artículo'].astype(str).tolist()
        print(lista)


    def mostrar_tabla_con_imagenes(self, df):
        self.model = ImagenesTableModel(df)
        self.tableView.setModel(self.model)

        self.tableView.setIconSize(QSize(200, 200))
        self.tableView.verticalHeader().setDefaultSectionSize(200)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()
        self.tableView.selectionBehavior()
        self.tableView.clicked.connect(self.mostrar_imagen_ampliada)


    def analizar_archivo(self):
        df = return_dataframe()
        df = df["Artículo"].astype(str).tolist()
        print(df)


    def obtener_imagenes_y_datos(self):
        df = return_dataframe()

        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(len(df))
        self.progressBar.setValue(0)

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        resultados = []

        contador = 0 

        for i, row in df.iterrows():
            contador = contador + 1 
            print(f"VUELTA########## Número {contador}##########")
            codigo = str(row["Artículo"])
            url = f"https://www.dexter.com.ar/buscar?q={codigo}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            img_tag = soup.find("img", class_="tile-image primary-image")

            if img_tag and "src" in img_tag.attrs:
                img_url = img_tag["src"]

                # Guardar imagen localmente
                img_data = requests.get(img_url).content
                filepath = f"images/{codigo}.jpg"
                with open(filepath, "wb") as f:
                    f.write(img_data)

            else:
                img_url = "No encontrada"
                filepath = "No guardada"

            resultados.append({
                "ID": row["ID"],
                "Artículo": row["Artículo"],
                "Nombre": row["Nombre"],
                "Física disponíble": row["Física disponíble"],
                "Almacen": row["Almacen"],
                "Clase": row["Clase"],
                "Marca": row["Marca"],
                "Matriz": row["Matriz"],
                "Tipo de Producto": row["Tipo de Producto"],
                "Precio anterior": row["Precio anterior"],
                "Precio actual": row["Precio actual"],
                "Imagen_Local": filepath
            })
            self.progressBar.setValue(i + 1)
            
            #if contador == 10:
                #break

        resultado_df = pd.DataFrame(resultados)
        self.mostrar_tabla_con_imagenes(resultado_df)
        print("ESTE ES EL DATAFRAME ************************************* \n", resultado_df)
        return resultado_df

    def mostrar_imagen_ampliada(self, index):
        if not index.isValid():
            return

        column_name = self.model._columns[index.column()]
        if column_name != "Imagen_Local":
            return

        # Obtener la ruta de la imagen desde el modelo
        filepath = self.model._data.at[index.row(), "Imagen_Local"]

        if not filepath or not os.path.exists(filepath):
            filepath = "images/default.jpg"

        # Crear diálogo para mostrar imagen
        dialog = QDialog(self)
        dialog.setWindowTitle("Vista previa de imagen")
        dialog.setMinimumSize(400, 400)

        layout = QVBoxLayout(dialog)
        label = QLabel()
        label.setAlignment(Qt.AlignCenter)

        pixmap = QPixmap(filepath).scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)

        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.exec()
        
    def delete_all_images(self):
        # Carpeta donde se puede escribir, por ejemplo junto al .exe o en una subcarpeta del USB
        base_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        image_folder = os.path.join(base_path, 'images')

        if not os.path.exists(image_folder):
            print(f"📁 Carpeta {image_folder} no existe, creando...")
            os.makedirs(image_folder)

        default_image = "default.jpg"

        for filename in os.listdir(image_folder):
            filepath = os.path.join(image_folder, filename)
            if os.path.isfile(filepath) and filename != default_image:
                try:
                    os.remove(filepath)
                    print(f"🗑 Imagen eliminada: {filename}")
                except Exception as e:
                    print(f"⚠️ Error eliminando {filename}: {e}")


    def delete_table(self):
        database.delete_all()
        self.delete_all_images()
        print(" borrado exitosamente")

    