import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QMenuBar, QMenu, QAction, QInputDialog, QDialog, QLineEdit, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from modulos.gestion_ambientes import GestorDeAmbientes, Ambiente
from modulos.gestion_clases import GestorDeActividades, Actividad
from modulos.administracion import Usuario
from modulos.gestion_horarios import Horario, HorariosDataFrame, Actividad
from modulos.importar_datos import cargar_datos, obtener_columnas_de_clase

# Todos los archivos deben encontrarse en la carpeta data
current_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(current_dir, 'data', 'database.xlsx')
csv_path_ambientes = os.path.join(current_dir, 'data', 'lista_ambientes.csv')
csv_path_actividades = os.path.join(current_dir, 'data', 'lista_actividades.csv')
csv_path_horarios = os.path.join(current_dir, 'data', 'horarios.csv')
ambientes_data=cargar_datos(csv_path_ambientes, excel_path, obtener_columnas_de_clase(Ambiente), hoja_excel="Hoja 1")
actividades_data=cargar_datos(csv_path_actividades, excel_path, obtener_columnas_de_clase(Actividad), hoja_excel='Hoja 2')
horarios_data=cargar_datos(csv_path_horarios, excel_path, obtener_columnas_de_clase(Horario), hoja_excel = 'Hoja 3')
admin=Usuario(nombre='Admin', rol='administrador')

class VentanaLogin(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login - Control de Ambientes UAM')
       

        self.label_usuario = QLabel('Usuario:')
        self.edit_usuario = QLineEdit()
        self.label_password = QLabel('Contraseña:')
        self.input_password = QLineEdit()
        self.btn_login = QPushButton('Iniciar Sesión')

        layout = QVBoxLayout()
        layout.addWidget(self.label_usuario)
        layout.addWidget(self.edit_usuario)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.btn_login)
        
        self.setLayout(layout)

        self.btn_login.clicked.connect(self.verificar_credenciales)

    def verificar_credenciales(self):
        usuario = self.edit_usuario.text().strip()
        contrasena = self.input_password.text().strip()

        if self.autenticar_usuario(usuario, contrasena):
            self.accept()  
        else:
            QMessageBox.warning(self, 'Error de Autenticación', 'Usuario o contraseña incorrectos')

    def autenticar_usuario(self, nombre_usuario, contrasena):
       
        if nombre_usuario == 'admin' and contrasena == 'admin1':
            
            self.usuario = Usuario(nombre_usuario, 'administrador')
            return True
        elif nombre_usuario == 'gabriel' and contrasena == 'banano':
            # 
            self.usuario = Usuario(nombre_usuario, 'basico')
            return True
        else:
            return False

    def obtener_usuario_autenticado(self):
        return self.usuario if hasattr(self, 'usuario') and self.usuario else None


