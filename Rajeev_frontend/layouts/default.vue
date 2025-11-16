<template>
  <div class="app-layout">
    <AppSidebar :collapsed="sidebarCollapsed" @close-sidebar="sidebarCollapsed = true" class="app-sidebar" />
    <div class="main-content">
      <AppHeader @toggle-sidebar="toggleSidebar" class="app-header" />
      <main class="page-content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppSidebar from '../pages/AppSidebar.vue'
import AppHeader from '../pages/AppHeader.vue'

const sidebarCollapsed = ref(false)

function toggleSidebar() {
  sidebarCollapsed.value = !sidebarCollapsed.value
}
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh; /* Use height instead of min-height */
  background: #f8fafc;
  overflow: hidden; /* Prevent entire page scroll */
}

.app-sidebar {
  flex: 0 0 260px;
  width: 260px;
  box-sizing: border-box;
  position: sticky;
  top: 0;
  align-self: flex-start;
  overflow-y: auto; /* Allow sidebar to scroll independently if needed */
  height: 100vh; /* Full viewport height */
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  height: 100vh; /* Full viewport height */
  overflow: hidden; /* Contain the content */
}

.app-header {
  position: sticky;
  top: 0;
  z-index: 40;
  background: white;
  flex-shrink: 0; /* Prevent header from shrinking */
}

.page-content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto; /* Only this area scrolls */
  background: #f8fafc;
  height: calc(100vh - 80px); /* Calculate height minus header */
}

@media (max-width: 768px) {
  .app-layout {
    flex-direction: column;
    height: auto; /* Allow natural height on mobile */
    min-height: 100vh;
  }

  .app-sidebar {
    width: 100%;
    flex: 0 0 auto;
    height: auto;
    position: relative;
    overflow-y: visible;
  }

  .main-content {
    height: auto;
    min-height: calc(100vh - 60px); /* Adjust for mobile */
  }

  .page-content {
    height: auto;
    min-height: calc(100vh - 140px); /* Adjust for mobile header + sidebar */
    padding: 1rem;
  }
}
</style>