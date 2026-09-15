from fastapi import FastAPI
from servicio_pagos_domicilios.rutas.rutas_pago import enrutador as enrutador_pagos
from servicio_pagos_domicilios.rutas.rutas_domicilio import enrutador as enrutador_domicilios

app = FastAPI(title="Servicio de Pagos y Domicilios")
app.include_router(enrutador_pagos)
app.include_router(enrutador_domicilios)