class VentanaPrincipal(QMainWindow):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle("Control de Ambientes UAM")
        self.setGeometry(100, 100, 800, 600)
        
        self.gestor_actividades = GestorDeActividades(usuario=admin, actividades_df=actividades_data)
        self.gestor_ambientes = GestorDeAmbientes(usuario=admin, ambientes_df=ambientes_data)
        self.horarios_df = HorariosDataFrame(horarios_data)
        
        self.initUI()

    def initUI(self):
        self.label_titulo = QLabel("Control de Ambientes UAM", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 24px; font-weight: bold; margin-top: 20px; margin-bottom: 20px;")

        self.btn_control_ambientes = QPushButton("Control de Ambientes", self)
        self.btn_control_actividades = QPushButton("Control de Actividades", self)
        self.btn_control_horarios = QPushButton("Control de Horarios", self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label_titulo)
        vbox.addWidget(self.btn_control_ambientes)
        vbox.addWidget(self.btn_control_actividades)
        vbox.addWidget(self.btn_control_horarios)
        vbox.addStretch()

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

        self.btn_control_ambientes.clicked.connect(self.mostrar_control_ambientes)
        self.btn_control_actividades.clicked.connect(self.mostrar_control_actividades)
        self.btn_control_horarios.clicked.connect(self.mostrar_control_horarios)

    def mostrar_control_ambientes(self):
        self.ventana_ambientes = VentanaControlAmbientes(self)
        self.ventana_ambientes.show()
        self.hide()

    def mostrar_control_actividades(self):
        self.ventana_actividades = VentanaControlActividades(self)
        self.ventana_actividades.show()
        self.hide()

    def mostrar_control_horarios(self):
        self.ventana_horarios = VentanaControlHorarios(self)
        self.ventana_horarios.show()
        self.hide()

class VentanaControlAmbientes(QWidget):
    def __init__(self, ventana_principal, parent=None):
        super().__init__(parent)
        self.ventana_principal = ventana_principal
        self.setWindowTitle("Control de Ambientes")
        self.setGeometry(200, 200, 600, 400)

        self.regreso_button = QPushButton("Regresar")
        self.regreso_button.clicked.connect(self.regresar)
        
        self.parent = parent
        self.gestor_ambientes = ventana_principal.gestor_ambientes
        
                 
        self.initUI()

    def initUI(self):
        self.label_titulo = QLabel("Control de Ambientes", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px; margin-bottom: 20px;")

        self.btn_agregar = QPushButton("Agregar Ambiente", self)
        self.btn_eliminar = QPushButton("Eliminar Ambiente", self)
        self.btn_actualizar = QPushButton("Actualizar Ambiente", self)
        self.btn_consultar = QPushButton("Consultar Ambiente", self)
        self.btn_mostrar_ambientes_disponibles = QPushButton("Mostrar Ambientes Disponibles", self)
        self.btn_buscar_con_filtros = QPushButton("Buscar con Filtros", self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label_titulo)
        vbox.addWidget(self.btn_agregar)
        vbox.addWidget(self.btn_eliminar)
        vbox.addWidget(self.btn_actualizar)
        vbox.addWidget(self.btn_consultar)
        vbox.addWidget(self.btn_mostrar_ambientes_disponibles)
        vbox.addWidget(self.btn_buscar_con_filtros)
        vbox.addStretch()
        
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.regreso_button)
        hbox.addStretch()

        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.btn_agregar.clicked.connect(self.agregar_ambiente)
        self.btn_eliminar.clicked.connect(self.eliminar_ambiente)
        self.btn_actualizar.clicked.connect(self.actualizar_ambiente)
        self.btn_consultar.clicked.connect(self.consultar_ambiente)
        self.btn_mostrar_ambientes_disponibles.clicked.connect(self.mostrar_ambientes_disponibles)
        self.btn_buscar_con_filtros.clicked.connect(self.buscar_con_filtros)
        
    def regresar(self):
        self.ventana_principal.show()  
        self.close()
        
    def agregar_ambiente(self):
        codigo, ok = QInputDialog.getText(self, "Agregar Ambiente", "Ingrese el código del ambiente:")
        if ok and codigo:
            tipo, ok = QInputDialog.getText(self, "Agregar Ambiente", "Ingrese el tipo de ambiente:")
            if ok and tipo:
                activo, ok = QInputDialog.getText(self, "Agregar Ambiente", "¿Está activo? (s/n):")
                if ok:
                    activo = activo.lower() == 's'
                    capacidad, ok = QInputDialog.getInt(self, "Agregar Ambiente", "Ingrese la capacidad:")
                    if ok:
                        nuevo_ambiente = Ambiente(codigo, tipo, activo, capacidad)
                        self.gestor_ambientes.agregar_ambiente(nuevo_ambiente)
                        self.exportar_ambientes()
                        QMessageBox.information(self, "Éxito", "Ambiente agregado correctamente.")
                        
    def eliminar_ambiente(self):
        codigo, ok = QInputDialog.getText(self, "Eliminar Ambiente", "Ingrese el código del ambiente a eliminar:")
        if ok and codigo:
            self.gestor_ambientes.eliminar_ambiente(codigo)
            QMessageBox.information(self, "Éxito", "Ambiente eliminado correctamente.")
            self.exportar_ambientes()
            self.mostrar_ambientes_disponibles()
            

    def actualizar_ambiente(self):
        codigo, ok = QInputDialog.getText(self, "Actualizar Ambiente", "Ingrese el código del ambiente a actualizar:")
        if ok and codigo:
            ambiente = self.gestor_ambientes.consultar_ambiente(codigo)
            if not ambiente.empty:
                tipo, ok = QInputDialog.getText(self, "Actualizar Ambiente", f"Tipo actual: {ambiente['tipo_ambiente'].iloc[0]}, ingrese el nuevo tipo de ambiente:")
                if ok and tipo:
                    activo, ok = QInputDialog.getText(self, "Actualizar Ambiente", f"Estado actual: {ambiente['activo'].iloc[0]}, ¿Está activo? (s/n):")
                    if ok:
                        activo = activo.lower() == 's'
                        capacidad, ok = QInputDialog.getInt(self, "Actualizar Ambiente", f"Capacidad actual: {ambiente['capacidad'].iloc[0]}, ingrese la nueva capacidad:")
                        if ok:
                            nuevo_ambiente = vars(Ambiente(codigo, tipo, activo, capacidad))
                            datos_actualizados = {k: v for k, v in nuevo_ambiente.items() if k != 'codigo_ambiente'}
                            self.gestor_ambientes.actualizar_ambiente(codigo, datos_actualizados)
                            QMessageBox.information(self, "Éxito", "Ambiente actualizado correctamente.")
                            self.exportar_ambientes()
                            self.mostrar_ambientes_disponibles()
                            
            else:
                QMessageBox.warning(self, "Error", f"Ambiente con código {codigo} no encontrado.")


    def consultar_ambiente(self):
        codigo, ok = QInputDialog.getText(self, "Consultar Ambiente", "Ingrese el código del ambiente a consultar:")
        if ok and codigo:
            ambiente = self.gestor_ambientes.consultar_ambiente(codigo)
            if not ambiente.empty:
                QMessageBox.information(self, "Consulta de Ambiente", f"Tipo de Ambiente: {ambiente['tipo_ambiente'].iloc[0]}\nEstado: {ambiente['activo'].iloc[0]}\nCapacidad: {ambiente['capacidad'].iloc[0]}")
            else:
                QMessageBox.warning(self, "Error", f"Ambiente con código {codigo} no encontrado.")
    def mostrar_ambientes_disponibles(self):
        try:
            ambientes_disponibles = self.gestor_ambientes.mostrar_ambientes_disponibles()
            if not ambientes_disponibles.empty:
                self.mostrar_ambientes_dialogo = MostrarAmbientesDialogo(ambientes_disponibles)
                self.mostrar_ambientes_dialogo.exec_()
            else:
                print("No hay ambientes disponibles para mostrar.")
        except Exception as e:
            print(f"Error al mostrar los ambientes disponibles: {e}")
            
    def exportar_ambientes(self):
        self.gestor_ambientes.exportar_a_csv(csv_path_ambientes)
    
    def buscar_con_filtros(self):
        tipo, ok_tipo = QInputDialog.getText(self, "Filtro por Tipo", "Ingrese el tipo de ambiente:")
        activo, ok_activo = QInputDialog.getText(self, "Filtro por Estado", "¿Está activo? (s/n):")
        capacidad_min, ok_cap_min = QInputDialog.getInt(self, "Filtro por Capacidad Mínima", "Ingrese la capacidad mínima:")
        capacidad_max, ok_cap_max = QInputDialog.getInt(self, "Filtro por Capacidad Máxima", "Ingrese la capacidad máxima:")

        if ok_tipo or ok_activo or ok_cap_min or ok_cap_max:
            ambientes_filtrados = self.gestor_ambientes.buscar_ambientes_con_filtros(
                tipo if ok_tipo else "",
                activo if ok_activo else "",
                capacidad_min if ok_cap_min else "",
                capacidad_max if ok_cap_max else ""
            )
            self.mostrar_resultados_busqueda(ambientes_filtrados)
        else:
            QMessageBox.warning(self, "Filtros Vacíos", "No se aplicaron filtros de búsqueda.")

    def mostrar_resultados_busqueda(self, ambientes_df):
        self.mostrar_ambientes_dialogo = MostrarAmbientesDialogo(ambientes_df)
        self.mostrar_ambientes_dialogo.exec_()
            
class MostrarAmbientesDialogo(QDialog):
    def __init__(self, ambientes_df, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mostrar Ambientes Disponibles")
        self.setGeometry(300, 300, 800, 600)
        
        self.ambientes_df = ambientes_df
        
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)

        self.label_titulo = QLabel("Ambientes Disponibles", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        vbox.addWidget(self.label_titulo)

        self.table = QTableWidget(self)
        
        if not self.ambientes_df.empty:
            self.table.setColumnCount(len(self.ambientes_df.columns))
            self.table.setHorizontalHeaderLabels(self.ambientes_df.columns.tolist())
            self.llenar_tabla()
        else:
            self.table.setColumnCount(1)
            self.table.setHorizontalHeaderLabels(["No hay ambientes disponibles"])

        vbox.addWidget(self.table)
        self.setLayout(vbox)
        
    def llenar_tabla(self):
        self.table.setRowCount(len(self.ambientes_df))

        for i, row in self.ambientes_df.iterrows():
            for j, (column, value) in enumerate(row.items()):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))
                
