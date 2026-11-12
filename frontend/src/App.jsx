import { useEffect, useState } from 'react';
import { setToken, setOnUnauthorized } from './api';
import Menu from './Menu.jsx';
import Auth from './Auth.jsx';
import Admin from './Admin.jsx';

export default function App() {
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem('user') || 'null'));
  const [view, setView] = useState('menu');
  const [cart, setCart] = useState({});

  const login = (u) => { localStorage.setItem('user', JSON.stringify(u)); setUser(u); setView('menu'); };
  const logout = () => { setToken(''); localStorage.removeItem('user'); setUser(null); setView('menu'); };
  useEffect(() => { setOnUnauthorized(logout); }, []);

  const isAdmin = user?.rol === 'ROLE_ADMIN';
  const count = Object.values(cart).reduce((s, i) => s + i.n, 0);

  return (
    <>
      <header className="top">
        <button className="brand" onClick={() => setView('menu')}>Restaurante y Cafetería</button>
        <nav>
          <button className={view === 'menu' ? 'on' : ''} onClick={() => setView('menu')}>
            Carta{count > 0 && <span className="badge">{count}</span>}
          </button>
          {isAdmin && <button className={view === 'admin' ? 'on' : ''} onClick={() => setView('admin')}>Administración</button>}
          {user ? (
            <button onClick={logout} title={user.correo}>Salir ({user.nombre_completo.split(' ')[0]})</button>
          ) : (
            <button className={view === 'login' ? 'on' : ''} onClick={() => setView('login')}>Ingresar</button>
          )}
        </nav>
      </header>
      <main>
        {view === 'menu' && <Menu user={user} cart={cart} setCart={setCart} goLogin={() => setView('login')} isAdmin={isAdmin} goAdmin={() => setView('admin')} />}
        {view === 'login' && <Auth onLogin={login} />}
        {view === 'admin' && isAdmin && <Admin />}
      </main>
    </>
  );
}
