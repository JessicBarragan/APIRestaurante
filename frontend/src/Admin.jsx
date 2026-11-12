import { useEffect, useState } from 'react';
import { api, money } from './api';

const SEMILLA = [
  ['Bebidas Calientes', 'Café Capuchino', 8500, 'Café expreso con leche vaporizada'],
  ['Bebidas Calientes', 'Tinto', 3000, 'Café colombiano recién colado'],
  ['Bebidas Calientes', 'Chocolate con queso', 7500, 'Chocolate espeso con queso campesino'],
  ['Bebidas Calientes', 'Aromática de frutas', 4500, 'Infusión de frutas y hierbas'],
  ['Bebidas Frías', 'Limonada de coco', 9000, 'Limón, crema de coco y hielo'],
  ['Bebidas Frías', 'Jugo de mora en leche', 8000, 'Mora fresca licuada con leche'],
  ['Bebidas Frías', 'Té frío de durazno', 6500, 'Té negro con durazno'],
  ['Desayunos', 'Calentado paisa', 16000, 'Frijoles, arroz, huevo y arepa'],
  ['Desayunos', 'Huevos pericos con arepa', 12000, 'Huevo con tomate y cebolla'],
  ['Desayunos', 'Caldo de costilla', 11000, 'Caldo con papa y cilantro'],
  ['Platos Fuertes', 'Bandeja paisa', 28000, 'Frijoles, chicharrón, carne, huevo y arepa'],
  ['Platos Fuertes', 'Sancocho de gallina', 22000, 'Sopa con yuca, plátano y mazorca'],
  ['Platos Fuertes', 'Pechuga a la plancha', 21000, 'Con arroz, ensalada y papas'],
  ['Postres', 'Torta de tres leches', 9500, 'Bizcocho húmedo con crema'],
  ['Postres', 'Brownie con helado', 10500, 'Brownie tibio con helado de vainilla'],
  ['Postres', 'Arroz con leche', 5500, 'Con canela y pasas'],
].map(([categoria, nombre, precio, descripcion]) => ({ categoria, nombre, precio, descripcion, disponible: true }));

const TABS = {
  productos: {
    titulo: 'Productos', semilla: true, api: api.productos, vacio: { nombre: '', categoria: '', precio: '', descripcion: '', disponible: true },
    campos: [['nombre', 'Nombre'], ['categoria', 'Categoría'], ['precio', 'Precio (COP)', 'number'], ['descripcion', 'Descripción'], ['disponible', 'Disponible', 'checkbox']],
    cols: [['nombre', 'Nombre'], ['categoria', 'Categoría'], ['precio', 'Precio', money], ['disponible', 'Disponible', (v) => (v ? 'Sí' : 'No')]],
  },
  clientes: {
    titulo: 'Clientes', api: api.clientes, vacio: { nombre_completo: '', correo: '', telefono: '', direccion: '' },
    campos: [['nombre_completo', 'Nombre completo'], ['correo', 'Correo', 'email'], ['telefono', 'Teléfono'], ['direccion', 'Dirección']],
    cols: [['nombre_completo', 'Nombre'], ['correo', 'Correo'], ['telefono', 'Teléfono'], ['direccion', 'Dirección']],
  },
  pagos: {
    titulo: 'Pagos', api: api.pagos, soloLectura: true,
    cols: [['id_pedido', 'Pedido'], ['monto', 'Monto', money], ['metodo_pago', 'Método'], ['estado', 'Estado']],
  },
  domicilios: {
    titulo: 'Domicilios', api: api.domicilios, soloLectura: true,
    cols: [['id_pedido', 'Pedido'], ['direccion_entrega', 'Dirección'], ['nombre_repartidor', 'Repartidor'], ['estado_envio', 'Estado']],
  },
};

export default function Admin() {
  const [tab, setTab] = useState('resumen');
  return (
    <>
      <h1>Administración</h1>
      <div className="chips">
        {[['resumen', 'Resumen'], ...Object.entries(TABS).map(([k, t]) => [k, t.titulo])].map(([k, l]) => <button key={k} className={k === tab ? 'on' : ''} onClick={() => setTab(k)}>{l}</button>)}
      </div>
      {tab === 'resumen' ? <Resumen /> : <Tabla key={tab} cfg={TABS[tab]} />}
    </>
  );
}