class VentanaControlActividades(QWidget):
    def __init__(self, ventana_principal, parent=None):
        super().__init__()
        self.ventana_principal = ventana_principal
        self.setWindowTitle("Control de Actividades")
        self.setGeometry(200, 200, 600, 400)

        self.gestor_actividades = ventana_principal.gestor_actividades
        
        self.regreso_button = QPushButton("Regresar")
        self.regreso_button.clicked.connect(self.regresar)
        
        self.initUI()

    def initUI(self):
        self.label_titulo = QLabel("Control de Actividades", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px; margin-bottom: 20px;")

        self.btn_agregar = QPushButton("Agregar Actividad", self)
        self.btn_eliminar = QPushButton("Eliminar Actividad", self)
        self.btn_actualizar = QPushButton("Actualizar Actividad", self)
        self.btn_consultar = QPushButton("Consultar Actividad", self)
        self.btn_mostrar =  QPushButton("Mostrar Actividades")
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.label_titulo)
        vbox.addWidget(self.btn_agregar)
        vbox.addWidget(self.btn_eliminar)
        vbox.addWidget(self.btn_actualizar)
        vbox.addWidget(self.btn_consultar)
        vbox.addWidget(self.btn_mostrar)
        vbox.addStretch()
        
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.regreso_button)
        hbox.addStretch()

        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.btn_agregar.clicked.connect(self.agregar_actividad)
        self.btn_eliminar.clicked.connect(self.eliminar_actividad)
        self.btn_actualizar.clicked.connect(self.actualizar_actividad)
        self.btn_consultar.clicked.connect(self.consultar_actividad)
        self.btn_mostrar.clicked.connect(self.mostrar_actividades)
    
    def regresar(self):
        self.ventana_principal.show()  
        self.close()
             
    def agregar_actividad(self):
        codigo_clase, ok = QInputDialog.getText(self, "Agregar Actividad", "Ingrese el código de la clase:")
        if not ok or not codigo_clase:
            return

        nombre, ok = QInputDialog.getText(self, "Agregar Actividad", "Ingrese el nombre de la actividad:")
        if not ok or not nombre:
            return

        duracion, ok = QInputDialog.getInt(self, "Agregar Actividad", "Ingrese la duración de la actividad (en periodos):")
        if not ok:
            return

        tamaño, ok = QInputDialog.getInt(self, "Agregar Actividad", "Ingrese el tamaño del grupo:")
        if not ok:
            return

        grupo, ok = QInputDialog.getText(self, "Agregar Actividad", "Ingrese el grupo:")
        if not ok or not grupo:
            return

        docente, ok = QInputDialog.getText(self, "Agregar Actividad", "Ingrese el nombre del docente (opcional):")
        if not ok:
            docente = None

        nueva_actividad = Actividad(codigo_clase, nombre, duracion, tamaño, grupo, docente)
        self.gestor_actividades.agregar_actividad(nueva_actividad)
        self.exportar_actividades()

    def eliminar_actividad(self):
        codigo_clase, ok = QInputDialog.getText(self, "Eliminar Actividad", "Ingrese el código de la clase de la actividad a eliminar:")
        if ok and codigo_clase:
            actividad_df = self.gestor_actividades.consultar_actividad(codigo_clase)
            if not actividad_df.empty:
                self.gestor_actividades.eliminar_actividad(codigo_clase)
                self.exportar_actividades()
                QMessageBox.information(self, "Éxito", "Actividad eliminada correctamente.")
            else:
                QMessageBox.warning(self, "Error", f"Actividad con código de clase {codigo_clase} no encontrada.")

    def actualizar_actividad(self):
        codigo_clase, ok = QInputDialog.getText(self, "Actualizar Actividad", "Ingrese el código de la clase de la actividad a actualizar:")
        if ok and codigo_clase:
            actividad_df = self.gestor_actividades.consultar_actividad(codigo_clase)
            if not actividad_df.empty:
                actividad = actividad_df.iloc[0]  # Obtener la primera fila del DataFrame
                nuevo_nombre, ok = QInputDialog.getText(self, "Actualizar Actividad", f"Nombre actual: {actividad['nombre']}, ingrese el nuevo nombre de la actividad:")
                if not ok:
                    return
                nueva_duracion, ok = QInputDialog.getInt(self, "Actualizar Actividad", f"Duración actual: {actividad['duracion']}, ingrese la nueva duración de la actividad (en periodos):")
                if not ok:
                    return
                nuevo_tamaño, ok = QInputDialog.getInt(self, "Actualizar Actividad", f"Tamaño actual: {actividad['tamaño']}, ingrese el nuevo tamaño del grupo:")
                if not ok:
                    return
                nuevo_grupo, ok = QInputDialog.getText(self, "Actualizar Actividad", f"Grupo actual: {actividad['grupo']}, ingrese el nuevo grupo:")
                if not ok:
                    return
                nuevo_docente, ok = QInputDialog.getText(self, "Actualizar Actividad", f"Docente actual: {actividad['docente']}, ingrese el nuevo nombre del docente (opcional):")
                if not ok:
                    nuevo_docente = actividad['docente']
                datos_actualizados = {
                    'nombre': nuevo_nombre,
                    'duracion': nueva_duracion,
                    'tamaño': nuevo_tamaño,
                    'grupo': nuevo_grupo,
                    'docente': nuevo_docente
                }
                self.gestor_actividades.actualizar_actividad(codigo_clase, datos_actualizados)
                self.exportar_actividades()
                QMessageBox.information(self, "Éxito", "Actividad actualizada correctamente.")
            else:
                QMessageBox.warning(self, "Error", f"Actividad con código de clase {codigo_clase} no encontrada.")


    def consultar_actividad(self):
        codigo_clase, ok = QInputDialog.getText(self, "Consultar Actividad", "Ingrese el código de la clase de la actividad a consultar:")
        if ok and codigo_clase:
            actividad_df = self.gestor_actividades.consultar_actividad(codigo_clase)
            if not actividad_df.empty:
                actividad = actividad_df.iloc[0]  # Obtener la primera fila del DataFrame
                QMessageBox.information(self, "Consulta de Actividad", 
                                        f"Código de Clase: {actividad['codigo_clase']}\n"
                                        f"Nombre de Actividad: {actividad['nombre']}\n"
                                        f"Duración: {actividad['duracion']} periodos\n"
                                        f"Tamaño: {actividad['tamaño']}\n"
                                        f"Grupo: {actividad['grupo']}\n"
                                        f"Docente: {actividad['docente']}")
            else:
                QMessageBox.warning(self, "Error", f"Actividad con código de clase {codigo_clase} no encontrada.")
                
    def exportar_actividades(self):
        self.gestor_actividades.exportar_a_csv(csv_path_actividades)
        
    def mostrar_actividades(self):
        actividades_df = self.gestor_actividades.actividades_df  # Obtener el DataFrame de actividades
        self.mostrar_actividades_dialogo = MostrarActividadesDialogo(actividades_df)
        self.mostrar_actividades_dialogo.exec_()

