from fastapi import FastAPI
from servicio_clientes_productos.rutas.rutas_cliente import enrutador as enrutador_clientes
from servicio_clientes_productos.rutas.rutas_producto import enrutador as enrutador_productos

app = FastAPI(title="Servicio de Clientes y Productos")
app.include_router(enrutador_clientes)
app.include_router(enrutador_productos)
