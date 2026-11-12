import { useEffect, useMemo, useState } from 'react';
import { api, money } from './api';

const METODOS = ['EFECTIVO', 'NEQUI', 'DAVIPLATA', 'TARJETA'];
const TINTS = ['#e3efe6', '#f7e4e4', '#fbefd5', '#e2e9f5', '#efe3f3'];
const emoji = (c, n) => {
  const s = `${c} ${n}`.toLowerCase();
  if (/postre|torta|brownie|helado|arroz con leche/.test(s)) return '🍰';
  if (/fría|frío|limonada|jugo|té /.test(s)) return '🧊';
  if (/caf|tinto|capuch|chocolate|arom|caliente/.test(s)) return '☕';
  if (/desayuno|huevo|calentado|arepa|caldo/.test(s)) return '🥐';
  if (/sancocho|bandeja|plato|pechuga|almuerzo/.test(s)) return '🍽️';
  return '🍴';
};

export default function Menu({ user, cart, setCart, goLogin, isAdmin, goAdmin }) {
  const [items, setItems] = useState(null);
  const [error, setError] = useState('');
  const [cat, setCat] = useState('Todas');
  const [q, setQ] = useState('');

  useEffect(() => { api.productos.list().then(setItems).catch((e) => setError(e.message)); }, []);
  const cats = useMemo(() => [...new Set((items || []).map((p) => p.categoria))], [items]);
  const visibles = (items || []).filter((p) => (cat === 'Todas' || p.categoria === cat) && `${p.nombre} ${p.descripcion}`.toLowerCase().includes(q.toLowerCase()));

  const chg = (p, d) => setCart((c) => {
    const n = (c[p.id]?.n || 0) + d;
    const { [p.id]: _, ...resto } = c;
    return n > 0 ? { ...c, [p.id]: { p, n } } : resto;
  });

  return (
    <>
      <section className="hero">
        <h1>Carta</h1>
        <p>Elige lo que se te antoje y te lo llevamos a la puerta.</p>
        <input type="search" aria-label="Buscar en la carta" placeholder="Buscar un plato o bebida" value={q} onChange={(e) => setQ(e.target.value)} />
      </section>
      <div className="split">
        <section>
          {error && <p className="error">{error}</p>}
          {!items && !error && <p className="muted">Cargando la carta…</p>}
          {items?.length === 0 && (
            <div className="panel">
              <p><b>La carta está vacía.</b></p>
              {isAdmin
                ? <><p className="muted">Carga la carta de ejemplo o crea tus productos desde Administración.</p><button className="primary" onClick={goAdmin}>Ir a Administración</button></>
                : <p className="muted">Pronto agregaremos productos. Vuelve en un rato.</p>}
            </div>
          )}
          {cats.length > 1 && (
            <div className="chips">
              {['Todas', ...cats].map((c) => (
                <button key={c} className={c === cat ? 'on' : ''} onClick={() => setCat(c)}>
                  {c} <small>{c === 'Todas' ? items.length : items.filter((p) => p.categoria === c).length}</small>
                </button>
              ))}
            </div>
          )}
          {items?.length > 0 && visibles.length === 0 && <p className="muted">Nada coincide con tu búsqueda.</p>}
          {cats.filter((c) => visibles.some((p) => p.categoria === c)).map((c) => (
            <div key={c}>
              <h2>{c}</h2>
              <div className="grid">
                {visibles.filter((p) => p.categoria === c).map((p) => (
                  <article key={p.id} className={'card' + (p.disponible ? '' : ' off')}>
                    <div className="tile" style={{ background: TINTS[cats.indexOf(c) % TINTS.length] }} aria-hidden="true">{emoji(c, p.nombre)}</div>
                    <div className="info">
                      <b>{p.nombre}</b>
                      <p>{p.descripcion}</p>
                      <div className="buy">
                        <span className="price">{money(p.precio)}</span>
                        {!p.disponible ? <em>Agotado</em> : cart[p.id] ? (
                          <span className="qty">
                            <button aria-label={`Quitar uno de ${p.nombre}`} onClick={() => chg(p, -1)}>−</button>{cart[p.id].n}
                            <button aria-label={`Agregar uno de ${p.nombre}`} onClick={() => chg(p, 1)}>+</button>
                          </span>
                        ) : <button className="add" onClick={() => chg(p, 1)}>Agregar</button>}
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            </div>
          ))}
        </section>
        <Comanda user={user} cart={cart} setCart={setCart} goLogin={goLogin} />
      </div>
    </>
  );
}

function Comanda({ user, cart, setCart, goLogin }) {
  const lines = Object.values(cart);
  const total = lines.reduce((s, { p, n }) => s + p.precio * n, 0);
  const [dir, setDir] = useState('');
  const [metodo, setMetodo] = useState('EFECTIVO');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [hecho, setHecho] = useState(null);

  const cambiar = (id, d) => setCart((c) => {
    const n = c[id].n + d;
    const { [id]: _, ...resto } = c;
    return n > 0 ? { ...c, [id]: { ...c[id], n } } : resto;
  });

  async function pedir(e) {
    e.preventDefault();
    setError(''); setBusy(true);
    // El backend no tiene "pedidos": el id lo generamos aquí y enlaza pago y domicilio.
    const id_pedido = 'PED-' + Date.now().toString(36).toUpperCase();
    try {
      await api.pagos.create({ id_pedido, monto: total, metodo_pago: metodo, estado: metodo === 'EFECTIVO' ? 'PENDIENTE' : 'COMPLETADO' });
      await api.domicilios.create({ id_pedido, direccion_entrega: dir, nombre_repartidor: 'Por asignar', estado_envio: 'PREPARANDO' });
      setHecho({ id: id_pedido, total, dir });
      setCart({});
    } catch (err) { setError(`${err.message} (pedido ${id_pedido})`); }
    setBusy(false);
  }

  if (hecho) return (
    <aside className="ticket">
      <h2>Pedido recibido</h2>
      <p><b>{hecho.id}</b></p>
      <p>Total {money(hecho.total)}. Lo llevamos a {hecho.dir}.</p>
      <button className="primary" onClick={() => setHecho(null)}>Hacer otro pedido</button>
    </aside>
  );

  return (
    <aside className="ticket">
      <h2>Tu pedido</h2>
      {lines.length === 0 ? <p className="muted">Agrega productos de la carta para empezar.</p> : (
        <form onSubmit={pedir}>
          <ul>
            {lines.map(({ p, n }) => (
              <li key={p.id}>
                <span>{p.nombre}</span>
                <span className="qty">
                  <button type="button" aria-label={`Quitar uno de ${p.nombre}`} onClick={() => cambiar(p.id, -1)}>−</button>
                  {n}
                  <button type="button" aria-label={`Agregar uno de ${p.nombre}`} onClick={() => cambiar(p.id, 1)}>+</button>
                </span>
                <span>{money(p.precio * n)}</span>
              </li>
            ))}
          </ul>
          <p className="total"><span>Total</span><b>{money(total)}</b></p>
          {user ? (
            <>
              <label>Dirección de entrega<input required value={dir} onChange={(e) => setDir(e.target.value)} placeholder="Calle 10 # 5-20" /></label>
              <label>Método de pago
                <select value={metodo} onChange={(e) => setMetodo(e.target.value)}>{METODOS.map((m) => <option key={m}>{m}</option>)}</select>
              </label>
              {error && <p className="error" role="alert">{error}</p>}
              <button className="primary" disabled={busy}>{busy ? 'Enviando…' : `Pedir por ${money(total)}`}</button>
            </>
          ) : (
            <button type="button" className="primary" onClick={goLogin}>Ingresa para pedir</button>
          )}
        </form>
      )}
    </aside>
  );
}
