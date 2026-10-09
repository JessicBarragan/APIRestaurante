from fastapi import FastAPI
from base_datos import engine, Base
import modelos.tablas

# Crea las tablas en PostgreSQL automáticamente al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servicio Clientes y Productos")

@app.get("/")
def inicio():
    return {"mensaje": "Servicio de Clientes y Productos activo con base de datos PostgreSQL"}
