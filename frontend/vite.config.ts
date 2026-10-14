import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(import.meta.dirname, 'src')
    }
  },
  server: {
    proxy: {
      // 后端所有路由都自带 /api 前缀：/api/health、/api/docs、/api/v1/*
      // 所以这里**一条规则、不做 rewrite** 就够了。
      //
      // 两个坑，别再踩：
      // 1. 一旦 rewrite 掉 /api，后端全部 404（后端路径里就有 /api）。
      // 2. 不要用 '/api/v1' 这种更长的 key 去"覆盖" '/api'：
      //    Vite 是按声明顺序取**第一个匹配**的前缀，不是最长匹配，
      //    第二个 key 永远不会生效。要分流只能写成 '/api/v1' 在前、'/api' 在后，
      //    但这在本项目里根本不需要 —— 后端路径本身就是完整的。
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
