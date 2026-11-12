// Capa de acceso al backend. Todo pasa por el gateway (/api/<servicio>/...).
// Las diferencias entre endpoints (email/correo, nombre/nombre_completo) se
// arreglan AQUÍ, para no tocar el backend.
const BASE = '/api';
let token = localStorage.getItem('token') || '';
let onUnauthorized = () => {};

export const setToken = (t) => {
  token = t || '';
  t ? localStorage.setItem('token', t) : localStorage.removeItem('token');
};
export const setOnUnauthorized = (fn) => (onUnauthorized = fn);
export const money = (n) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(n);

async function req(path, { method = 'GET', body } = {}) {
  let res;
  try {
    res = await fetch(BASE + path, {
      method,
      headers: { ...(body && { 'Content-Type': 'application/json' }), ...(token && { Authorization: `Bearer ${token}` }) },
      body: body && JSON.stringify(body),
    });
  } catch {
    throw new Error('No hay conexión con el servidor. Revisa que el gateway esté corriendo en el puerto 8000.');
  }
  const data = await res.json().catch(() => null);
  if (!res.ok) {
    if (res.status === 401 && token) onUnauthorized();
    const d = data?.detail;
    if (res.status === 403 && d === 'Not authenticated') throw new Error('Inicia sesión para continuar.');
    const msg = Array.isArray(d) ? d.map((e) => `${e.loc?.slice(-1)[0]}: ${e.msg}`).join(', ') : d;
    throw new Error(msg || `Error ${res.status}`);
  }
  return data;
}

// El backend devuelve {id, nombre, email} al listar, pero pide {nombre_completo, correo} al guardar.
const cliente = (c) => ({
  id: c.id,
  nombre_completo: c.nombre ?? c.nombre_completo,
  correo: c.correo ?? c.email,
  telefono: c.telefono ?? '',
  direccion: c.direccion ?? '',
});

const crud = (ruta, map = (x) => x) => ({
  list: async () => (await req(`/${ruta}/`)).map(map),
  create: (b) => req(`/${ruta}/`, { method: 'POST', body: b }),
  update: (id, b) => req(`/${ruta}/${id}`, { method: 'PUT', body: b }),
  remove: (id) => req(`/${ruta}/${id}`, { method: 'DELETE' }),
});

export const api = {
  async login(correo, contrasena) {
    const r = await req('/auth/login', { method: 'POST', body: { correo, contrasena } });
    setToken(r.access_token);
    return req('/auth/perfil'); // {id, nombre_completo, correo, rol}
  },
  registro: (nombre_completo, correo, contrasena) =>
    req('/auth/registro', { method: 'POST', body: { nombre_completo, correo, contrasena } }),
  productos: crud('productos'),
  clientes: crud('clientes', cliente),
  pagos: { list: () => req('/pagos/'), create: (b) => req('/pagos/', { method: 'POST', body: b }) },
  domicilios: { list: () => req('/domicilios/'), create: (b) => req('/domicilios/', { method: 'POST', body: b }) },
};
