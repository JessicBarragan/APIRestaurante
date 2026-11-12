# Frontend – Restaurante y Cafetería

React + Vite. Consume el gateway (`http://localhost:8000`) sin modificar el backend.

## Cómo correrlo
1. Levanta el backend: `docker compose up --build` (en la raíz de APIRestaurante).
2. En esta carpeta: `npm install` y `npm run dev` → http://localhost:5173
3. Si el gateway está en otra URL: `GATEWAY_URL=http://otra:8000 npm run dev`

El gateway no tiene CORS, por eso Vite reenvía `/api/*` al gateway (ver `vite.config.js`).

## Qué incluye
- Carta pública (agrupada por categoría) y carrito.
- Login / registro con JWT. Pedido: crea un pago y un domicilio enlazados por un `id_pedido` generado en el front.
- Panel de administración (solo `ROLE_ADMIN`): CRUD de productos y clientes; lista de pagos y domicilios.

## Límites del backend que el front tiene que esquivar
- `/auth/registro` siempre crea `ROLE_USER`; no hay forma de crear un admin por la API.
- No existe endpoint de pedidos: los ítems del carrito no se guardan, solo monto y dirección.
- `nombre_repartidor` es obligatorio en domicilios: se envía "Por asignar".
- Usuarios, pagos y domicilios viven en memoria: se pierden al reiniciar los contenedores.
- Clientes devuelve `email`/`nombre` pero pide `correo`/`nombre_completo`: se adapta en `src/api.js`.

## Ver el panel de administración (desarrollo)
El backend no permite crear admins, así que para probar localmente:
1. Desde la raíz de APIRestaurante: `pip install pyjwt cryptography` y `python frontend/scripts/token_admin.py` (usa tu `private_key.pem`, dura 8 h).
2. En el front: Ingresar → "Entrar con token de administrador" → pega el token.
3. Administración → Productos → "Cargar carta de ejemplo".
Es solo para desarrollo: el grupo debe acordar cómo crear un admin real.
