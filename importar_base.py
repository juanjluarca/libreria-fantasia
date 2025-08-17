import subprocess

# Configuración de la base de datos
db_host = 'localhost'
db_user = 'root' # Aquí se coloca el usuario de tu base de datos
db_password = 'F_r24Q16z' # Aquí se coloca la contraseña de la base de datos
db_name = 'modelo_proyecto'

# Ruta del archivo SQL
backup_file = 'modelo_proyecto.sql'

# Comando para importar usando mysql CLI
command = f"mysql -h {db_host} -u {db_user} -p{db_password} {db_name} < {backup_file}"

# Ejecutar el comando
try:
    subprocess.run(command, shell=True, check=True)
    print("Backup importado correctamente.")
except subprocess.CalledProcessError as e:
    print("Error al importar el backup:", e)
