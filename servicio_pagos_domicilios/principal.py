from fastapi import FastAPI
from base_datos import engine, Base
import modelos.tablas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servicio Pagos y Domicilios")

@app.get("/")
def inicio():
    return {"mensaje": "Servicio de Pagos y Domicilios activo"}
