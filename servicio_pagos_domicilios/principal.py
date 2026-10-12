from fastapi import FastAPI
from base_datos import engine, Base
import modelos.tablas

from rutas.rutas_pago import enrutador as enrutador_pagos
from rutas.rutas_domicilio import enrutador as enrutador_domicilios

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servicio Pagos y Domicilios")

app.include_router(enrutador_pagos)
app.include_router(enrutador_domicilios)


@app.get("/")
def inicio():
    return {"mensaje": "Servicio de Pagos y Domicilios activo"}