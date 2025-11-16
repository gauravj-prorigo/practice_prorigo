<template>
    <section class="admin-dashboard">
        <div class="dashboard-grid">
            <!-- Quick Stats -->
            <div class="quick-stats">
                <div class="stat-card">
                    <div class="stat-icon">👥</div>
                    <div class="stat-info">
                        <div class="stat-number">{{ users.length }}</div>
                        <div class="stat-label">Total Users</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">👑</div>
                    <div class="stat-info">
                        <div class="stat-number">{{ adminCount }}</div>
                        <div class="stat-label">Admins</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">💼</div>
                    <div class="stat-info">
                        <div class="stat-number">{{ employeeCount }}</div>
                        <div class="stat-label">Employees</div>
                    </div>
                </div>
            </div>

            <!-- Users List -->
            <div class="users-card">
                <div class="card-header">
                    <h3 class="card-title">User Management</h3>
                    <div class="header-actions">
                        <button class="btn btn-secondary" @click="fetchUsers" :disabled="loadingUsers">
                            <span v-if="loadingUsers" class="btn-loading">
                                <span class="spinner"></span>
                            </span>
                            <span v-else>🔄 Refresh</span>
                        </button>
                        <button class="btn btn-primary" @click="showUserForm = true">
                            ➕ Add User
                        </button>
                    </div>
                </div>

                <div v-if="loadingUsers" class="loading-state">
                    <div class="spinner"></div>
                    <p>Loading users...</p>
                </div>

                <div v-else class="users-list">
                    <div class="user-item" v-for="user in users" :key="user.id">
                        <div class="user-avatar">
                            {{ getInitials(user.username) }}
                        </div>
                        <div class="user-details">
                            <div class="user-main">
                                <h4 class="user-name">{{ user.username }}</h4>
                                <span class="user-role" :class="`role-${user.role}`">
                                    {{ user.role }}
                                </span>
                            </div>
                            <div class="user-meta">
                                <span class="user-email">{{ user.email || 'No email' }}</span>
                                <span class="user-id">ID: {{ user.id }}</span>
                            </div>
                        </div>
                        <div class="user-actions">
                            <select v-model="user.role" @change="assignRole(user)" 
                                class="role-select" :class="`role-${user.role}`">
                                <option value="user">User</option>
                                <option value="employee">Employee</option>
                                <option value="admin">Admin</option>
                                 <option value="maneger">Maneger</option>
                            </select>
                            <button class="btn btn-sm btn-view" @click="viewUser(user)">
                                👁️ View
                            </button>
                            <button class="btn btn-sm btn-edit" @click="editUser(user)">
                                ✏️ Edit
                            </button>
                        </div>
                    </div>

                    <div v-if="users.length === 0" class="empty-state">
                        <div class="empty-icon">👥</div>
                        <p>No users found</p>
                        <button class="btn btn-primary" @click="fetchUsers">
                            Try Again
                        </button>
                    </div>
                </div>
            </div>

            <!-- Quick Actions -->
            <div class="actions-card">
                <h3 class="card-title">Quick Actions</h3>
                <div class="quick-actions">
                    <button class="action-btn" @click="exportUsers">
                        <span class="action-icon">📤</span>
                        <span class="action-text">Export Users</span>
                    </button>
                    <button class="action-btn" @click="sendBulkEmail">
                        <span class="action-icon">✉️</span>
                        <span class="action-text">Bulk Email</span>
                    </button>
                    <button class="action-btn" @click="showAnalytics">
                        <span class="action-icon">📊</span>
                        <span class="action-text">View Analytics</span>
                    </button>
                    <button class="action-btn" @click="managePermissions">
                        <span class="action-icon">🔐</span>
                        <span class="action-text">Permissions</span>
                    </button>
                </div>
            </div>
        </div>

        <UserModal v-if="selectedUser" :key="selectedUser.id" :user="selectedUser" @close="closeUserModal" />
    </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '#imports'
import UserModal from '../pages/usermodel.vue'

const showUserForm = ref(false)
const auth = useAuthStore()
const API_BASE = 'http://127.0.0.1:8000'

const users = ref([])
const loadingUsers = ref(false)
const selectedUser = ref(null)

// Computed properties for stats
const adminCount = computed(() => users.value.filter(u => u.role === 'admin').length)
const employeeCount = computed(() => users.value.filter(u => u.role === 'employee').length)

onMounted(() => {
    fetchUsers()
})

async function fetchUsers() {
    loadingUsers.value = true
    try {
        const res = await fetch(`${API_BASE}/api/users/`, {
            headers: { Authorization: `Bearer ${auth.token}` }
        })
        users.value = await res.json()
    } catch (e) {
        console.error('Failed to fetch users:', e)
    } finally {
        loadingUsers.value = false
    }
}

async function assignRole(user) {
    const originalRole = user.role
    try {
        await fetch(`${API_BASE}/api/users/${user.id}/role/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${auth.token}`
            },
            body: JSON.stringify({ role: user.role })
        })
        console.log(`Role updated to ${user.role} for user ${user.username}`)
    } catch (e) {
        console.error('Failed to update role:', e)
        user.role = originalRole
    }
}

function viewUser(user) {
    selectedUser.value = { ...user }
}

