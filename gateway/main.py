from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
import httpx

app = FastAPI(title="API Gateway - Restaurante & Cafetería")

# Diccionario que le dice al Gateway a qué microservicio
# (y puerto) debe redirigir cada tipo de petición.
SERVICES = {
    "customers": "http://localhost:4001",
    "products": "http://localhost:4001",
    "orders": "http://localhost:4002",
    "inventory": "http://localhost:4002",
    "payments": "http://localhost:4003",
    "deliveries": "http://localhost:4003",
}


@app.get("/")
async def home():
    """Ruta simple para comprobar que el Gateway está vivo."""
    return {"mensaje": "API Gateway del restaurante funcionando 🚀"}


@app.api_route("/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway_proxy(service_name: str, path: str, request: Request):
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail="Servicio no encontrado en el Gateway")

    target_url = f"{SERVICES[service_name]}/{service_name}/{path}"

    client = httpx.AsyncClient()
    body = await request.body()

    try:
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=dict(request.headers),
            params=dict(request.query_params),
            content=body,
            timeout=10.0
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
    except httpx.RequestError as exc:
        return JSONResponse(
            status_code=503,
            content={"detail": f"El servicio '{service_name}' no está disponible actualmente. Error: {str(exc)}"}
        )
    finally:
        await client.aclose()
