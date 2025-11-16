// stores/useAuth.js
import { defineStore } from '#imports'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,       // JWT access token
    user: null,        // Full user object including role
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.user?.role ?? null,
  },

  actions: {
    // Initialize auth from localStorage
    initFromStorage() {
      try {
        const data = localStorage.getItem('auth')
        if (data) {
          const { token, user } = JSON.parse(data)
          this.token = token
          this.user = user
        }
      } catch (err) {
        console.error('Failed to read auth from storage', err)
      }
    },

    // Persist token + user in localStorage
    persist() {
      try {
        localStorage.setItem('auth', JSON.stringify({ token: this.token, user: this.user }))
      } catch (err) {
        console.error('Failed to persist auth to storage', err)
      }
    },

    // Clear localStorage
    clearPersist() {
      try {
        localStorage.removeItem('auth')
      } catch (err) {}
    },

    // Login action
    async login(credentials) {
      try {
        // Step 1: call backend login endpoint
        const loginUrl = 'http://127.0.0.1:8000/api/token/'  // JWT token endpoint
        const res = await fetch(loginUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(credentials)
        })
        const data = await res.json().catch(() => null)
        if (!res.ok) {
          throw new Error(data?.detail || `Login failed (${res.status})`)
        }

        // Step 2: extract access token
        const token = data?.access ?? null
        if (!token) throw new Error('Login response missing access token')
        this.token = token

        // Step 3: fetch user info from /me/
        const meRes = await fetch('http://127.0.0.1:8000/api/me/', {
          headers: { 'Authorization': `Bearer ${this.token}` }
        })
        if (!meRes.ok) {
          const errBody = await meRes.text().catch(() => '')
          throw new Error(`Failed to fetch user profile (${meRes.status}) ${errBody}`)
        }
        const user = await meRes.json()
        this.user = user

        // Step 4: save to localStorage
        this.persist()

        return user
      } catch (err) {
        throw err
      }
    },

    // Register new user (role automatically set to 'user' in backend)
    async register(payload) {
      const url = 'http://127.0.0.1:8000/api/register/'
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (!res.ok) throw new Error('Registration failed')
      const data = await res.json()
      return data
    },

    // Logout action
    logout() {
      this.token = null
      this.user = null
      this.clearPersist()
    },

    // Manually set token + user (optional, e.g., after refresh)
    setTokenAndUser(token, user) {
      this.token = token
      this.user = user
      this.persist()
    },

    // Check if user has a specific role
    hasRole(role) {
      if (!this.user) return false
      if (Array.isArray(role)) return role.includes(this.user.role)
      return this.user.role === role
    }
  }
})
