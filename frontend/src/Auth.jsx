import { useState } from 'react';
import { api, setToken } from './api';

const decodificar = (tk) => JSON.parse(decodeURIComponent(escape(atob(tk.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')))));

export default function Auth({ onLogin }) {
  const [modo, setModo] = useState('login');
  const [f, setF] = useState({ nombre: '', correo: '', clave: '' });
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [tk, setTk] = useState('');
  function conToken(e) {
    e.preventDefault();
    try {
      const p = decodificar(tk.trim());
      setToken(tk.trim());
      onLogin({ id: p.sub, nombre_completo: p.correo.split('@')[0], correo: p.correo, rol: p.rol });
    } catch { setError('Ese token no es válido. Genera uno nuevo con scripts/token_admin.py.'); }
  }
  const set = (k) => (e) => setF({ ...f, [k]: e.target.value });

  async function enviar(e) {
    e.preventDefault();
    setError(''); setBusy(true);
    try {
      if (modo === 'registro') await api.registro(f.nombre, f.correo, f.clave);
      onLogin(await api.login(f.correo, f.clave));
    } catch (err) { setError(err.message); }
    setBusy(false);
  }

  return (
    <form className="panel narrow" onSubmit={enviar}>
      <h1>{modo === 'login' ? 'Ingresar' : 'Crear cuenta'}</h1>
      {modo === 'registro' && (
        <label>Nombre completo<input required value={f.nombre} onChange={set('nombre')} autoComplete="name" /></label>
      )}
      <label>Correo<input required type="email" value={f.correo} onChange={set('correo')} autoComplete="email" /></label>
      <label>Contraseña
        <input required type="password" minLength={modo === 'registro' ? 6 : 1} maxLength={72} value={f.clave} onChange={set('clave')}
          autoComplete={modo === 'login' ? 'current-password' : 'new-password'} />
      </label>
      {modo === 'registro' && <small>Entre 6 y 72 caracteres.</small>}
      {error && <p className="error" role="alert">{error}</p>}
      <button className="primary" disabled={busy}>{busy ? 'Un momento…' : modo === 'login' ? 'Ingresar' : 'Crear cuenta e ingresar'}</button>
      <button type="button" className="link" onClick={() => { setError(''); setModo(modo === 'login' ? 'registro' : 'login'); }}>
        {modo === 'login' ? '¿No tienes cuenta? Regístrate' : '¿Ya tienes cuenta? Ingresa'}
      </button>
      <details className="dev">
        <summary>Entrar con token de administrador (desarrollo)</summary>
        <label>Token JWT<input value={tk} onChange={(e) => setTk(e.target.value)} placeholder="eyJ..." /></label>
        <button type="button" onClick={conToken} disabled={!tk.trim()}>Usar token</button>
      </details>
    </form>
  );
}
