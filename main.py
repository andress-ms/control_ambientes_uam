import sys
from PyQt5.QtWidgets import QApplication, QDialog
from menu import VentanaPrincipal
from menu import VentanaLogin  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    ventana_login = VentanaLogin()
    
    if ventana_login.exec_() == VentanaLogin.Accepted:
        usuario_autenticado = ventana_login.obtener_usuario_autenticado()
        
        if usuario_autenticado:
            window = VentanaPrincipal(usuario_autenticado)
            window.show()
            sys.exit(app.exec_())
    else:
        sys.exit(-1)