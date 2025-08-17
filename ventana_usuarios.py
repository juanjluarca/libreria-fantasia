from codigo import Codigo
from PyQt6.QtWidgets import QApplication ,QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QMessageBox, QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem, QHeaderView 
from PyQt6.QtGui import QIcon, QPixmap, QGuiApplication, QLinearGradient, QColor, QBrush, QPalette
from PyQt6.QtCore import Qt, QSize
import bcrypt


class Ventana_usuarios(Codigo):
    def __init__(self, main_layout, botones, base_datos, nivel, ventana_principal):
        super().__init__()
        self.layout = main_layout
        self.botones = botones
        self.base_datos = base_datos
        self.layout_extra: QVBoxLayout | None = None
        self.nivel = nivel
        self.ventana_principal = ventana_principal

    def usuario(self):
        self.limpieza_layout(self.layout)
        self.color_acceso_nivel(self.nivel, self.botones)
        self.color_boton_oprimido(self.botones[0])
        self.activar_botones(self.botones)
        self.botones[0].setEnabled(False)
        
        main_layout = QHBoxLayout()

        layout1 = QVBoxLayout()

        layout2 = QHBoxLayout()
        layout2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        self.layout3 = QHBoxLayout()
        self.layout3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.boton_editar = QPushButton()
        self.boton_editar.setIcon(QIcon(self.imagen("imagenes/editar.png", 50, 50)))
        self.boton_editar.setIconSize(QSize(70, 70))
        self.boton_editar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_boton_sin_oprimir(self.boton_editar)
        self.boton_editar.clicked.connect(self.editar_usuario)  

        self.boton_eliminar = QPushButton()
        self.boton_eliminar.setIcon(QIcon(self.imagen("imagenes/eliminar.png", 50, 50)))
        self.boton_eliminar.setIconSize(QSize(70, 70))
        self.boton_eliminar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_boton_sin_oprimir(self.boton_eliminar)
        self.boton_eliminar.clicked.connect(self.eliminar_usuario)

        self.boton_agregar = QPushButton()
        self.boton_agregar.setIcon(QIcon(self.imagen("imagenes/agregar.png", 50, 50)))
        self.boton_agregar.setIconSize(QSize(70, 70))
        self.boton_agregar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_boton_sin_oprimir(self.boton_agregar)
        self.boton_agregar.clicked.connect(self.agregar_usuario)

        self.boton_busqueda = QPushButton()
        self.boton_busqueda.setIcon(QIcon(self.imagen("imagenes/buscar.png", 50, 50)))
        self.boton_busqueda.setIconSize(QSize(70, 70))
        self.boton_busqueda.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.color_boton_sin_oprimir(self.boton_busqueda)
        self.boton_busqueda.clicked.connect(self.buscar_usuario)
        self.asignacion_tecla(self.ventana_principal, "Return", self.boton_busqueda)
        

        self.ingreso_busqueda = QLineEdit()
        self.ingreso_busqueda.setPlaceholderText("Ingrese el nombre del usuario...")
        self.color_linea(self.ingreso_busqueda)
        self.ingreso_busqueda.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ingreso_busqueda.setFixedSize(400, 80)
        self.ingreso_busqueda.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # creacion de tabla,
        # usuarios =  [["1", "root", "Ejemplo@gmail.com", "Telefono1", "Vendedora"]] 
        usuarios = self.base_datos.obtener_usuarios() # (id, nombre, email, tipo, telefono)

        # Crear la tabla con el número correcto de filas y columnas
        self.tabla_usuarios = QTableWidget(len(usuarios), 5)
        self.tabla_usuarios.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Define los encabezados de las columnas
        self.tabla_usuarios.setHorizontalHeaderLabels(["ID", "Usuario", "Correo", "Puesto", "Telefono"])

        # Llenar la tabla con los datos
        for fila, usuario in enumerate(usuarios):
            id_item = QTableWidgetItem(str(usuario['id']))
            nombre_item = QTableWidgetItem(usuario['nombre'])
            email_item = QTableWidgetItem(usuario['email'])
            telefono_item = QTableWidgetItem(usuario['tipo'])
            puesto_item = QTableWidgetItem(usuario['telefono'])
            
            # Añadir items a la tabla
            # Verificar que el usuario esté activo (estado = 1)
            if usuario['estado'] == 1:
                self.tabla_usuarios.setItem(fila, 0, id_item)
                self.tabla_usuarios.setItem(fila, 1, nombre_item)
                self.tabla_usuarios.setItem(fila, 2, email_item)
                self.tabla_usuarios.setItem(fila, 3, telefono_item)
                self.tabla_usuarios.setItem(fila, 4, puesto_item)
                
                # Configurar flags para todos los items
                for col in range(5):
                    item = self.tabla_usuarios.item(fila, col)
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            

        # Opcional: Ajustar el tamaño de las columnas al contenido
        self.tabla_usuarios.resizeColumnsToContents()
        #Modificacion del color, bordes y fondo de la tabla
        self.color_tabla(self.tabla_usuarios)
        self.tabla_usuarios.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_usuarios.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout2.addWidget(self.boton_editar)
        layout2.addWidget(self.boton_eliminar)
        layout2.addWidget(self.boton_agregar)
        layout2.addWidget(self.boton_busqueda)
        layout2.addWidget(self.ingreso_busqueda)

        self.layout3.addWidget(self.tabla_usuarios)
        
        layout1.addLayout(layout2)
        layout1.addLayout(self.layout3)

        main_layout.addItem(self.espacio(35, 35))
        main_layout.addLayout(layout1)
        self.layout.addLayout(main_layout)

    def agregar_usuario(self):
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
        agregar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        agregar_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        agregar_label.setScaledContents(True)

        self.ingreso_nombre = QLineEdit()
        self.color_linea(self.ingreso_nombre)
        self.ingreso_nombre.setFixedWidth(200)
        self.ingreso_nombre.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_email = QLineEdit()
        self.color_linea(self.ingreso_email)
        self.ingreso_email.setFixedWidth(200)
        self.ingreso_email.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_telefono = QLineEdit()
        self.color_linea(self.ingreso_telefono)
        self.ingreso_telefono.setFixedWidth(200)
        self.ingreso_telefono.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_puesto = QLineEdit()
        self.color_linea(self.ingreso_puesto)
        self.ingreso_puesto.setFixedWidth(200)
        self.ingreso_puesto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        self.ingreso_contrasennia = QLineEdit()
        self.color_linea(self.ingreso_contrasennia)
        self.ingreso_contrasennia.setFixedWidth(200)
        self.ingreso_contrasennia.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_nombre = QLabel("Ingrese el usuario: ")
        label_nombre.setStyleSheet("color: Black; font-size: 12px")
        label_nombre.setFixedWidth(200)
        label_nombre.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        label_nombre.setAlignment(Qt.AlignmentFlag.AlignRight)

        label_email = QLabel("Ingrese el email: ")
        label_email.setStyleSheet("color: Black; font-size: 12px")
        label_email.setFixedWidth(200)
        label_email.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        label_email.setAlignment(Qt.AlignmentFlag.AlignRight)

        label_telfono = QLabel("Ingrese el telefono: ")
        label_telfono.setStyleSheet("color: Black; font-size: 12px")
        label_telfono.setFixedWidth(200)
        label_telfono.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        label_telfono.setAlignment(Qt.AlignmentFlag.AlignRight)

        label_puesto = QLabel("Puesto(0 = Admin, 1 = Vend): ")
        label_puesto.setStyleSheet("color: Black; font-size: 12px")
        label_puesto.setFixedWidth(200)
        label_puesto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        label_puesto.setAlignment(Qt.AlignmentFlag.AlignRight)

        label_contrasennia = QLabel("Ingrese la contraseña: ")
        label_contrasennia.setStyleSheet("color: Black; font-size: 12px")
        label_contrasennia.setFixedWidth(200)
        label_contrasennia.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        label_contrasennia.setAlignment(Qt.AlignmentFlag.AlignRight)

        boton_confirmar = QPushButton("Agregar")
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setFixedWidth(200)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_confirmar.clicked.connect(self.agregar_usuario_base)

        boton_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setFixedWidth(200)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_cancelar.clicked.connect(self.cancelar)

        layout1.addWidget(agregar_label)
        layout1.addItem(self.espacio(50, 50))

        layout2.addWidget(label_nombre, 0, 0)
        layout2.addWidget(self.ingreso_nombre, 0, 1)
        layout2.addWidget(label_telfono, 1, 0)
        layout2.addWidget(self.ingreso_telefono, 1, 1)
        layout2.addWidget(label_email, 2, 0)
        layout2.addWidget(self.ingreso_email, 2, 1)
        layout2.addWidget(label_puesto, 3, 0)
        layout2.addWidget(self.ingreso_puesto, 3, 1)
        layout2.addWidget(label_contrasennia, 4, 0)
        layout2.addWidget(self.ingreso_contrasennia, 4, 1)
        layout2.addWidget(boton_confirmar, 5, 0)
        layout2.addWidget(boton_cancelar, 5, 1)
        
        self.layout_extra.addLayout(layout1)
        self.layout_extra.addLayout(layout2)

        self.layout3.addLayout(self.layout_extra)


    def editar_usuario(self):
        # Cada que se complete una insercion o elemiminacion el Layout se tiene que volver a poner como none (esto no es definitivo)
        if self.layout_extra is not None:
            self.limpieza_layout(self.layout_extra)

        self.tabla_usuarios.cellClicked.connect(self.llenar_campos)

        self.layout_extra = QVBoxLayout()
        self.layout_extra.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout1 = QVBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout2 = QGridLayout()
        layout2.setSpacing(30)

        imagen_agregar = self.imagen("imagenes/editar.png", 90, 90)
        agregar_label = QLabel()
        agregar_label.setPixmap(imagen_agregar)
        agregar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        agregar_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        agregar_label.setScaledContents(True)

        self.ingreso_nombre = QLineEdit()
        self.color_linea(self.ingreso_nombre)
        self.ingreso_nombre.setFixedWidth(200)
        self.ingreso_nombre.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_email = QLineEdit()
        self.color_linea(self.ingreso_email)
        self.ingreso_email.setFixedWidth(200)
        self.ingreso_email.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_telefono = QLineEdit()
        self.color_linea(self.ingreso_telefono)
        self.ingreso_telefono.setFixedWidth(200)
        self.ingreso_telefono.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.ingreso_puesto = QLineEdit()
        self.color_linea(self.ingreso_puesto)
        self.ingreso_puesto.setFixedWidth(200)
        self.ingreso_puesto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        self.ingreso_contrasennia = QLineEdit() #ingreso_nombre, ingreso_email, ingreso_telefono, ingreso_puesto, ingreso_contrasennia
        self.color_linea(self.ingreso_contrasennia)
        self.ingreso_contrasennia.setFixedWidth(200)
        self.ingreso_contrasennia.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        label_nombre = QLabel("Ingrese el usuario: ")
        label_nombre.setFixedWidth(200)
        label_nombre.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        label_nombre.setStyleSheet("color: Black; font-size: 12px")
        label_nombre.setAlignment(Qt.AlignmentFlag.AlignRight)

        label_email = QLabel("Ingrese el email: ")
        label_email.setFixedWidth(200)
        label_email.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        label_email.setStyleSheet("color: Black; font-size: 12px")
        label_email.setAlignment(Qt.AlignmentFlag.AlignRight)

        label_telfono = QLabel("Ingrese el telefono: ")
        label_telfono.setFixedWidth(200)
        label_telfono.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        label_telfono.setStyleSheet("color: Black; font-size: 12px")
        label_telfono.setAlignment(Qt.AlignmentFlag.AlignRight)

        label_puesto = QLabel("Puesto(0 = Admin, 1 = Vend): ")
        label_puesto.setFixedWidth(200)
        label_puesto.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        label_puesto.setStyleSheet("color: Black; font-size: 12px")
        label_puesto.setAlignment(Qt.AlignmentFlag.AlignRight)

        label_contrasennia = QLabel("Ingrese la contraseña: ")
        label_contrasennia.setFixedWidth(200)
        label_contrasennia.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        label_contrasennia.setStyleSheet("color: Black; font-size: 12px")
        label_contrasennia.setAlignment(Qt.AlignmentFlag.AlignRight)

        boton_confirmar = QPushButton("Modificar")
        self.color_boton_sin_oprimir(boton_confirmar)
        boton_confirmar.setFixedWidth(200)
        boton_confirmar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_confirmar.clicked.connect(self.modificar_usuario_base)

        boton_cancelar = QPushButton("Cancelar")
        self.color_boton_sin_oprimir(boton_cancelar)
        boton_cancelar.setFixedWidth(200)
        boton_cancelar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        boton_cancelar.clicked.connect(self.cancelar)

        layout1.addWidget(agregar_label)
        layout1.addItem(self.espacio(50, 50))

        layout2.addWidget(label_nombre, 0, 0)
        layout2.addWidget(self.ingreso_nombre, 0, 1)
        layout2.addWidget(label_telfono, 1, 0)
        layout2.addWidget(self.ingreso_telefono, 1, 1)
        layout2.addWidget(label_email, 2, 0)
        layout2.addWidget(self.ingreso_email, 2, 1)
        layout2.addWidget(label_puesto, 3, 0)
        layout2.addWidget(self.ingreso_puesto, 3, 1)
        layout2.addWidget(label_contrasennia, 4, 0)
        layout2.addWidget(self.ingreso_contrasennia, 4, 1)
        layout2.addWidget(boton_confirmar, 5, 0)
        layout2.addWidget(boton_cancelar, 5, 1)
        
        self.layout_extra.addLayout(layout1)
        self.layout_extra.addLayout(layout2)

        self.layout3.addLayout(self.layout_extra)

    def llenar_campos(self, row): #ingreso_nombre, ingreso_email, ingreso_puesto, ingreso_telefono, (agregar contraseña)
        self.nombre = self.tabla_usuarios.item(row, 1).text()
        self.email = self.tabla_usuarios.item(row, 2).text()
        if self.tabla_usuarios.item(row, 3).text() == "Administrador":
            self.puesto = "0"
        elif self.tabla_usuarios.item(row, 3).text() == "Vendedor":
            self.puesto = "1"
        self.telefono = self.tabla_usuarios.item(row, 4).text()
        self.id = self.tabla_usuarios.item(row, 0).text()
        # self.contrasennia = self.tabla_usuarios.item(row, 5).text()


        self.ingreso_nombre.setText(self.nombre)
        self.ingreso_email.setText(self.email)
        self.ingreso_puesto.setText(self.puesto)
        self.ingreso_telefono.setText(self.telefono)

    def eliminar_usuario(self):
        # Obtener el id del usuario seleccionado
        fila_seleccionada = self.tabla_usuarios.currentRow()
        if fila_seleccionada == -1:
            self.mensaje_error("Error", "Por favor seleccione un usuario para eliminar")
            return

        id_usuario = self.tabla_usuarios.item(fila_seleccionada, 0).text()

        # Confirmar la eliminación
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
            try:
                # Llamar al método de la base de datos para eliminar el usuario
                self.base_datos.eliminar_usuario(int(id_usuario))
                self.limpieza_layout(self.layout_extra)
                self.usuario()
            except Exception as e:
                self.mensaje_error("Error", f"Error al eliminar el usuario: {e}")


    def agregar_usuario_base(self):
        # (nombre, email, tipo, contrasennia, telefono)
        nombre = self.ingreso_nombre.text()
        email = self.ingreso_email.text()
        telefono = self.ingreso_telefono.text()
        tipo = self.ingreso_puesto.text()
        contrasennia = self.ingreso_contrasennia.text()
        # Validacion de tipo de usuario
        if tipo == "0":
            tipo = "Administrador"
        elif tipo == "1":
            tipo = "Vendedor"
        else:
            self.mensaje_error("Error", "Tipo de usuario no valido")
            return
        # Validacion de campos vacios
        if not nombre or not email or not telefono or not tipo or not contrasennia:
            self.mensaje_error("Error", "Por favor complete todos los campos")
            return
        # Ingreso a la base de datos
        try:
            # Agregar usuario a la base y recargar la tabla
            # Encriptar la contrasennia con utf-8 antes de agregarla a la base de datos

            # Paso 1: codificar en UTF-8
            contrasena_bytes = contrasennia.encode('utf-8')

            # Paso 2: hashear con bcrypt
            hash_bcrypt = bcrypt.hashpw(contrasena_bytes, bcrypt.gensalt())

            print("Contraseña hasheada:", hash_bcrypt.decode())  # Opcionalmente lo decodificas para guardarlo como texto


            print(f"Datos del usuario: {nombre}, {email}, {tipo}, {contrasennia}, {telefono}")
            self.base_datos.agregar_usuario(nombre, email, tipo, hash_bcrypt, telefono)
            self.limpieza_layout(self.layout_extra)
            self.usuario()
        except Exception as e:
            self.mensaje_error("Error", f"Error al agregar el usuario: {e}")
            return
        
    def buscar_usuario(self):
        nombre = self.ingreso_busqueda.text()

        # Buscar el usuario en la base de datos
        try:
            resultado = self.base_datos.buscar_usuario_por_nombre(nombre)
            if resultado:
                # Limpiar la tabla antes de mostrar los resultados
                self.tabla_usuarios.setRowCount(0)

                for usuario in resultado:
                    id_item = QTableWidgetItem(str(usuario['id']))
                    nombre_item = QTableWidgetItem(usuario['nombre'])
                    email_item = QTableWidgetItem(usuario['email'])
                    telefono_item = QTableWidgetItem(usuario['tipo'])
                    puesto_item = QTableWidgetItem(usuario['telefono'])

                    # Añadir items a la tabla
                    self.tabla_usuarios.insertRow(self.tabla_usuarios.rowCount())
                    self.tabla_usuarios.setItem(self.tabla_usuarios.rowCount() - 1, 0, id_item)
                    self.tabla_usuarios.setItem(self.tabla_usuarios.rowCount() - 1, 1, nombre_item)
                    self.tabla_usuarios.setItem(self.tabla_usuarios.rowCount() - 1, 2, email_item)
                    self.tabla_usuarios.setItem(self.tabla_usuarios.rowCount() - 1, 3, telefono_item)
                    self.tabla_usuarios.setItem(self.tabla_usuarios.rowCount() - 1, 4, puesto_item)

                # Ajustar el tamaño de las columnas al contenido
                self.tabla_usuarios.resizeColumnsToContents()
                self.tabla_usuarios.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
                self.tabla_usuarios.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


            else:
                self.mensaje_error("Error", "No se encontraron resultados")
        except Exception as e:
            self.mensaje_error("Error", f"Error al buscar el usuario: {e}")
            return
        
    def modificar_usuario_base(self):
        # (nombre, email, tipo, contrasennia, telefono)
        id = self.id
        nombre = self.ingreso_nombre.text()
        email = self.ingreso_email.text()
        telefono = self.ingreso_telefono.text()
        tipo = self.ingreso_puesto.text()
        contrasennia = self.ingreso_contrasennia.text()
        # Validacion de tipo de usuario
        if tipo == "0":
            tipo = "Administrador"
        elif tipo == "1":
            tipo = "Vendedor"
        else:
            self.mensaje_error("Error", "Tipo de usuario no valido")
            return
        # Validacion de campos vacios
        if not nombre or not email or not telefono or not tipo or not contrasennia:
            self.mensaje_error("Error", "Por favor complete todos los campos")
            return
        # Ingreso a la base de datos
        try:
            # Agregar usuario a la base y recargar la tabla
            # Encriptar la contrasennia con utf-8 antes de agregarla a la base de datos

            # Paso 1: codificar en UTF-8
            contrasena_bytes = contrasennia.encode('utf-8')

            # Paso 2: hashear con bcrypt
            hash_bcrypt = bcrypt.hashpw(contrasena_bytes, bcrypt.gensalt())

            print("Contraseña hasheada:", hash_bcrypt.decode())  # Opcionalmente lo decodificas para guardarlo como texto


            self.base_datos.modificar_usuario(id, nombre, email, tipo, hash_bcrypt, telefono) 
            self.limpieza_layout(self.layout_extra)
            self.usuario()
        except Exception as e:
            self.mensaje_error("Error", f"Error al modificar el usuario: {e}")
            return
        
    def cancelar(self):
        self.limpieza_layout(self.layout_extra)
        self.usuario()



