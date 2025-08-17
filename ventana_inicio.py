import sys
import bcrypt
import pymysql
from codigo import Codigo
from ventana_principal import Ventana_principal
from Base_datos import BaseDatos
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QSizePolicy
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class Ventana_inicio(Codigo):
    def __init__(self):
        super().__init__()
        self.base_datos = None
        self.window2 = None

# Inicio de las ventanas del programa
    def inicio(self):
        self.window1 = QWidget()
        self.window1.setWindowTitle("Inicio de sesión")
        self.fondo_degradado(self.window1, "#5DA9F5", "#0037FF")
        self.window1.setWindowIcon(QIcon("imagenes/logo.ico"))
        self.window1.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.main_layout = QVBoxLayout()
        layout1 = QGridLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout2 = QHBoxLayout()
        layout2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        usuario_imagen = self.imagen("imagenes/usuario.png", 150, 150)
        usuario_label = QLabel()
        usuario_label.setPixmap(usuario_imagen)
        usuario_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        usuario_label.setScaledContents(True)

        usuario = QLabel("Ingrese el usuario:")
        usuario.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        usuario.setStyleSheet("Color: black")

        self.ingreso_usuario = QLineEdit()
        self.color_linea(self.ingreso_usuario)
        self.ingreso_usuario.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_usuario.setFixedWidth(200)

        contrasenia = QLabel("Ingrese la contraseña:")
        contrasenia.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        contrasenia.setStyleSheet("Color: black")

        self.ingreso_contrasenia = QLineEdit()
        self.color_linea(self.ingreso_contrasenia)
        self.ingreso_contrasenia.setEchoMode(QLineEdit.EchoMode.Password)
        self.ingreso_contrasenia.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ingreso_contrasenia.setFixedWidth(200)

        self.boton_ingresar = QPushButton("Ingresar")
        self.boton_ingresar.clicked.connect(self.verificacion)
        self.color_boton_sin_oprimir(self.boton_ingresar)
        self.boton_ingresar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_ingresar.setFixedWidth(200)
        self.asignacion_tecla(self.window1, "Return", self.boton_ingresar)

        self.boton_salir = QPushButton("Salir")
        self.boton_salir.clicked.connect(self.cerrar_programa)
        self.color_boton_sin_oprimir(self.boton_salir)
        self.boton_salir.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.boton_salir.setFixedWidth(200)
        self.asignacion_tecla(self.window1, "Esc", self.boton_salir)

        layout1.addWidget(usuario, 0, 0)
        layout1.addWidget(self.ingreso_usuario, 0, 1)
        layout1.addItem(self.espacio(10, 10), 1, 0, 1, 1)
        layout1.addWidget(contrasenia, 2, 0)
        layout1.addWidget(self.ingreso_contrasenia, 2, 1)
        layout1.addItem(self.espacio(10, 10), 3, 0, 3, 1)
        layout1.addWidget(self.boton_ingresar, 4, 0)
        layout1.addWidget(self.boton_salir, 4, 1)

        layout2.addWidget(usuario_label)

        self.main_layout.addLayout(layout2)
        self.main_layout.addLayout(layout1)
        self.window1.setLayout(self.main_layout)
        self.window1.showNormal()

    def verificacion(self):
        user = self.ingreso_usuario.text()
        password = self.ingreso_contrasenia.text()

        try:
            base_datos = BaseDatos('root', 'F_r24Q16z')

            # Cambio principal: PyMySQL no tiene is_connected(), verificamos con ping()
            if base_datos.conexion and base_datos.conexion.open:
                try:
                    base_datos.conexion.ping(reconnect=True)  # Verifica que la conexión esté activa

                    pwd = password.encode('utf-8') 
                    password = base_datos.obtener_contraseña(user)
                    id = base_datos.obtener_id_usuario(user)
                    # Verificar si el usuario está activo, si no está activo no se permite el ingreso

                    if password is None:
                        self.mensaje_error("Error", "Usuario o contraseña incorrectos")
                        self.ingreso_usuario.clear()
                        self.ingreso_contrasenia.clear()
                        
                    elif bcrypt.checkpw(pwd, password.encode('utf-8')):
                            if self.window2 is None:
                                self.window2 = Ventana_principal(self.ingreso_usuario, base_datos, Ventana_inicio(), self.boton_ingresar, self.boton_salir, id)
                                self.window2.principal()
                                self.window1.close()
                                
                            else:
                                self.window2.principal()
                                self.window1.close()
                            
                    else:
                        self.mensaje_error("Error", "Usuario o contraseña incorrectos")
                        self.ingreso_usuario.clear()
                        self.ingreso_contrasenia.clear()
                        
                except Exception as e:
                    self.mensaje_error("Error", f"Conexión interrumpida: {str(e)}")
                    self.ingreso_usuario.clear()
                    self.ingreso_contrasenia.clear()
            else:
                self.mensaje_error("Error", "No se pudo conectar a la base de datos")
                self.ingreso_usuario.clear()
                self.ingreso_contrasenia.clear()

        except pymysql.Error as e:  # Captura específicamente errores de PyMySQL
            error_msg = f"Error de MySQL ({e.args[0]}): {e.args[1]}"
            print(f"Error al conectar: {error_msg}")
            self.mensaje_error("Error de conexión",
                                f"No se pudo conectar a la base de datos:\n{error_msg}")
            self.ingreso_usuario.clear()
            self.ingreso_contrasenia.clear()
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            self.mensaje_error("Error",
                                f"Ocurrió un error inesperado:\n{str(e)}")
            self.ingreso_usuario.clear()
            self.ingreso_contrasenia.clear()


    def cerrar_programa(self):
        self.window1.close()
        sys.exit()
