<template>
  <aside class="profile-dropdown" role="dialog" aria-label="User profile" v-show="visible">
    <div class="dropdown-header">
      <div class="user-info-compact">
        <div class="compact-avatar">{{ initials }}</div>
        <div class="compact-details">
          <div class="compact-name">{{ user?.username ?? '-' }}</div>
          <div :class="['compact-role', roleClass]">{{ roleLabel }}</div>
        </div>
      </div>
      <button class="close-btn" @click="close" aria-label="Close profile">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <div class="dropdown-content">
      <div class="info-row">
        <div class="info-item">
          <span class="info-label">Email</span>
          <span class="info-value">{{ user?.email ? user.email : '-' }}</span>
        </div>
      </div>
    </div>

    <div class="dropdown-actions">
      <button class="action-btn edit-btn" @click="$emit('edit', user)" :disabled="!user">
        <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
        </svg>
        Edit
      </button>
      <button class="action-btn logout-btn" @click="onLogout" :disabled="!user">
        <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
        Logout
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '#imports'
import { useRouter, useRoute } from 'vue-router'

const props = defineProps({
  visible: { type: Boolean, default: true },
  title: { type: String, default: 'Profile' }
})
const emit = defineEmits(['close', 'edit'])

// auth store
const auth = useAuthStore()
const user = computed(() => auth.user ?? null)

// initials for avatar
const initials = computed(() => {
  const name = user.value?.username || user.value?.first_name || ''
  if (!name) return '?'
  const parts = name.trim().split(/\s+/)
  if (parts.length === 1) return parts[0].slice(0,2).toUpperCase()
  return (parts[0][0] + parts[1][0]).toUpperCase()
})

// display role label and class
const roleLabel = computed(() => (user.value?.role ?? (auth.user?.is_superuser ? 'admin' : 'user')).toString())
const roleClass = computed(() => {
  const r = roleLabel.value.toLowerCase()
  return r === 'admin' ? 'role-admin' : (r === 'employee' ? 'role-employee' : 'role-user')
})

// router for logout redirect
const router = useRouter()
const route = useRoute()

function close() {
  emit('close')
}

function onLogout() {
  // logout in store
  auth.logout()

  // redirect to login page and include ?next=currentPath so user can come back after login
  const next = encodeURIComponent(route.fullPath || '/')
  router.push({ path: '/login', query: { next } })
}
</script>

<style scoped>
.profile-dropdown {
  width: 280px;
  background: #1f2937;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
  border: 1px solid #374151;
  overflow: hidden;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  color: white;
}

/* Header */
.dropdown-header {
  padding: 1rem 1rem 0.75rem;
  background: linear-gradient(135deg, #374151 0%, #4b5563 100%);
  border-bottom: 1px solid #374151;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.user-info-compact {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.compact-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.compact-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 0;
  flex: 1;
}

.compact-name {
  font-weight: 600;
  font-size: 0.95rem;
  color: white;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.compact-role {
  padding: 0.2rem 0.6rem;
  border-radius: 9999px;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: inline-block;
  width: fit-content;
}

.role-admin {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.role-employee {
  background: rgba(6, 182, 212, 0.2);
  color: #06b6d4;
  border: 1px solid rgba(6, 182, 212, 0.3);
}

.role-user {
  background: rgba(139, 92, 246, 0.2);
  color: #8b5cf6;
  border: 1px solid rgba(139, 92, 246, 0.3);
}

.close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 6px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #9ca3af;
  flex-shrink: 0;
  margin-left: 0.5rem;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
}

.close-btn svg {
  width: 16px;
  height: 16px;
}

/* Content */
.dropdown-content {
  padding: 0.75rem 1rem;
}

.info-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-label {
  font-size: 0.75rem;
  color: #9ca3af;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 0.875rem;
  color: #e5e7eb;
  font-weight: 500;
  word-break: break-all;
}

/* Actions */
.dropdown-actions {
  padding: 0.75rem 1rem;
  display: flex;
  gap: 0.5rem;
  border-top: 1px solid #374151;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.6rem 0.75rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  line-height: 1;
  white-space: nowrap;
  flex: 1;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

.edit-btn {
  background: rgba(6, 182, 212, 0.2);
  color: #06b6d4;
  border: 1px solid rgba(6, 182, 212, 0.3);
}

.edit-btn:hover:not(:disabled) {
  background: rgba(6, 182, 212, 0.3);
  transform: translateY(-1px);
}

.logout-btn {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.logout-btn:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.3);
  transform: translateY(-1px);
}

.btn-icon {
  width: 1rem;
  height: 1rem;
  flex-shrink: 0;
}

/* Small screens */
@media (max-width: 420px) {
  .profile-dropdown {
    width: 260px;
  }
  
  .dropdown-header,
  .dropdown-content,
  .dropdown-actions {
    padding-left: 0.875rem;
    padding-right: 0.875rem;
  }
}
</style>