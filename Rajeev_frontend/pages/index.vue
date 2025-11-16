<template>
  <div class="auth-page" :key="route.fullPath">
    <div class="auth-card" role="region" aria-labelledby="login-title">
      <h1 id="login-title">Login</h1>

      <p v-if="infoMessage" class="info">{{ infoMessage }}</p>

      <form @submit.prevent="onSubmit" class="form" novalidate>
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="form.username"
            autocomplete="username"
            placeholder="Username"
            required
            :class="{ invalid: fieldErrors.username }"
            @blur="validateField('username')
            "
          />
          <p v-if="fieldErrors.username" class="field-error">{{ fieldErrors.username }}</p>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            type="password"
            placeholder="Password"
            v-model="form.password"
            autocomplete="current-password"
            required
            minlength="6"
            :class="{ invalid: fieldErrors.password }"
            @blur="validateField('password')"
          />
          <p v-if="fieldErrors.password" class="field-error">{{ fieldErrors.password }}</p>
        </div>

        <button type="submit" :disabled="loading" class="btn-primary" aria-busy="loading">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>

        <p class="server-error" v-if="error">{{ error }}</p>
      </form>

      <p class="switch-text">
        Don’t have an account?
        <NuxtLink to="/register">Register</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter, useRoute } from '#imports'
import { useAuthStore } from '#imports'
definePageMeta({
  layout: 'public'
  // No middleware needed - handled globally
})
const auth = useAuthStore()
if (process.client && typeof auth.initFromStorage === 'function') {
  auth.initFromStorage()
}

const router = useRouter()
const route = useRoute()

const form = reactive({ username: '', password: '' })
const loading = ref(false)
const error = ref(null)

const fieldErrors = reactive({
  username: null,
  password: null
})

const reason = computed(() => route.query.reason)
const infoMessage = computed(() => {
  if (reason.value === 'auth_required') return 'Please log in to continue.'
  return ''
})

function validateField(field) {
  fieldErrors[field] = null
  if (field === 'username' && (!form.username || form.username.trim().length < 3)) {
    fieldErrors.username = 'Enter your username (min 3 chars).'
  }
  if (field === 'password' && (!form.password )) {
    fieldErrors.password = 'Password must be at least 4 characters.'
  }
}

async function onSubmit() {
  // simple client validation
  validateField('username')
  validateField('password')
  if (fieldErrors.username || fieldErrors.password) {
    error.value = 'Please fix the highlighted fields.'
    return
  }

  loading.value = true
  error.value = null

  try {
    console.log('Logging in…')
    const user = await auth.login({ username: form.username, password: form.password })
    console.log('Login resolved, user:', user, 'store token:', auth.token)

    // sanity check: token and user present
    if (!auth.token || !auth.user) {
      throw new Error('Login succeeded but auth state not set.')
    }

    // compute next route; use navigateTo (Nuxt 3)
    const next = route.query.next ? decodeURIComponent(String(route.query.next)) : '/dashboard'
    console.log('Navigating to', next)

    // navigate and await it
    await navigateTo(next)
    console.log('Navigation complete')
  } catch (err) {
    console.error('Login error:', err)
    error.value = err?.message || err?.data?.message || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Page wrapper */
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  /* background: #c9aaf054; */
    background-image: url("https://e1.pxfuel.com/desktop-wallpaper/407/1022/desktop-wallpaper-website-backgrounds-login-page.jpg");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  padding: 24px;
  box-sizing: border-box;
}

/* Card */
.auth-card {
  width: 100%;
  max-width: 420px;
  background: #ffffff;

  border-radius: 8px;
  padding: 22px;
  box-sizing: border-box;
  border: 1px solid #e6eef8;
  box-shadow: 0 6px 18px rgba(20, 40, 80, 0.04);
}

/* Title */
h1 {
  margin: 0 0 10px;
  font-size: 1.25rem;
  color: #102a43;
  text-align: center;
}

/* Info message shown when redirected */
.info {
  margin: 0 0 12px;
  text-align: center;
  color: #276749; /* greenish */
  background: #ecfdf5;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 0.95rem;
}

/* Form */
.form { display: grid; gap: 12px; }

/* Form group */
.form-group { display: flex; flex-direction: column; gap: 6px; }

label {
  font-weight: 600;
  font-size: 0.9rem;
  color: #243b53;
}

/* Inputs */
input {
  padding: 10px 12px;
  border-radius: 6px;
  border: 1px solid #dbe9fb;
  background: #fbfdff;
  font-size: 0.95rem;
  outline: none;
  transition: border-color .12s ease, box-shadow .12s ease;
}

input:focus {
  border-color: #2b6cb0;
  box-shadow: 0 6px 14px rgba(43,108,176,0.06);
}

/* Invalid input */
.invalid {
  border-color: #e53e3e !important;
}

/* Field error */
.field-error {
  color: #e53e3e;
  font-size: 0.85rem;
  margin-top: 4px;
}

/* Primary button */
.btn-primary {
  margin-top: 4px;
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  border: none;
  font-weight: 700;
 background: rgb(72, 163, 224);
  color: white;
  cursor: pointer;
  transition: transform .12s ease, opacity .12s ease;
}

.btn-primary[disabled] {
  opacity: 0.65;
  cursor: not-allowed;
  transform: none;
}

.server-error {
  margin-top: 8px;
  color: #972a2a;
  text-align: center;
  font-weight: 600;
}

/* Footer text */
.switch-text {
  margin-top: 12px;
  text-align: center;
  color: #334e68;
  font-size: 0.95rem;
}

.switch-text a {
  color: #1f6feb;
  text-decoration: none;
  font-weight: 700;
}

/* Small screens */
@media (max-width: 420px) {
  .auth-card { padding: 16px; border-radius: 6px; }
  input { padding: 9px 10px; }
  .btn-primary { padding: 10px; border-radius: 6px; }
}
</style>