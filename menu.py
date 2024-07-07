import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QMenuBar, QMenu, QAction, QInputDialog
from PyQt5.QtCore import Qt
from modulos.gestion_ambientes import GestorDeAmbientes, Ambiente
from modulos.gestion_clases import GestorDeActividades, Actividad
from modulos.administracion import Usuario
from modulos.gestion_horarios import Horario, HorariosDataFrame, Actividad

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Ambientes UAM")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        self.label_titulo = QLabel("Bienvenido al Sistema de Control de Ambientes UAM", self)
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
        self.ventana_ambientes = VentanaControlAmbientes()
        self.setCentralWidget(self.ventana_ambientes)

    def mostrar_control_actividades(self):
        self.ventana_actividades = VentanaControlActividades()
        self.setCentralWidget(self.ventana_actividades)

    def mostrar_control_horarios(self):
        self.ventana_horarios = VentanaControlHorarios()
        self.setCentralWidget(self.ventana_horarios)

class VentanaControlAmbientes(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Control de Ambientes")
        self.setGeometry(200, 200, 600, 400)

        self.parent = parent
        self.gestor_ambientes = GestorDeAmbientes(Usuario("NombreUsuario", "RolUsuario"))

        self.initUI()

    def initUI(self):
        self.label_titulo = QLabel("Control de Ambientes", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px; margin-bottom: 20px;")

        self.btn_agregar = QPushButton("Agregar Ambiente", self)
        self.btn_eliminar = QPushButton("Eliminar Ambiente", self)
        self.btn_actualizar = QPushButton("Actualizar Ambiente", self)
        self.btn_consultar = QPushButton("Consultar Ambiente", self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label_titulo)
        vbox.addWidget(self.btn_agregar)
        vbox.addWidget(self.btn_eliminar)
        vbox.addWidget(self.btn_actualizar)
        vbox.addWidget(self.btn_consultar)
        vbox.addStretch()

        self.setLayout(vbox)

        self.btn_agregar.clicked.connect(self.agregar_ambiente)
        self.btn_eliminar.clicked.connect(self.eliminar_ambiente)
        self.btn_actualizar.clicked.connect(self.actualizar_ambiente)
        self.btn_consultar.clicked.connect(self.consultar_ambiente)

    def agregar_ambiente(self):
        codigo, ok = QInputDialog.getText(self, "Agregar Ambiente", "Ingrese el código del ambiente:")
        if ok and codigo:
            tipo, ok = QInputDialog.getText(self, "Agregar Ambiente", "Ingrese el tipo de ambiente:")
            if ok and tipo:
                disponibilidad, ok = QInputDialog.getText(self, "Agregar Ambiente", "¿Está disponible? (s/n):")
                if ok:
                    disponibilidad = disponibilidad.lower() == 's'
                    activo, ok = QInputDialog.getText(self, "Agregar Ambiente", "¿Está activo? (s/n):")
                    if ok:
                        activo = activo.lower() == 's'
                        capacidad, ok = QInputDialog.getInt(self, "Agregar Ambiente", "Ingrese la capacidad:")
                        if ok:
                            nuevo_ambiente = Ambiente(codigo, tipo, disponibilidad, activo, capacidad)
                            self.gestor_ambientes.agregar_ambiente(nuevo_ambiente)
                            QMessageBox.information(self, "Éxito", "Ambiente agregado correctamente.")

    def eliminar_ambiente(self):
        codigo, ok = QInputDialog.getText(self, "Eliminar Ambiente", "Ingrese el código del ambiente a eliminar:")
        if ok and codigo:
            self.gestor_ambientes.eliminar_ambiente(codigo)
            QMessageBox.information(self, "Éxito", "Ambiente eliminado correctamente.")

    def actualizar_ambiente(self):
        codigo, ok = QInputDialog.getText(self, "Actualizar Ambiente", "Ingrese el código del ambiente a actualizar:")
        if ok and codigo:
            ambiente = self.gestor_ambientes.consultar_ambiente(codigo)
            if not ambiente.empty:
                tipo, ok = QInputDialog.getText(self, "Actualizar Ambiente", f"Tipo actual: {ambiente['tipo_ambiente'].iloc[0]}, ingrese el nuevo tipo de ambiente:")
                if ok and tipo:
                    disponibilidad, ok = QInputDialog.getText(self, "Actualizar Ambiente", f"Disponibilidad actual: {ambiente['estado'].iloc[0]}, ¿Está disponible? (s/n):")
                    if ok:
                        disponibilidad = disponibilidad.lower() == 's'
                        activo, ok = QInputDialog.getText(self, "Actualizar Ambiente", f"Activo actual: {ambiente['activo'].iloc[0]}, ¿Está activo? (s/n):")
                        if ok:
                            activo = activo.lower() == 's'
                            capacidad, ok = QInputDialog.getInt(self, "Actualizar Ambiente", f"Capacidad actual: {ambiente['capacidad'].iloc[0]}, ingrese la nueva capacidad:")
                            if ok:
                                nuevo_ambiente = Ambiente(codigo, tipo, disponibilidad, activo, capacidad)
                                self.gestor_ambientes.actualizar_ambiente(nuevo_ambiente)
                                QMessageBox.information(self, "Éxito", "Ambiente actualizado correctamente.")
            else:
                QMessageBox.warning(self, "Error", f"Ambiente con código {codigo} no encontrado.")

    def consultar_ambiente(self):
        codigo, ok = QInputDialog.getText(self, "Consultar Ambiente", "Ingrese el código del ambiente a consultar:")
        if ok and codigo:
            ambiente = self.gestor_ambientes.consultar_ambiente(codigo)
            if not ambiente.empty:
                QMessageBox.information(self, "Consulta de Ambiente", f"Tipo de Ambiente: {ambiente['tipo_ambiente'].iloc[0]}\nEstado: {ambiente['estado'].iloc[0]}\nCapacidad: {ambiente['capacidad'].iloc[0]}")
            else:
                QMessageBox.warning(self, "Error", f"Ambiente con código {codigo} no encontrado.")

class VentanaControlActividades(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Actividades")
        self.setGeometry(200, 200, 600, 400)

        self.gestor_actividades = GestorDeActividades(Usuario("NombreUsuario", "RolUsuario"))

        self.initUI()

    def initUI(self):
        self.label_titulo = QLabel("Control de Actividades", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px; margin-bottom: 20px;")

        self.btn_agregar = QPushButton("Agregar Actividad", self)
        self.btn_eliminar = QPushButton("Eliminar Actividad", self)
        self.btn_actualizar = QPushButton("Actualizar Actividad", self)
        self.btn_consultar = QPushButton("Consultar Actividad", self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label_titulo)
        vbox.addWidget(self.btn_agregar)
        vbox.addWidget(self.btn_eliminar)
        vbox.addWidget(self.btn_actualizar)
        vbox.addWidget(self.btn_consultar)
        vbox.addStretch()

        self.setLayout(vbox)

        self.btn_agregar.clicked.connect(self.agregar_actividad)
        self.btn_eliminar.clicked.connect(self.eliminar_actividad)
        self.btn_actualizar.clicked.connect(self.actualizar_actividad)
        self.btn_consultar.clicked.connect(self.consultar_actividad)
        
    def agregar_actividad(self):
        codigo = input("Ingrese el código de la actividad: ")
        nombre = input("Ingrese el nombre de la actividad: ")
        duracion = int(input("Ingrese la duración: "))
        tamaño = int(input("Ingrese el tamaño del grupo: "))
        grupo = input("Ingrese el grupo: ")
        docente = input("Ingrese el nombre del docente: ")
        nueva_actividad = Actividad(codigo, nombre, duracion, tamaño, grupo, docente)
        self.gestor_actividades.agregar_actividad(nueva_actividad)
        QMessageBox.information(self, "Éxito", "Actividad agregada correctamente.")

    def eliminar_actividad(self):
        codigo = input("Ingrese el código de la actividad: ")
        self.gestor_actividades.eliminar_actividad(codigo)
        QMessageBox.information(self, "Actividad eliminada exitosamente")

    def actualizar_actividad(self):
        # Implementación de la lógica para actualizar actividad
        pass

    def consultar_actividad(self):
        # Implementación de la lógica para consultar actividad
        pass
        
    

class VentanaControlHorarios(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Horarios")
        self.setGeometry(200, 200, 800, 600)

        self.horarios_contenedor = HorariosDataFrame()

        self.initUI()

    def initUI(self):
        self.label_titulo = QLabel("Control de Horarios", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px; margin-bottom: 20px;")

        self.table_horarios = QTableWidget()
        self.table_horarios.setColumnCount(15)
        self.table_horarios.setHorizontalHeaderLabels([
            'Ambiente', '7-7:50 AM', '8-8:50 AM', '9-9:50 AM', '10-10:50 AM', '11-11:50 AM', 
            '12M-12:50 PM', '1-1:50 PM', '2-2:50 PM', '3-3:50 PM', '4-4:50 PM', 
            '5-5:50 PM', '5:50-6:40 PM', '6:45-7:35 PM', '7:40-8:30 PM', '8:30-9:20 PM'
        ])

        vbox = QVBoxLayout()
        vbox.addWidget(self.label_titulo)
        vbox.addWidget(self.table_horarios)

        self.setLayout(vbox)

        self.setup_menu()

        self.mostrar_horarios()

    def setup_menu(self):
        menu_bar = QMenuBar(self)

        gestion_menu = menu_bar.addMenu('Gestión de Horarios')

        mostrar_horarios_action = QAction('Mostrar Horarios', self)
        mostrar_horarios_action.triggered.connect(self.mostrar_horarios)
        gestion_menu.addAction(mostrar_horarios_action)

        consultar_horario_action = QAction('Consultar Horario', self)
        consultar_horario_action.triggered.connect(self.consultar_horario_dialogo)
        gestion_menu.addAction(consultar_horario_action)

        asignar_actividad_action = QAction('Asignar Actividad', self)
        asignar_actividad_action.triggered.connect(self.asignar_actividad)
        gestion_menu.addAction(asignar_actividad_action)

        verificar_disponibilidad_action = QAction('Verificar Disponibilidad', self)
        verificar_disponibilidad_action.triggered.connect(self.verificar_disponibilidad)
        gestion_menu.addAction(verificar_disponibilidad_action)

    def mostrar_horarios(self):
        horarios = self.horarios_contenedor.mostrar_horarios()
        self.actualizar_tabla_horarios(horarios)
        

    def consultar_horario_dialogo(self):
        codigo_ambiente, ok = QInputDialog.getText(self, 'Consultar Horario', 'Ingrese el codigo del ambiente:')
        if ok:
            horario = self.horarios_contenedor.consultar_horario(codigo_ambiente)
        else:
            print(f"No se encontro el ambiente con el codigo '{codigo_ambiente}'")

    def asignar_actividad(self):
        # Implementar la lógica para asignar una actividad a un horario
        # Ejemplo: Puedes usar un cuadro de diálogo para asignar actividad a un horario específico
        pass

    def verificar_disponibilidad(self):
        # Implementar la lógica para verificar la disponibilidad de un horario
        # Ejemplo: Puedes usar un cuadro de diálogo para verificar la disponibilidad de un horario específico
        pass

    def actualizar_tabla_horarios(self, horarios):
        if horarios is None:
            QMessageBox.warning(self, "Error", "No se han encontrado horarios.")
            return

        self.table_horarios.setRowCount(len(horarios))
        for row_index, (ambiente, horario) in enumerate(horarios.items()):
            self.table_horarios.setItem(row_index, 0, QTableWidgetItem(ambiente))
            for col_index, (periodo, actividad) in enumerate(horario.items(), start=1):
                if actividad:
                    self.table_horarios.setItem(row_index, col_index, QTableWidgetItem(actividad))
                else:
                    self.table_horarios.setItem(row_index, col_index, QTableWidgetItem("Libre"))

def main():
    app = QApplication(sys.argv)
    ventana_principal = VentanaPrincipal()
    ventana_principal.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
