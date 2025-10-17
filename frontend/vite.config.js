import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // Zeabur 使用根路径，CloudBase 使用 /lead-management/
  base: process.env.VITE_DEPLOY_TARGET === 'cloudbase' ? '/lead-management/' : '/',
  server: {
    port: 3002,
    open: true,
    proxy: {
      '/api': {
        target: 'http://localhost:5002',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})


