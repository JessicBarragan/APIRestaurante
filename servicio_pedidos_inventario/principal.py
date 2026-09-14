from fastapi import FastAPI
from servicio_pedidos_inventario.rutas.rutas_pedido import enrutador as enrutador_pedidos
from servicio_pedidos_inventario.rutas.rutas_inventario import enrutador as enrutador_inventario

app = FastAPI(title="Servicio de Pedidos e Inventario")
app.include_router(enrutador_pedidos)
app.include_router(enrutador_inventario)