class MostrarActividadesDialogo(QDialog):
    def __init__(self, actividades_df, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mostrar Actividades")
        self.setGeometry(300, 300, 800, 600)
        
        self.actividades_df = actividades_df.fillna('-')  # Reemplazar NaN con '-'
        
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)

        self.label_titulo = QLabel("Actividades Registradas", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        vbox.addWidget(self.label_titulo)

        self.table = QTableWidget(self)
        
        if not self.actividades_df.empty:
            self.table.setColumnCount(len(self.actividades_df.columns))
            self.table.setHorizontalHeaderLabels(self.actividades_df.columns.tolist())
            self.llenar_tabla()
        else:
            self.table.setColumnCount(1)
            self.table.setHorizontalHeaderLabels(["No hay actividades registradas"])

        vbox.addWidget(self.table)
        self.setLayout(vbox)
        
    def llenar_tabla(self):
        self.table.setRowCount(len(self.actividades_df))

        for i, row in self.actividades_df.iterrows():
            for j, (column, value) in enumerate(row.items()):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))


class VentanaControlHorarios(QWidget):
    def __init__(self, ventana_principal, parent=None):
        super().__init__(parent)
        self.ventana_principal = ventana_principal
        self.setWindowTitle("Control de Horarios")
        self.setGeometry(200, 200, 600, 400)

        self.regreso_button = QPushButton("Regresar")
        self.regreso_button.clicked.connect(self.regresar)
        
        self.gestor_actividades = ventana_principal.gestor_actividades
        self.gestor_ambientes = ventana_principal.gestor_ambientes
        self.horarios_df = ventana_principal.horarios_df
        
        self.initUI()

    def initUI(self):
        self.label_titulo = QLabel("Control de Horarios", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px; margin-bottom: 20px;")

        self.btn_consultar_horario = QPushButton("Consultar Horario", self)
        self.btn_asignar_actividad = QPushButton("Asignar Actividad", self)
        self.btn_asignar_aula_actividad = QPushButton("Asignar Aula a Actividad", self)
        self.btn_mostrar_horarios = QPushButton("Mostrar Horarios", self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label_titulo)
        vbox.addWidget(self.btn_consultar_horario)
        vbox.addWidget(self.btn_asignar_actividad)
        vbox.addWidget(self.btn_asignar_aula_actividad)
        vbox.addWidget(self.btn_mostrar_horarios)
        vbox.addStretch()

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.regreso_button)
        hbox.addStretch()

        vbox.addLayout(hbox)
        
        self.setLayout(vbox)

        self.btn_consultar_horario.clicked.connect(self.consultar_horario)
        self.btn_asignar_actividad.clicked.connect(self.asignar_actividad)
        self.btn_asignar_aula_actividad.clicked.connect(self.asignar_aula_actividad)
        self.btn_mostrar_horarios.clicked.connect(self.mostrar_horarios)
        
    def regresar(self):
        self.ventana_principal.show()  
        self.close()
             
    def consultar_horario(self):
        self.consultar_horario_dialogo = ConsultarHorarioDialogo(self.gestor_ambientes, self.gestor_actividades, self.horarios_df)
        self.consultar_horario_dialogo.exec_()

    def asignar_actividad(self):
        self.asignar_actividad_dialogo = AsignarActividadDialogo(self.gestor_ambientes, self.gestor_actividades, self.horarios_df)
        self.asignar_actividad_dialogo.exec_()
    
    def asignar_aula_actividad(self):
        self.asignar_aula_actividad_dialogo = AsignarAulaActividadDialogo(self.gestor_ambientes, self.gestor_actividades, self.horarios_df)
        self.asignar_aula_actividad_dialogo.exec_()
        
    def mostrar_horarios(self):
        try:
            if not self.horarios_df.horarios_df.empty:
                self.mostrar_horarios_dialogo = MostrarHorariosDialogo(self.horarios_df.horarios_df)
                self.mostrar_horarios_dialogo.exec_()
            else:
                print("No hay horarios disponibles para mostrar.")
        except Exception as e:
            print(f"Error al mostrar los horarios: {e}")

