"""Solo para desarrollo local: firma un token de ADMIN con TU private_key.pem.
No modifica el backend; el backend lo acepta porque verifica con la misma llave.
Uso (desde la raíz de APIRestaurante):
    pip install pyjwt cryptography
    python frontend/scripts/token_admin.py
Copia el token y pégalo en Ingresar > "Entrar con token de administrador".
"""
from datetime import datetime, timedelta, timezone
import jwt

with open("private_key.pem", "rb") as f:
    llave = f.read()

print(jwt.encode(
    {"sub": "admin", "correo": "admin@restaurante.local", "rol": "ROLE_ADMIN",
     "exp": datetime.now(timezone.utc) + timedelta(hours=8)},
    llave, algorithm="RS256"))
