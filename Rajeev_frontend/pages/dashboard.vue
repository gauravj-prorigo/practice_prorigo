<template>
  <div class="dashboard-page">
    <div class="dashboard-content">
      <Manegerdashboard v-if="auth.hasRole('maneger')"/>
      <AdminDashboard v-else-if="auth.hasRole('admin')" />
      <EmployeeDashboard v-else-if="auth.hasRole('employee')" />
      <UserDashboard v-else-if="auth.hasRole('user')" />
      <div v-else class="unknown-role">
        <div class="unknown-content">
          <svg class="warning-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <h2>Unknown Role</h2>
          <p>Your account has an unrecognized role. Please contact the system administrator.</p>
          <button class="btn btn-primary" @click="logout">Return to Login</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '#imports'
import AdminDashboard from '~/components/AdminDashboard.vue'
import EmployeeDashboard from '~/components/EmployeeDashboard.vue'
import UserDashboard from '~/components/UserDashboard.vue'
import Manegerdashboard from '~/components/Manegerdashboard.vue'

const auth = useAuthStore()

function logout() {
  auth.logout()
}
</script>

<style scoped>
.dashboard-page {
  min-height: calc(100vh - 200px);
}

.dashboard-content {
  height: 100%;
}

/* Unknown Role State */
.unknown-role {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 2rem;
}

.unknown-content {
  text-align: center;
  max-width: 400px;
  padding: 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 
    0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.warning-icon {
  width: 4rem;
  height: 4rem;
  color: #f59e0b;
  margin: 0 auto 1.5rem;
}

.unknown-content h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 1rem 0;
}

.unknown-content p {
  color: #64748b;
  line-height: 1.6;
  margin: 0 0 1.5rem 0;
}

/* Button Styles */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  text-decoration: none;
  line-height: 1;
  white-space: nowrap;
}

.btn:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
}

/* Animation for smooth transitions */
.dashboard-content > * {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .unknown-role {
    padding: 1rem;
  }
  
  .unknown-content {
    padding: 1.5rem;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .unknown-content {
    background: #1e293b;
    border-color: #334155;
  }
  
  .unknown-content h2 {
    color: #f1f5f9;
  }
  
  .unknown-content p {
    color: #94a3b8;
  }
}
</style>