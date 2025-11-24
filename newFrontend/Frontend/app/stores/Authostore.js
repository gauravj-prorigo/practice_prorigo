import { defineStore } from "pinia";
export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    user: null,
    token: null,
    role: null,
  }),

  actions: {
    async login(data) {
      const loginUrl = 'http://127.0.0.1:8000/api/token/';
      try {
        const response = await fetch(loginUrl, {
          method: 'POST',
          headers: { 'content-Type': 'application/json' },
          body: JSON.stringify(data)
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const result = await response.json();
        this.isAuthenticated = true;
        this.token = result.access;
        console.log('Login successful:', result);

        const userResponse = await fetch('http://127.0.0.1:8000/api/me/', {
          headers: { 'Authorization': `Bearer ${this.token}` }
        })
        if (!userResponse.ok) {
          throw new Error('Failed to fetch user data');
        }
        const ans = await userResponse.json();
        console.log('User data fetched:', ans);
        this.user = ans;
        this.role = ans.role;
          this.persist();
        return ans;
      } catch (error) {
        console.error('Error during login:', error);
      }
    },
    persist() {
      console.log('Persisting auth state to localStorage');
      try {
        localStorage.setItem('auth', JSON.stringify({ user: this.user, token: this.token, isAuthenticated: this.isAuthenticated }))
      } catch (error) {
        console.error('Error persisting auth state:', error);
      }
    },

       async register(payload) {
      const url = 'http://127.0.0.1:8000/register/'
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (!res.ok) throw new Error('Registration failed')
      const data = await res.json()
      return data
    },
    logout() {
      this.isAuthenticated = false;
      this.user = null;
      this.token = null;
      this.role = null;
      localStorage.removeItem('auth');
      console.log('User logged out, auth state cleared');
    }
  }
});