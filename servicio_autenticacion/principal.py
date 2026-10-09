from fastapi import FastAPI

from servicio_autenticacion.rutas.rutas_auth import enrutador as enrutador_auth

app = FastAPI(title="Servicio de Autenticación")
app.include_router(enrutador_auth)
