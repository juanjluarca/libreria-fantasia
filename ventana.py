import sys
from Base_datos import BaseDatos
from PyQt6.QtWidgets import QApplication ,QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QMessageBox, QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem, QHeaderView 
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QGuiApplication
import mysql.connector

class Ventana:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window1 = QWidget()
        self.window2 = QWidget()

        self.window1.setStyleSheet("background-color: #5DA9F5;")
        self.window1.setWindowTitle("Inicio de sesion")
        self.window1.setWindowIcon(QIcon("imagenes/logo.ico"))

        self.window2.setStyleSheet("background-color: #5DA9F5;")
        self.window2.setWindowIcon(QIcon("imagenes/logo.ico"))

# Funciones para optimizar el codigo

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
        mesaje_error.setStyleSheet("QMessageBox { color: black; background-color: #e15f5f;} QPushButton {color: black; background-color: #ff0000;} QLabel{color: black;}")
        mesaje_error.setWindowIcon(QIcon("imagenes/warning.ico")) 
        mesaje_error.setWindowTitle(titulo)
        mesaje_error.setText(mensaje)
        mesaje_error.setDefaultButton(QMessageBox.StandardButton.Ok)
        mesaje_error.exec()

    def mensaje_informacion(self, titulo, mensaje):
        mensaje_informacion = QMessageBox()
        mensaje_informacion.setStyleSheet("QMessageBox { color: black; background-color: #36dfea;} QPushButton {color: black; background-color: #22a4ac;} QLabel{color: black;}")
        mensaje_informacion.setWindowIcon(QIcon("imagenes/infomation.ico"))
        mensaje_informacion.setWindowTitle(titulo)
        mensaje_informacion.setText(mensaje)
        mensaje_informacion.setIcon(QMessageBox.Icon.Information)
        mensaje_informacion.setDefaultButton(QMessageBox.StandardButton.Ok) 
        mensaje_informacion.exec()

    def color_boton_sin_oprimir(self, boton):
        boton.setStyleSheet("QPushButton {background-color: white; border: 5px solid black; color: black} QPushButton:hover {background-color: #e1e1e1;} QPushButton:pressed {background-color: #c1c1c1;}")

    def color_boton_oprimido(self, boton):
        boton.setStyleSheet("QPushButton {background-color: #c1c1c1; border: 5px solid black;} QPushButton:hover {background-color: #e1e1e1;} QPushButton:pressed {background-color: #c1c1c1;}")

    def imagen(self, ruta, ancho, alto):
        imagen = QPixmap(ruta)
        imagen = imagen.scaled(ancho, alto, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        return imagen

    def activar_botones(self):
        self.boton_compras.setEnabled(True)
        self.boton_ventas.setEnabled(True)
        self.boton_usuario.setEnabled(True)
        self.boton_inventario.setEnabled(True)
        self.boton_inicio.setEnabled(True)

    def recoloreas_botones(self):
        self.color_boton_sin_oprimir(self.boton_compras)
        self.color_boton_sin_oprimir(self.boton_ventas)
        self.color_boton_sin_oprimir(self.boton_usuario)
        self.color_boton_sin_oprimir(self.boton_inventario)

    def color_tabla(self, tabla):
        tabla.setStyleSheet("QTableWidget {background-color: white; border: 5px solid black;} QTableWidget::item {background-color: 00f4ff; color: black;} QTableWidget::item:selected {background-color: #1fdde5; color: black;} QTableWidget::item:hover {background-color: #4cd9df; color: black;} QHeaderView::section {background-color: #94fbff; color: black;}")

    def ventana_maxima(self, window):
        pantalla = QGuiApplication.primaryScreen() 
        screen_rect = pantalla.availableGeometry()
        window.setGeometry(screen_rect)
    
    def espacio(self, x: int, y: int):
        return QSpacerItem(x, y, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

# Inicio de las ventanas del programa

    def inicio(self):
        main_layout = QVBoxLayout()
        layout1 = QGridLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout2 = QHBoxLayout()
        layout2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        usuario_imagen = self.imagen("imagenes/usuario.png", 150, 150)
        usuario_label = QLabel()
        usuario_label.setPixmap(usuario_imagen)
        usuario_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout2.addWidget(usuario_label)

        usuario = QLabel("Ingrese el usuario:")
        usuario.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        usuario.setStyleSheet("Color: black")

        self.ingreso_usuario = QLineEdit()
        self.ingreso_usuario.setStyleSheet("Color: black; background-color: #bf35e1;")
        self.ingreso_usuario.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_usuario.setFixedWidth(200)

        contrasenia = QLabel("Ingrese la contraseña:")
        contrasenia.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        contrasenia.setStyleSheet("Color: black")

        self.ingreso_contrasenia = QLineEdit()
        self.ingreso_contrasenia.setStyleSheet("Color: black; background-color: #bf35e1;")
        self.ingreso_contrasenia.setEchoMode(QLineEdit.EchoMode.Password)
        self.ingreso_contrasenia.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_contrasenia.setFixedWidth(200)

        boton_ingresar = QPushButton("Ingresar")
        boton_ingresar.clicked.connect(self.verificacion)
        boton_ingresar.setStyleSheet("background-color: white; color: black")
        boton_ingresar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_ingresar.setFixedWidth(200)

        boton_cancelar = QPushButton("cancelar")
        boton_cancelar.clicked.connect(self.cancelar_inicio)
        boton_cancelar.setStyleSheet("background-color: white; color: black")
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_cancelar.setFixedWidth(200)

        layout1.addWidget(usuario, 0, 0)
        layout1.addWidget(self.ingreso_usuario, 0, 1)
        layout1.addItem(self.espacio(10, 10), 1, 0, 1, 1)
        layout1.addWidget(contrasenia, 2, 0)
        layout1.addWidget(self.ingreso_contrasenia, 2, 1)
        layout1.addItem(self.espacio(10, 10), 3, 0, 3, 1)
        layout1.addWidget(boton_ingresar, 4, 0)
        layout1.addWidget(boton_cancelar, 4, 1)

        main_layout.addLayout(layout2)
        main_layout.addLayout(layout1)
        self.window1.setLayout(main_layout)
        self.window1.showNormal()
        self.window1.activateWindow()

    def verificacion(self):
        user = self.ingreso_usuario.text()
        password = self.ingreso_contrasenia.text()
            
        try:
            print("Iniciando base de datos...")
            self.base_datos = BaseDatos(user, password)

            if self.base_datos.conexion and self.base_datos.conexion.is_connected():
                print("Base de datos iniciada correctamente")
                self.window1.close()
                self.ventana_principal()
            else:

                self.mensaje_error("Error", "No se pudo conectar a la base de datos")

        except:
            self.mensaje_error("Error", f"Usuario o contraseña incorrectos:")
            # Limpiar campos
            self.ingreso_usuario.clear()
            self.ingreso_contrasenia.clear()
    def cancelar_inicio(self):
        self.ingreso_usuario.clear()
        self.ingreso_contrasenia.clear()
        self.mensaje_informacion("Cancelado", "Inicio de sesion cancelado")

    def regreso(self):
        aviso = QMessageBox()
        aviso.setStyleSheet("QMessageBox { color: black; background-color: #36dfea;} QPushButton {color: black; background-color: #22a4ac;} QLabel{color: black;}")
        aviso.setWindowIcon(QIcon("imagenes/infomation.ico"))
        aviso.setWindowTitle("¿Cerrar sesion?")
        aviso.setText("Seguro que quiere cerrar la sesion actual")
        aviso.setIcon(QMessageBox.Icon.Information)
        aviso.addButton("Si", QMessageBox.ButtonRole.YesRole)
        aviso.addButton("No", QMessageBox.ButtonRole.NoRole)
        respuesta = aviso.exec()
        if respuesta == 2:
            self.window2.close()
            self.inicio()
            self.mensaje_informacion("Sesion cerrada", "La sesion se ha cerrado correctamente")
        
        elif respuesta == 3:
            self.mensaje_informacion("Cierre de sesion cancelada", "La sesion se a cancelado correctamente")

    def ventana_principal(self):
        self.window2.setWindowTitle("Bienvenido usuario: " + "admin")
        main_layout = QHBoxLayout()

        layout1 = QVBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.layout2 = QVBoxLayout()
        self.layout2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        sub_layout2 = QHBoxLayout()

        espacio_layout2 = QSpacerItem(100, 100, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        self.boton_inicio = QPushButton()
        self.boton_inicio.setIcon(QIcon(self.imagen("imagenes/inicio.png", 80, 80)))
        self.boton_inicio.setIconSize(QSize(150, 100))
        self.color_boton_sin_oprimir(self.boton_inicio)
        self.boton_inicio.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_inicio.clicked.connect(self.regreso)

        self.boton_usuario = QPushButton()
        self.boton_usuario.setIcon(QIcon(self.imagen("imagenes/usuarios.png", 100, 100)))
        self.boton_usuario.setIconSize(QSize(150, 150))
        self.color_boton_sin_oprimir(self.boton_usuario)
        self.boton_usuario.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_usuario.clicked.connect(self.ventana_usuario)

        self.boton_ventas = QPushButton()
        self.boton_ventas.setIcon(QIcon(self.imagen("imagenes/ventas.png", 100, 100)))
        self.boton_ventas.setIconSize(QSize(150, 150))
        self.color_boton_sin_oprimir(self.boton_ventas)
        self.boton_ventas.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_ventas.clicked.connect(self.ventana_ventas)

        self.boton_compras = QPushButton()
        self.boton_compras.setIcon(QIcon(self.imagen("imagenes/compras.png", 100, 100)))
        self.boton_compras.setIconSize(QSize(150, 150))
        self.color_boton_sin_oprimir(self.boton_compras)
        self.boton_compras.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_compras.clicked.connect(self.ventana_compras)

        self.boton_inventario = QPushButton()
        self.boton_inventario.setIcon(QIcon(self.imagen("imagenes/inventario.png", 100, 100)))
        self.boton_inventario.setIconSize(QSize(150, 150))
        self.color_boton_sin_oprimir(self.boton_inventario)
        self.boton_inventario.clicked.connect(self.ventana_inventario)
        self.boton_inventario.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        logo = QLabel()
        logo.setPixmap(self.imagen("imagenes/logo_libreria.png", 400, 400))
        logo.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sub_layout2.addWidget(logo)

        sub_layout2.addItem(espacio_layout2)

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
        
        main_layout.addLayout(layout1)
        main_layout.addLayout(self.layout2)
        self.window2.setLayout(main_layout)
        self.ventana_maxima(self.window2)
        self.window2.showMaximized()

    def ventana_usuario(self):
        self.limpieza_layout(self.layout2)
        self.recoloreas_botones()
        self.color_boton_oprimido(self.boton_usuario)
        self.activar_botones()
        self.boton_usuario.setEnabled(False)

    def ventana_ventas(self):
        self.limpieza_layout(self.layout2)
        self.recoloreas_botones()
        self.color_boton_oprimido(self.boton_ventas)
        self.activar_botones()
        self.boton_ventas.setEnabled(False)

    def ventana_compras(self):
        self.limpieza_layout(self.layout2)
        self.recoloreas_botones()
        self.color_boton_oprimido(self.boton_compras)
        self.activar_botones()
        self.boton_compras.setEnabled(False)

    
    def ventana_inventario(self):
        self.limpieza_layout(self.layout2)
        self.recoloreas_botones()
        self.color_boton_oprimido(self.boton_inventario)
        self.activar_botones()
        self.boton_inventario.setEnabled(False)
        
        self.main_layout_ventana_inventario = QHBoxLayout()

        sub_layout = QVBoxLayout()

        layout3 = QHBoxLayout()
        layout3.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        layout4 = QHBoxLayout()
        layout4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        espacio = QSpacerItem(60, 60, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.boton_editar = QPushButton()
        self.boton_editar.setIcon(QIcon(self.imagen("imagenes/editar.png", 50, 50)))
        self.boton_editar.setIconSize(QSize(70, 70))
        self.boton_editar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_boton_sin_oprimir(self.boton_editar)
        self.boton_editar.clicked.connect(self.editar_producto)

        self.boton_eliminar = QPushButton()
        self.boton_eliminar.setIcon(QIcon(self.imagen("imagenes/eliminar.png", 50, 50)))
        self.boton_eliminar.setIconSize(QSize(70, 70))
        self.boton_eliminar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_boton_sin_oprimir(self.boton_eliminar)
        self.boton_eliminar.clicked.connect(self.eliminar_producto)

        self.boton_agregar = QPushButton()
        self.boton_agregar.setIcon(QIcon(self.imagen("imagenes/agregar.png", 50, 50)))
        self.boton_agregar.setIconSize(QSize(70, 70))
        self.boton_agregar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_boton_sin_oprimir(self.boton_agregar)
        self.boton_agregar.clicked.connect(self.agregar_producto)

        self.boton_busqueda = QPushButton()
        self.boton_busqueda.setIcon(QIcon(self.imagen("imagenes/buscar.png", 50, 50)))
        self.boton_busqueda.setIconSize(QSize(70, 70))
        self.boton_busqueda.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_boton_sin_oprimir(self.boton_busqueda)
        self.boton_busqueda.clicked.connect(self.buscar_producto)
        

        self.ingreso_busqueda = QLineEdit()
        self.ingreso_busqueda.setPlaceholderText("Ingrese el nombre del producto...")
        self.ingreso_busqueda.setStyleSheet("Color: black; background-color: #77f9ff; border: 5px solid black;")
        self.ingreso_busqueda.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ingreso_busqueda.setFixedSize(400, 80)
        self.ingreso_busqueda.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # creacion de tabla,
        # Modificar desde la base de datos
        #Matriz de ejemplo
        inventario = self.base_datos.obtener_productos()
        for i in range(len(inventario)):
            inventario[i] = list(map(str, inventario[i]))

        #inventario = [["1", "Caja de lapices","2","15Q", "Descripcion 1"], ["2", "Caja de boradores","5" ,"20Q", "Descripcion 2"], ["3", "Resma de hojas","10" ,"25Q", "Descripcion 3"]]
        self.tabla = QTableWidget(len(inventario), len(inventario[0]))
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.fila = len(inventario)
        self.columna = len(inventario[0])
        self.items = []

        #Define el indice de las columnas
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Existencias", "Precio", "Descripcion", "Costo"])
        
        #Se ingresan los datos a la tabla con base a la posicion en (x, y) junto con el valor
        for fila in range(self.fila):
            for columna in range(self.columna):
                self.tabla.setItem(fila, columna, QTableWidgetItem(inventario[fila][columna]))
                item = self.tabla.item(fila, columna)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

        #Modificacion del color, bordes y fondo de la tabla
        self.color_tabla(self.tabla)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout3.addWidget(self.boton_editar)
        layout3.addWidget(self.boton_eliminar)
        layout3.addWidget(self.boton_agregar)
        layout3.addWidget(self.boton_busqueda)
        layout3.addWidget(self.ingreso_busqueda)

        layout4.addWidget(self.tabla)
        
        sub_layout.addLayout(layout3)
        sub_layout.addLayout(layout4)
        self.main_layout_ventana_inventario.addItem(espacio)
        self.main_layout_ventana_inventario.addLayout(sub_layout)
        self.layout2.addLayout(self.main_layout_ventana_inventario)

    def llenar_campos(self, row):
        self.nombre_producto = self.tabla.item(row, 1).text()
        self.existencia_producto = self.tabla.item(row, 2).text()
        self.precio_producto = self.tabla.item(row, 3).text()
        self.descripcion_producto = self.tabla.item(row, 4).text()


        self.ingreso_nombre_producto.setText(self.nombre_producto)
        self.ingreso_existencia_producto.setText(self.existencia_producto)
        self.ingreso_precio_producto.setText(self.precio_producto)
        self.ingreso_descripcion_producto.setText(self.descripcion_producto)


    def agregar_producto(self):
        self.boton_editar.setEnabled(False)
        self.boton_agregar.setEnabled(False)
        self.main_layout_editar_producto = QHBoxLayout()
        layout_espacio = QVBoxLayout()
        layout_espacio.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_imagen = QVBoxLayout()
        layout_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        layout1 = QVBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout2 = QGridLayout()

        image_editar = self.imagen("imagenes/agregar.png", 100, 100)
        imagen = QLabel()
        imagen.setPixmap(image_editar)
        imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagen.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        nombre_producto = QLabel("Nombre del producto: ")
        nombre_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        nombre_producto.setStyleSheet("Color: black")

        self.ingreso_nombre_producto = QLineEdit() # Ingreso de texto de nombre
        self.ingreso_nombre_producto.setStyleSheet("Color: black; background-color: #bf35e1;")
        self.ingreso_nombre_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_nombre_producto.setFixedWidth(200)

        existencia_producto = QLabel("Existencias del producto: ")
        existencia_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        existencia_producto.setStyleSheet("Color: black")

        self.ingreso_existencia_producto = QLineEdit() # Ingreso de texto de existencia
        self.ingreso_existencia_producto.setStyleSheet("Color: black; background-color: #bf35e1;")
        self.ingreso_existencia_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_existencia_producto.setFixedWidth(200)

        precio_producto = QLabel("Precio del producto: ")
        precio_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        precio_producto.setStyleSheet("Color: black")

        self.ingreso_precio_producto = QLineEdit() # Ingreso de texto de precio
        self.ingreso_precio_producto.setStyleSheet("Color: black; background-color: #bf35e1;")
        self.ingreso_precio_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_precio_producto.setFixedWidth(200)

        descripcion_producto = QLabel("Descripcion del producto: ")
        descripcion_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        descripcion_producto.setStyleSheet("Color: black")

        # Existencia mínima
        existencia_minima_producto = QLabel("Existencia mínima del producto: ")
        existencia_minima_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        existencia_minima_producto.setStyleSheet("Color: black")

        self.ingreso_existencia_minima_producto = QLineEdit() # Ingreso de texto de existencia mínima
        self.ingreso_existencia_minima_producto.setStyleSheet("Color: black; background-color: #bf35e1;")
        self.ingreso_existencia_minima_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_existencia_minima_producto.setFixedWidth(200)


        self.ingreso_descripcion_producto = QLineEdit() # Ingreso de texto de descripción
        self.ingreso_descripcion_producto.setStyleSheet("Color: black; background-color: #bf35e1;")
        self.ingreso_descripcion_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_descripcion_producto.setFixedWidth(200)

        boton_confirmar = QPushButton("Confirmar")
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_confirmar.clicked.connect(self.confirmar_insercion)

        boton_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_cancelar.clicked.connect(self.cancelar_insercion)

        layout_espacio.addItem(self.espacio(100, 100))

        layout_imagen.addWidget(imagen)
        layout_imagen.addItem(self.espacio(50, 50))

        layout2.addWidget(nombre_producto, 0, 0)
        layout2.addWidget(self.ingreso_nombre_producto, 0, 1)

        layout2.addItem(self.espacio(30, 30), 1, 0)
        layout2.addWidget(existencia_producto, 2, 0)
        layout2.addWidget(self.ingreso_existencia_producto, 2, 1)

        layout2.addItem(self.espacio(30, 30), 3, 0)
        layout2.addWidget(precio_producto, 4, 0)
        layout2.addWidget(self.ingreso_precio_producto, 4, 1)

        layout2.addItem(self.espacio(30, 30), 5, 0)
        layout2.addWidget(descripcion_producto, 6, 0)
        layout2.addWidget(self.ingreso_descripcion_producto, 6, 1)

        layout2.addItem(self.espacio(30, 30), 7, 0)
        layout2.addWidget(existencia_minima_producto, 8, 0)
        layout2.addWidget(self.ingreso_existencia_minima_producto, 8, 1)


        layout2.addItem(self.espacio(30, 30), 8, 0)
        layout2.addWidget(boton_confirmar, 9, 0)
        layout2.addWidget(boton_cancelar, 9, 1)

        layout1.addLayout(layout_espacio)
        layout1.addLayout(layout_imagen)
        layout1.addLayout(layout2)

        self.main_layout_editar_producto.addItem(self.espacio(30, 60))
        self.main_layout_editar_producto.addLayout(layout1)
        self.main_layout_ventana_inventario.addLayout(self.main_layout_editar_producto)

    def buscar_producto(self):
        # Buscar el producto por nombre en la base de datos
        nombre_producto = self.ingreso_busqueda.text()
        resultado = self.base_datos.buscar_producto_por_nombre(nombre_producto)
        print(resultado)
        
        if resultado != []:
            # Limpiar la tabla antes de mostrar los resultados
            self.tabla.clearContents()
            self.tabla.setRowCount(len(resultado))
            
            for i, producto in enumerate(resultado):
                for j, valor in enumerate(producto):
                    self.tabla.setItem(i, j, QTableWidgetItem(str(valor)))
        else:
            self.mensaje_error("Error", "No se encontraron productos con ese nombre")

    def eliminar_producto(self):
        # Eliminar el producto seleccionado en la tabla
        fila = self.tabla.currentRow()
        if fila != -1:
            # Ventana para confirmar eliminacion
            self.confirmar_eliminacion(fila)
            
        else:
            self.mensaje_error("Error", "No se ha seleccionado ningun producto")

    def editar_producto(self):
        self.boton_agregar.setEnabled(False)
        self.boton_editar.setEnabled(False)
        self.tabla.cellClicked.connect(self.llenar_campos)
        self.main_layout_editar_producto = QHBoxLayout()
        layout_espacio = QVBoxLayout()
        layout_espacio.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_imagen = QVBoxLayout()
        layout_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        layout1 = QVBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout2 = QGridLayout()

        image_editar = self.imagen("imagenes/editar.png", 100, 100)
        imagen = QLabel()
        imagen.setPixmap(image_editar)
        imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagen.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        nombre_producto = QLabel("Nombre del producto: ")
        nombre_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        nombre_producto.setStyleSheet("Color: black")

        self.ingreso_nombre_producto = QLineEdit()
        self.ingreso_nombre_producto.setStyleSheet("Color: black; background-color: #bf35e1;")
        self.ingreso_nombre_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_nombre_producto.setFixedWidth(200)

        existencia_producto = QLabel("Existencias del producto: ")
        existencia_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        existencia_producto.setStyleSheet("Color: black")

        self.ingreso_existencia_producto = QLineEdit()
        self.ingreso_existencia_producto.setStyleSheet("Color: black; background-color: #bf35e1;")
        self.ingreso_existencia_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_existencia_producto.setFixedWidth(200)

        precio_producto = QLabel("Precio del producto: ")
        precio_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        precio_producto.setStyleSheet("Color: black")

        self.ingreso_precio_producto = QLineEdit()
        self.ingreso_precio_producto.setStyleSheet("Color: black; background-color: #bf35e1;")
        self.ingreso_precio_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_precio_producto.setFixedWidth(200)

        descripcion_producto = QLabel("Descripcion del producto: ")
        descripcion_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        descripcion_producto.setStyleSheet("Color: black")


        self.ingreso_descripcion_producto = QLineEdit()
        self.ingreso_descripcion_producto.setStyleSheet("Color: black; background-color: #bf35e1;")
        self.ingreso_descripcion_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_descripcion_producto.setFixedWidth(200)


        existencia_minima_producto = QLabel("Existencia mínima del producto: ")
        existencia_minima_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        existencia_minima_producto.setStyleSheet("Color: black")

        self.ingreso_existencia_minima_producto = QLineEdit()
        self.ingreso_existencia_minima_producto.setStyleSheet("Color: black; background-color: #bf35e1;")
        self.ingreso_existencia_minima_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_existencia_minima_producto.setFixedWidth(200)

        boton_confirmar = QPushButton("Confirmar")
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_confirmar.clicked.connect(self.confirmar_edicion)

        boton_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_cancelar.clicked.connect(self.cancelar_edicion)

        layout_espacio.addItem(self.espacio(100, 100))

        layout_imagen.addWidget(imagen)
        layout_imagen.addItem(self.espacio(50, 50))

        layout2.addWidget(nombre_producto, 0, 0)
        layout2.addWidget(self.ingreso_nombre_producto, 0, 1)

        layout2.addItem(self.espacio(30, 30), 1, 0)
        layout2.addWidget(existencia_producto, 2, 0)
        layout2.addWidget(self.ingreso_existencia_producto, 2, 1)

        layout2.addItem(self.espacio(30, 30), 3, 0)
        layout2.addWidget(precio_producto, 4, 0)
        layout2.addWidget(self.ingreso_precio_producto, 4, 1)

        layout2.addItem(self.espacio(30, 30), 5, 0)
        layout2.addWidget(descripcion_producto, 6, 0)
        layout2.addWidget(self.ingreso_descripcion_producto, 6, 1)

        layout2.addItem(self.espacio(30, 30), 7, 0)
        layout2.addWidget(existencia_minima_producto, 8, 0)
        layout2.addWidget(self.ingreso_existencia_minima_producto, 8, 1)

        layout2.addItem(self.espacio(30, 30), 9, 0)
        layout2.addWidget(boton_confirmar, 10, 0)
        layout2.addWidget(boton_cancelar, 10, 1)

        layout1.addLayout(layout_espacio)
        layout1.addLayout(layout_imagen)
        layout1.addLayout(layout2)

        self.main_layout_editar_producto.addItem(self.espacio(30, 60))
        self.main_layout_editar_producto.addLayout(layout1)
        self.main_layout_ventana_inventario.addLayout(self.main_layout_editar_producto)

    def confirmar_eliminacion(self, fila):
        aviso = QMessageBox()
        aviso.setStyleSheet("QMessageBox { color: black; background-color: #36dfea;} QPushButton {color: black; background-color: #22a4ac;} QLabel{color: black;}")
        aviso.setWindowIcon(QIcon("imagenes/infomation.ico"))
        aviso.setWindowTitle("¿Eliminar producto?") 
        aviso.setText("Seguro que quiere eliminar el producto seleccionado")
        aviso.setIcon(QMessageBox.Icon.Information)
        aviso.addButton("Si", QMessageBox.ButtonRole.YesRole)
        aviso.addButton("No", QMessageBox.ButtonRole.NoRole)
        respuesta = aviso.exec()
        if respuesta == 2:
            id_producto = self.tabla.item(fila, 0).text()
            self.base_datos.eliminar_producto(id_producto)
            self.tabla.removeRow(fila)
            self.limpieza_layout(self.main_layout_ventana_inventario)
            self.ventana_inventario()
            self.mensaje_informacion("Producto eliminado", "El producto ha sido eliminado correctamente")
        elif respuesta == 3:
            self.mensaje_informacion("Eliminacion cancelada", "La eliminacion se ha cancelado correctamente")

    def confirmar_edicion(self):
        self.limpieza_layout(self.main_layout_editar_producto)
        self.boton_agregar.setEnabled(True)
        self.boton_editar.setEnabled(True)
        # Implementar función para guardar los cambios en la base de datos
        nombre = self.ingreso_nombre_producto.text()
        existencia = int(self.ingreso_existencia_producto.text())
        precio = float(self.ingreso_precio_producto.text())
        descripcion = self.ingreso_descripcion_producto.text()
        id_producto = int(self.tabla.item(self.tabla.currentRow(), 0).text())
        existencia_minima = int(self.ingreso_existencia_minima_producto.text())
        # Aquí se debe de modificar el producto en la base de datos
        self.base_datos.modificar_producto(id_producto, nombre, precio, descripcion, existencia, existencia_minima)
        # volver a cargar el inventario
        self.limpieza_layout(self.main_layout_ventana_inventario)
        self.ventana_inventario()

        self.mensaje_informacion("Correcciones guardadas", "Los cambios se han guardado correctamente")
    
    def cancelar_edicion(self):
        self.limpieza_layout(self.main_layout_editar_producto)
        self.boton_agregar.setEnabled(True)
        self.boton_editar.setEnabled(True)
        self.mensaje_informacion("Correcciones canceladas", "El cambio se ha cancelado correctamente")

    def confirmar_insercion(self):
        # Lógica para ingresar productos a la base de datos
        self.limpieza_layout(self.main_layout_editar_producto)
        self.boton_editar.setEnabled(True)
        self.boton_agregar.setEnabled(True)

        nombre = self.ingreso_nombre_producto.text()
        existencia = int(self.ingreso_existencia_producto.text())
        precio = float(self.ingreso_precio_producto.text())
        descripcion = self.ingreso_descripcion_producto.text()
        existencia_minima = int(self.ingreso_existencia_minima_producto.text())

        # Aquí se debe de agregar el producto a la base de datos
        self.base_datos.agregar_producto(nombre, precio, existencia, descripcion, existencia_minima)
        
        # Volver a cargar el inventario
        self.limpieza_layout(self.main_layout_ventana_inventario)
        self.ventana_inventario()

        self.mensaje_informacion("Inserción realizada", "El producto se ha insertado correctamente")
        
    def cancelar_insercion(self):
        self.limpieza_layout(self.main_layout_editar_producto)
        self.boton_agregar.setEnabled(True)
        self.boton_editar.setEnabled(True)
        self.mensaje_informacion("Inserción cancelada", "La inserción se canceló correctamente")