function editUser(user) {
    // Implement edit functionality
    console.log('Edit user:', user)
    selectedUser.value = { ...user }
}

function closeUserModal() {
    selectedUser.value = null
}

// Quick actions functions
function exportUsers() {
    console.log('Export users functionality')
    // Implement export logic
}

function sendBulkEmail() {
    console.log('Bulk email functionality')
    // Implement bulk email
}

function showAnalytics() {
    console.log('Show analytics functionality')
    // Implement analytics view
}

function managePermissions() {
    console.log('Manage permissions functionality')
    // Implement permissions management
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
.admin-dashboard {
    padding: 1rem;
    max-width: 1200px;
    margin: 0 auto;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #334155;
}

/* Dashboard Grid */
.dashboard-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
}

@media (min-width: 1024px) {
    .dashboard-grid {
        grid-template-columns: 2fr 1fr;
        grid-template-areas: 
            "stats stats"
            "users actions";
    }
    
    .quick-stats {
        grid-area: stats;
    }
    
    .users-card {
        grid-area: users;
    }
    
    .actions-card {
        grid-area: actions;
    }
}

/* Quick Stats */
.quick-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1rem;
}

.stat-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.stat-icon {
    font-size: 2rem;
    opacity: 0.8;
}

.stat-info {
    flex: 1;
}

.stat-number {
    font-size: 2rem;
    font-weight: 700;
    color: #1e293b;
    line-height: 1;
}

.stat-label {
    font-size: 0.875rem;
    color: #64748b;
    margin-top: 0.25rem;
}

/* Cards */
.users-card,
.actions-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    overflow: hidden;
    padding: 15px;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #f1f5f9;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0;
    color: #1e293b;
}

.header-actions {
    display: flex;
    gap: 0.75rem;
}

/* Users List */
.users-list {
    padding: 0;
}

.user-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid #f1f5f9;
    transition: background-color 0.2s;
}

.user-item:hover {
    background: #f8fafc;
}

.user-item:last-child {
    border-bottom: none;
}

.user-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 0.875rem;
    flex-shrink: 0;
}

.user-details {
    flex: 1;
    min-width: 0;
}

.user-main {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
}

.user-name {
    font-size: 1rem;
    font-weight: 600;
    margin: 0;
    color: #1e293b;
}

.user-role {
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.role-user {
    background: #f1f5f9;
    color: #475569;
}

.role-employee {
    background: #fffbeb;
    color: #d97706;
}

.role-admin {
    background: #f0fdf4;
    color: #059669;
}

.user-meta {
    display: flex;
    gap: 1rem;
    font-size: 0.875rem;
    color: #64748b;
}

.user-email {
    flex: 1;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.user-id {
    font-family: 'Monaco', 'Consolas', monospace;
    color: #94a3b8;
}

.user-actions {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    flex-shrink: 0;
}

/* Buttons */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.2s;
    text-decoration: none;
    gap: 0.5rem;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-primary {
    background: #3b82f6;
    color: white;
}

.btn-primary:hover:not(:disabled) {
    background: #2563eb;
}

.btn-secondary {
    background: #f1f5f9;
    color: #475569;
    border: 1px solid #e2e8f0;
}

.btn-secondary:hover:not(:disabled) {
    background: #e2e8f0;
}

.btn-sm {
    padding: 0.375rem 0.75rem;
    font-size: 0.75rem;
}

.btn-view {
    background: #f8fafc;
    color: #475569;
    border: 1px solid #e2e8f0;
}

.btn-view:hover {
    background: #e2e8f0;
}

.btn-edit {
    background: #f0f9ff;
    color: #0369a1;
    border: 1px solid #bae6fd;
}

.btn-edit:hover {
    background: #e0f2fe;
}

/* Role Select */
.role-select {
    padding: 0.375rem 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 0.75rem;
    background: white;
    cursor: pointer;
    transition: border-color 0.2s;
    min-width: 100px;
}

.role-select:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Quick Actions */
.quick-actions {
    padding: 1rem;
    display: grid;
    gap: 0.75rem;
}

.action-btn {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
    text-align: left;
    width: 100%;
}

.action-btn:hover {
    background: #f8fafc;
    border-color: #3b82f6;
    transform: translateX(4px);
}

.action-icon {
    font-size: 1.25rem;
    opacity: 0.8;
}

.action-text {
    font-weight: 500;
    color: #374151;
}

/* Loading State */
.loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    color: #64748b;
}

.spinner {
    width: 24px;
    height: 24px;
    border: 2px solid transparent;
    border-top: 2px solid #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Empty State */
.empty-state {
    padding: 3rem;
    text-align: center;
    color: #64748b;
}

.empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.5;
}

/* Responsive */
@media (max-width: 768px) {
    .admin-dashboard {
        padding: 0.5rem;
    }
    
    .user-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }
    
    .user-actions {
        width: 100%;
        justify-content: flex-end;
    }
    
    .user-meta {
        flex-direction: column;
        gap: 0.25rem;
    }
    
    .header-actions {
        flex-direction: column;
        width: 100%;
        margin-top: 1rem;
    }
    
    .card-header {
        flex-direction: column;
        align-items: flex-start;
    }
}
</style>