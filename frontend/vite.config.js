import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// El gateway no tiene CORS, así que en desarrollo el navegador habla con Vite
// (mismo origen) y Vite reenvía /api/* al gateway. No hay que tocar el backend.
const GATEWAY = process.env.GATEWAY_URL || 'http://localhost:8000';

export default defineConfig({
  plugins: [react()],
  server: { port: 5173, proxy: { '/api': { target: GATEWAY, changeOrigin: true } } },
  preview: { port: 5173, proxy: { '/api': { target: GATEWAY, changeOrigin: true } } },
});
