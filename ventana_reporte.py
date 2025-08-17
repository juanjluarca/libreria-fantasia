from codigo import Codigo
from PyQt6.QtWidgets import QFileDialog, QDateEdit, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QMessageBox, QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox 
from PyQt6.QtGui import QIcon, QPixmap, QGuiApplication, QLinearGradient, QColor, QBrush, QPalette
from PyQt6.QtCore import Qt, QSize, QDate
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime

class Ventana_reporte(Codigo):
    def __init__(self, main_layout, base_datos, botones, nivel, ventana_principal):
        super().__init__()
        self.layout = main_layout
        self.base_datos = base_datos
        self.botones = botones
        self.nivel = nivel
        self.nueva_ventana = None
        self.verificacion = None
        self.ventana_principal = ventana_principal
    
    def reportes(self):
        self.limpieza_layout(self.layout)
        self.color_acceso_nivel(self.nivel, self.botones)
        self.color_boton_oprimido(self.botones[4])
        self.activar_botones(self.botones)
        self.botones[4].setEnabled(False)

        main_layot = QVBoxLayout()
        main_layot.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()
        layout3 = QVBoxLayout()

        self.boton_reporte_ventas = QPushButton()
        self.boton_reporte_ventas.setIcon(QIcon(self.imagen("imagenes/reporte ventas.png", 90, 90)))
        self.boton_reporte_ventas.setIconSize(QSize(100, 100))
        self.color_boton_sin_oprimir(self.boton_reporte_ventas)
        self.boton_reporte_ventas.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_reporte_ventas.clicked.connect(self.reporte_ventas)

        self.boton_reporte_compras = QPushButton()
        self.boton_reporte_compras.setIcon(QIcon(self.imagen("imagenes/reporte compras.png", 90, 90)))
        self.boton_reporte_compras.setIconSize(QSize(100, 100))
        self.color_boton_sin_oprimir(self.boton_reporte_compras)
        self.boton_reporte_compras.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_reporte_compras.clicked.connect(self.reporte_compras)

        self.boton_generar_reporte = QPushButton()
        self.boton_generar_reporte.setIcon(QIcon(self.imagen("imagenes/generar reporte.png", 90, 90)))
        self.boton_generar_reporte.setIconSize(QSize(100, 100))
        self.color_boton_sin_oprimir(self.boton_generar_reporte)
        self.boton_generar_reporte.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_generar_reporte.clicked.connect(self.generar_reporte)

        informar = QLabel("Oprima uno de los botones que tiene en la parte superior izquierda")
        informar.setStyleSheet("color: Black; font-size: 20px")
        informar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        layout1.addItem(self.espacio(35, 35))
        layout1.addWidget(self.boton_reporte_ventas)
        layout1.addWidget(self.boton_reporte_compras)
        layout1.addWidget(self.boton_generar_reporte)
        layout1.addStretch()

        layout3.addStretch()
        layout3.addWidget(informar)
        layout3.addStretch()
        
        self.layout2.addLayout(layout3)

        main_layot.addLayout(layout1)
        main_layot.addLayout(self.layout2)
        self.layout.addLayout(main_layot)

    def reporte_ventas(self):
        if self.nueva_ventana is not None:
            self.nueva_ventana.close()
            self.nueva_ventana = None

        self.limpieza_layout(self.layout2)
        self.color_boton_oprimido(self.boton_reporte_ventas)
        self.color_boton_sin_oprimir(self.boton_reporte_compras)
        self.color_boton_sin_oprimir(self.boton_generar_reporte)

        main_layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.orden_tabla = QComboBox()
        self.orden_tabla.addItems(["Día", "Mes", "Año", "Todas"])

        # Conectar la señal a las funciones
        self.orden_tabla.currentTextChanged.connect(self.actualizar_vista)

        # Establecer "Dia" como selección por defecto (opcional)
        self.orden_tabla.setCurrentIndex(0)  # Esto activará automáticamente la función para "Dia"

        self.color_caja_opciones(self.orden_tabla)
        self.orden_tabla.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Obtener el formato seleccionado en orden_tabla

        orden_label = QLabel("Ingrese la forma en la que desea ordenar las ventas: ")
        orden_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        orden_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_linea(orden_label)
        # registro_ventas = [["2023-10-01", 1000, 5, 500, "Calculadora"], ["2023-10-02", 2000, 10, 1000, "Tijera"]]
        # Fecha, ingresos, productos vendidos, ganancias
        reporte = self.base_datos.obtener_reporte_ventas_por_dia()

        self.tabla = QTableWidget(len(reporte), 4)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.tabla.setHorizontalHeaderLabels(["Fecha", "Ingresos totales", "Total de Productos vendidos", "Ganancias totales"])

        self.color_tabla(self.tabla)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout1.addWidget(orden_label)
        layout1.addWidget(self.orden_tabla)
        
        main_layout.addLayout(layout1)
        main_layout.addWidget(self.tabla)

        self.layout2.addItem(self.espacio(35, 35))
        self.layout2.addLayout(main_layout)
        self.actualizar_vista()

    
    def mostrar_detalles_venta(self, fila):
        if self.verificacion is not None:
            self.limpieza_layout(self.verificacion)
            
        layout1 = QVBoxLayout()
        self.verificacion = layout1

        cartelera = QLabel("Detalles de la venta")
        self.color_linea(cartelera)
        cartelera.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        cartelera.setFixedHeight(50)
        cartelera.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cartelera.setEnabled(False)

        boton_cerrar = QPushButton("cerrar")
        self.color_boton_sin_oprimir(boton_cerrar)
        boton_cerrar.setFixedHeight(50)
        boton_cerrar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        boton_cerrar.clicked.connect(self.limpieza_detalle_venta)

        id_venta = self.tabla.item(fila, 0).text()
        
        detalle_vendidos = self.base_datos.obtener_detalles_por_id_venta(id_venta) # Devolver IdOrden, Producto, CantidadVendida, Total 

        self.detalle_venta = QTableWidget(len(detalle_vendidos), 4)
        self.detalle_venta.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.detalle_venta.setHorizontalHeaderLabels(["IdOrden", "Producto", "Cantidad", "Precio"])

        for fila, producto in enumerate(detalle_vendidos):

            id_item = QTableWidgetItem(f"{producto['IdOrden']}")
            producto_item = QTableWidgetItem(producto['Producto'])
            cantidad_item = QTableWidgetItem(f"{producto['CantidadVendida']}")
            total_item = QTableWidgetItem(f"Q{producto['Total']:.2f}") 
            
            self.detalle_venta.setItem(fila, 0, id_item)
            self.detalle_venta.setItem(fila, 1, producto_item)
            self.detalle_venta.setItem(fila, 2, cantidad_item)
            self.detalle_venta.setItem(fila, 3, total_item)

            for col in range(4):
                item = self.detalle_venta.item(fila, col)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

        self.color_tabla(self.detalle_venta)
        self.detalle_venta.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.detalle_venta.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout1.addWidget(cartelera)
        layout1.addWidget(self.detalle_venta)
        layout1.addWidget(boton_cerrar)

        self.layout2.addLayout(layout1)

    def limpieza_detalle_venta(self):
        self.limpieza_layout(self.layout2)
        self.reporte_ventas()
        self.verificacion = None
        self.orden_tabla.setCurrentIndex(3)  

    def mostrar_detalles_venta_dia(self, fila):
        if self.verificacion is not None:
            self.limpieza_layout(self.verificacion)

        layout1 = QVBoxLayout()
        self.verificacion = layout1

        cartelera = QLabel("Detalles de la venta")
        self.color_linea(cartelera)
        cartelera.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        cartelera.setFixedHeight(50)
        cartelera.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cartelera.setEnabled(False)

        boton_cerrar = QPushButton("cerrar")
        self.color_boton_sin_oprimir(boton_cerrar)
        boton_cerrar.setFixedHeight(50)
        boton_cerrar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        boton_cerrar.clicked.connect(self.limpieza_detalle_venta)

        fecha = self.tabla.item(fila, 0).text()
        # Devolver IdVenta, Producto, Cantidad, Precio
        if self.orden_tabla.currentText() == "Día":
            detalle_vendidos = self.base_datos.obtener_ventas_dia(fecha) 
        elif self.orden_tabla.currentText() == "Mes":
            detalle_vendidos = self.base_datos.obtener_ventas_mes(fecha)
        else:
            detalle_vendidos = {}
            

        self.detalle_venta = QTableWidget(len(detalle_vendidos), 4)
        self.detalle_venta.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.detalle_venta.setHorizontalHeaderLabels(["IdProducto", "Producto", "Cantidad", "Precio"])

        for fila, producto in enumerate(detalle_vendidos):

            id_item = QTableWidgetItem(f"{producto['IdVenta']}")
            producto_item = QTableWidgetItem(producto['Producto'])
            cantidad_item = QTableWidgetItem(f"{producto['Cantidad']}")
            total_item = QTableWidgetItem(f"Q{producto['Precio']:.2f}") 
            
            self.detalle_venta.setItem(fila, 0, id_item)
            self.detalle_venta.setItem(fila, 1, producto_item)
            self.detalle_venta.setItem(fila, 2, cantidad_item)
            self.detalle_venta.setItem(fila, 3, total_item)

            for col in range(4):
                item = self.detalle_venta.item(fila, col)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

        self.color_tabla(self.detalle_venta)
        self.detalle_venta.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.detalle_venta.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout1.addWidget(cartelera)
        layout1.addWidget(self.detalle_venta)
        layout1.addWidget(boton_cerrar)

        self.layout2.addLayout(layout1)

    def actualizar_vista(self):
        texto = self.orden_tabla.currentText()  # Obtiene el texto seleccionado
        if self.verificacion is not None:
            self.limpieza_layout(self.verificacion)

        try:
            self.tabla.cellDoubleClicked.disconnect()
        except TypeError:
            # No había conexiones activas
            pass

        if texto == "Día":
            reporte = self.base_datos.obtener_reporte_ventas_por_dia()
            self.tabla.cellDoubleClicked.connect(self.mostrar_detalles_venta_dia)
        elif texto == "Mes":
            reporte = self.base_datos.obtener_reporte_ventas_por_mes()
            self.tabla.cellDoubleClicked.connect(self.mostrar_detalles_venta_dia)
        elif texto == "Año":
            reporte = self.base_datos.obtener_reporte_ventas_por_anio()
        elif texto == "Todas":
            reporte = self.base_datos.obtener_reporte_ventas()
            self.tabla.setHorizontalHeaderLabels(["IdVenta", "Empleado", "Fecha", "Total"])
            self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.tabla.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.tabla.cellDoubleClicked.connect(self.mostrar_detalles_venta)
            self.generar_tabla_todas_ventas(reporte)
            return

        # Limpiar la tabla antes de llenarla
        self.tabla.clearContents()
        self.generar_tabla(reporte)

    def generar_tabla(self, reporte):
        # Limpiar la tabla antes de llenarla
        self.tabla.clearContents()
        self.tabla.setRowCount(len(reporte))
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Fecha", "Ingresos", "Total de Productos vendidos", "Ganancias"])
        # Verificar si es orden de compra o venta
        for fila, registro in enumerate(reporte):

            fecha_item = QTableWidgetItem(f"{registro['Fecha']}")
            ingreso_item = QTableWidgetItem(f"Q{registro['IngresoTotal']:.2f}")
            productos_item = QTableWidgetItem(f"{registro['ProductosVendidos']}")
            ganancias_item = QTableWidgetItem(f"Q{registro['Ganancia']:.2f}") 

            self.tabla.setItem(fila, 0, fecha_item)
            self.tabla.setItem(fila, 1, ingreso_item)
            self.tabla.setItem(fila, 2, productos_item)
            self.tabla.setItem(fila, 3, ganancias_item)

            for col in range(4):
                item = self.tabla.item(fila, col)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

    def generar_tabla_todas_ventas(self, reporte): # Devolver IdVenta, Empleado, Fecha, Total
    # Limpiar la tabla antes de llenarla
        self.tabla.setHorizontalHeaderLabels(["IdVenta", "Empleado", "Fecha", "Total"])
        self.tabla.clearContents()
        self.color_tabla(self.tabla)
        self.tabla.setRowCount(len(reporte))
        self.tabla.setColumnCount(4)
        self.tabla.cellDoubleClicked.connect(self.mostrar_detalles_venta)


        # Verificar si es orden de compra o venta
        for fila, registro in enumerate(reporte):

            id_item = QTableWidgetItem(f"{registro['IdVenta']}")
            empleado_item = QTableWidgetItem(f"{registro['Empleado']}")
            fecha_item = QTableWidgetItem(f"{registro['Fecha']}")
            total_item = QTableWidgetItem(f"Q{registro['Total']:.2f}") 

            self.tabla.setItem(fila, 0, id_item)
            self.tabla.setItem(fila, 1, empleado_item)
            self.tabla.setItem(fila, 2, fecha_item)
            self.tabla.setItem(fila, 3, total_item)

            for col in range(4):
                item = self.tabla.item(fila, col)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

    def reporte_compras(self):
        if self.nueva_ventana is not None:
            self.nueva_ventana.close()
            self.nueva_ventana = None
    
        self.limpieza_layout(self.layout2)
        self.color_boton_oprimido(self.boton_reporte_compras)
        self.color_boton_sin_oprimir(self.boton_reporte_ventas)
        self.color_boton_sin_oprimir(self.boton_generar_reporte)

        main_layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.orden_tabla_compras = QComboBox()
        self.orden_tabla_compras.addItems(["Día", "Mes", "Año", "Todas"])

        # Conectar la señal a las funciones
        self.orden_tabla_compras.currentTextChanged.connect(self.actualizar_vista_compras)

        # Establecer "Dia" como selección por defecto (opcional)
        self.orden_tabla_compras.setCurrentIndex(0)  # Esto activará automáticamente la función para "Dia"



        self.color_caja_opciones(self.orden_tabla_compras)
        self.orden_tabla_compras.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        orden_label = QLabel("Ingrese la forma en la que desea ordenar las compras: ")
        orden_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        orden_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_linea(orden_label)

        registro_ventas = self.base_datos.obtener_reporte_compras_por_dia() # Devuelve "Fecha", "CantidadProductos", "Gastos"


        self.tabla = QTableWidget(len(registro_ventas), 3)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.tabla.setHorizontalHeaderLabels(["Fecha", "Cantidad de Productos", "Gastos"])


        self.color_tabla(self.tabla)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout1.addWidget(orden_label)
        layout1.addWidget(self.orden_tabla_compras)

        main_layout.addLayout(layout1)
        main_layout.addWidget(self.tabla)

        self.layout2.addItem(self.espacio(35, 35))
        self.layout2.addLayout(main_layout)
        self.actualizar_vista_compras()
    
    def actualizar_vista_compras(self):
        texto = self.orden_tabla_compras.currentText()  # Obtiene el texto seleccionado
        if self.verificacion is not None:
            self.limpieza_layout(self.verificacion)


        if texto == "Día":
            reporte = self.base_datos.obtener_reporte_compras_por_dia()
        elif texto == "Mes":
            reporte = self.base_datos.obtener_reporte_compras_por_mes()
        elif texto == "Año":
            reporte = self.base_datos.obtener_reporte_compras_por_anio()
        elif texto == "Todas":
            # Hacer que al dar doble click en la tabla se abra la ventana de detalles
            reporte = self.base_datos.obtener_compras()
            self.tabla.cellDoubleClicked.connect(self.mostrar_detalles_compra)
            self.generar_tabla_todas_compras(reporte)
            return
        self.tabla.clearContents()
        self.generar_tabla_compras(reporte)

    def generar_tabla_compras(self, reporte):
        # Limpiar la tabla antes de llenarla
        self.tabla.clearContents()
        self.tabla.setRowCount(len(reporte))
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Fecha", "Cantidad de Productos", "Gastos"])
        for fila, producto in enumerate(reporte):

            fecha_item = QTableWidgetItem(f"{producto['Fecha']}")
            ingreso_item = QTableWidgetItem(f"{producto['CantidadProductos']}")
            ganancias_item = QTableWidgetItem(f"Q{producto['Gastos']:.2f}") 
            
            self.tabla.setItem(fila, 0, fecha_item)
            self.tabla.setItem(fila, 1, ingreso_item)
            self.tabla.setItem(fila, 2, ganancias_item)

            for col in range(3):
                item = self.tabla.item(fila, col)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

    def generar_tabla_todas_compras(self, reporte): # IdCompra, Proveedor, Empleado, FechaCompra, Total
        # Limpiar la tabla antes de llenarla
        self.tabla.clearContents()
        self.tabla.setRowCount(len(reporte))
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["IdCompra", "Proveedor", "Empleado", "FechaCompra", "Total"])
        for fila, compra in enumerate(reporte):

            id_item = QTableWidgetItem(f"{compra['IdCompra']}")
            proveedor_item = QTableWidgetItem(f"{compra['Proveedor']}")
            empleado_item = QTableWidgetItem(f"{compra['Empleado']}") 
            fecha_compra_item = QTableWidgetItem(f"{compra['FechaCompra']}")
            total_item = QTableWidgetItem(f"Q{compra['Total']:.2f}")

            self.tabla.setItem(fila, 0, id_item)
            self.tabla.setItem(fila, 1, proveedor_item)
            self.tabla.setItem(fila, 2, empleado_item)
            self.tabla.setItem(fila, 3, fecha_compra_item)
            self.tabla.setItem(fila, 4, total_item)

            for col in range(5):
                item = self.tabla.item(fila, col)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)


    def mostrar_detalles_compra(self, fila):
        if self.verificacion is not None:
            self.limpieza_layout(self.verificacion)
        
        layout1 = QVBoxLayout()
        self.verificacion = layout1

        cartelera = QLabel("Detalles de la compra")
        self.color_linea(cartelera)
        cartelera.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        cartelera.setFixedHeight(50)
        cartelera.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cartelera.setEnabled(False)

        boton_cerrar = QPushButton("cerrar")
        self.color_boton_sin_oprimir(boton_cerrar)
        boton_cerrar.setFixedHeight(50)
        boton_cerrar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        boton_cerrar.clicked.connect(self.limpieza_detalle_compra)

        fecha = self.tabla.item(fila, 0).text()
        
        detalle_vendidos = self.base_datos.obtener_detalles_por_id_compra(fecha) # Devuelve IdOrden, Producto, CantidadRecibida, Total

        self.detalle_compra = QTableWidget(len(detalle_vendidos), 4)
        self.detalle_compra.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.detalle_compra.setHorizontalHeaderLabels(["IdOrden", "Producto", "Cantidad recibida", "Gasto total"])

        for fila, producto in enumerate(detalle_vendidos):

            id_item = QTableWidgetItem(f"{producto['IdOrden']}")
            producto_item = QTableWidgetItem(producto['Producto'])
            cantidad_item = QTableWidgetItem(f"{producto['CantidadRecibida']}")
            gasto_item = QTableWidgetItem(f"Q{producto['Total']:.2f}") 
            
            self.detalle_compra.setItem(fila, 0, id_item)
            self.detalle_compra.setItem(fila, 1, producto_item)
            self.detalle_compra.setItem(fila, 2, cantidad_item)
            self.detalle_compra.setItem(fila, 3, gasto_item)

            for col in range(4):
                item = self.detalle_compra.item(fila, col)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

        self.color_tabla(self.detalle_compra)
        self.detalle_compra.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.detalle_compra.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout1.addWidget(cartelera)
        layout1.addWidget(self.detalle_compra)
        layout1.addWidget(boton_cerrar)
        self.layout2.addLayout(layout1)

    def limpieza_detalle_compra(self):
        self.limpieza_layout(self.layout2)
        self.reporte_compras()
        self.verificacion = None
        self.orden_tabla_compras.setCurrentIndex(3)  # Cambia a "Todas" al cerrar el detalle

    def generar_reporte(self):
        self.nueva_ventana = QWidget()
        self.nueva_ventana.setWindowTitle("Generar Reporte")
        self.fondo_degradado(self.nueva_ventana, "#0037FF", "#5DA9F5")
        self.nueva_ventana.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.limpieza_layout(self.layout2)
        self.color_boton_oprimido(self.boton_generar_reporte)
        self.color_boton_sin_oprimir(self.boton_reporte_ventas)
        self.color_boton_sin_oprimir(self.boton_reporte_compras)

        main_layout = QVBoxLayout()

        layout1 = QGridLayout()
        layout2 = QVBoxLayout()
        layout3 = QHBoxLayout()

        # Widgets de selección de tipo de reporte
        seleccion_label = QLabel("Escoja el tipo de reporte que requiere")
        self.color_linea(seleccion_label)
        seleccion_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        seleccion_label.setFixedHeight(30)
        seleccion_label.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        self.opcion = QComboBox()
        self.opcion.addItems(["Ventas", "Compras", "Ventas por Producto"])
        self.color_caja_opciones(self.opcion)
        self.tipo = self.opcion.currentText

        # Widgets para selección de fechas con calendario
        fecha_inicio_label = QLabel("Seleccione la fecha de inicio:")
        fecha_inicio_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        fecha_inicio_label.setFixedHeight(30)
        self.color_linea(fecha_inicio_label)

        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)  # Activar el popup de calendario
        self.fecha_inicio.setDisplayFormat("yyyy-MM-dd")
        self.fecha_inicio.setDate(QDate.currentDate())  # Fecha actual por defecto
        self.fecha_inicio.setFixedSize(130, 30)
        self.fecha_inicio.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_caja_fechas(self.fecha_inicio)

        fecha_fin_label = QLabel("Seleccione la fecha final:")
        fecha_fin_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        fecha_fin_label.setFixedHeight(30)
        self.color_linea(fecha_fin_label)

        self.fecha_fin = QDateEdit()
        self.fecha_fin.setCalendarPopup(True)  # Activar el popup de calendario
        self.fecha_fin.setDisplayFormat("yyyy-MM-dd")
        self.fecha_fin.setDate(QDate.currentDate())  # Fecha actual por defecto
        self.fecha_fin.setFixedSize(130, 30)
        self.fecha_fin.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_caja_fechas(self.fecha_fin)

        # Botones
        boton_confirmar = QPushButton("Confirmar")
        boton_confirmar.setFixedHeight(30)
        boton_confirmar.clicked.connect(self.creacion_reporte)
        self.asignacion_tecla(self.nueva_ventana, "Return", boton_confirmar)
        self.color_boton_sin_oprimir(boton_confirmar)

        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.setFixedHeight(30)
        boton_cancelar.clicked.connect(self.cancelar_reporte)
        self.asignacion_tecla(self.nueva_ventana, "Esc", boton_cancelar)
        self.color_boton_sin_oprimir(boton_cancelar)

        # Mensaje informativo
        informar = QLabel("Seleccione las fechas usando los calendarios")
        informar.setStyleSheet("color: Black; font-size: 20px")
        informar.setAlignment(Qt.AlignmentFlag.AlignAbsolute)
        informar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Organización del layout
        layout1.addWidget(fecha_inicio_label, 0, 0)
        layout1.addWidget(self.fecha_inicio, 0, 1)
        layout1.addWidget(fecha_fin_label, 1, 0)
        layout1.addWidget(self.fecha_fin, 1, 1)

        layout3.addWidget(boton_confirmar)
        layout3.addWidget(boton_cancelar)

        main_layout.addWidget(seleccion_label)
        main_layout.addWidget(self.opcion)
        main_layout.addLayout(layout1)
        main_layout.addLayout(layout3)

        layout2.addStretch()
        layout2.addWidget(informar)
        layout2.addStretch()

        self.layout2.addLayout(layout2)
        self.nueva_ventana.setLayout(main_layout)
        self.nueva_ventana.showNormal()

    def creacion_reporte(self):
        # Obtener las fechas seleccionadas
        fecha_inicio = self.fecha_inicio.date().toString("yyyy-MM-dd")
        fecha_fin = self.fecha_fin.date().toString("yyyy-MM-dd")
        
        # Obtener el tipo de reporte seleccionado
        tipo_reporte = self.opcion.currentText()
        if tipo_reporte == "Ventas":
            # Aquí procesarías el reporte de ventas con las fechas obtenidas
            # Reporte devuelve una lista de diccionarios con los datos de ventas
            reporte = self.base_datos.obtener_reporte_ventas_por_fecha(fecha_inicio, fecha_fin)
            # Generar el PDF del reporte de ventas
            self.generar_pdf_ventas(reporte, fecha_inicio, fecha_fin)
            pass
        elif tipo_reporte == "Compras":
            # Aquí procesarías el reporte de compras con las fechas obtenidas
            reporte = self.base_datos.obtener_reporte_compras_por_fecha(fecha_inicio, fecha_fin)
            # Generar el PDF del reporte de compras
            self.generar_reporte_compras(reporte, fecha_inicio, fecha_fin)
            pass
        elif tipo_reporte == "Ventas por Producto":
            reporte = self.base_datos.obtener_reporte_ventas_por_producto(fecha_inicio, fecha_fin)
            self.generar_pdf_ventas_por_producto(reporte, fecha_inicio, fecha_fin)
        
        self.nueva_ventana.close()


    def generar_pdf_ventas(self, reporte, fecha_inicio, fecha_fin):
        try:
            # Convertir fechas a strings si son objetos date
            if hasattr(fecha_inicio, 'strftime'):
                fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')
            else:
                fecha_inicio_str = str(fecha_inicio)
            
            if hasattr(fecha_fin, 'strftime'):
                fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')
            else:
                fecha_fin_str = str(fecha_fin)

            # Configurar diálogo para guardar archivo
            file_path, _ = QFileDialog.getSaveFileName(
                self.layout.parentWidget(),
                "Guardar Reporte de Ventas",
                "C:/Users/queme/Desktop/reportes/" + f"Reporte_Ventas_{fecha_inicio_str}_a_{fecha_fin_str}.pdf",
                "PDF Files (*.pdf)"
            )
            
            if not file_path:
                return  # Usuario canceló

            # Crear PDF
            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter
            
            # 1. Encabezado principal
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, height - 80, "REPORTE DE VENTAS")
            
            c.setFont("Helvetica", 10)
            c.drawString(100, height - 110, f"Período: {fecha_inicio_str} a {fecha_fin_str}")
            c.drawString(100, height - 130, f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            c.drawString(100, height - 150, f"Total de días reportados: {len(reporte)}")
            
            # 2. Tabla de datos
            # Encabezados de tabla
            c.setFont("Helvetica-Bold", 12)
            c.drawString(100, height - 190, "DETALLE DE VENTAS DIARIAS")
            c.line(100, height - 195, width - 100, height - 195)
            
            y_position = height - 220
            c.setFont("Helvetica", 10)
            
            # Encabezados de columnas
            c.drawString(100, y_position, "Fecha")
            c.drawString(200, y_position, "Ingresos (Q)")
            c.drawString(300, y_position, "Productos")
            c.drawString(400, y_position, "Ganancias (Q)")
            y_position -= 25
            
            # Datos del reporte
            c.setFont("Helvetica", 10)
            for registro in reporte:
                if y_position < 100:  # Salto de página
                    c.showPage()
                    y_position = height - 50
                    c.setFont("Helvetica", 10)
                
                # Formatear fecha del registro
                fecha_registro = registro["Fecha"]
                if hasattr(fecha_registro, 'strftime'):
                    fecha_str = fecha_registro.strftime('%d/%m/%Y')
                else:
                    fecha_str = str(fecha_registro)
                
                c.drawString(100, y_position, fecha_str)
                c.drawString(200, y_position, f"Q{registro['IngresoTotal']:.2f}")
                c.drawString(300, y_position, str(registro["ProductosVendidos"]))
                c.drawString(400, y_position, f"Q{registro['Ganancia']:.2f}")
                y_position -= 20
            
            # 3. Totales
            c.setFont("Helvetica-Bold", 12)
            c.line(100, y_position - 10, width - 100, y_position - 10)
            
            total_ingresos = sum(r['IngresoTotal'] for r in reporte)
            total_productos = sum(r['ProductosVendidos'] for r in reporte)
            total_ganancias = sum(r['Ganancia'] for r in reporte)
            
            c.drawString(100, y_position - 30, "TOTALES:")
            c.drawString(200, y_position - 30, f"Q{total_ingresos:.2f}")
            c.drawString(300, y_position - 30, str(total_productos))
            c.drawString(400, y_position - 30, f"Q{total_ganancias:.2f}")
            
            # 4. Pie de página
            c.setFont("Helvetica-Oblique", 8)
            c.drawCentredString(width/2, 50, "Sistema de Gestión Comercial - Reporte generado automáticamente")
            
            c.save()

            self.imprimir_reporte(file_path, "¿Imprimir reporte?", "¿Desea imprimir el reporte?")
            
        except Exception as e:
            self.mensaje_error("Error en PDF", f"No se pudo generar el reporte:\n{str(e)}")

    def safe_int(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0
    def generar_pdf_ventas_por_producto(self, reporte, fecha_inicio, fecha_fin):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from datetime import datetime
            from PyQt6.QtWidgets import QFileDialog

            # Formato de fecha
            if hasattr(fecha_inicio, 'strftime'):
                fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')
            else:
                fecha_inicio_str = str(fecha_inicio)
            
            if hasattr(fecha_fin, 'strftime'):
                fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')
            else:
                fecha_fin_str = str(fecha_fin)

            # Diálogo para guardar
            file_path, _ = QFileDialog.getSaveFileName(
                self.layout.parentWidget(),
                "Guardar Reporte de Ventas por Producto",
                "C:/Users/queme/Desktop/reportes/" + f"Ventas_Por_Producto_{fecha_inicio_str}_a_{fecha_fin_str}.pdf",
                "PDF Files (*.pdf)"
            )

            if not file_path:
                return  # Cancelado

            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter

            # Encabezado
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, height - 80, "REPORTE DE VENTAS POR PRODUCTO")
            c.setFont("Helvetica", 10)
            c.drawString(100, height - 110, f"Período: {fecha_inicio_str} a {fecha_fin_str}")
            c.drawString(100, height - 130, f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            c.drawString(100, height - 150, f"Total de productos reportados: {len(reporte)}")

            # Tabla
            c.setFont("Helvetica-Bold", 12)
            c.drawString(100, height - 190, "DETALLE DE PRODUCTOS VENDIDOS")
            c.line(100, height - 195, width - 100, height - 195)

            y_position = height - 220
            c.setFont("Helvetica-Bold", 10)
            c.drawString(80, y_position, "ID")
            c.drawString(120, y_position, "Producto")
            c.drawString(300, y_position, "Cantidad")
            c.drawString(370, y_position, "Precio Unitario")
            c.drawString(470, y_position, "Total Generado")
            y_position -= 20

            c.setFont("Helvetica", 10)

            total_general = 0
            total_cantidad = 0

            for prod in reporte:
                if y_position < 100:
                    c.showPage()
                    y_position = height - 50
                    c.setFont("Helvetica", 10)

                c.drawString(80, y_position, str(prod['IdProducto']))
                c.drawString(120, y_position, str(prod['Producto']))
                c.drawString(300, y_position, str(prod['CantidadVendida']))
                c.drawString(370, y_position, f"Q{prod['PrecioUnitario']:.2f}")
                c.drawString(470, y_position, f"Q{prod['TotalGenerado']:.2f}")
                total_general += prod['TotalGenerado']
                total_cantidad += prod['CantidadVendida']
                y_position -= 20

            # Totales
            c.setFont("Helvetica-Bold", 12)
            c.line(100, y_position - 10, width - 100, y_position - 10)
            c.drawString(100, y_position - 30, "TOTALES:")
            c.drawString(300, y_position - 30, str(total_cantidad))
            c.drawString(470, y_position - 30, f"Q{total_general:.2f}")

            # Pie
            c.setFont("Helvetica-Oblique", 8)
            c.drawCentredString(width / 2, 50, "Sistema de Gestión Comercial - Reporte generado automáticamente")

            c.save()
            self.imprimir_reporte(file_path, "¿Imprimir reporte?", "¿Desea imprimir el reporte?")

        except Exception as e:
            self.mensaje_error("Error en PDF", f"No se pudo generar el reporte:\n{str(e)}")


    def generar_reporte_compras(self, reporte, fecha_inicio, fecha_fin):
        try:
            # 1. Configurar diálogo para guardar archivo
            fecha_gen = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path, _ = QFileDialog.getSaveFileName(
                self.layout.parentWidget(),
                "Guardar Reporte de Compras",
                "C:/Users/queme/Desktop/reportes/" + f"Reporte_Ventas_{fecha_inicio}_a_{fecha_fin}.pdf",
                "PDF Files (*.pdf)"
            )
            
            if not file_path:
                return False  # Usuario canceló

            # 2. Crear PDF
            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter
            
            # Estilos
            titulo_estilo = ("Helvetica-Bold", 16)
            subtitulo_estilo = ("Helvetica-Bold", 12)
            texto_estilo = ("Helvetica", 10)
            pie_estilo = ("Helvetica-Oblique", 8)

            # 3. Encabezado
            c.setFont(*titulo_estilo)
            c.drawString(100, height - 80, "REPORTE DE COMPRAS")
            
            c.setFont(*texto_estilo)
            c.drawString(100, height - 110, f"Período: {fecha_inicio} a {fecha_fin}")
            c.drawString(100, height - 130, f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            c.drawString(100, height - 150, f"Total de órdenes: {len(reporte)}")

            # 4. Tabla de compras
            c.setFont(*subtitulo_estilo)
            c.drawString(100, height - 190, "DETALLE DE ÓRDENES DE COMPRA")
            c.line(100, height - 195, width - 100, height - 195)
            
            # Encabezados de tabla
            y_position = height - 220
            headers = ["Fecha", "Orden #", "Proveedor", "Total (Q)", "Productos"]
            positions = [100, 175, 250, 350, 450]
            
            c.setFont("Helvetica-Bold", 10)
            for pos, header in zip(positions, headers):
                c.drawString(pos, y_position, header)
            
            # Datos
            y_position -= 20
            c.setFont(*texto_estilo)
            
            for compra in reporte:
                if y_position < 100:  # Salto de página
                    c.showPage()
                    y_position = height - 50
                    c.setFont(*texto_estilo)
                
                # Formatear fecha
                fecha = compra.get('fecha', '')
                if hasattr(fecha, 'strftime'):
                    fecha_str = fecha.strftime('%d/%m/%Y')
                else:
                    fecha_str = str(fecha)
                
                # Dibujar fila
                c.drawString(positions[0], y_position, fecha_str)
                c.drawString(positions[1], y_position, str(compra.get('orden_id', '')))
                c.drawString(positions[2], y_position, compra.get('proveedor', '')[:20])  # Limitar caracteres
                c.drawString(positions[3], y_position, f"Q{compra.get('total', 0):.2f}")
                c.drawString(positions[4], y_position, str(compra.get('productos_totales', 0)))
                y_position -= 20

            # 5. Totales
            total_gastado = sum(c['total'] for c in reporte)
            total_productos = sum(c['productos_totales'] for c in reporte)
            promedio_orden = total_gastado / len(reporte) if reporte else 0
            
            c.setFont(*subtitulo_estilo)
            c.line(100, y_position - 10, width - 100, y_position - 10)
            
            c.drawString(100, y_position - 30, "TOTALES:")
            c.drawString(350, y_position - 30, f"Q{total_gastado:.2f}")
            c.drawString(450, y_position - 30, str(total_productos))

            # 6. Resumen estadístico
            y_position -= 60
            c.setFont(*subtitulo_estilo)
            c.drawString(100, y_position, "RESUMEN ESTADÍSTICO")
            c.line(100, y_position - 5, width - 100, y_position - 5)
            
            c.setFont(*texto_estilo)
            y_position -= 25
            
            if reporte:
                # Encontrar proveedor con más compras
                proveedores = {}
                for compra in reporte:
                    prov = compra['proveedor']
                    proveedores[prov] = proveedores.get(prov, 0) + compra['total']
                
                top_proveedor = max(proveedores.items(), key=lambda x: x[1]) if proveedores else ('N/A', 0)
                
                stats = [
                    f"Proveedor principal: {top_proveedor[0]} (Q{top_proveedor[1]:.2f})",
                    f"Orden más grande: Q{max(c['total'] for c in reporte):.2f}",
                    f"Promedio por orden: Q{promedio_orden:.2f}"
                ]
                
                for stat in stats:
                    c.drawString(120, y_position, stat)
                    y_position -= 20

            # 7. Pie de página
            c.setFont(*pie_estilo)
            c.drawCentredString(width/2, 50, "Sistema de Gestión Comercial - Reporte generado automáticamente")

            # 8. Guardar PDF
            c.save()
            # 9. Imprimir reporte
            self.imprimir_reporte(file_path, "¿Imprimir reporte?", "¿Desea imprimir el reporte?")
            return True
            
        except Exception as e:
            QMessageBox.critical(
                self.layout.parentWidget(),
                "Error en PDF",
                f"No se pudo generar el reporte:\n{str(e)}"
            )
            return False

    def cancelar_reporte(self):
        self.nueva_ventana.close()
        self.limpieza_layout(self.layout2)

        layout = QVBoxLayout()
                        
        informar = QLabel("Oprima uno de los botones que tiene en la parte superior izquierda")
        informar.setStyleSheet("color: Black; font-size: 20px")
        informar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        layout.addStretch()
        layout.addWidget(informar)
        layout.addStretch()

        self.nueva_ventana = None

        self.layout2.addLayout(layout)
