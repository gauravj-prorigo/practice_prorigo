<template>
    <div class="dashboard-container">
        <h1>Welcome to the Dashboard</h1>
        <p>This is a protected area of the application.</p>
        <button class="btn" @click="logout">Logout</button>
        <div class="mains">
            <div class="main">
                <admin v-if="store.role === 'admin'" />
                <manager v-else-if="store.role === 'manager'" />
                <employee v-else-if="store.role === 'employee'" />
                <user v-else-if="store.role === 'user'" />
            </div>
        </div>

    </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/Authostore';
import { useRouter } from 'vue-router';
const store = useAuthStore();
const router = useRouter();

function logout() {
    store.logout();
  router.push('/');
}
</script>

<style scoped>
.dashboard-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    /* justify-content: center; */
    height: 100vh;
    text-align: center;
}

.mains {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 2px solid #d6e6fb;
    border-radius: 12px;
    padding: 40px;
}

.btn{
      cursor: pointer;
    margin-top: 10px;
    padding: 10px 12px;
    border-radius: 8px; 
}
</style>