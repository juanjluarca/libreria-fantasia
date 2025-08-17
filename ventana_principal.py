import sys
from codigo import Codigo
from ventana_usuarios import Ventana_usuarios
from ventana_ventas import Ventana_ventas
from ventana_compras import Ventana_compras
from ventana_inventario import Ventana_inventario
from ventana_reporte import Ventana_reporte
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

class Ventana_principal(Codigo):
    def __init__(self, linea1, base_datos, window1: QWidget, boton_ingresar: QPushButton, Boton_salir: QPushButton, id_usuario):
        super().__init__()
        self.line1 = linea1
        self.base_datos = base_datos
        self.botones: list[QPushButton] = []
        self.window1 = window1
        self.boton_ingresar = boton_ingresar
        self.boton_salir = Boton_salir
        self.id_usuario = id_usuario
        # self.ventana2 = Ventana_principal(self.line1, self.base_datos, self.window1, self.boton_ingresar, self.boton_salir)

    def principal(self):
        self.window2 = QWidget()
        self.window2.setWindowIcon(QIcon("imagenes/logo.ico"))
        self.fondo_degradado(self.window2, "#0037FF", "#5DA9F5")
        self.window2.setWindowTitle("Bienvenido al sistema" + " " + self.line1.text())
        nivel = self.base_datos.obtener_nivel_usuario(self.line1.text())

        main_layout = QHBoxLayout()

        layout1 = QVBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.layout2 = QVBoxLayout()
        
        sub_layout2 = QHBoxLayout()

        self.boton_inicio = QPushButton()
        self.boton_inicio.setIcon(QIcon(self.imagen("imagenes/inicio.png", 110, 100)))
        self.boton_inicio.setIconSize(QSize(120, 110))
        self.color_boton_sin_oprimir(self.boton_inicio)
        self.boton_inicio.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_inicio.clicked.connect(self.regreso)

        self.boton_inventario = QPushButton()
        self.boton_inventario.setIcon(QIcon(self.imagen("imagenes/inventario.png", 110, 100)))
        self.boton_inventario.setIconSize(QSize(120, 110))
        self.color_boton_sin_oprimir(self.boton_inventario)
        self.boton_inventario.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.boton_usuario = QPushButton()
        self.boton_usuario.setIcon(QIcon(self.imagen("imagenes/usuarios.png", 110, 100)))
        self.boton_usuario.setIconSize(QSize(120, 110))
        self.color_boton_sin_oprimir(self.boton_usuario)
        self.boton_usuario.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.boton_ventas = QPushButton()
        self.boton_ventas.setIcon(QIcon(self.imagen("imagenes/ventas.png", 110, 100)))
        self.boton_ventas.setIconSize(QSize(120, 110))
        self.color_boton_sin_oprimir(self.boton_ventas)
        self.boton_ventas.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.boton_compras = QPushButton()
        self.boton_compras.setIcon(QIcon(self.imagen("imagenes/compras.png", 110, 100)))
        self.boton_compras.setIconSize(QSize(120, 110))
        self.color_boton_sin_oprimir(self.boton_compras)
        self.boton_compras.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.boton_reporte = QPushButton()
        self.boton_reporte.setIcon(QIcon(self.imagen("imagenes/reportes.png", 110, 100)))
        self.boton_reporte.setIconSize(QSize(120, 110))
        self.color_boton_sin_oprimir(self.boton_reporte)
        self.boton_reporte.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        if nivel == 'Administrador':
            self.boton_usuario.clicked.connect(self.ventana_usuarios)   
            self.boton_inventario.clicked.connect(self.ventana_inventario)
            self.boton_ventas.clicked.connect(self.ventana_ventas)
            self.boton_compras.clicked.connect(self.ventana_compras)
            self.boton_reporte.clicked.connect(self.ventana_reporte)
                
        elif nivel == 'Vendedor':
            self.boton_ventas.clicked.connect(self.ventana_ventas)
            self.color_boton__bloqueado(self.boton_usuario)
            self.color_boton__bloqueado(self.boton_inventario)
            self.color_boton__bloqueado(self.boton_compras)
            self.color_boton__bloqueado(self.boton_reporte)
            self.boton_usuario.clicked.connect(self.aviso_acceso)
            self.boton_inventario.clicked.connect(self.aviso_acceso)
            self.boton_reporte.clicked.connect(self.aviso_acceso)
            self.boton_compras.clicked.connect(self.aviso_acceso)

        self.logo = QLabel()
        self.logo.setPixmap(self.imagen("imagenes/logo_libreria.png", 400, 400))
        self.logo.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.logo.setScaledContents(True)
        
        if len (self.botones) == 0:                            
            self.botones.append(self.boton_usuario) #[0]
            self.botones.append(self.boton_ventas) #[1]
            self.botones.append(self.boton_compras) #[2]
            self.botones.append(self.boton_inventario) #[3]
            self.botones.append(self.boton_reporte) #[4]

        else:
            pass
        
        self.usu = Ventana_usuarios(self.layout2, self.botones, self.base_datos, nivel, self.window2)
        self.ven = Ventana_ventas(self.layout2, self.botones, self.base_datos, self.id_usuario, nivel, self.window2)
        self.com = Ventana_compras(self.layout2, self.botones, self.base_datos, self.id_usuario, nivel, self.window2)
        self.inv = Ventana_inventario(self.layout2, self.botones, self.base_datos, nivel, self.window2)
        self.rep = Ventana_reporte(self.layout2, self.base_datos, self.botones, nivel, self.window2)

        sub_layout2.addStretch()
        sub_layout2.addWidget(self.logo)
        sub_layout2.addStretch()

        self.layout2.addLayout(sub_layout2)

        layout1.addWidget(self.boton_inicio)
        layout1.addItem(self.espacio(10, 10))
        layout1.addWidget(self.boton_usuario)
        layout1.addItem(self.espacio(10, 10))
        layout1.addWidget(self.boton_ventas)
        layout1.addItem(self.espacio(10, 10))
        layout1.addWidget(self.boton_compras)
        layout1.addItem(self.espacio(10, 10))
        layout1.addWidget(self.boton_inventario)
        layout1.addItem(self.espacio(10, 10))
        layout1.addWidget(self.boton_reporte)
        
        main_layout.addLayout(layout1)
        main_layout.addLayout(self.layout2)
        self.window2.setLayout(main_layout)
        self.ventana_maxima(self.window2)
    
    def ventana_usuarios(self):
        self.usu.usuario()

    def ventana_ventas(self):
        self.ven.ventas()

    def ventana_compras(self):
        self.com.compras()

    def ventana_inventario(self):
        self.inv.inventario()

    def ventana_reporte(self):
        self.rep.reportes()

    def regreso(self):
        aviso = QMessageBox()
        aviso.setStyleSheet("QMessageBox { color: black; background-color: #40BCFF;} QPushButton {color: black; background-color: #7C9DFF; border: 2px solid black; min-width: 50px; min-height: 20px;} QPushButton:hover {background-color: #38B3F5;} QPushButton:pressed {background-color: #2268F5;} QLabel{color: black;}")
        aviso.setWindowIcon(QIcon("imagenes/infomation.ico"))
        aviso.setWindowTitle("¿Cerrar sesión?")
        aviso.setText("¿Seguro que desea cerrar la sesión actual?")
        aviso.setIcon(QMessageBox.Icon.Information)
        aviso.addButton("Si", QMessageBox.ButtonRole.YesRole)
        aviso.addButton("No", QMessageBox.ButtonRole.NoRole)
        respuesta = aviso.exec()
        if respuesta == 2:
            if self.rep.nueva_ventana is not None:
                self.rep.nueva_ventana.close()

            if self.ven.nueva_ventana is not None:
                self.ven.nueva_ventana.close()

            if self.com.nueva_ventana is not None:
                self.com.nueva_ventana.close()

            self.window2.close()
            self.window1.inicio()