class ConsultarHorarioDialogo(QDialog):
    def __init__(self, gestor_ambientes, gestor_actividades, horarios_df, parent=None):
        super().__init__(parent)
        self.gestor_ambientes = gestor_ambientes
        self.gestor_actividades = gestor_actividades
        self.horarios_df = horarios_df

        self.setWindowTitle("Consultar Horario")
        self.setGeometry(300, 300, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Consulta de Horarios")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(self.label)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Código", "Hora Inicio", "Hora Fin", "Actividad"])
        layout.addWidget(self.table)

        self.btn_consultar = QPushButton("Consultar", self)
        self.btn_consultar.clicked.connect(self.consultar)
        layout.addWidget(self.btn_consultar)

        self.setLayout(layout)

    def consultar(self, codigo_ambiente):
        
        self.table.setRowCount(0)
        
        gestor_ambientes = GestorDeAmbientes()
        
        horarios = HorariosDataFrame.consultar_horario(self, codigo_ambiente, gestor_ambientes) 
        for horario in horarios:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(horario.codigo_ambiente))
            self.table.setItem(row_position, 1, QTableWidgetItem(horario.hora_inicio))
            self.table.setItem(row_position, 2, QTableWidgetItem(horario.hora_fin))
            self.table.setItem(row_position, 3, QTableWidgetItem(horario.actividad.nombre if horario.actividad else ""))

