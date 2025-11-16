<template>
  <header class="app-header">
    <div class="header-content">
      <div class="header-left">
        <button class="sidebar-toggle" @click="$emit('toggle-sidebar')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        <div class="header-title">
          <h1 class="title">{{ currentPageTitle }}</h1>
          <p class="subtitle">{{ currentPageSubtitle }}</p>
        </div>
      </div>

      <div class="header-actions">
        <div class="user-info">
          <div class="user-avatar-container">
            <div class="user-avatar" @click="showProfile = !showProfile">
              {{ getInitials(auth.user?.username) }}
            </div>
            <div v-if="showProfile" class="profile-dropdown">
              <Profile @close="showProfile = false" />
            </div>
          </div>
        </div>

        <button class="btn btn-logout" @click="logout">Logout</button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '#imports'
import Profile from './profile.vue'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()
const showProfile = ref(false)

const currentPageTitle = computed(() => {
  const routeName = route.name
  const titles = {
    index: 'Dashboard',
    blogs: 'Blogs',
    profile: 'Profile',
    'profile-edit': 'Edit Profile',
  }
  return titles[routeName] || 'Dashboard'
})

const currentPageSubtitle = computed(() => {
  return `Welcome back, ${auth.user?.username ?? 'User'}`
})

function logout() {
  auth.logout?.()
  router.push('/')
}

function getInitials(username) {
  if (!username) return '??'
  return username
    .split(' ')
    .map(n => n.charAt(0))
    .join('')
    .toUpperCase()
    .substring(0, 2)
}
</script>

<style scoped>
.app-header {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  position: sticky;
  top: 0;
  z-index: 40;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  max-width: 100%;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
  min-width: 0;
}

.sidebar-toggle {
  background: none;
  border: none;
  padding: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  color: #64748b;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar-toggle:hover {
  background: #f1f5f9;
  color: #374151;
}

.sidebar-toggle svg {
  width: 20px;
  height: 20px;
}

.header-title {
  min-width: 0;
}

.header-title .title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: #1f2937;
  line-height: 1.2;
}

.header-title .subtitle {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.2;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
}

.user-avatar-container {
  position: relative;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.user-avatar:hover {
  transform: scale(1.05);
}

.profile-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  z-index: 50;
}

.btn-logout {
  background: #ef4444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-logout:hover {
  background: #dc2626;
}

@media (max-width: 768px) {
  .header-content {
    padding: 1rem;
  }
  
  .header-title .title {
    font-size: 1.125rem;
  }
  
  .header-title .subtitle {
    font-size: 0.8125rem;
  }
}
</style>