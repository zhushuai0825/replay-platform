import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000, // 使用 3000 端口（更常见的开发端口）
    host: 'localhost', // 使用 localhost 避免 Windows 权限问题
    strictPort: false, // 如果端口被占用，自动尝试下一个可用端口
  },
})
