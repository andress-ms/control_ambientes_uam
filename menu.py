import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QFormLayout, QMessageBox, QInputDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from modulos.gestion_ambientes import GestorDeAmbientes, Ambiente
from modulos.gestion_clases import Actividad, GestorDeActividades
from modulos.administracion import Usuario
from modulos.importar_datos import cargar_datos, obtener_columnas_de_clase
from modulos.gestion_horarios import Horario, HorariosDataFrame

# IMPORTANTE, database.xlsx debe estar dentro de la carpeta de data
current_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(current_dir, 'data', 'database.xlsx')
csv_path_ambientes = os.path.join(current_dir,'data', 'lista_ambientes.csv')
csv_path_actividades = os.path.join(current_dir, 'data', 'lista_actividades.csv')
csv_path_horarios = os.path.join(current_dir, 'data', 'horarios.csv')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Ambientes UAM")

        # Configuración inicial
        admin = Usuario(nombre='Admin', rol='administrador')
        self.gestor_ambientes = GestorDeAmbientes(usuario=admin)
        self.gestor_actividades = GestorDeActividades(usuario=admin)
        self.horarios_contenedor = HorariosDataFrame()

        # Leer los datos de los archivos
        self.cargar_datos()

        # Diseño de la ventana principal
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Etiqueta del título
        self.label = QLabel("Control de Ambientes UAM")
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        layout.addWidget(self.label)

        # Botones del menú
        botones = [
            ("Agregar Ambiente", self.agregar_ambiente),
            ("Eliminar Ambiente", self.eliminar_ambiente),
            ("Agregar Actividad", self.agregar_actividad),
            ("Eliminar Actividad", self.eliminar_actividad),
            ("Asignar Actividad a Horario", self.asignar_actividad_a_horario),
            ("Mostrar Horarios", self.mostrar_horarios),
            ("Salir", self.close)
        ]

        for texto, funcion in botones:
            boton = QPushButton(texto)
            boton.clicked.connect(funcion)
            layout.addWidget(boton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def cargar_datos(self):
        self.gestor_ambientes.ambientes_df = cargar_datos(csv_path_ambientes, excel_path, obtener_columnas_de_clase(Ambiente), hoja_excel="Hoja 1")
        self.gestor_actividades.actividades_df = cargar_datos(csv_path_actividades, excel_path, obtener_columnas_de_clase(Actividad), hoja_excel='Hoja 2')
        self.horarios_contenedor.horarios_df = cargar_datos(csv_path_horarios, excel_path, ['codigo_ambiente', 'periodo', 'codigo_clase', 'nombre', 'duracion', 'tamaño', 'grupo', 'docente'])

    def agregar_ambiente(self):
        dialog = QFormLayout()
        codigo = QLineEdit()
        tipo = QLineEdit()
        disponibilidad = QLineEdit()
        activo = QLineEdit()
        capacidad = QLineEdit()
        dialog.addRow("Código del Ambiente:", codigo)
        dialog.addRow("Tipo de Ambiente:", tipo)
        dialog.addRow("Disponibilidad (s/n):", disponibilidad)
        dialog.addRow("Activo (s/n):", activo)
        dialog.addRow("Capacidad:", capacidad)

        buttonBox = QMessageBox()
        buttonBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        buttonBox.button(QMessageBox.Ok).clicked.connect(lambda: self.procesar_agregar_ambiente(codigo, tipo, disponibilidad, activo, capacidad))
        buttonBox.setLayout(dialog)
        buttonBox.exec()

    def procesar_agregar_ambiente(self, codigo, tipo, disponibilidad, activo, capacidad):
        try:
            nuevo_ambiente = Ambiente(
                codigo_ambiente=codigo.text(),
                tipo_ambiente=tipo.text(),
                disponibilidad=disponibilidad.text().lower() == 's',
                activo=activo.text().lower() == 's',
                capacidad=int(capacidad.text())
            )
            self.gestor_ambientes.agregar_ambiente(nuevo_ambiente)
            self.gestor_ambientes.exportar_a_csv(csv_path_ambientes)
            QMessageBox.information(self, "Éxito", "Ambiente agregado exitosamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def eliminar_ambiente(self):
        codigo, ok = QInputDialog.getText(self, "Eliminar Ambiente", "Ingrese el código del ambiente a eliminar:")
        if ok:
            try:
                self.gestor_ambientes.eliminar_ambiente(codigo)
                self.gestor_ambientes.exportar_a_csv(csv_path_ambientes)
                QMessageBox.information(self, "Éxito", "Ambiente eliminado exitosamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def agregar_actividad(self):
        dialog = QFormLayout()
        codigo = QLineEdit()
        nombre = QLineEdit()
        duracion = QLineEdit()
        tamaño = QLineEdit()
        grupo = QLineEdit()
        docente = QLineEdit()
        dialog.addRow("Código de la Actividad:", codigo)
        dialog.addRow("Nombre:", nombre)
        dialog.addRow("Duración:", duracion)
        dialog.addRow("Tamaño:", tamaño)
        dialog.addRow("Grupo:", grupo)
        dialog.addRow("Docente:", docente)

        buttonBox = QMessageBox()
        buttonBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        buttonBox.button(QMessageBox.Ok).clicked.connect(lambda: self.procesar_agregar_actividad(codigo, nombre, duracion, tamaño, grupo, docente))
        buttonBox.setLayout(dialog)
        buttonBox.exec()

    def procesar_agregar_actividad(self, codigo, nombre, duracion, tamaño, grupo, docente):
        try:
            nueva_actividad = Actividad(
                codigo_clase=codigo.text(),
                nombre=nombre.text(),
                duracion=int(duracion.text()),
                tamaño=int(tamaño.text()),
                grupo=int(grupo.text()),
                docente=docente.text()
            )
            self.gestor_actividades.agregar_actividad(nueva_actividad)
            self.gestor_actividades.exportar_a_csv(csv_path_actividades)
            QMessageBox.information(self, "Éxito", "Actividad agregada exitosamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def eliminar_actividad(self):
        codigo, ok = QInputDialog.getText(self, "Eliminar Actividad", "Ingrese el código de la actividad a eliminar:")
        if ok:
            try:
                self.gestor_actividades.eliminar_actividad(codigo)
                self.gestor_actividades.exportar_a_csv(csv_path_actividades)
                QMessageBox.information(self, "Éxito", "Actividad eliminada exitosamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def asignar_actividad_a_horario(self):
        dialog = QFormLayout()
        codigo_ambiente = QLineEdit()
        periodo = QLineEdit()
        codigo_actividad = QLineEdit()
        dialog.addRow("Código del Ambiente:", codigo_ambiente)
        dialog.addRow("Periodo (e.g., '8-8:50 AM'):", periodo)
        dialog.addRow("Código de la Actividad:", codigo_actividad)

        buttonBox = QMessageBox()
        buttonBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        buttonBox.button(QMessageBox.Ok).clicked.connect(lambda: self.procesar_asignar_actividad(codigo_ambiente, periodo, codigo_actividad))
        buttonBox.setLayout(dialog)
        buttonBox.exec()

    def procesar_asignar_actividad(self, codigo_ambiente, periodo, codigo_actividad):
        try:
            ambiente = self.gestor_ambientes.consultar_ambiente(codigo_ambiente.text())
            if not ambiente.empty:
                actividad = self.gestor_actividades.consultar_actividad(codigo_actividad.text())
                if not actividad.empty:
                    actividad_obj = Actividad(**actividad.iloc[0].to_dict())
                    self.horarios_contenedor.asignar_actividad_a_ambiente(codigo_ambiente.text(), periodo.text(), actividad_obj)
                    self.horarios_contenedor.exportar_a_csv(csv_path_horarios)
                    QMessageBox.information(self, "Éxito", f"Actividad '{actividad_obj.nombre}' asignada exitosamente.")
                else:
                    QMessageBox.critical(self, "Error", "No se encontró la actividad.")
            else:
                QMessageBox.critical(self, "Error", "No se encontró el ambiente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def mostrar_horarios(self):
        self.horarios_contenedor.mostrar_horarios()
        QMessageBox.information(self, "Horarios", "Se ha mostrado la información de los horarios.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
