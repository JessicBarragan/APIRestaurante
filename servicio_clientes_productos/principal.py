from fastapi import FastAPI
from base_datos import engine, Base
import modelos.tablas

from rutas.rutas_cliente import enrutador as enrutador_clientes
from rutas.rutas_producto import enrutador as enrutador_productos

# Crear las tablas de la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servicio Clientes y Productos")

# Registrar las rutas existentes
app.include_router(enrutador_clientes)
app.include_router(enrutador_productos)


@app.get("/")
def inicio():
    return {
        "mensaje": (
            "Servicio de Clientes y Productos activo "
            "con base de datos PostgreSQL"
        )
    }