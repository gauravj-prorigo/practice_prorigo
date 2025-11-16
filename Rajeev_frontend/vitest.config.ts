// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'happy-dom', // ALWAYS uses happy-dom
    include: ['test/**/*.test.*', 'test/**/*.spec.*'],
    testTimeout: 10000
  }
})
