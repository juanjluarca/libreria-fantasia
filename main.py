from ventana_inicio import Ventana_inicio
import sys

def main():
    ventana = Ventana_inicio()
    app = ventana.app
    ventana.inicio()
    sys.exit(app.exec())
    
main()
