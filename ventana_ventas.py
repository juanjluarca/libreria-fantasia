from codigo import Codigo
from PyQt6.QtWidgets import QFileDialog, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QMessageBox, QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem, QHeaderView 
from PyQt6.QtGui import QIcon, QPixmap, QGuiApplication, QLinearGradient, QColor, QBrush, QPalette
from PyQt6.QtCore import Qt, QSize
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class Ventana_ventas(Codigo):
    def __init__(self, main_layout: QVBoxLayout, botones, base_datos, id_usuario, nivel, ventana_principal):
        super().__init__()
        self.layout = main_layout
        self.botones = botones
        self.base_datos = base_datos
        self.nivel = nivel
        self.fila_carrito = 0
        self.carrito = []
        self.total_venta = 0
        self.id_usuario = id_usuario
        self.nueva_ventana = None
        self.ventana_principal = ventana_principal

    def ventas(self):
        self.limpieza_layout(self.layout)
        self.color_acceso_nivel(self.nivel, self.botones)
        self.color_boton_oprimido(self.botones[1])
        self.activar_botones(self.botones)
        self.botones[1].setEnabled(False)

        main_layout = QHBoxLayout()
        layout1 = QVBoxLayout()

        layout2 = QHBoxLayout()
        layout2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout3 = QVBoxLayout()

        layout4 = QVBoxLayout()
        layout4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout5 = QHBoxLayout()
        layout5.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.ingreso_busqueda = QLineEdit()
        self.ingreso_busqueda.setPlaceholderText("Ingrese el nombre del producto...")
        self.color_linea(self.ingreso_busqueda)
        self.ingreso_busqueda.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ingreso_busqueda.setFixedHeight(80)
        self.ingreso_busqueda.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        boton_buscar = QPushButton()
        boton_buscar.setIcon(QIcon(self.imagen("imagenes/buscar.png", 65, 65)))
        boton_buscar.setIconSize(QSize(75, 75))
        self.color_boton_sin_oprimir(boton_buscar)
        boton_buscar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_buscar.clicked.connect(self.buscar_producto)
        self.asignacion_tecla(self.ventana_principal, "Return", boton_buscar)
        
        inventario = self.base_datos.obtener_productos_ventas()

        #Tabla de ventas
        self.tabla1 = QTableWidget(len(inventario), 5)
        self.tabla1.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.tabla1.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción", "Existencias", "Precio" ]) 

        
        # Llenar la tabla con los datos
        for fila, producto in enumerate(inventario):
            # Convertir los valores a strings (excepto los que ya lo son)
            id_item = QTableWidgetItem(str(producto['id']))
            nombre_item = QTableWidgetItem(producto['nombre'])
            descripcion_item = QTableWidgetItem(producto['descripcion'])
            existencia_item = QTableWidgetItem(str(producto['stock']))
            precio_item = QTableWidgetItem(f"Q{producto['precio']:.2f}")  # Formato con 2 decimales
            
            # Añadir items a la tabla
            self.tabla1.setItem(fila, 0, id_item)
            self.tabla1.setItem(fila, 1, nombre_item)
            self.tabla1.setItem(fila, 2, descripcion_item)
            self.tabla1.setItem(fila, 3, existencia_item)
            self.tabla1.setItem(fila, 4, precio_item)
            
            # Configurar flags para todos los items
            for col in range(5):
                item = self.tabla1.item(fila, col)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

        self.tabla1.resizeColumnsToContents()
        self.color_tabla(self.tabla1)
        self.tabla1.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tabla1.cellDoubleClicked.connect(self.agregar_cantidad)

        carrito_label = QLineEdit()
        carrito_label.setPlaceholderText("Carrito")
        self.color_linea(carrito_label)
        carrito_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        carrito_label.setFixedHeight(80)
        carrito_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        carrito_label.setEnabled(False)

        #Tabla carrito
        self.tabla2 = QTableWidget(0, 4)
        self.tabla2.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.tabla2.setHorizontalHeaderLabels(["ID","Nombre", "Cantidad", "Precio"]) 

        self.tabla2.resizeColumnsToContents()
        self.color_tabla(self.tabla2)
        self.tabla2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tabla2.cellDoubleClicked.connect(self.restar_cantidad)

        self.total = QLineEdit()
        self.total.setText(f"Total de compra: Q{self.total_venta:.2f}")
        self.color_linea(self.total)
        self.total.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total.setFixedHeight(50)
        self.total.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.total.setEnabled(False)

        boton_confirmar = QPushButton("Confirmar")
        boton_confirmar.setFixedHeight(50)
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        boton_confirmar.clicked.connect(self.confirmar_venta)
        
        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.setFixedHeight(50)
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        boton_cancelar.clicked.connect(self.cancelar_compra)

        layout2.addWidget(self.ingreso_busqueda)
        layout2.addWidget(boton_buscar)

        layout1.addLayout(layout2)
        layout1.addWidget(self.tabla1)

        layout5.addWidget(boton_confirmar)
        layout5.addWidget(boton_cancelar)

        layout4.addWidget(self.total)
        layout4.addLayout(layout5)

        layout3.addWidget(carrito_label)
        layout3.addWidget(self.tabla2)
        layout3.addLayout(layout4)

        main_layout.addItem(self.espacio(35, 35))
        main_layout.addLayout(layout1)
        main_layout.addLayout(layout3)
        self.layout.addLayout(main_layout)

    def restar_cantidad(self):
        if self.nueva_ventana is not None:
            self.nueva_ventana.close()

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
        boton_confirmar.clicked.connect(self.confirmar_modificar_cantidad)
        self.asignacion_tecla(self.nueva_ventana, "Return", boton_confirmar)

        boton_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setFixedSize(100, 20)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_cancelar.clicked.connect(self.cancelar_cantidad)
        self.asignacion_tecla(self.nueva_ventana, "Esc", boton_cancelar)

        layout1.addWidget(boton_confirmar)
        layout1.addWidget(boton_cancelar)

        main_layout.addWidget(cantidad_label, 0, 0)
        main_layout.addWidget(self.nueva_cantidad, 1, 0)
        main_layout.addLayout(layout1, 2, 0)

        self.nueva_ventana.setLayout(main_layout)
        self.nueva_ventana.showNormal()

    def confirmar_modificar_cantidad(self):
        fila = self.tabla2.currentRow()
        cantidad_anterior = self.tabla2.item(fila, 2).text() #  "ID","Nombre", "Cantidad", "Precio"
        precio = self.tabla2.item(fila, 3).text()[1:]
        nueva_cantidad = self.nueva_cantidad.text()
        # Verificar que la nueva cantidad sea un número positivo
        # Recorrer el carrito para modificar la cantidad en el producto con el id correspondiente
        if int(nueva_cantidad) > 0:
            for i in range(len(self.carrito)):
                if self.carrito[i][0] == int(self.tabla2.item(fila, 0).text()):  # El carrito almacena id, nuevo_stock, cantidad, precio
                    # Si el producto ya existe, actualizar la cantidad 
                    self.carrito[i][2] = nueva_cantidad
                    break
        self.tabla2.setItem(fila, 2, QTableWidgetItem(str(nueva_cantidad))) #
        # Actualizar el total de la venta
        antiguo_total_producto = int(cantidad_anterior) * float(precio)
        nuevo_total_producto = int(nueva_cantidad) * float(precio)
        self.total_venta = self.total_venta - antiguo_total_producto + nuevo_total_producto
        self.total.setText(f"Total de compra: Q{self.total_venta:.2f}")
        # Cerrar la ventana de cantidad
        self.nueva_ventana.close()

    def agregar_cantidad(self):
        if self.nueva_ventana is not None:
            self.nueva_ventana.close()

        self.nueva_ventana = QWidget()
        self.fondo_degradado(self.nueva_ventana, "#5DA9F5", "#0037FF")
        self.nueva_ventana.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        main_layout = QGridLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout1 = QHBoxLayout()

        label_cantidad = QLabel("Ingrese la cantidad")
        label_cantidad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_cantidad.setFixedHeight(30)
        self.color_linea(label_cantidad)
        label_cantidad.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        self.cantidad = QLineEdit()
        self.cantidad.setPlaceholderText("Ingrese la cantidad...")
        self.color_linea(self.cantidad)
        self.cantidad.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cantidad.setFixedHeight(30)
        self.cantidad.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        boton_confirmar = QPushButton("Confirmar")
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setFixedSize(100, 20)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.asignacion_tecla(self.nueva_ventana, "Return", boton_confirmar)
        boton_confirmar.clicked.connect(self.confirmar_cantidad)

        boton_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setFixedSize(100, 20)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.asignacion_tecla(self.nueva_ventana, "Esc", boton_cancelar)
        boton_cancelar.clicked.connect(self.cancelar_cantidad)
        
        layout1.addWidget(boton_confirmar)
        layout1.addWidget(boton_cancelar)

        main_layout.addWidget(label_cantidad, 0, 0)
        main_layout.addWidget(self.cantidad, 1, 0)
        main_layout.addLayout(layout1, 2, 0)

        self.nueva_ventana.setLayout(main_layout)
        self.nueva_ventana.showNormal()

    def confirmar_cantidad(self):
        fila = self.tabla1.currentRow()
        cantidad = self.cantidad.text()

        # Verificar que la cantidad sea menor o igual a la existencia del producto
        # y que sea un número positivo
        if int(cantidad) <= int(self.tabla1.item(fila, 3).text()) and int(cantidad) > 0:
            # Buscar en tabla carrito si el producto ya existe
            nueva_cantidad = 0
            for i in range(self.tabla2.rowCount()):
                if self.tabla2.item(i, 0).text() == self.tabla1.item(fila, 0).text():
                    # Si el producto ya existe, actualizar la cantidad 
                    nueva_cantidad = int(self.tabla2.item(i, 2).text()) + int(cantidad)
                    self.tabla2.setItem(i, 2, QTableWidgetItem(str(nueva_cantidad)))
                    break
            id_producto = int(self.tabla1.item(fila, 0).text())
            precio_producto = float(self.tabla1.item(fila, 4).text()[1:])
            total_producto = int(cantidad) * precio_producto
            nombre_producto = self.tabla1.item(fila, 1).text()
            if nueva_cantidad == 0:
                # 👇 Insertar nueva fila en la tabla2
                self.tabla2.insertRow(self.fila_carrito)

                item_id = QTableWidgetItem(str(id_producto))
                item_nombre = QTableWidgetItem(nombre_producto)
                item_cantidad = QTableWidgetItem(f"{cantidad}")
                item_precio = QTableWidgetItem(f"Q{precio_producto:.2f}")

                self.tabla2.setItem(self.fila_carrito, 0, item_id)
                self.tabla2.setItem(self.fila_carrito, 1, item_nombre)
                self.tabla2.setItem(self.fila_carrito, 2, item_cantidad)
                self.tabla2.setItem(self.fila_carrito, 3, item_precio)

                for col in range(4):
                    item = self.tabla2.item(self.fila_carrito, col)
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

                self.fila_carrito += 1

            self.total_venta += total_producto
            self.total.setText(f"Total de compra: Q{self.total_venta:.2f}")
            # Modificar el stock del producto en la base de datos
            nuevo_stock = int(self.tabla1.item(fila, 3).text()) - int(cantidad)
            self.carrito.append([id_producto, nuevo_stock, cantidad, precio_producto]) # El carrito almacena id, nuevo_stock, cantidad, precio


            # Actualizar la tabla de ventas
            self.tabla1.setItem(fila, 3, QTableWidgetItem(str(nuevo_stock)))
            
            # Cerrar la ventana de cantidad
            self.nueva_ventana.close()
            
        else:
            self.mensaje_error("Error", "La cantidad ingresada es mayor a la existencia del producto o no es válida")
            return



    def confirmar_venta(self):
        # Primero confirmar la venta en la base de datos
        self.base_datos.agregar_venta(self.id_usuario, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.total_venta)
        id_venta = self.base_datos.obtener_id_ultima_venta()
        
        for producto in self.carrito:
            id_producto = producto[0]
            nuevo_stock = producto[1]
            stock_venta = producto[2]
            precio = producto[3]
            self.base_datos.modificar_producto_stock(id_producto, nuevo_stock)
            self.base_datos.agregar_detalle_venta(id_producto, id_venta, stock_venta, precio)

        # Preguntar si desea generar PDF
        respuesta = QMessageBox()
        respuesta.setStyleSheet("QMessageBox { color: black; background-color: #40BCFF;} QPushButton {color: black; background-color: #7C9DFF; border: 2px solid black; min-width: 50px; min-height: 20px;} QPushButton:hover {background-color: #38B3F5;} QPushButton:pressed {background-color: #2268F5;} QLabel{color: black;}")
        respuesta.setWindowIcon(QIcon("imagenes/infomation.ico"))
        respuesta.setWindowTitle("¿Generar comprobante?")
        respuesta.setText("¿Desea generar un comprobante en PDF de esta venta?")
        respuesta.setIcon(QMessageBox.Icon.Information)
        respuesta.addButton("Si", QMessageBox.ButtonRole.YesRole)
        respuesta.addButton("No", QMessageBox.ButtonRole.NoRole)
        respuesta = respuesta.exec()
        if respuesta == 2:
            self.generar_pdf_venta(id_venta)
        
        self.tabla2.clearContents()
        self.tabla2.setRowCount(0)
        self.tabla2.setColumnCount(4)
        self.carrito.clear()
        self.total.clear()
        self.total.setText("Total de compra: Q0")
        self.fila_carrito = 0
        self.total_venta = 0   

    def generar_pdf_venta(self, id_venta):
        try:
            # Obtener detalles de la venta
            detalles_venta = self.base_datos.obtener_detalles_venta_para_pdf(id_venta)
            if not detalles_venta:
                raise ValueError("No se encontraron detalles para la venta")
                
            # Configurar diálogo para guardar archivo
            fecha_venta = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path, _ = QFileDialog.getSaveFileName(
                self.layout.parentWidget(),
                "Guardar Comprobante",
                "C:/Users/queme/Desktop/ventas/" + f"Venta_{id_venta}_{fecha_venta}.pdf", 
                "PDF Files (*.pdf)"
            )
            
            if not file_path:
                return  # Usuario canceló

            # Crear PDF
            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter  # Ahora letter está definido
            
            # Diseño del PDF
            # 1. Encabezado
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, height - 100, "COMPROBANTE DE VENTA")
            
            c.setFont("Helvetica", 10)
            c.drawString(100, height - 130, f"N° Venta: {id_venta}")
            c.drawString(100, height - 150, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            c.drawString(100, height - 170, f"Atendido por: Empleado_{self.id_usuario}")
            
            # 2. Detalles de productos
            c.setFont("Helvetica-Bold", 12)
            c.drawString(100, height - 210, "DETALLE DE PRODUCTOS")
            c.line(100, height - 215, width - 100, height - 215)
            
            y_position = height - 240
            c.setFont("Helvetica-Bold", 10)
            
            # Encabezados de tabla
            c.drawString(100, y_position, "Producto")
            c.drawString(300, y_position, "Cant.")
            c.drawString(350, y_position, "P.Unit.")
            c.drawString(450, y_position, "Subtotal")
            y_position -= 20
            c.setFont("Helvetica", 10)
            
            # Productos
            for producto in detalles_venta:
                if y_position < 100:  # Salto de página
                    c.showPage()
                    y_position = height - 50
                    c.setFont("Helvetica", 10)
                
                c.drawString(100, y_position, producto['nombre'][:30])  # Limita caracteres
                c.drawString(300, y_position, str(producto['cantidad']))
                c.drawString(350, y_position, f"Q{producto['precio_unitario']:.2f}")
                c.drawString(450, y_position, f"Q{producto['subtotal']:.2f}")
                y_position -= 20
            
            # 3. Totales
            c.setFont("Helvetica-Bold", 12)
            c.line(100, y_position - 10, width - 100, y_position - 10)
            c.drawString(350, y_position - 30, "TOTAL:")
            c.drawString(450, y_position - 30, f"Q{detalles_venta[0]['total_venta']:.2f}")
            
            # 4. Pie de página
            c.setFont("Helvetica-Oblique", 8)
            c.drawCentredString(width/2, 50, "Gracias por su compra - Sistema de Ventas")
            
            c.save()
            
            self.imprimir_reporte(file_path, "¿Imprimir ticket?", "¿Desea imprimir el ticket de la venta?")
            
        except Exception as e:
            self.mensaje_error("Error en PDF", f"No se pudo generar el comprobante:\n{str(e)}")

    def llenar_inventario(self):
        # Volver a cargar la tabla de ventas con los productos originales
        inventario = self.base_datos.obtener_productos_ventas()
        self.tabla1.setRowCount(len(inventario))

        # Llenar la tabla con los datos
        for fila, producto in enumerate(inventario):
            id_item = QTableWidgetItem(str(producto['id']))
            nombre_item = QTableWidgetItem(producto['nombre'])
            descripcion_item = QTableWidgetItem(producto['descripcion'])
            existencia_item = QTableWidgetItem(str(producto['stock']))
            precio_item = QTableWidgetItem(f"Q{producto['precio']:.2f}")

            # Añadir items a la tabla
            self.tabla1.setItem(fila, 0, id_item)
            self.tabla1.setItem(fila, 1, nombre_item)
            self.tabla1.setItem(fila, 2, descripcion_item)
            self.tabla1.setItem(fila, 3, existencia_item)
            self.tabla1.setItem(fila, 4, precio_item)

    def cancelar_compra(self):
        # Volver a cargar la tabla de ventas con los productos originales
        self.llenar_inventario()
        self.tabla2.clearContents()
        self.tabla2.setRowCount(0)
        self.tabla2.setColumnCount(4)
        self.carrito.clear()
        self.total.clear()
        self.total.setText("Total de compra: Q0")
        self.total_venta = 0
        self.fila_carrito = 0

    def cancelar_cantidad(self):
        self.nueva_ventana.close()
        self.nueva_ventana = None

    def buscar_producto(self):
        # Buscar el producto por nombre en la base de datos
        nombre_producto = self.ingreso_busqueda.text()
        resultado = self.base_datos.buscar_producto_ventas_por_nombre(nombre_producto)
        
        if len(resultado) != 0:
            # Limpiar la tabla antes de mostrar los resultados
            self.tabla1.clearContents()
            self.tabla1.setRowCount(len(resultado))
            # Llenar la tabla con los resultados de la búsqueda
            for fila, producto in enumerate(resultado):
                id_item = QTableWidgetItem(str(producto['id']))
                nombre_item = QTableWidgetItem(producto['nombre'])
                descripcion_item = QTableWidgetItem(producto['descripcion'])
                existencia_item = QTableWidgetItem(str(producto['stock']))
                precio_item = QTableWidgetItem(f"Q{producto['precio']:.2f}")

                # Añadir items a la tabla
                self.tabla1.setItem(fila, 0, id_item)
                self.tabla1.setItem(fila, 1, nombre_item)
                self.tabla1.setItem(fila, 2, descripcion_item)
                self.tabla1.setItem(fila, 3, existencia_item)
                self.tabla1.setItem(fila, 4, precio_item)

        else:
            self.mensaje_error("Error", "No se encontraron productos con ese nombre")

        self.ingreso_busqueda.clear()


