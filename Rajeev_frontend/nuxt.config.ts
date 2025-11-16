// nuxt.config.ts
export default defineNuxtConfig({
  compatibilityDate: '2025-11-06',
  modules: ['@pinia/nuxt', '@nuxt/test-utils/module'],
  runtimeConfig: {
    public: {
      apiBase: 'http://127.0.0.1:8000/api' // Django API base
    }
  },
  devtools: { enabled: true }
})
