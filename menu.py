import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QMenuBar, QMenu, QAction, QInputDialog, QDialog, QLineEdit
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
        self.setCentralWidget(self.ventana_ambientes)

    def mostrar_control_actividades(self):
        self.ventana_actividades = VentanaControlActividades(self)
        self.setCentralWidget(self.ventana_actividades)

    def mostrar_control_horarios(self):
        self.ventana_horarios = VentanaControlHorarios(self)
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
    def __init__(self, parent=None):
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
        nombre, ok = QInputDialog.getText(self, "Agregar Actividad", "Ingrese el nombre de la actividad:")
        if ok and nombre:
            tipo, ok = QInputDialog.getText(self, "Agregar Actividad", "Ingrese el tipo de actividad:")
            if ok and tipo:
                nueva_actividad = Actividad(nombre, tipo)
                self.gestor_actividades.agregar_actividad(nueva_actividad)

    def eliminar_actividad(self):
        nombre, ok = QInputDialog.getText(self, "Eliminar Actividad", "Ingrese el nombre de la actividad a eliminar:")
        if ok and nombre:
            self.gestor_actividades.eliminar_actividad(nombre)
            QMessageBox.information(self, "Éxito", "Actividad eliminada correctamente.")

    def actualizar_actividad(self):
       nombre, ok = QInputDialog.getText(self, "Actualizar Actividad", "Ingrese el nombre de la actividad a actualizar:")
       if ok and nombre:
            actividad = self.gestor_actividades.consultar_actividad(nombre)
            if actividad is not None:
                nuevo_nombre, ok = QInputDialog.getText(self, "Actualizar Actividad", f"Nombre actual: {actividad.nombre}, ingrese el nuevo nombre de la actividad:")
                if ok and nuevo_nombre:
                    nuevo_tipo, ok = QInputDialog.getText(self, "Actualizar Actividad", f"Tipo actual: {actividad.tipo}, ingrese el nuevo tipo de actividad:")
                    if ok and nuevo_tipo:
                        nueva_actividad = Actividad(nuevo_nombre, nuevo_tipo)
                        self.gestor_actividades.actualizar_actividad(nombre, nueva_actividad)
                        QMessageBox.information(self, "Éxito", "Actividad actualizada correctamente.")
            else:
                QMessageBox.warning(self, "Error", f"Actividad con nombre {nombre} no encontrada.")

    def consultar_actividad(self):
        nombre, ok = QInputDialog.getText(self, "Consultar Actividad", "Ingrese el nombre de la actividad a consultar:")
        if ok and nombre:
            actividad = self.gestor_actividades.consultar_actividad(nombre)
            if actividad is not None:
                QMessageBox.information(self, "Consulta de Actividad", f"Nombre de Actividad: {actividad.nombre}\nTipo: {actividad.tipo}")
            else:
                QMessageBox.warning(self, "Error", f"Actividad con nombre {nombre} no encontrada.")
        
    

class VentanaControlHorarios(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Control de Horarios")
        self.setGeometry(200, 200, 600, 400)

        self.gestor_actividades = GestorDeActividades(Usuario("NombreUsuario", "RolUsuario"))
        self.gestor_ambientes = GestorDeAmbientes(Usuario("NombreUsuario", "RolUsuario"))
        self.horarios_df = HorariosDataFrame()
        
        self.initUI()

    def initUI(self):
        self.label_titulo = QLabel("Control de Horarios", self)
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px; margin-bottom: 20px;")

        self.btn_consultar_horario = QPushButton("Consultar Horario", self)
        self.btn_asignar_actividad = QPushButton("Asignar Actividad", self)
        self.btn_mostrar_horarios = QPushButton("Mostrar Horarios", self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label_titulo)
        vbox.addWidget(self.btn_consultar_horario)
        vbox.addWidget(self.btn_asignar_actividad)
        vbox.addWidget(self.btn_mostrar_horarios)
        vbox.addStretch()

        self.setLayout(vbox)

        self.btn_consultar_horario.clicked.connect(self.consultar_horario)
        self.btn_asignar_actividad.clicked.connect(self.asignar_actividad)
        self.btn_mostrar_horarios.clicked.connect(self.mostrar_horarios)
        
    def consultar_horario(self):
        self.consultar_horario_dialogo = ConsultarHorarioDialogo(self.gestor_ambientes, self.gestor_actividades)
        self.consultar_horario_dialogo.exec_()

    def asignar_actividad(self):
        self.asignar_actividad_dialogo = AsignarActividadDialogo(self.gestor_ambientes, self.gestor_actividades)
        self.asignar_actividad_dialogo.exec_()
    
    def mostrar_horarios(self):
        horarios = self.horarios_df.mostrar_horarios()
        self.mostrar_horarios_dialogo = MostrarHorariosDialogo(horarios)
        self.mostrar_horarios_dialogo.exec_()

class ConsultarHorarioDialogo(QDialog):
    def __init__(self, gestor_ambientes, gestor_actividades, parent=None):
        super().__init__(parent)
        self.gestor_ambientes = gestor_ambientes
        self.gestor_actividades = gestor_actividades

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

    def consultar(self):
        self.table.setRowCount(0)
        horarios = HorariosDataFrame.obtener_horarios()  # Ajusta esta llamada según cómo obtienes los horarios
        for horario in horarios:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(horario.codigo_ambiente))
            self.table.setItem(row_position, 1, QTableWidgetItem(horario.hora_inicio))
            self.table.setItem(row_position, 2, QTableWidgetItem(horario.hora_fin))
            self.table.setItem(row_position, 3, QTableWidgetItem(horario.actividad.nombre if horario.actividad else ""))

class AsignarActividadDialogo(QDialog):
    def __init__(self, gestor_ambientes, gestor_actividades, parent=None):
        super().__init__(parent)
        self.gestor_ambientes = gestor_ambientes
        self.gestor_actividades = gestor_actividades

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
                actividad_nombre, ok = QInputDialog.getText(self, "Asignar Actividad", "Ingrese el nombre de la actividad:")
                if ok and actividad_nombre:
                    actividad = self.gestor_actividades.consultar_actividad(actividad_nombre)
                    if actividad is not None:
                        self.gestor_ambientes.asignar_actividad(codigo_ambiente, actividad)
                        QMessageBox.information(self, "Éxito", "Actividad asignada correctamente.")
                    else:
                        QMessageBox.warning(self, "Error", f"Actividad con nombre {actividad_nombre} no encontrada.")
            else:
                QMessageBox.warning(self, "Error", f"Ambiente con código {codigo_ambiente} no encontrado.")

class MostrarHorariosDialogo(QDialog): 
    def __init__(self, horarios, parent=None):
        super().__init__(parent)
        self.horarios = horarios

        self.setWindowTitle("Mostrar Horarios")
        self.setGeometry(300, 300, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Horarios")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(self.label)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Código", "Hora Inicio", "Hora Fin", "Actividad"])
        layout.addWidget(self.table)

        for horario in self.horarios:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(horario.codigo_ambiente))
            self.table.setItem(row_position, 1, QTableWidgetItem(horario.hora_inicio))
            self.table.setItem(row_position, 2, QTableWidgetItem(horario.hora_fin))
            self.table.setItem(row_position, 3, QTableWidgetItem(horario.actividad.nombre if horario.actividad else ""))

        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    ventana_principal = VentanaPrincipal()
    ventana_principal.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
