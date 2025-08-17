import sys
from PyQt6.QtWidgets import QApplication, QMainWindow ,QWidget, QPushButton, QLineEdit, QMessageBox, QSizePolicy, QSpacerItem, QComboBox, QDateEdit 
from PyQt6.QtGui import QIcon, QPixmap, QGuiApplication, QLinearGradient, QColor, QBrush, QPalette, QShortcut, QKeySequence
from PyQt6.QtCore import Qt
import sys, os

class Codigo:
    def __init__(self):    
        self.app = QApplication(sys.argv)

# Funciones para optimizar el codigo
    def fondo_degradado(self, window: QWidget, color1, color2):
        gradiente = QLinearGradient(0, 0, window.width(), window.height())
        color1 = self.conversion_color(color1)
        color2 = self.conversion_color(color2)
        gradiente.setColorAt(0.0, QColor(color1[0], color1[1], color1[2]))
        gradiente.setColorAt(1.0, QColor(color2[0], color2[1], color2[2]))

        pincel = QBrush(gradiente)

        paleta = window.palette()
        paleta.setBrush(QPalette.ColorRole.Window, pincel)
        window.setPalette(paleta)

    def imprimir_reporte(self, Direccion, titulo, mensaje):
        aviso = QMessageBox()
        aviso.setStyleSheet("QMessageBox { color: black; background-color: #40BCFF;} QPushButton {color: black; background-color: #7C9DFF; border: 2px solid black; min-width: 50px; min-height: 20px;} QPushButton:hover {background-color: #38B3F5;} QPushButton:pressed {background-color: #2268F5;} QLabel{color: black;}")
        aviso.setWindowIcon(QIcon("imagenes/infomation.ico"))
        aviso.setWindowTitle(titulo)
        aviso.setText(mensaje)
        aviso.setIcon(QMessageBox.Icon.Information)
        aviso.addButton("Si", QMessageBox.ButtonRole.YesRole)
        aviso.addButton("No", QMessageBox.ButtonRole.NoRole)
        respuesta = aviso.exec()
        if respuesta == 2:
            if sys.platform == "win32":
                try:
                    os.startfile(Direccion, "print")
                except Exception as e:
                    self.mensaje_error("Error", f"No se pudo imprimir el archivo: {e}")

    def conversion_color(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def limpieza_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                sub_layout = item.layout()
                if sub_layout is not None:
                    self.limpieza_layout(sub_layout)
    
    def mensaje_error(self, titulo, mensaje):
        mesaje_error = QMessageBox()
        mesaje_error.setIcon(QMessageBox.Icon.Warning)
        mesaje_error.setStyleSheet("QMessageBox { color: black; background-color: #FF0024;} QPushButton {color: black; background-color: #FF4866; border: 2px solid black; min-width: 50px; min-height: 20px; border-radius: 5px;} QPushButton:hover {background-color: #FF3D7E;} QPushButton:pressed {background-color: #FF0000;} QLabel{color: black;}")
        mesaje_error.setWindowIcon(QIcon(self.generacion_directorio("imagenes/warning.ico"))) 
        mesaje_error.setWindowTitle(titulo)
        mesaje_error.setText(mensaje)
        mesaje_error.setDefaultButton(QMessageBox.StandardButton.Ok)
        mesaje_error.exec()

    def mensaje_informacion(self, titulo, mensaje):
        mensaje_informacion = QMessageBox()
        mensaje_informacion.setStyleSheet("QMessageBox { color: black; background-color: #40BCFF;} QPushButton {color: black; background-color: #7C9DFF; border: 2px solid black; min-width: 50px; min-height: 20px; border-radius: 5px;} QPushButton:hover {background-color: #38B3F5;} QPushButton:pressed {background-color: #2268F5;} QLabel{color: black;}")
        mensaje_informacion.setWindowIcon(QIcon(self.generacion_directorio("imagenes/infomation.ico")))
        mensaje_informacion.setWindowTitle(titulo)
        mensaje_informacion.setText(mensaje)
        mensaje_informacion.setIcon(QMessageBox.Icon.Information)
        mensaje_informacion.setDefaultButton(QMessageBox.StandardButton.Ok) 
        mensaje_informacion.exec()

    def color_boton_sin_oprimir(self, boton: QPushButton):
        boton.setStyleSheet("QPushButton {background-color: white; border: 3px solid black; color: black; border-radius: 5px;} QPushButton:hover {background-color: #38B3F5;} QPushButton:pressed {background-color: #2268F5;}")

    def color_boton_oprimido(self, boton: QPushButton):
        boton.setStyleSheet("QPushButton {background-color: #00CAE0; border: 3px solid black; border-radius: 5px;} QPushButton:hover {background-color: #38B3F5;} QPushButton:pressed {background-color: #2268F5;}")

    def color_boton__bloqueado(self, boton: QPushButton):
        boton.setStyleSheet("QPushButton {background-color: #78ADEB; border: 3px solid black; border-radius: 5px;} QPushButton:hover {background-color: #788AEA;} QPushButton:pressed {background-color: #B178EB;}")
        
    def imagen(self, ruta, ancho, alto):
        ruta = self.generacion_directorio(ruta)
        imagen = QPixmap(ruta)
        imagen = imagen.scaled(ancho, alto, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        return imagen
    
    def generacion_directorio(self, ruta):
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, ruta)

    def activar_botones(self, botones: list[QPushButton]):
        botones[0].setEnabled(True)
        botones[1].setEnabled(True)
        botones[2].setEnabled(True)
        botones[3].setEnabled(True)
        botones[4].setEnabled(True)

    def recoloreas_botones(self, botones: list[QPushButton]):
        self.color_boton_sin_oprimir(botones[0])
        self.color_boton_sin_oprimir(botones[1])
        self.color_boton_sin_oprimir(botones[2])
        self.color_boton_sin_oprimir(botones[3])
        self.color_boton_sin_oprimir(botones[4])

    def color_tabla(self, tabla):
        tabla.setStyleSheet("QTableWidget {background-color: white; border: 5px solid black;} QTableWidget::item {color: black;} QTableWidget::item:selected {background-color: #1fdde5; color: black;} QTableWidget::item:hover {background-color: #4cd9df; color: black;} QHeaderView::section {background-color: #00B4D8; color: black;}")

    def ventana_maxima(self, window: QWidget):
        window.showFullScreen()
        pantalla = QGuiApplication.primaryScreen() 
        screen_rect = pantalla.availableGeometry()
        window.setGeometry(screen_rect)
    
    def espacio(self, x: int, y: int):
        return QSpacerItem(x, y, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    
    def color_linea(self, linea: QLineEdit):
        linea.setStyleSheet("Color: black; background-color: white; border: 3px solid black; border-radius: 5px")
    
    def asignacion_tecla(self, ventana, tecla, boton: QPushButton):
        asignacion = QShortcut(QKeySequence(tecla), ventana)
        asignacion.activated.connect(boton.click)

    def aviso_acceso(self):
        self.mensaje_informacion("Aviso de acceso", "Usted no tiene los permisos necesarios para esta opcion")

    def color_acceso_nivel(self, nivel: str, botones: list[QPushButton]):
        if self.nivel != "Vendedor":
            self.recoloreas_botones(self.botones)

    def color_caja_opciones(self, caja: QComboBox):
        caja.setStyleSheet("""QComboBox {background-color: white; color: Black; border: 3px solid black; border-radius: 5px; padding: 1px 18px 1px 3px;} QComboBox:hover {border: 3px solid #555;} QComboBox:on { border: 3px solid #555; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px;} QComboBox::drop-down {subcontrol-origin: padding; subcontrol-position: top right; width: 20px; border-left-width: 1px; border-left-color: darkgray; border-left-style: solid; border-top-right-radius: 3px; border-bottom-right-radius: 3px; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f0f0f0, stop: 1 #d9d9d9);} QComboBox::down-arrow:on {top: 1px; left: 1px;} QComboBox QAbstractItemView {border: 3px solid black; selection-background-color: white; selection-color: blue; background-color: white; color: Black;} QComboBox QAbstractItemView::item {padding: 5px; min-height: 20px;} QComboBox QAbstractItemView::item:selected {background-color: #e0e0e0; color: black;}""")
    
    def color_caja_fechas(self, caja: QDateEdit):
        caja.setStyleSheet(""" QDateEdit {background-color: white; color: Black; border: 3px solid black; border-radius: 5px; padding: 1px 18px 1px 3px;} QDateEdit:hover { border: 3px solid #555;} QDateEdit:on { border: 3px solid #555; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px;} QDateEdit::drop-down {subcontrol-origin: padding; subcontrol-position: top right; width: 20px; border-left-width: 1px; border-left-color: darkgray; border-left-style: solid; border-top-right-radius: 3px; border-bottom-right-radius: 3px; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f0f0f0, stop: 1 #d9d9d9);} QDateEdit::down-arrow:on {top: 1px; left: 1px;} QDateEdit QAbstractItemView {border: 3px solid black; selection-background-color: white; selection-color: blue; background-color: white; color: Black;} QDateEdit QAbstractItemView::item {padding: 5px; min-height: 20px;} QDateEdit QAbstractItemView::item:selected {background-color: #e0e0e0; color: black;} """)
