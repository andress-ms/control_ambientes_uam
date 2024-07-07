import sys
from PyQt5.QtWidgets import QApplication
from menu import VentanaPrincipal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec_())
