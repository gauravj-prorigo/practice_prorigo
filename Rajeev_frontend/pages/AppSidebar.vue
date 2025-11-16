<template>
    <aside :class="['app-sidebar', { collapsed }]" aria-hidden="false">
        <div class="sidebar-inner">
            <div class="brand">
                <div class="logo">📝</div>
                <div class="app-name">BlogApp</div>
            </div>

            <nav class="nav">
                <a class="nav-item" href="#/" @click.prevent="go('/dashboard')">
                    <span class="nav-icon">📊</span>
                    <span class="nav-text">Dashboard</span>
                </a>
                <a class="nav-item" href="#/blogs" @click.prevent="go('/blogs')">
                    <span class="nav-icon">📄</span>
                    <span class="nav-text">Blogs</span>
                </a>
                <a v-if="isAdmin && isemployee"  class="nav-item" @click.prevent="goToBlogs">
                    <span class="nav-icon">📄</span>
                    <span class="nav-text">Create</span>
                </a>
                <a v-if="isAdmin" class="nav-item" href="#/admin/users" @click.prevent="go('/admin/users')">
                    <span class="nav-icon">👥</span>
                    <span class="nav-text">Users</span>
                </a>
            </nav>

            <div class="sidebar-footer">
                <button class="collapse-btn" @click="toggle">
                    <span class="btn-icon">↔</span>
                    <span v-if="!collapsed" class="btn-text">Collapse</span>
                    <span v-else class="btn-text">Expand</span>
                </button>
            </div>
        </div>
    </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '#imports'

const props = defineProps({
    collapsed: {
        type: Boolean,
        default: false
    }
})

function goToBlogs() {
  router.push('/blogcreate').catch(() => {})
}

const emit = defineEmits(['update:collapsed', 'close-sidebar'])

const router = useRouter()
const auth = useAuthStore()

function go(path) {
    router.push(path)
    if (window.innerWidth <= 768) {
        emit('update:collapsed', true)
        emit('close-sidebar')
    }
}

function toggle() {
    emit('update:collapsed', !props.collapsed)
}

const isAdmin = computed(() => auth.user?.role === 'admin')
const isemployee = computed(() => auth.user?.role === 'employee')
</script>

<style scoped>
.app-sidebar {
    background: white;
    height: 100vh;
    padding: 1.25rem;
    box-sizing: border-box;
    border-right: 1px solid #e5e7eb;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: sticky;
    top: 0;
    align-self: flex-start;
    transition: all 0.3s ease;
    overflow: hidden;
}

.app-sidebar {
    width: 260px;
    flex: 0 0 260px;
}

.app-sidebar.collapsed {
    width: 80px;
    flex: 0 0 80px;
}

.app-sidebar.collapsed .nav-text,
.app-sidebar.collapsed .app-name,
.app-sidebar.collapsed .btn-text {
    display: none;
}

.sidebar-inner {
    display: flex;
    flex-direction: column;
    height: 100%;
    gap: 2rem;
}

.brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 0;
}

.logo {
    font-size: 1.5rem;
    flex-shrink: 0;
}

.app-name {
    font-weight: 600;
    font-size: 1.125rem;
    color: #1f2937;
    white-space: nowrap;
}

.nav {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    flex: 1;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    color: #374151;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
}

.nav-item:hover {
    background: #f3f4f6;
    color: #111827;
}

.nav-item:active {
    background: #e5e7eb;
}

.nav-icon {
    font-size: 1.125rem;
    width: 20px;
    text-align: center;
    flex-shrink: 0;
}

.nav-text {
    font-weight: 500;
    font-size: 0.9375rem;
}

.sidebar-footer {
    padding-top: 1rem;
    border-top: 1px solid #f3f4f6;
}

.collapse-btn {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    cursor: pointer;
    width: 100%;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: #374151;
    transition: all 0.2s;
    white-space: nowrap;
}

.collapse-btn:hover {
    background: #f1f5f9;
    border-color: #d1d5db;
}

.btn-icon {
    font-size: 1rem;
    flex-shrink: 0;
}

.btn-text {
    font-weight: 500;
    font-size: 0.875rem;
}

@media (max-width: 768px) {
    .app-sidebar {
        width: 100%;
        height: auto;
        position: relative;
        border-right: none;
        border-bottom: 1px solid #e5e7eb;
    }

    .app-sidebar.collapsed {
        width: 100%;
    }

    .app-sidebar.collapsed .nav-text,
    .app-sidebar.collapsed .app-name,
    .app-sidebar.collapsed .btn-text {
        display: block;
    }

    .nav {
        flex-direction: row;
        overflow-x: auto;
        padding-bottom: 0.5rem;
    }

    .nav-item {
        flex-shrink: 0;
    }

    .sidebar-inner {
        gap: 1rem;
    }
}
</style>