function Resumen() {
  const [d, setD] = useState(null);
  useEffect(() => {
    Promise.allSettled([api.productos.list(), api.clientes.list(), api.pagos.list(), api.domicilios.list()])
      .then((r) => setD(r.map((x) => (x.status === 'fulfilled' ? x.value : []))));
  }, []);
  if (!d) return <p className="muted">Cargando…</p>;
  const [pr, cl, pa, dom] = d;
  const stats = [[pr.length, 'productos en la carta'], [pr.filter((p) => p.disponible).length, 'disponibles'], [cl.length, 'clientes'],
    [pa.length, 'pedidos'], [dom.length, 'domicilios'], [money(pa.reduce((s, p) => s + p.monto, 0)), 'vendido']];
  return <div className="stats">{stats.map(([v, l]) => <div key={l}><b>{v}</b><span>{l}</span></div>)}</div>;
}

function Tabla({ cfg }) {
  const [rows, setRows] = useState(null);
  const [form, setForm] = useState(null); // null = cerrado; {id?, ...campos}
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  async function sembrar() {
    setError(''); setBusy(true);
    for (const p of SEMILLA) {
      try { await api.productos.create(p); } catch (e) { if (!/ya se encuentra/.test(e.message)) { setError(e.message); break; } }
    }
    setBusy(false); cargar();
  }

  const cargar = () => cfg.api.list().then(setRows).catch((e) => setError(e.message));
  useEffect(() => { cargar(); }, []);

  async function guardar(e) {
    e.preventDefault();
    setError('');
    const { id, ...datos } = form;
    if ('precio' in datos) datos.precio = parseFloat(datos.precio);
    try {
      await (id ? cfg.api.update(id, datos) : cfg.api.create(datos));
      setForm(null);
      cargar();
    } catch (err) { setError(err.message); }
  }

  async function borrar(r) {
    if (!confirm(`¿Eliminar "${r[cfg.cols[0][0]]}"? No se puede deshacer.`)) return;
    try { await cfg.api.remove(r.id); cargar(); } catch (err) { setError(err.message); }
  }

  return (
    <section>
      {error && <p className="error" role="alert">{error}</p>}
      {!cfg.soloLectura && !form && <button className="primary" onClick={() => setForm({ ...cfg.vacio })}>Nuevo</button>}
      {cfg.semilla && !form && <button className="seed" disabled={busy} onClick={sembrar}>{busy ? 'Cargando…' : 'Cargar carta de ejemplo'}</button>}
      {form && (
        <form className="panel" onSubmit={guardar}>
          <h2>{form.id ? 'Editar' : 'Nuevo'}</h2>
          {cfg.campos.map(([k, l, t = 'text']) => t === 'checkbox' ? (
            <label key={k} className="check"><input type="checkbox" checked={form[k]} onChange={(e) => setForm({ ...form, [k]: e.target.checked })} />{l}</label>
          ) : (
            <label key={k}>{l}<input required type={t} min={t === 'number' ? 0 : undefined} value={form[k]} onChange={(e) => setForm({ ...form, [k]: e.target.value })} /></label>
          ))}
          <div className="row"><button className="primary">Guardar</button><button type="button" onClick={() => setForm(null)}>Cancelar</button></div>
        </form>
      )}
      {!rows && !error && <p className="muted">Cargando…</p>}
      {rows?.length === 0 && <p className="muted">No hay registros todavía.</p>}
      {rows?.length > 0 && (
        <div className="scroll">
          <table>
            <thead><tr>{cfg.cols.map(([, l]) => <th key={l}>{l}</th>)}{!cfg.soloLectura && <th />}</tr></thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.id}>
                  {cfg.cols.map(([k, , fmt = (v) => v]) => <td key={k}>{fmt(r[k])}</td>)}
                  {!cfg.soloLectura && <td className="acts"><button onClick={() => setForm({ ...r })}>Editar</button><button onClick={() => borrar(r)}>Eliminar</button></td>}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
