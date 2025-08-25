import mysql.connector

# Conexión sin base de datos
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="120365"
)

cursor = db.cursor()

# Crear la base de datos si no existe
cursor.execute("CREATE DATABASE IF NOT EXISTS parte2")
cursor.execute("USE parte2")

# Leer el archivo SQL
with open(r"C:\Users\DELL\PycharmProjects\libreria-fantasia\modelo_proyecto.sql", "r", encoding="utf-8", errors="ignore") as f:
    sql_script = f.read()

# Ejecutar cada sentencia por separado
statements = sql_script.split(';')
for statement in statements:
    stmt = statement.strip()
    if stmt:  # Ignorar líneas vacías
        try:
            cursor.execute(stmt)
        except mysql.connector.Error as err:
            print(f"Error ejecutando la sentencia: {err}")

db.commit()
cursor.close()
db.close()

print("Backup importado correctamente.")
