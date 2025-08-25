import mysql.connector


# Configuración de la base de datos
db_host = 'localhost'
db_user = 'root' # Aquí se coloca el usuario de tu base de datos
db_password = '2025000' # Aquí se coloca la contraseña de la base de datos
db_name = 'modelo_proyecto'

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