class AsignarActividadDialogo(QDialog):
    def __init__(self, gestor_ambientes, gestor_actividades, horarios_df, parent=None):
        super().__init__(parent)
        self.gestor_ambientes = gestor_ambientes
        self.gestor_actividades = gestor_actividades
        self.horarios_df = horarios_df

        self.setWindowTitle("Asignar Actividad")
        self.setGeometry(300, 300, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Asignar Actividad")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(self.label)

        self.btn_asignar = QPushButton("Asignar", self)
        self.btn_asignar.clicked.connect(self.asignar)
        layout.addWidget(self.btn_asignar)

        self.setLayout(layout)

    def asignar(self):
        codigo_ambiente, ok = QInputDialog.getText(self, "Asignar Actividad", "Ingrese el código del ambiente:")
        if ok and codigo_ambiente:
            ambiente = self.gestor_ambientes.consultar_ambiente(codigo_ambiente)
            if not ambiente.empty:
                periodo, ok = QInputDialog.getText(self, "Asignar Actividad", "Ingrese el período (e.g., '8-8:50 AM'): ")
                if ok and periodo:
                    codigo_actividad, ok = QInputDialog.getText(self, "Asignar Actividad", "Ingrese el código de la actividad:")
                    if ok and codigo_actividad:
                        actividad = self.gestor_actividades.consultar_actividad(codigo_actividad)
                        if not actividad.empty:
                            actividad_obj = Actividad(**actividad.iloc[0].to_dict())
                            self.horarios_df.asignar_actividad_a_ambiente(codigo_ambiente, periodo, actividad_obj, self.gestor_ambientes)
                            QMessageBox.information(self, "Éxito", "Actividad asignada correctamente.")
                        else:
                            QMessageBox.warning(self, "Error", f"Actividad con código {codigo_actividad} no encontrada.")
            else:
                QMessageBox.warning(self, "Error", f"Ambiente con código {codigo_ambiente} no encontrado.")

class AsignarAulaActividadDialogo(QDialog):
    def __init__(self, gestor_ambientes, gestor_actividades, horarios_df, parent=None):
        super().__init__(parent)
        self.gestor_ambientes = gestor_ambientes
        self.gestor_actividades = gestor_actividades
        self.horarios_df = horarios_df

        self.setWindowTitle("Asignar Aula a Actividad")
        self.setGeometry(300, 300, 500, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Asignar Aula a Actividad")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(self.label)

        # Step 1: Select Activity
        self.label_actividad = QLabel("Seleccione la Actividad:", self)
        layout.addWidget(self.label_actividad)

        self.combo_actividades = QComboBox(self)
        self.combo_actividades.addItem("")  # Opción en blanco
        self.combo_actividades.addItems(self.gestor_actividades.actividades_df['nombre'].tolist())
        layout.addWidget(self.combo_actividades)

        # Step 2: Select Environment (filtered by activity requirements)
        self.label_ambiente = QLabel("Seleccione el Ambiente:", self)
        layout.addWidget(self.label_ambiente)

        self.combo_ambientes = QComboBox(self)
        layout.addWidget(self.combo_ambientes)

        # Step 3: Select Free Period
        self.label_periodo = QLabel("Seleccione el Periodo Libre:", self)
        layout.addWidget(self.label_periodo)

        self.combo_periodos = QComboBox(self)
        layout.addWidget(self.combo_periodos)

        self.btn_asignar = QPushButton("Asignar", self)
        self.btn_asignar.clicked.connect(self.asignar)
        layout.addWidget(self.btn_asignar)

        self.setLayout(layout)

        # Conectar señales
        self.combo_actividades.currentIndexChanged.connect(self.update_ambientes)

    def update_ambientes(self):
        # Desconectar señal para evitar que se dispare automáticamente al seleccionar opción en blanco
        try:
            self.combo_ambientes.currentIndexChanged.disconnect(self.update_periodos)
        except TypeError:
            pass 
        
        # Obtener nombre de la actividad seleccionada
        actividad_nombre = self.combo_actividades.currentText()

        # Verificar si se ha seleccionado una actividad válida (no la opción en blanco)
        if actividad_nombre:
            actividad_data = self.gestor_actividades.actividades_df[self.gestor_actividades.actividades_df['nombre'] == actividad_nombre].iloc[0]
            actividad = Actividad(**actividad_data.to_dict())
            
            # Obtener ambientes disponibles para la actividad seleccionada
            ambientes_disponibles = self.horarios_df.mostrar_ambientes_disponibles(actividad, self.gestor_ambientes)

            # Actualizar combo de ambientes
            self.combo_ambientes.clear()
            self.combo_ambientes.addItem("")  # Opción en blanco
            self.combo_ambientes.addItems(ambientes_disponibles)

        # Reconectar señal al finalizar actualización
        self.combo_ambientes.currentIndexChanged.connect(self.update_periodos)

    def update_periodos(self):
        # Desconectar señal para evitar que se dispare automáticamente al seleccionar opción en blanco
        try:
            self.combo_periodos.currentIndexChanged.disconnect(self.asignar)
        except TypeError:
            pass

        # Obtener nombre de ambiente seleccionado
        ambiente_codigo = self.combo_ambientes.currentText()

        # Verificar si se ha seleccionado un ambiente válido (no la opción en blanco)
        if ambiente_codigo:
            # Obtener nombre de la actividad seleccionada
            actividad_nombre = self.combo_actividades.currentText()
            actividad_data = self.gestor_actividades.actividades_df[self.gestor_actividades.actividades_df['nombre'] == actividad_nombre].iloc[0]
            actividad = Actividad(**actividad_data.to_dict())
            
            # Obtener periodos libres para el ambiente y duración de la actividad seleccionados
            periodos_libres = self.horarios_df.obtener_periodos_libres(ambiente_codigo, actividad.duracion)

            # Actualizar combo de periodos libres
            self.combo_periodos.clear()
            self.combo_periodos.addItem("")  # Opción en blanco
            self.combo_periodos.addItems(periodos_libres)

        # Reconectar señal al finalizar actualización
        self.combo_periodos.currentIndexChanged.connect(self.asignar)

    def asignar(self):
        # Obtener valores seleccionados
        actividad_nombre = self.combo_actividades.currentText()
        ambiente_codigo = self.combo_ambientes.currentText()
        periodo_inicio = self.combo_periodos.currentText()

        # Verificar si se han seleccionado todos los valores necesarios
        if not actividad_nombre or not ambiente_codigo or not periodo_inicio:
            QMessageBox.critical(self, "Error", "Debe seleccionar una actividad, un ambiente y un periodo libre.")
            return

        # Obtener datos de la actividad seleccionada
        actividad_data = self.gestor_actividades.actividades_df[self.gestor_actividades.actividades_df['nombre'] == actividad_nombre].iloc[0]
        actividad = Actividad(**actividad_data.to_dict())
        
        # Asignar actividad al ambiente y periodo seleccionados
        self.horarios_df.asignar_actividad_a_ambiente(ambiente_codigo, periodo_inicio, actividad, self.gestor_ambientes)
        
        QMessageBox.information(self, "Éxito", "Actividad asignada correctamente.")


class MostrarHorariosDialogo(QDialog):
    def __init__(self, horarios_df, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mostrar Horarios")
        self.setGeometry(300, 300, 800, 600)
        
        if horarios_df is not None:
            self.horarios_df = horarios_df.fillna('-')
        else:
            self.horarios_df = pd.DataFrame()  # Crear un DataFrame vacío para evitar errores
        
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)

        self.label_titulo = QLabel("Horarios", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        vbox.addWidget(self.label_titulo)

        self.table = QTableWidget(self)
        
        if not self.horarios_df.empty:
            self.table.setColumnCount(len(self.horarios_df.columns) + 1)
            self.table.setHorizontalHeaderLabels(["Ambiente"] + list(self.horarios_df.columns))
            self.llenar_tabla()
        else:
            self.table.setColumnCount(1)
            self.table.setHorizontalHeaderLabels(["No hay horarios disponibles"])

        vbox.addWidget(self.table)
        
    def llenar_tabla(self):
        self.table.setRowCount(len(self.horarios_df))

        for i, (ambiente, row) in enumerate(self.horarios_df.iterrows()):
            self.table.setItem(i, 0, QTableWidgetItem(ambiente))
            for j, (periodo, actividad) in enumerate(row.items(), start=1):
                self.table.setItem(i, j, QTableWidgetItem(actividad))
            
def main():
    app = QApplication(sys.argv)
    ventana_principal = VentanaPrincipal()
    ventana_principal.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
