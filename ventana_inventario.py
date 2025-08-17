from codigo import Codigo
from PyQt6.QtWidgets import QApplication ,QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QMessageBox, QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem, QHeaderView 
from PyQt6.QtGui import QIcon, QPixmap, QGuiApplication, QLinearGradient, QColor, QBrush, QPalette
from PyQt6.QtCore import Qt, QSize

class Ventana_inventario(Codigo):
    def __init__(self, main_layout, botones, base_datos, nivel, ventana_principal):
        super().__init__()
        self.layout = main_layout
        self.botones = botones
        self.base_datos = base_datos
        self.nivel = nivel
        self.layout_extra: QVBoxLayout | None = None
        self.ventana_principal = ventana_principal

    def inventario(self):
        self.limpieza_layout(self.layout)
        self.color_acceso_nivel(self.nivel, self.botones)
        self.color_boton_oprimido(self.botones[3])
        self.activar_botones(self.botones)
        self.botones[3].setEnabled(False)
        
        self.main_layout = QHBoxLayout()

        layout1 = QVBoxLayout()

        layout2 = QHBoxLayout()
        layout2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    
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
        self.asignacion_tecla(self.ventana_principal, "Return", self.boton_busqueda)
        
        self.ingreso_busqueda = QLineEdit()
        self.ingreso_busqueda.setPlaceholderText("Ingrese el nombre del producto...")
        self.color_linea(self.ingreso_busqueda)
        self.ingreso_busqueda.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ingreso_busqueda.setFixedSize(400, 80)
        self.ingreso_busqueda.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # creacion de tabla,
        # Modificar desde la base de datos
        #Matriz de ejemplo
        inventario = self.base_datos.obtener_productos()  # Esto devuelve la lista de diccionarios

        # Crear la tabla con el número correcto de filas y columnas
        # Las columnas son: ID, Nombre, Existencias, Precio, Descripción, Costo (6 columnas), existencia minima
        self.tabla = QTableWidget(len(inventario), 7)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Define los encabezados de las columnas
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Descripcion", "Existencias", "Precio", "Costo", "Existencia mínima"])

        # Llenar la tabla con los datos
        for fila, producto in enumerate(inventario):
            # Convertir los valores a strings (excepto los que ya lo son)
            # Si la existencia es menor a la minima, cambiar el color de la celda

            
            id_item = QTableWidgetItem(str(producto['id']))
            nombre_item = QTableWidgetItem(producto['nombre'])
            descripcion_item = QTableWidgetItem(producto['descripcion'])
            precio_item = QTableWidgetItem(f"Q{producto['precio']:.2f}")  # Formato con 2 decimales
            costo_item = QTableWidgetItem(f"Q{producto['costo']:.2f}")  # Formato con 2 decimales
            existencia_minima_item = QTableWidgetItem(str(producto['stock_minimo']))
            
            # Añadir items a la tabla
            self.tabla.setItem(fila, 0, id_item)
            self.tabla.setItem(fila, 1, nombre_item)
            self.tabla.setItem(fila, 2, descripcion_item)


            if producto['stock'] < producto['stock_minimo']:
                self.tabla.setItem(fila, 3, QTableWidgetItem(str(producto['stock'])))
                self.tabla.item(fila, 3).setBackground(QBrush(QColor(255, 0, 0)))  # Cambiar el color de fondo a rojo
            else:
                self.tabla.setItem(fila, 3, QTableWidgetItem(str(producto['stock'])))

            self.tabla.setItem(fila, 4, precio_item)
            self.tabla.setItem(fila, 5, costo_item)
            self.tabla.setItem(fila, 6, existencia_minima_item)
            
            # Configurar flags para todos los items
            for col in range(6):
                item = self.tabla.item(fila, col)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        # Ocultal la columna 6 de existencia mínima
        self.tabla.setColumnHidden(0, True)
        self.tabla.setColumnHidden(6, True)


        # Opcional: Ajustar el tamaño de las columnas al contenido
        # self.tabla.resizeColumnsToContents()

        #Modificacion del color, bordes y fondo de la tabla
        self.color_tabla(self.tabla)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout2.addWidget(self.boton_editar)
        layout2.addWidget(self.boton_eliminar)
        layout2.addWidget(self.boton_agregar)
        layout2.addWidget(self.boton_busqueda)
        layout2.addWidget(self.ingreso_busqueda)
        
        layout1.addLayout(layout2)
        layout1.addWidget(self.tabla)

        self.main_layout.addItem(self.espacio(35, 35))
        self.main_layout.addLayout(layout1)
        self.layout.addLayout(self.main_layout)

    def llenar_campos(self, row):
        self.nombre_producto = self.tabla.item(row, 1).text()
        # self.existencia_producto = self.tabla.item(row, 2).text()
        self.descripcion_producto = self.tabla.item(row, 2).text()
        
        self.precio_producto = self.tabla.item(row, 4).text()
        self.existencia_minima = self.tabla.item(row, 6).text()
        # Quitar el formato de moneda
        self.precio_producto = self.precio_producto.replace("Q", "")
        self.ingreso_nombre_producto.setText(self.nombre_producto)

        self.ingreso_precio_producto.setText(self.precio_producto)
        # self.ingreso_existencia_producto.setText(self.existencia_producto)
        self.ingreso_descripcion_producto.setText(self.descripcion_producto)
        self.ingreso_existencia_minima_producto.setText(self.existencia_minima)


    def agregar_producto(self):
        if self.layout_extra is not None:
            self.limpieza_layout(self.layout_extra)

        self.main_layout1 = QVBoxLayout()
        self.main_layout1.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_extra = self.main_layout1

        layout1 = QVBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout2 = QGridLayout()
        layout2.setSpacing(30)

        image_editar = self.imagen("imagenes/agregar.png", 90, 90)
        imagen = QLabel()
        imagen.setPixmap(image_editar)
        imagen.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        imagen.setScaledContents(True)

        nombre_producto = QLabel("Nombre del producto: ")
        nombre_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        nombre_producto.setFixedWidth(200)
        nombre_producto.setStyleSheet("color: Black; font-size: 12px")
        nombre_producto.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.ingreso_nombre_producto = QLineEdit()
        self.color_linea(self.ingreso_nombre_producto)
        self.ingreso_nombre_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_nombre_producto.setFixedWidth(200)

        existencia_producto = QLabel("Existencias del producto: ")
        existencia_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        existencia_producto.setFixedWidth(200)
        existencia_producto.setStyleSheet("color: Black; font-size: 12px")
        existencia_producto.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.ingreso_existencia_producto = QLineEdit()
        self.color_linea(self.ingreso_existencia_producto)

        self.ingreso_existencia_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_existencia_producto.setFixedWidth(200)

        precio_producto = QLabel("Precio del producto: Q")
        precio_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        precio_producto.setFixedWidth(200)
        precio_producto.setStyleSheet("color: Black; font-size: 12px")
        precio_producto.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.ingreso_precio_producto = QLineEdit()
        self.color_linea(self.ingreso_precio_producto)

        self.ingreso_precio_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_precio_producto.setFixedWidth(200)

        descripcion_producto = QLabel("Descripción del producto: ")
        descripcion_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        descripcion_producto.setFixedWidth(200)
        descripcion_producto.setStyleSheet("color: Black; font-size: 12px")
        descripcion_producto.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Existencia mínima
        existencia_minima_producto = QLabel("Existencia mínima del producto: ")
        existencia_minima_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        existencia_minima_producto.setFixedWidth(200)
        existencia_minima_producto.setStyleSheet("color: Black; font-size: 12px")
        existencia_minima_producto.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.ingreso_existencia_minima_producto = QLineEdit() # Ingreso de texto de existencia mínima
        self.color_linea(self.ingreso_existencia_minima_producto)
        
        self.ingreso_existencia_minima_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_existencia_minima_producto.setFixedWidth(200)

        self.ingreso_descripcion_producto = QLineEdit()
        self.color_linea(self.ingreso_descripcion_producto)

        self.ingreso_descripcion_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_descripcion_producto.setFixedWidth(200)

        boton_confirmar = QPushButton("Confirmar")
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setFixedWidth(200)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_confirmar.clicked.connect(self.confirmar_insercion)

        boton_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setFixedWidth(200)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_cancelar.clicked.connect(self.cancelar_insercion)

        layout1.addWidget(imagen)
        layout1.addItem(self.espacio(50, 50))

        layout2.addWidget(nombre_producto, 0, 0)
        layout2.addWidget(self.ingreso_nombre_producto, 0, 1)

        layout2.addWidget(precio_producto, 1, 0)
        layout2.addWidget(self.ingreso_precio_producto, 1, 1)

        layout2.addWidget(descripcion_producto, 2, 0)
        layout2.addWidget(self.ingreso_descripcion_producto, 2, 1)

        layout2.addWidget(existencia_minima_producto, 3, 0)
        layout2.addWidget(self.ingreso_existencia_minima_producto, 3, 1)

        layout2.addWidget(boton_confirmar, 4, 0)
        layout2.addWidget(boton_cancelar, 4, 1)

        self.main_layout1.addItem(self.espacio(80, 80))
        self.main_layout1.addLayout(layout1)
        self.main_layout1.addLayout(layout2)

        self.main_layout.addLayout(self.main_layout1)

    def buscar_producto(self):
        # Buscar el producto por nombre en la base de datos
        nombre_producto = self.ingreso_busqueda.text()
        resultado = self.base_datos.buscar_producto_por_nombre(nombre_producto)
        
        if len(resultado) != 0:
            # Limpiar la tabla antes de mostrar los resultados
            self.tabla.clearContents()
            self.tabla.setRowCount(len(resultado))
            # Llenar la tabla con los resultados de la búsqueda
            for fila, producto in enumerate(resultado):
                id_item = QTableWidgetItem(str(producto['id']))
                nombre_item = QTableWidgetItem(producto['nombre'])
                descripcion_item = QTableWidgetItem(producto['descripcion'])
                existencia_item = QTableWidgetItem(str(producto['stock']))
                precio_item = QTableWidgetItem(f"Q{producto['precio']:.2f}")
                costo_item = QTableWidgetItem(f"Q{producto['costo']:.2f}")
                existencia_minima_item = QTableWidgetItem(str(producto['stock_minimo']))

                # Añadir items a la tabla
                self.tabla.setItem(fila, 0, id_item)
                self.tabla.setItem(fila, 1, nombre_item)
                self.tabla.setItem(fila, 2, descripcion_item)
                self.tabla.setItem(fila, 3, existencia_item)
                self.tabla.setItem(fila, 4, precio_item)
                self.tabla.setItem(fila, 5, costo_item)
                self.tabla.setItem(fila, 6, existencia_minima_item)
        else:
            self.mensaje_error("Error", "No se encontraron productos con ese nombre")

        self.ingreso_busqueda.clear()

    def eliminar_producto(self):
        # Eliminar el producto seleccionado en la tabla
        fila = self.tabla.currentRow()
        if fila != -1:
            # Ventana para confirmar eliminacion
            self.confirmar_eliminacion(fila)
            
        else:
            self.mensaje_error("Error", "No se ha seleccionado ningún producto")

    def editar_producto(self):
        if self.layout_extra is not None:
            self.limpieza_layout(self.layout_extra)

        self.tabla.cellClicked.connect(self.llenar_campos)

        self.main_layout1 = QVBoxLayout()
        self.main_layout1.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_extra = self.main_layout1

        layout1 = QVBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout2 = QGridLayout()
        layout2.setSpacing(30)

        image_editar = self.imagen("imagenes/editar.png", 90, 90)
        imagen = QLabel()
        imagen.setPixmap(image_editar)
        imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imagen.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        imagen.setScaledContents(True)

        nombre_producto = QLabel("Nombre del producto: ")
        nombre_producto.setFixedWidth(200)
        nombre_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        nombre_producto.setStyleSheet("color: Black; font-size: 12px")
        nombre_producto.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.ingreso_nombre_producto = QLineEdit()
        self.color_linea(self.ingreso_nombre_producto)
        self.ingreso_nombre_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_nombre_producto.setFixedWidth(200)

        precio_producto = QLabel("Precio del producto: ")
        precio_producto.setFixedWidth(200)
        precio_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        precio_producto.setStyleSheet("color: Black; font-size: 12px")
        precio_producto.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.ingreso_precio_producto = QLineEdit()
        self.color_linea(self.ingreso_precio_producto)
        self.ingreso_precio_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_precio_producto.setFixedWidth(200)

        descripcion_producto = QLabel("Descripción del producto: ")
        descripcion_producto.setFixedWidth(200)
        descripcion_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        descripcion_producto.setStyleSheet("color: Black; font-size: 12px")
        descripcion_producto.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.ingreso_descripcion_producto = QLineEdit()
        self.color_linea(self.ingreso_descripcion_producto)
        self.ingreso_descripcion_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_descripcion_producto.setFixedWidth(200)

        existencia_minima_producto = QLabel("Existencia mínima del producto: ")
        existencia_minima_producto.setFixedWidth(200)
        existencia_minima_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        existencia_minima_producto.setStyleSheet("color: Black; font-size: 12px")
        existencia_minima_producto.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.ingreso_existencia_minima_producto = QLineEdit()
        self.color_linea(self.ingreso_existencia_minima_producto)
        self.ingreso_existencia_minima_producto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_existencia_minima_producto.setFixedWidth(200)

        boton_confirmar = QPushButton("Confirmar")
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setFixedWidth(200)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_confirmar.clicked.connect(self.confirmar_edicion)

        boton_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setFixedWidth(200)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_cancelar.clicked.connect(self.cancelar_edicion)

        layout1.addWidget(imagen)
        layout1.addItem(self.espacio(50, 50))

        layout2.addWidget(nombre_producto, 0, 0)
        layout2.addWidget(self.ingreso_nombre_producto, 0, 1)

        layout2.addWidget(precio_producto, 1, 0)
        layout2.addWidget(self.ingreso_precio_producto, 1, 1)

        layout2.addWidget(descripcion_producto, 2, 0)
        layout2.addWidget(self.ingreso_descripcion_producto, 2, 1)

        layout2.addWidget(existencia_minima_producto, 3, 0)
        layout2.addWidget(self.ingreso_existencia_minima_producto, 3, 1)

        layout2.addWidget(boton_confirmar, 4, 0)
        layout2.addWidget(boton_cancelar, 4, 1)

        self.main_layout1.addItem(self.espacio(80, 80))
        self.main_layout1.addLayout(layout1)
        self.main_layout1.addLayout(layout2)

        self.main_layout.addLayout(self.main_layout1)

    def confirmar_eliminacion(self, fila):
        aviso = QMessageBox()
        aviso.setStyleSheet("QMessageBox { color: black; background-color: #40BCFF;} QPushButton {color: black; background-color: #7C9DFF; border: 2px solid black; min-width: 50px; min-height: 20px;} QPushButton:hover {background-color: #38B3F5;} QPushButton:pressed {background-color: #2268F5;} QLabel{color: black;}")
        aviso.setWindowIcon(QIcon("imagenes/infomation.ico"))
        aviso.setWindowTitle("¿Eliminar producto?") 
        aviso.setText("¿Seguro que desea eliminar el producto seleccionado?")
        aviso.setIcon(QMessageBox.Icon.Information)
        aviso.addButton("Si", QMessageBox.ButtonRole.YesRole)
        aviso.addButton("No", QMessageBox.ButtonRole.NoRole)
        respuesta = aviso.exec()
        if respuesta == 2:
            id_producto = self.tabla.item(fila, 0).text()
            self.base_datos.eliminar_producto(id_producto)
            self.tabla.removeRow(fila)
            self.limpieza_layout(self.main_layout)
            self.inventario()

    def confirmar_edicion(self):
        self.layout_extra = None
        self.limpieza_layout(self.main_layout1)
        self.boton_agregar.setEnabled(True)
        self.boton_editar.setEnabled(True)
        # Implementar función para guardar los cambios en la base de datos
        nombre = self.ingreso_nombre_producto.text()
        precio = float(self.ingreso_precio_producto.text().replace("Q", ""))
        descripcion = self.ingreso_descripcion_producto.text()
        id_producto = int(self.tabla.item(self.tabla.currentRow(), 0).text())
        existencia_minima = int(self.ingreso_existencia_minima_producto.text())
        # Aquí se debe de modificar el producto en la base de datos
        self.base_datos.modificar_producto(id_producto, nombre, precio, descripcion, existencia_minima)
        # volver a cargar el inventario
        self.limpieza_layout(self.main_layout)
        self.inventario()
    
    def cancelar_edicion(self):
        self.layout_extra = None
        self.limpieza_layout(self.main_layout1)
        self.boton_agregar.setEnabled(True)
        self.boton_editar.setEnabled(True)

    def confirmar_insercion(self):
        self.layout_extra = None
        # Lógica para ingresar productos a la base de datos
        self.limpieza_layout(self.main_layout1)
        self.boton_editar.setEnabled(True)
        self.boton_agregar.setEnabled(True)
        # Verificar que los campos no estén vacíos
        if not self.ingreso_nombre_producto.text() or not self.ingreso_precio_producto.text() or not self.ingreso_existencia_minima_producto.text():
            self.mensaje_error("Error", "Por favor, complete todos los campos")
            return
        # Verificar que el precio y la existencia mínima sean número
        try:
            float(self.ingreso_precio_producto.text())
            int(self.ingreso_existencia_minima_producto.text())
        except ValueError:
            self.mensaje_error("Error", "El precio y la existencia mínima deben ser números")
            return
        nombre = self.ingreso_nombre_producto.text()
        # existencia = int(self.ingreso_existencia_producto.text())
        precio = float(self.ingreso_precio_producto.text())
        descripcion = self.ingreso_descripcion_producto.text()
        existencia_minima = int(self.ingreso_existencia_minima_producto.text())
        try:

        # Aquí se debe de agregar el producto a la base de datos
            self.base_datos.agregar_producto(nombre, precio, descripcion, existencia_minima)
        except Exception as e:
            self.mensaje_error("Error", f"Error al insertar el producto: {str(e)}")
            return
        # Volver a cargar el inventario
        self.limpieza_layout(self.main_layout)
        self.inventario()
        
    def cancelar_insercion(self):
        self.layout_extra = None
        self.limpieza_layout(self.main_layout1)
        self.boton_agregar.setEnabled(True)
        self.boton_editar.setEnabled(True)

