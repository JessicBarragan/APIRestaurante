import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

app = FastAPI(title="API Gateway - Restaurante & Cafetería")

# Nombre de la ruta -> microservicio al que se redirige.
# Los nombres coinciden con los prefijos reales de cada servicio.
SERVICIOS = {
    "clientes": "http://localhost:4001",
    "productos": "http://localhost:4001",
    "pedidos": "http://localhost:4002",
    "inventario": "http://localhost:4002",
    "pagos": "http://localhost:4003",
    "domicilios": "http://localhost:4003",
    "auth": "http://localhost:4004",
}

# Cabeceras que NO se deben copiar entre peticiones/respuestas
CABECERAS_IGNORADAS = {"host", "content-length", "content-encoding",
                       "transfer-encoding", "connection"}


@app.get("/")
async def inicio():
    return {"mensaje": "API Gateway del restaurante funcionando", "servicios": list(SERVICIOS)}


@app.api_route("/{nombre_servicio}", methods=["GET", "POST", "PUT", "DELETE"])
@app.api_route("/{nombre_servicio}/{ruta:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(nombre_servicio: str, request: Request, ruta: str = ""):
    if nombre_servicio not in SERVICIOS:
        return JSONResponse(status_code=404,
                            content={"detail": f"'{nombre_servicio}' no existe en el Gateway"})

    url_destino = f"{SERVICIOS[nombre_servicio]}/{nombre_servicio}/{ruta}"
    cabeceras = {k: v for k, v in request.headers.items() if k.lower() not in CABECERAS_IGNORADAS}
    cuerpo = await request.body()

    try:
        async with httpx.AsyncClient(timeout=10.0) as cliente:
            respuesta = await cliente.request(
                method=request.method,
                url=url_destino,
                headers=cabeceras,
                params=dict(request.query_params),
                content=cuerpo,
            )
    except httpx.RequestError as exc:
        return JSONResponse(
            status_code=503,
            content={"detail": f"El servicio '{nombre_servicio}' no está disponible actualmente. Error: {exc}"},
        )

    cabeceras_respuesta = {k: v for k, v in respuesta.headers.items()
                           if k.lower() not in CABECERAS_IGNORADAS}
    return Response(content=respuesta.content, status_code=respuesta.status_code,
                    headers=cabeceras_respuesta)
