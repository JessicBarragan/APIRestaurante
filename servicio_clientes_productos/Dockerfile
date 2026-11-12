FROM python:3.11-slim

WORKDIR /app

COPY servicio_clientes_productos/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY servicio_clientes_productos/ .

COPY shared/ ./shared/

CMD ["uvicorn", "principal:app", "--host", "0.0.0.0", "--port", "8000"]