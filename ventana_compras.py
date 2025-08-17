from codigo import Codigo
from PyQt6.QtWidgets import QDateEdit, QDialog, QComboBox, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QMessageBox, QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem, QHeaderView 
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize, QDate
from datetime import datetime

class Ventana_compras(Codigo):
    def __init__(self, main_layout, botones, base_datos, id_usuario, nivel, ventana_principal):
        super().__init__()
        self.layout = main_layout
        self.botones = botones
        self.base_datos = base_datos
        self.id_usuario = id_usuario
        self.carrito_ingreso = []
        self.fila_ingreso = 0
        self.total_compra = 0
        self.layout_extra: QVBoxLayout | None = None
        self.nivel = nivel
        self.nueva_ventana = None
        self.ventana_principal = ventana_principal

    def compras(self):
        self.limpieza_layout(self.layout)
        self.color_acceso_nivel(self.nivel, self.botones)
        self.color_boton_oprimido(self.botones[2])
        self.activar_botones(self.botones)
        self.botones[2].setEnabled(False)

        main_layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout2 = QHBoxLayout()

        self.layout3 = QHBoxLayout()
        self.layout3.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.boton_proveedores = QPushButton()
        self.boton_proveedores.setIcon(QIcon(self.imagen("imagenes/proveedores.png", 90, 90)))
        self.boton_proveedores.setIconSize(QSize(100, 100))
        self.color_boton_sin_oprimir(self.boton_proveedores)
        self.boton_proveedores.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_proveedores.clicked.connect(self.proveedores)

        self.boton_pedido = QPushButton()
        self.boton_pedido.setIcon(QIcon(self.imagen("imagenes/pedido.png", 90, 90)))
        self.boton_pedido.setIconSize(QSize(100, 100))
        self.color_boton_sin_oprimir(self.boton_pedido)
        self.boton_pedido.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_pedido.clicked.connect(self.ingreso_pedido)

        # Agregar botón para acceder a las ordenes de compra (para poder confirmarlas)
        self.boton_ordenes = QPushButton()
        self.boton_ordenes.setIcon(QIcon(self.imagen("imagenes/ordenes.png", 90, 90)))
        self.boton_ordenes.setIconSize(QSize(100, 100))
        self.color_boton_sin_oprimir(self.boton_ordenes)
        self.boton_ordenes.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_ordenes.clicked.connect(self.ordenes_compra)

        # Agregar botón de servicios, que permitirá hacer los pagos de luz, agua, etc.
        self.boton_servicios = QPushButton()
        self.boton_servicios.setIcon(QIcon(self.imagen("imagenes/servicios.png", 90, 90)))
        self.boton_servicios.setIconSize(QSize(100, 100))
        self.color_boton_sin_oprimir(self.boton_servicios)
        self.boton_servicios.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_servicios.clicked.connect(self.servicios)

        informar = QLabel("Oprima uno de los botones que tiene en la parte superior izquierda")
        informar.setStyleSheet("color: Black; font-size: 20px")
        informar.setAlignment(Qt.AlignmentFlag.AlignTop)
        informar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        layout1.addItem(self.espacio(35, 35))
        layout1.addWidget(self.boton_proveedores)
        layout1.addWidget(self.boton_pedido)
        layout1.addWidget(self.boton_ordenes)
        # layout1.addWidget(self.boton_servicios)
        layout1.addStretch()
        
        self.layout3.addStretch()
        self.layout3.addWidget(informar)
        self.layout3.addStretch()

        layout2.addItem(self.espacio(35, 35))
        layout2.addLayout(self.layout3)

        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)

        self.layout.addLayout(main_layout)

    def servicios(self):
        pass

    def proveedores(self):
        self.limpieza_layout(self.layout3)
        self.color_boton_oprimido(self.boton_proveedores)
        self.color_boton_sin_oprimir(self.boton_pedido)
        self.color_boton_sin_oprimir(self.boton_ordenes)

        layout_main = QVBoxLayout()
        layout_main.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)    

        layout1 = QHBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.layout4 = QHBoxLayout()

        self.boton_agregar = QPushButton()
        self.boton_agregar.setIcon(QIcon(self.imagen("imagenes/agregar.png", 45, 45)))
        self.boton_agregar.setIconSize(QSize(55, 55))
        self.color_boton_sin_oprimir(self.boton_agregar)
        self.boton_agregar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_agregar.clicked.connect(self.agregar_proveedor)

        self.boton_eliminar = QPushButton()
        self.boton_eliminar.setIcon(QIcon(self.imagen("imagenes/eliminar.png", 45, 45)))
        self.boton_eliminar.setIconSize(QSize(55, 55))
        self.color_boton_sin_oprimir(self.boton_eliminar)
        self.boton_eliminar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_eliminar.clicked.connect(self.eliminar_proveedor)

        self.boton_editar = QPushButton()
        self.boton_editar.setIcon(QIcon(self.imagen("imagenes/editar.png", 45, 45)))
        self.boton_editar.setIconSize(QSize(55, 55))
        self.color_boton_sin_oprimir(self.boton_editar)
        self.boton_editar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_editar.clicked.connect(self.editar_proveedor)

        self.boton_buscar = QPushButton()
        self.boton_buscar.setIcon(QIcon(self.imagen("imagenes/buscar.png", 45, 45)))
        self.boton_buscar.setIconSize(QSize(55, 55))
        self.color_boton_sin_oprimir(self.boton_buscar)
        self.boton_buscar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_busqueda = QLineEdit()
        self.ingreso_busqueda.setPlaceholderText("Ingrese el ID del proveedor")
        self.color_linea(self.ingreso_busqueda)
        self.ingreso_busqueda.setFixedSize(400, 60)
        self.ingreso_busqueda.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        #Tabla de proveedores
        #proveedores = [["1", "Francisco Queme", "Direccion X", "Ejemplo@gmail.com"]]
        proveedores = self.base_datos.obtener_proveedores()

        #tabla de proveedores
        self.tabla_proveedores = QTableWidget(len(proveedores), 5)

        self.tabla_proveedores.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.tabla_proveedores.setHorizontalHeaderLabels(["ID", "Nombre", "Direccion", "Email", "Teléfono"]) 

        for fila, valor in enumerate(proveedores):
            # Convertir los valores a strings (excepto los que ya lo son)
            # Si la existencia es menor a la minima, cambiar el color de la celda

            
            id_proveedor = QTableWidgetItem(str(valor['id']))
            nombre_proveedor = QTableWidgetItem(valor['nombre'])
            direccion_proveedor = QTableWidgetItem(valor['direccion'])
            email_proveedor = QTableWidgetItem(valor['email'])  # Formato con 2 decimales
            telefono_proveedor = QTableWidgetItem(valor['telefono'])  # Formato con 2 decimales
            
            # Añadir items a la tabla
            self.tabla_proveedores.setItem(fila, 0, id_proveedor)
            self.tabla_proveedores.setItem(fila, 1, nombre_proveedor)
            self.tabla_proveedores.setItem(fila, 2, direccion_proveedor)
            self.tabla_proveedores.setItem(fila, 3, email_proveedor)
            self.tabla_proveedores.setItem(fila, 4, telefono_proveedor)
            
            # Configurar flags para todos los items
            for col in range(5):
                item = self.tabla_proveedores.item(fila, col)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        
        self.tabla_proveedores.resizeColumnsToContents()
        self.color_tabla(self.tabla_proveedores)
        self.tabla_proveedores.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_proveedores.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout1.addWidget(self.boton_agregar)
        layout1.addWidget(self.boton_eliminar)
        layout1.addWidget(self.boton_editar)
        # layout1.addWidget(self.boton_buscar)
        # layout1.addWidget(self.ingreso_busqueda)

        self.layout4.addWidget(self.tabla_proveedores)

        layout_main.addLayout(layout1)
        layout_main.addLayout(self.layout4)

        self.layout3.addLayout(layout_main)
    
    def eliminar_proveedor(self):
        # Se obtiene el id del proveedor seleccionado y se pregunta al usuario si está seguro de eliminarlo
        fila = self.tabla_proveedores.currentRow()
        if fila == -1:
            self.mensaje_error("Error", "Seleccione un proveedor para eliminar.")
            return
        id_proveedor = int(self.tabla_proveedores.item(fila, 0).text())
        nombre_proveedor = self.tabla_proveedores.item(fila, 1).text()
        # Preguntar al usuario si está seguro de eliminar el proveedor
        aviso = QMessageBox()
        aviso.setStyleSheet("QMessageBox { color: black; background-color: #40BCFF;} QPushButton {color: black; background-color: #7C9DFF; border: 2px solid black; min-width: 50px; min-height: 20px;} QPushButton:hover {background-color: #38B3F5;} QPushButton:pressed {background-color: #2268F5;} QLabel{color: black;}")
        aviso.setWindowIcon(QIcon("imagenes/infomation.ico"))
        aviso.setWindowTitle("Eliminar proveedor")
        aviso.setText(f"¿Seguro que desea eliminar al proveedor {nombre_proveedor}?")
        aviso.setIcon(QMessageBox.Icon.Information)
        aviso.addButton("Sí", QMessageBox.ButtonRole.YesRole)
        aviso.addButton("No", QMessageBox.ButtonRole.NoRole)
        respuesta = aviso.exec()
        if respuesta == 2:
            self.base_datos.eliminar_proveedor(id_proveedor)
            self.proveedores()

    def agregar_proveedor(self):
        # Cada que se complete una insercion o elemiminacion el Layout se tiene que volver a poner como none (esto no es definitivo)
        if self.layout_extra is not None:
            self.limpieza_layout(self.layout_extra)

        self.layout_extra = QVBoxLayout()
        self.layout_extra.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout1 = QVBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout2 = QGridLayout()
        layout2.setSpacing(30)

        imagen_agregar = self.imagen("imagenes/agregar.png", 90, 90)
        agregar_label = QLabel()
        agregar_label.setPixmap(imagen_agregar)
        agregar_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        agregar_label.setScaledContents(True)

        self.ingreso_nombre = QLineEdit()
        self.color_linea(self.ingreso_nombre)
        self.ingreso_nombre.setFixedWidth(200)
        self.ingreso_nombre.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_direccion = QLineEdit()
        self.color_linea(self.ingreso_direccion)
        self.ingreso_direccion.setFixedWidth(200)
        self.ingreso_direccion.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_email = QLineEdit()
        self.color_linea(self.ingreso_email)
        self.ingreso_email.setFixedWidth(200)
        self.ingreso_email.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_telefono = QLineEdit()
        self.color_linea(self.ingreso_telefono)
        self.ingreso_telefono.setFixedWidth(200)
        self.ingreso_telefono.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_nombre = QLabel("Ingrese el nombre: ")
        label_nombre.setStyleSheet("color: Black; font-size: 12px")
        label_nombre.setAlignment(Qt.AlignmentFlag.AlignRight)
        label_nombre.setFixedWidth(200)
        label_nombre.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_direccion = QLabel("Ingrese la dirección: ")
        label_direccion.setStyleSheet("color: Black; font-size: 12px")
        label_direccion.setAlignment(Qt.AlignmentFlag.AlignRight)
        label_direccion.setFixedWidth(200)
        label_direccion.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_email = QLabel("Ingrese el email: ")
        label_email.setStyleSheet("color: Black; font-size: 12px")
        label_email.setAlignment(Qt.AlignmentFlag.AlignRight)
        label_email.setFixedWidth(200)
        label_email.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_telefono = QLabel("Ingrese el teléfono: ")
        label_telefono.setStyleSheet("color: Black; font-size: 12px")
        label_telefono.setAlignment(Qt.AlignmentFlag.AlignRight)
        label_telefono.setFixedWidth(200)
        label_telefono.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        boton_agregar = QPushButton("Agregar")
        self.color_boton_sin_oprimir(boton_agregar)
        boton_agregar.setFixedWidth(200)
        boton_agregar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_agregar.clicked.connect(self.agregar_proveedor_bd)

        boton_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setFixedWidth(200)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_cancelar.clicked.connect(self.cancelar_agregado)

        layout1.addWidget(agregar_label)
        layout1.addItem(self.espacio(50, 50))

        layout2.addWidget(label_nombre, 0, 0)
        layout2.addWidget(self.ingreso_nombre, 0, 1)
        layout2.addWidget(label_direccion, 1, 0)
        layout2.addWidget(self.ingreso_direccion, 1, 1)
        layout2.addWidget(label_email, 2, 0)
        layout2.addWidget(self.ingreso_email, 2, 1)
        layout2.addWidget(label_telefono, 3, 0)
        layout2.addWidget(self.ingreso_telefono, 3, 1)
        layout2.addWidget(boton_agregar, 4, 0)
        layout2.addWidget(boton_cancelar, 4, 1)

        self.layout_extra.addLayout(layout1)
        self.layout_extra.addLayout(layout2)

        self.layout4.addLayout(self.layout_extra)


    def editar_proveedor(self):
        # Cada que se complete una insercion o elemiminacion el Layout se tiene que volver a poner como none (esto no es definitivo)
        if self.layout_extra is not None:
            self.limpieza_layout(self.layout_extra)
        
        self.tabla_proveedores.cellClicked.connect(self.llenar_campos)
        
        self.layout_extra = QVBoxLayout()
        self.layout_extra.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout1 = QVBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout2 = QGridLayout()
        layout2.setSpacing(30)   

        imagen_agregar = self.imagen("imagenes/editar.png", 90, 90)
        agregar_label = QLabel()
        agregar_label.setPixmap(imagen_agregar)
        agregar_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        agregar_label.setScaledContents(True)

        self.ingreso_nombre = QLineEdit()
        self.color_linea(self.ingreso_nombre)
        self.ingreso_nombre.setFixedWidth(200)
        self.ingreso_nombre.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_direccion = QLineEdit()
        self.color_linea(self.ingreso_direccion)
        self.ingreso_direccion.setFixedWidth(200)
        self.ingreso_direccion.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_email = QLineEdit()
        self.color_linea(self.ingreso_email)
        self.ingreso_email.setFixedWidth(200)
        self.ingreso_email.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_telefono = QLineEdit()
        self.color_linea(self.ingreso_telefono)
        self.ingreso_telefono.setFixedWidth(200)
        self.ingreso_telefono.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_nombre = QLabel("Ingrese el nombre: ")
        label_nombre.setStyleSheet("color: Black; font-size: 12px")
        label_nombre.setAlignment(Qt.AlignmentFlag.AlignRight)
        label_nombre.setFixedWidth(200)
        label_nombre.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_direccion = QLabel("Ingrese la dirección: ")
        label_direccion.setStyleSheet("color: Black; font-size: 12px")
        label_direccion.setAlignment(Qt.AlignmentFlag.AlignRight)
        label_direccion.setFixedWidth(200)
        label_direccion.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_email = QLabel("Ingrese el email: ")
        label_email.setStyleSheet("color: Black; font-size: 12px")
        label_email.setAlignment(Qt.AlignmentFlag.AlignRight)
        label_email.setFixedWidth(200)
        label_email.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_telefono = QLabel("Ingrese el teléfono: ")
        label_telefono.setStyleSheet("color: Black; font-size: 12px")
        label_telefono.setAlignment(Qt.AlignmentFlag.AlignRight)
        label_telefono.setFixedWidth(200)
        label_telefono.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        boton_confirmar = QPushButton("Confirmar")
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setFixedWidth(200)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_confirmar.clicked.connect(self.editar_proveedor_bd)

        boton_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setFixedWidth(200)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_cancelar.clicked.connect(self.cancelar_edicion)

        layout1.addWidget(agregar_label)
        layout1.addItem(self.espacio(50, 50))

        layout2.addWidget(label_nombre, 0, 0)
        layout2.addWidget(self.ingreso_nombre, 0, 1)
        layout2.addWidget(label_direccion, 1, 0)
        layout2.addWidget(self.ingreso_direccion, 1, 1)
        layout2.addWidget(label_email, 2, 0)
        layout2.addWidget(self.ingreso_email, 2, 1)
        layout2.addWidget(label_telefono, 3, 0)
        layout2.addWidget(self.ingreso_telefono, 3, 1)
        layout2.addWidget(boton_confirmar, 4, 0)
        layout2.addWidget(boton_cancelar, 4, 1)


        self.layout_extra.addLayout(layout1)
        self.layout_extra.addLayout(layout2)

        self.layout4.addLayout(self.layout_extra)

    def agregar_proveedor_bd(self):
        nombre = self.ingreso_nombre.text()
        direccion = self.ingreso_direccion.text()
        email = self.ingreso_email.text()
        telefono = self.ingreso_telefono.text()

        if not nombre or not direccion or not email or not telefono:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos.")
            return

        try:
            self.base_datos.agregar_proveedor(nombre, direccion, email, telefono)
            self.limpieza_layout(self.layout_extra)
            self.proveedores()
        except Exception as e:
            self.mensaje_error("Error al agregar el proveedor", str(e))

    def editar_proveedor_bd(self):
        nombre = self.ingreso_nombre.text()
        direccion = self.ingreso_direccion.text()
        email = self.ingreso_email.text()
        telefono = self.ingreso_telefono.text()

        if not nombre or not direccion or not email or not telefono:
            self.mensaje_error("Error", "Por favor complete todos los campos.")
            return

        try:
            id_proveedor = int(self.tabla_proveedores.item(self.tabla_proveedores.currentRow(), 0).text())
            self.base_datos.editar_proveedor(id_proveedor, nombre, direccion, email, telefono)
            self.limpieza_layout(self.layout_extra)
            self.proveedores()
        except Exception as e:
            self.mensaje_error("Error al editar el proveedor", str(e))
    


    def cancelar_edicion(self):
        self.limpieza_layout(self.layout_extra)
        self.proveedores()

    def cancelar_agregado(self):
        self.limpieza_layout(self.layout_extra)
        self.proveedores()

    def llenar_campos(self):
        # Obtener la fila seleccionada
        fila = self.tabla_proveedores.currentRow()

        # Obtener los valores de la fila seleccionada
        nombre_proveedor = self.tabla_proveedores.item(fila, 1).text()
        direccion_proveedor = self.tabla_proveedores.item(fila, 2).text()
        email_proveedor = self.tabla_proveedores.item(fila, 3).text()
        telefono_proveedor = self.tabla_proveedores.item(fila, 4).text()

        # Llenar los campos de texto con los valores obtenidos
        self.ingreso_nombre.setText(nombre_proveedor)
        self.ingreso_direccion.setText(direccion_proveedor)
        self.ingreso_email.setText(email_proveedor)
        self.ingreso_telefono.setText(telefono_proveedor)

    def ingreso_pedido(self):
        self.total_compra = 0
        self.color_boton_oprimido(self.boton_pedido)
        self.color_boton_sin_oprimir(self.boton_proveedores)
        self.color_boton_sin_oprimir(self.boton_ordenes)
        self.limpieza_layout(self.layout3)

        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()

        layout_tabla1 = QVBoxLayout()

        layout_tabla2 = QVBoxLayout()

        #Tabla de compras  id, nombre, stock, precio, descripcion
        # compras = [["1", "Calculadora", 10, 150]]
        
        inventario = self.base_datos.obtener_productos_ventas()
        self.tabla_inventario = QTableWidget(len(inventario), 5)


        #Tabla de compras
        self.tabla_inventario.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.tabla_inventario.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción", "Existencia Actual", "Costo" ]) 
        #"ID", "Nombre", "Descripción", "Existencia Actual", "Costo" - inventario
        # "ID", "Nombre", "Cantidad", "Costo" - ingreso

        # Llenar la tabla con los datos
        for fila, orden in enumerate(inventario):
            # Convertir los valores a strings (excepto los que ya lo son)
            id_item = QTableWidgetItem(str(orden['id']))
            nombre_item = QTableWidgetItem(orden['nombre'])
            descripcion_item = QTableWidgetItem(orden['descripcion'])
            stock_item = QTableWidgetItem(str(orden['stock']))
            precio_item = QTableWidgetItem(f"Q{(orden['precio'] - orden['precio']*0.15):.2f}")  # Formato con 2 decimales
            
            # Añadir items a la tabla
            self.tabla_inventario.setItem(fila, 0, id_item)
            self.tabla_inventario.setItem(fila, 1, nombre_item)
            self.tabla_inventario.setItem(fila, 2, descripcion_item)
            self.tabla_inventario.setItem(fila, 3, stock_item)
            self.tabla_inventario.setItem(fila, 4, precio_item)
            
            # Configurar flags para todos los items
            for col in range(5):
                item = self.tabla_inventario.item(fila, col)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

        self.tabla_inventario.resizeColumnsToContents()
        self.color_tabla(self.tabla_inventario)
        self.tabla_inventario.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_inventario.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tabla_inventario.cellDoubleClicked.connect(self.agregar_cantidad)

        self.boton_buscar = QPushButton()
        self.boton_buscar.setIcon(QIcon(self.imagen("imagenes/buscar.png", 45, 45)))
        self.boton_buscar.setIconSize(QSize(55, 55))
        self.color_boton_sin_oprimir(self.boton_buscar)
        self.boton_buscar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_buscar.clicked.connect(self.buscar_producto)
        self.asignacion_tecla(self.ventana_principal, "Return", self.boton_buscar)

        self.ingreso_busqueda = QLineEdit()
        self.ingreso_busqueda.setPlaceholderText("Ingrese el nombre del producto...")
        self.color_linea(self.ingreso_busqueda)
        self.ingreso_busqueda.setFixedHeight(60)
        self.ingreso_busqueda.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        #Tabla de Ingreso de nuevo orden
        # ingreso = [["1", "Calculadora", 10, 150]]

        self.tabla_ingreso = QTableWidget(0, 4)

        self.tabla_ingreso.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.tabla_ingreso.setHorizontalHeaderLabels(["ID", "Nombre", "Cantidad", "Costo"]) 


        self.tabla_ingreso.resizeColumnsToContents()
        self.color_tabla(self.tabla_ingreso)
        self.tabla_ingreso.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_ingreso.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tabla_ingreso.cellDoubleClicked.connect(self.restar_cantidad)

        ingreso_label = QLineEdit()
        ingreso_label.setPlaceholderText("Detalles del ingreso")
        self.color_linea(ingreso_label)
        ingreso_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ingreso_label.setFixedHeight(60)
        ingreso_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        ingreso_label.setEnabled(False)

        self.total = QLineEdit()
        self.total.setPlaceholderText(f"Total del ingreso: Q{self.total_compra:.2f}")
        self.color_linea(self.total)
        self.total.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total.setFixedHeight(50)
        self.total.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.total.setEnabled(False)

        boton_confirmar = QPushButton("Confirmar")
        boton_confirmar.setFixedHeight(50)
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        boton_confirmar.clicked.connect(self.generar_orden_compra) # Generará una orden de compra


        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.setFixedHeight(50)
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        boton_cancelar.clicked.connect(self.cancelar_orden_ingreso) # Cancelará la orden de compra

        layout1.addWidget(self.ingreso_busqueda)
        layout1.addWidget(self.boton_buscar)

        layout_tabla1.addLayout(layout1)
        layout_tabla1.addWidget(self.tabla_inventario)

        layout2.addWidget(boton_confirmar)
        layout2.addWidget(boton_cancelar)

        layout_tabla2.addWidget(ingreso_label)
        layout_tabla2.addWidget(self.tabla_ingreso)
        layout_tabla2.addWidget(self.total)
        layout_tabla2.addLayout(layout2)
        self.boton_eliminar_item = QPushButton("Eliminar orden seleccionada")
        self.color_boton_sin_oprimir(self.boton_eliminar_item)
        self.boton_eliminar_item.setFixedHeight(50)
        self.boton_eliminar_item.clicked.connect(self.eliminar_orden_ingreso)
        layout_tabla2.addWidget(self.boton_eliminar_item)


        self.layout3.addLayout(layout_tabla1)
        self.layout3.addLayout(layout_tabla2)

    def buscar_producto(self):
        # Buscar el producto por nombre en la base de datos
        nombre_producto = self.ingreso_busqueda.text()
        resultado = self.base_datos.buscar_producto_por_nombre(nombre_producto)
        
        if len(resultado) != 0:
            # Limpiar la tabla antes de mostrar los resultados
            self.tabla_inventario.clearContents()
            self.tabla_inventario.setRowCount(len(resultado))
            # Llenar la tabla con los resultados de la búsqueda
            for fila, producto in enumerate(resultado):
                id_item = QTableWidgetItem(str(producto['id']))
                nombre_item = QTableWidgetItem(producto['nombre'])
                descripcion_item = QTableWidgetItem(producto['descripcion'])
                existencia_item = QTableWidgetItem(str(producto['stock']))
                costo_item = QTableWidgetItem(f"Q{producto['costo']:.2f}")

                # Añadir items a la tabla
                self.tabla_inventario.setItem(fila, 0, id_item)
                self.tabla_inventario.setItem(fila, 1, nombre_item)
                self.tabla_inventario.setItem(fila, 2, descripcion_item)
                self.tabla_inventario.setItem(fila, 3, existencia_item)
                self.tabla_inventario.setItem(fila, 4, costo_item)

        else:
            self.mensaje_error("Error", "No se encontraron productos con ese nombre")

        self.ingreso_busqueda.clear()



    def eliminar_orden_ingreso(self):
        fila = self.tabla_ingreso.currentRow()
        if fila == -1:
            self.mensaje_error("Error", "Seleccione un orden para eliminar.")
            return
        # Encabezados de tabla_ingreso: ["ID", "IdProducto", "Producto", "Precio Unitario", "Cantidad", "Cantidad Recibida"]
        subtotal = float(self.tabla_ingreso.item(fila, 3).text()[1:]) * int(self.tabla_ingreso.item(fila, 2).text())
        self.total_compra -= subtotal
        self.total.setPlaceholderText(f"Total del ingreso: Q{self.total_compra:.2f}")

        id_a_eliminar = int(self.tabla_ingreso.item(fila, 0).text())
        self.carrito_ingreso = [item for item in self.carrito_ingreso if item[0] != id_a_eliminar]

        self.tabla_ingreso.removeRow(fila)
        self.fila_ingreso -= 1


    def cancelar_orden_ingreso(self):
        self.tabla_ingreso.clearContents()
        self.tabla_ingreso.setRowCount(0)
        self.tabla_ingreso.setColumnCount(4)
        self.total.clear()
        self.total.setPlaceholderText("Total del ingreso: Q0")
        self.carrito_ingreso.clear()
        self.total_compra = 0
        self.fila_ingreso = 0
        self.limpieza_layout(self.layout3)
        self.ingreso_pedido()


    # Función para generar una orden de compra y enviarla a la base de datos
    def generar_orden_compra(self):
        if not self.carrito_ingreso:
            self.mensaje_error("Error", "No hay órdenes en el carrito.")
            return

        # Crear ventana de selección de proveedor
        dialogo = QDialog()
        dialogo.setWindowTitle("Seleccionar proveedor")
        layout = QVBoxLayout()
        # Hacer más grande el cuadro de diálogo
        dialogo.setMinimumSize(300, 150)
        dialogo.setMaximumSize(300, 150)
        # Colocar los colores de la ventana 
        self.fondo_degradado(dialogo,  "#5DA9F5", "#5DA9F5")
        dialogo.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        label = QLabel("Seleccione un proveedor:")
        self.color_linea(label)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFixedHeight(30)
        label.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(label)

        combo_proveedores = QComboBox()
        self.color_caja_opciones(combo_proveedores)
        proveedores = self.base_datos.obtener_proveedores()  # Debe retornar lista de tuplas: (id, nombre)
        
        if not proveedores:
            self.mensaje_error("Error", "No hay proveedores registrados.")
            return

        proveedor_id_por_nombre = {}  # Para mapear el nombre al ID

        for proveedor in proveedores:
            nombre = proveedor["nombre"]
            id_prov = proveedor["id"]
            combo_proveedores.addItem(nombre)
            proveedor_id_por_nombre[nombre] = id_prov
            layout.addWidget(combo_proveedores)

        # Botones Aceptar y Cancelar
        botones = QHBoxLayout()

        btn_aceptar = QPushButton("Aceptar")
        self.color_boton_sin_oprimir(btn_aceptar)
        btn_aceptar.setFixedHeight(30)
        btn_aceptar.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        btn_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(btn_cancelar)
        btn_cancelar.setFixedHeight(30)
        btn_cancelar.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        
        botones.addWidget(btn_aceptar)
        botones.addWidget(btn_cancelar)

        layout.addLayout(botones)

        dialogo.setLayout(layout)

        # Acción de botones
        def aceptar():
            dialogo.accept()

        def cancelar():
            dialogo.reject()

        btn_aceptar.clicked.connect(aceptar)
        btn_cancelar.clicked.connect(cancelar)

        if dialogo.exec() != QDialog.DialogCode.Accepted:
            return  # Usuario canceló

        # Obtener ID del proveedor
        nombre_seleccionado = combo_proveedores.currentText()
        id_proveedor = proveedor_id_por_nombre[nombre_seleccionado]

        # Generar la orden de compra
        try:
            id_compra = self.base_datos.agregar_compra(id_proveedor, datetime.now(), self.id_usuario, self.total_compra)
            for orden in self.carrito_ingreso:
                id_orden = orden[0]
                cantidad = orden[1]
                precio_unitario = orden[2]
                self.base_datos.agregar_detalle_compra(id_orden, id_compra, cantidad, precio_unitario, cantidad)

            self.tabla_ingreso.clearContents()
            self.tabla_ingreso.setRowCount(0)
            self.tabla_ingreso.setColumnCount(4)
            self.total.clear()
            self.total.setPlaceholderText("Total del ingreso: Q0")
            self.carrito_ingreso.clear()
            self.total_compra = 0
            self.fila_ingreso = 0

        except Exception as e:
            self.mensaje_error("Error", f"No se pudo generar la orden de compra: {str(e)}")
            return
        
    def cancelar_orden_compra(self):
        # Limpiar la tabla de ingreso
        self.tabla_ingreso.clearContents()
        self.tabla_ingreso.setRowCount(0)
        self.tabla_ingreso.setColumnCount(4)
        self.total.clear()
        self.total.setPlaceholderText("Total del ingreso: Q0")
        self.carrito_ingreso.clear()
        self.total_compra = 0
        self.fila_ingreso = 0
        self.limpieza_layout(self.layout3)
        self.ingreso_pedido()

    def agregar_cantidad(self):
        if self.nueva_ventana is not None:
            self.nueva_ventana.close()
            self.nueva_ventana = None

        # Esta función se llamará cuando se haga doble clic en una celda de la tabla de inventario
        self.nueva_ventana = QWidget()
        self.fondo_degradado(self.nueva_ventana, "#5DA9F5", "#0037FF")
        self.nueva_ventana.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        main_layout = QGridLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout1 = QHBoxLayout()
        # Agregar etiqueta de "Ingrese la cantidad"
        label_cantidad = QLabel("Ingrese la cantidad:")
        label_cantidad.setStyleSheet("color: Black")
        label_cantidad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.color_linea(label_cantidad)   
        label_cantidad.setFixedHeight(30)
            
        self.cantidad = QLineEdit()
        self.cantidad.setPlaceholderText("Ingrese la cantidad")
        self.color_linea(self.cantidad)
        self.cantidad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cantidad.setFixedHeight(30)
        self.cantidad.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        boton_confirmar = QPushButton("Confirmar")
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setFixedSize(100, 20)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_confirmar.clicked.connect(self.confirmar_cantidad_ingreso)
        self.asignacion_tecla(self.nueva_ventana, "Return", boton_confirmar)

        boton_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setFixedSize(100, 20)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.asignacion_tecla(self.nueva_ventana, "Esc", boton_cancelar)
        boton_cancelar.clicked.connect(self.cancelar_cantidad_ingreso)

        layout1.addWidget(boton_confirmar)
        layout1.addWidget(boton_cancelar)

        # Agregar la etiqueta y el campo de texto al layout principal
        main_layout.addWidget(label_cantidad, 0, 0)   
        main_layout.addWidget(self.cantidad, 1, 0)
        main_layout.addLayout(layout1, 2, 0)

        self.nueva_ventana.setLayout(main_layout)
        self.nueva_ventana.showNormal()


    def cancelar_cantidad(self):
        self.nueva_ventana.close()
        self.nueva_ventana = None

    def restar_cantidad(self):
        if self.nueva_ventana is not None:  
            self.nueva_ventana.close()
            self.nueva_ventana = None


        self.nueva_ventana = QWidget()
        self.fondo_degradado(self.nueva_ventana, "#5DA9F5", "#0037FF")
        self.nueva_ventana.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        main_layout = QGridLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout1 = QHBoxLayout()

        cantidad_label = QLabel("Ingrese la nueva cantidad")
        cantidad_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.color_linea(cantidad_label)   
        cantidad_label.setFixedHeight(30)
        cantidad_label.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        self.nueva_cantidad = QLineEdit()
        self.nueva_cantidad.setPlaceholderText("Ingrese la cantidad ...")
        self.color_linea(self.nueva_cantidad)
        self.nueva_cantidad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nueva_cantidad.setFixedHeight(30)
        self.nueva_cantidad.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        boton_confirmar = QPushButton("Confirmar")
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setFixedSize(100, 20)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.asignacion_tecla(self.nueva_ventana, "Return", boton_confirmar)
        boton_confirmar.clicked.connect(self.confirmar_modificar_cantidad)

        boton_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setFixedSize(100, 20)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.asignacion_tecla(self.nueva_ventana, "Esc", boton_cancelar)
        boton_cancelar.clicked.connect(self.cancelar_cantidad)

        layout1.addWidget(boton_confirmar)
        layout1.addWidget(boton_cancelar)

        main_layout.addWidget(cantidad_label, 0, 0)
        main_layout.addWidget(self.nueva_cantidad, 1, 0)
        main_layout.addLayout(layout1, 2, 0)

        self.nueva_ventana.setLayout(main_layout)
        self.nueva_ventana.showNormal()


    def confirmar_modificar_cantidad(self):
        # self.carrito_ingreso.append([id_producto, cantidad, precio_producto])
        # tabla_ingreso  "ID", "Nombre", "Cantidad", "Costo"

        fila = self.tabla_ingreso.currentRow()
        cantidad_anterior = self.tabla_ingreso.item(fila, 2).text()
        precio = self.tabla_ingreso.item(fila, 3).text()[1:]
        nueva_cantidad = self.nueva_cantidad.text()
        # Verificar que la nueva cantidad sea un número positivo
        # Recorrer el carrito para modificar la cantidad en el producto con el id correspondiente
        if int(nueva_cantidad) > 0:
        #"ID", "Nombre", "Descripción", "Existencia Actual", "Costo" - inventario
        # "ID", "Nombre", "Cantidad", "Costo" - ingreso

            for i in range(len(self.carrito_ingreso)):
                if self.carrito_ingreso[i][0] == int(self.tabla_ingreso.item(fila, 0).text()):
                    # Si el producto ya existe, actualizar la cantidad 
                    self.carrito_ingreso[i][1] = nueva_cantidad # Carrio guarada id, cantidad, precio_producto
                    break
        self.tabla_ingreso.setItem(fila, 2, QTableWidgetItem(str(nueva_cantidad)))
        # Actualizar el total de la venta
        antiguo_total_producto = int(cantidad_anterior) * float(precio)
        nuevo_total_producto = int(nueva_cantidad) * float(precio)
        self.total_compra = self.total_compra - antiguo_total_producto + nuevo_total_producto
        self.total.setText(f"Total de compra: Q{self.total_compra:.2f}")
        # Cerrar la ventana de cantidad
        self.nueva_ventana.close()
        self.nueva_ventana = None

    def confirmar_cantidad_ingreso(self):
        try:
            # Obtener fila seleccionada y cantidad
            fila = self.tabla_inventario.currentRow()
            cantidad_texto = self.cantidad.text()
            
            # Validar cantidad
            if not cantidad_texto.isdigit() or int(cantidad_texto) <= 0:
                self.mensaje_error("Error", "Ingrese una cantidad válida (número mayor que 0).")
                return

            cantidad = int(cantidad_texto)

            # Obtener datos del producto
            id_producto = int(self.tabla_inventario.item(fila, 0).text())
            nombre_producto = self.tabla_inventario.item(fila, 1).text()
            precio_texto = self.tabla_inventario.item(fila, 4).text()[1:]  # Eliminar 'Q'
            precio_producto = float(precio_texto)
            total_producto = cantidad * precio_producto

            # Verificar si el producto ya está en el carrito
            for i in range(self.tabla_ingreso.rowCount()):
                if int(self.tabla_ingreso.item(i, 0).text()) == id_producto:
                    # Actualizar cantidad existente
                    cantidad_actual = int(self.tabla_ingreso.item(i, 2).text())
                    self.tabla_ingreso.item(i, 2).setText(str(cantidad_actual + cantidad))
                    self.total_compra += total_producto
                    self.total.setPlaceholderText(f"Total del ingreso: Q{self.total_compra:.2f}")
                    self.nueva_ventana.close()
                    return

            # Si no existe, agregar nueva fila
            fila_nueva = self.tabla_ingreso.rowCount()
            self.tabla_ingreso.insertRow(fila_nueva)

            # Crear items para cada columna
            items = [
                QTableWidgetItem(str(id_producto)),
                QTableWidgetItem(nombre_producto),
                QTableWidgetItem(str(cantidad)),
                QTableWidgetItem(f"Q{precio_producto:.2f}")
            ]

            # Configurar items y añadirlos a la tabla
            for col, item in enumerate(items):
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                self.tabla_ingreso.setItem(fila_nueva, col, item)

            # Actualizar variables de estado
            self.carrito_ingreso.append([id_producto, cantidad, precio_producto]) # Carrio guarada id, cantidad, precio_producto
            self.total_compra += total_producto
            self.total.setPlaceholderText(f"Total del ingreso: Q{self.total_compra:.2f}")
            self.nueva_ventana.close()
            self.nueva_ventana = None

        except Exception as e:
            self.mensaje_error("Error", f"Ocurrió un error al agregar el producto: {str(e)}")

    def cancelar_cantidad_ingreso(self):
        self.nueva_ventana.close()
        self.nueva_ventana = None


    # Esta tabla servirá para ver las ordenes de compra, y los detalles de cada una. Servirá para confirmar el ingreso
    def ordenes_compra(self): 
        self.limpieza_layout(self.layout3)
        self.color_boton_oprimido(self.boton_ordenes)
        self.color_boton_sin_oprimir(self.boton_pedido)
        self.color_boton_sin_oprimir(self.boton_proveedores)
        self.total_compra = 0

        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()

        layout_tabla1 = QVBoxLayout()
        layout_tabla2 = QVBoxLayout()

        # Tabla de compras  id, nombre, stock, precio, descripcion
        # compras = [["1", "Calculadora", 10, 150]]
        
        compras = self.base_datos.obtener_compras_pendientes() # Retorna IdCompra, Proveedor, Fecha, Total
        self.tabla_compras = QTableWidget(len(compras), 4)

        self.carrito_ingreso = []

        #Tabla de compras
        self.tabla_compras.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.tabla_compras.setHorizontalHeaderLabels(["IdCompra", "Proveedor", "Fecha", "Total"]) 

        

        # Llenar la tabla con los datos
        for fila, orden in enumerate(compras):
            # Convertir los valores a strings (excepto los que ya lo son)
            id_item = QTableWidgetItem(str(orden['IdCompra']))
            nombre_item = QTableWidgetItem(orden['Proveedor'])
            fecha_item = QTableWidgetItem(str(orden['Fecha']))
            # Convertir el total a string con formato de moneda
            total_item = QTableWidgetItem(f"Q{orden['Total']:.2f}")  # Formato con 2 decimales
            
            # Añadir items a la tabla
            self.tabla_compras.setItem(fila, 0, id_item)
            self.tabla_compras.setItem(fila, 1, nombre_item)
            self.tabla_compras.setItem(fila, 2, fecha_item)
            self.tabla_compras.setItem(fila, 3, total_item)
            
            # Configurar flags para todos los items
            for col in range(4):
                item = self.tabla_compras.item(fila, col)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

        self.tabla_compras.resizeColumnsToContents()
        self.color_tabla(self.tabla_compras)
        self.tabla_compras.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_compras.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tabla_compras.cellDoubleClicked.connect(self.ver_detalles_de_orden)

        self.boton_buscar = QPushButton()
        self.boton_buscar.setIcon(QIcon(self.imagen("imagenes/buscar.png", 45, 45)))
        self.boton_buscar.setIconSize(QSize(55, 55))
        self.color_boton_sin_oprimir(self.boton_buscar)
        self.boton_buscar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        

        self.ingreso_busqueda = QLineEdit()
        self.ingreso_busqueda.setPlaceholderText("Ingrese el ID del orden")
        self.color_linea(self.ingreso_busqueda)
        self.ingreso_busqueda.setFixedHeight(60)
        self.ingreso_busqueda.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        #Tabla de Ingreso de nuevo orden
        # ingreso = [["1", "Calculadora", 10, 150]]

        self.tabla_ingreso = QTableWidget(0, 5)

        self.tabla_ingreso.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # Se debe devolver IdProducto, NombreProducto, PrecioUnitario, Cantidad

        self.tabla_ingreso.setHorizontalHeaderLabels(["ID","IdProducto", "Producto", "Precio Unitario", "Cantidad", "Cantidad Recibida"]) 


        self.tabla_ingreso.resizeColumnsToContents()
        self.color_tabla(self.tabla_ingreso)
        self.tabla_ingreso.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_ingreso.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        ingreso_label = QLineEdit()
        ingreso_label.setPlaceholderText("Detalles de orden")
        self.color_linea(ingreso_label)
        ingreso_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ingreso_label.setFixedHeight(60)
        ingreso_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        ingreso_label.setEnabled(False)

        self.total = QLineEdit()
        self.total.setPlaceholderText(f"Total del ingreso: Q{self.total_compra:.2f}")
        self.color_linea(self.total)
        self.total.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total.setFixedHeight(50)
        self.total.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.total.setEnabled(False)

        boton_confirmar = QPushButton("Confirmar")
        boton_confirmar.setFixedHeight(50)
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        boton_confirmar.clicked.connect(self.confirmar_ingreso) # Validará la orden de compra


        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.setFixedHeight(50)
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        boton_cancelar.clicked.connect(self.cancelar_orden_compra)

        # layout1.addWidget(self.ingreso_busqueda)
        # layout1.addWidget(self.boton_buscar)

        layout_tabla1.addLayout(layout1)
        layout_tabla1.addWidget(self.tabla_compras)

        layout2.addWidget(boton_confirmar)
        layout2.addWidget(boton_cancelar)

        layout_tabla2.addWidget(ingreso_label)
        layout_tabla2.addWidget(self.tabla_ingreso)
        layout_tabla2.addWidget(self.total)
        layout_tabla2.addLayout(layout2)
        self.boton_eliminar_item = QPushButton("Eliminar orden seleccionado")
        self.color_boton_sin_oprimir(self.boton_eliminar_item)
        self.boton_eliminar_item.setFixedHeight(50)
        self.boton_eliminar_item.clicked.connect(self.eliminar_orden_ingreso)
        # layout_tabla2.addWidget(self.boton_eliminar_item)


        self.layout3.addLayout(layout_tabla1)
        self.layout3.addLayout(layout_tabla2)

    def ver_detalles_de_orden(self):
        self.fila_ingreso = 0
        self.total_compra = 0
        fila = self.tabla_compras.currentRow()
        id_orden = int(self.tabla_compras.item(fila, 0).text())
        detalles = self.base_datos.obtener_detalle_compra(id_orden)
        
        # Configurar tabla
        self.tabla_ingreso.clear()
        self.tabla_ingreso.setRowCount(0)
        self.tabla_ingreso.setColumnCount(6)
        self.tabla_ingreso.setHorizontalHeaderLabels([
            "ID", "IdProducto", "Producto", 
            "Precio Unitario", "Cantidad", "Cantidad Recibida"
        ])
        self.tabla_ingreso.resizeColumnsToContents()
        self.color_tabla(self.tabla_ingreso)
        self.tabla_ingreso.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_ingreso.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        
        # Habilitar edición para la tabla
        self.tabla_ingreso.setEditTriggers(
            QTableWidget.EditTrigger.DoubleClicked | 
            QTableWidget.EditTrigger.EditKeyPressed
        )
        
        for detalle in detalles:
            row = self.tabla_ingreso.rowCount()
            self.tabla_ingreso.insertRow(row)
            
            # Crear items para columnas no editables
            for col, value in enumerate([
                str(detalle['ID']),
                str(detalle['IdProducto']),
                detalle['NombreProducto'],
                f"Q{detalle['PrecioUnitario']:.2f}",
                str(detalle['Cantidad'])
            ]):
                item = QTableWidgetItem(value)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                self.tabla_ingreso.setItem(row, col, item)
            
            # Item editable para Cantidad Recibida (columna 5)
            item_recibida = QTableWidgetItem(str(detalle['CantidadRecibida']))
            item_recibida.setFlags(
                Qt.ItemFlag.ItemIsEnabled | 
                Qt.ItemFlag.ItemIsSelectable | 
                Qt.ItemFlag.ItemIsEditable
            )
            self.tabla_ingreso.setItem(row, 5, item_recibida)
            
            self.total_compra += detalle['PrecioUnitario'] * detalle['Cantidad']
            self.fila_ingreso += 1
        
        self.total.setPlaceholderText(f"Total del ingreso: Q{self.total_compra:.2f}")
        

    def confirmar_ingreso(self):  
        try:
            # Recorrer la tabla_ingreso para obtener detalles del carrito
            # y actualizar el stock de cada orden
            fila = self.tabla_compras.currentRow()
            id_orden = int(self.tabla_compras.item(fila, 0).text())

            for i in range(self.tabla_ingreso.rowCount()):
                # Verificar que la cantidad sea igual a la cantidad recibida
                id_detalle = int(self.tabla_ingreso.item(i, 0).text())
                id_producto = int(self.tabla_ingreso.item(i, 1).text())
                precio_unitario = float(self.tabla_ingreso.item(i, 3).text()[1:])
                cantidad = int(self.tabla_ingreso.item(i, 4).text())
                cantidad_recibida = int(self.tabla_ingreso.item(i, 5).text())

                if cantidad_recibida != cantidad:
                    # Modificar el detalle de la orden en bd
                    cantidad = cantidad_recibida
                    self.base_datos.modificar_detalle_compra(id_detalle, cantidad)


                # Agregar al carrito de ingreso
                self.carrito_ingreso.append([id_producto, cantidad, precio_unitario, id_detalle])

            for producto in self.carrito_ingreso:
                id_producto = producto[0]
                cantidad = producto[1]
                # Actualizar el stock del producto

                self.base_datos.aumentar_stock_producto(id_producto, cantidad)
            # Cambiar el estado de la orden a 1 (confirmada)
            self.base_datos.confirmar_orden_compra(id_orden)

            # Recargar la tabla de compras
            self.ordenes_compra()
            # Limpiar la tabla de ingreso
            self.tabla_ingreso.clearContents()
            self.tabla_ingreso.setRowCount(0)
            self.tabla_ingreso.setColumnCount(4)
            self.total.clear()
            self.total.setPlaceholderText("Total del ingreso: Q0")
            self.carrito_ingreso.clear()
            self.total_compra = 0
            self.fila_ingreso = 0

        except Exception as e:
            self.mensaje_error("Error", f"No se pudo registrar el ingreso: {str(e)}")



    def cancelar_ingreso(self):
        self.tabla_ingreso.clearContents()
        self.tabla_ingreso.setRowCount(0)
        self.tabla_ingreso.setColumnCount(4)
        self.total.clear()
        self.total.setPlaceholderText("Total del ingreso: Q0")
        self.carrito_ingreso.clear()
        self.total_compra = 0
        self.fila_ingreso = 0

