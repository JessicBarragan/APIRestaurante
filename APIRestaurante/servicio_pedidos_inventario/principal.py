from fastapi import FastAPI
from servicio_pedidos_inventario.rutas.rutas_pedido import enrutador as enrutador_pedidos
from servicio_pedidos_inventario.rutas.rutas_inventario import enrutador as enrutador_inventario

app = FastAPI(title="Servicio de Pedidos e Inventario")
app.include_router(enrutador_pedidos)
app.include_router(enrutador_inventario)

from fastapi import FastAPI
from servicio_clientes_productos.rutas.rutas_cliente import enrutador as enrutador_clientes
from servicio_clientes_productos.rutas.rutas_producto import enrutador as enrutador_productos

app = FastAPI(title="Servicio de Clientes y Productos")
app.include_router(enrutador_clientes)
app.include_router(enrutador_productos)
