import pytest
from Base_datos import BaseDatos
import pymysql

@pytest.fixture(scope="module")
def test_db():
    # Conexión a la base de datos de pruebas
    connection = pymysql.connect(
        host="localhost",
        user="usuario_prueba",
        password="password_prueba",
        database="modelo_proyecto_test",
        cursorclass=pymysql.cursors.DictCursor
    )
    
    # Verificar si la tabla existe, si no, crearla
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS producto (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                precio DECIMAL(10,2) NOT NULL,
                stock INT NOT NULL,
                descripcion TEXT,
                costo DECIMAL(10,2),
                stock_minimo INT
            )
        """)
    connection.commit()
    
    yield connection  # Proporcionar la conexión a las pruebas
    
    # Limpieza: Vaciar la tabla SIN eliminarla
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE producto")
    connection.commit()
    connection.close()

@pytest.fixture
def db_instance(test_db):
    """Fixture que proporciona una instancia de BaseDatos configurada para pruebas"""
    # Configuración temporal para usar la conexión de prueba
    original_init = BaseDatos.__init__
    
    def mock_init(self, user, password):
        self.conexion = test_db
    
    # Aplicar el mock
    BaseDatos.__init__ = mock_init
    db = BaseDatos("usuario_prueba", "password_prueba")
    
    yield db
    
    # Restaurar la implementación original
    BaseDatos.__init__ = original_init

def test_agregar_producto(db_instance, test_db):
    # Datos de prueba
    test_product = {
        "nombre": "Libro de Prueba",
        "precio": "100.00",
        "stock": 10,
        "descripcion": "Descripción de prueba",
        "existencia_minima": 2
    }
    
    # Ejecutar el método a probar
    db_instance.agregar_producto(**test_product)
    
    # Verificar en la base de datos
    with test_db.cursor() as cursor:
        cursor.execute("SELECT * FROM producto WHERE nombre = %s", (test_product["nombre"],))
        result = cursor.fetchone()
        
        assert result is not None
        assert float(result["precio"]) == test_product["precio"]
        assert result["stock"] == test_product["stock"]
        # Comparación con tolerancia para decimales
        assert abs(float(result["costo"]) - (test_product["precio"] * 0.85)) < 0.01

def test_obtener_productos(db_instance, test_db):
    # Insertar datos de prueba directamente
    with test_db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO producto 
            (nombre, precio, stock, descripcion, costo, stock_minimo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, ("Libro Existente", 50.0, 5, "Descripción existente", 42.5, 1))
        test_db.commit()
    
    # Obtener productos
    productos = db_instance.obtener_productos()
    
    # Verificar
    assert isinstance(productos, list)
    assert len(productos) >= 1
    assert any(p["nombre"] == "Libro Existente" for p in productos)

def test_eliminar_producto(db_instance, test_db):
    # Insertar producto para eliminar
    with test_db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO producto 
            (nombre, precio, stock, descripcion, costo, stock_minimo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, ("Libro a Eliminar", 75.0, 5, "Para eliminar", 63.75, 1))
        cursor.execute("SELECT LAST_INSERT_ID() AS id")
        product_id = cursor.fetchone()["id"]
        test_db.commit()
    
    # Eliminar producto
    db_instance.eliminar_producto(product_id)
    
    # Verificar eliminación
    with test_db.cursor() as cursor:
        cursor.execute("SELECT * FROM producto WHERE id = %s", (product_id,))
        assert cursor.fetchone() is None