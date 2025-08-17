import bcrypt

contrasennia = "paco123"

# Paso 1: codificar en UTF-8
contrasena_bytes = contrasennia.encode('utf-8')

# Paso 2: hashear con bcrypt
hash_bcrypt = bcrypt.hashpw(contrasena_bytes, bcrypt.gensalt())

print("Contraseña hasheada:", hash_bcrypt.decode())  # Opcionalmente lo decodificas para guardarlo como texto
