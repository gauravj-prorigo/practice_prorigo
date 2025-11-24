<template>
    <div class="main-container">
        <div class="main">
            <form v-on:submit.prevent="submit" class="form">
                <label for="username" class="username">Username</label>
                <input type="text" class="username" id="username" v-model="form.username" required />
                <label for="password" class="password">Password</label>
                <input type="password" class="password" id="password" v-model="form.password" required />
                <button type="submit" class="btn">Submit</button>
                <nuxt-link to="/register" class="register">Register</nuxt-link>
            </form>
        </div>


    </div>
</template>

<script setup>
import { useAuthStore } from '../stores/Authostore';
import { reactive } from 'vue'
import { useRouter } from 'vue-router';
const form = reactive({
    username: '',
    password: ''
})
const authStore = useAuthStore();
const router = useRouter();

async function submit() {
    try {
        const response = await authStore.login(form);
        console.log("the response", response);

        if (!authStore.isAuthenticated) {
            alert("Invalid credentials");
            return;
        }
        router.push('/dashboard');
    } catch (error) {
        console.log("the error", error);
    }
}
</script>

<style scoped>
.main-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
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

.form {
    display: flex;
    flex-direction: column;
    width: 300px;
}

.username,
.password {
    margin-bottom: 10px;
}

input {
    padding: 10px 12px;
    border-radius: 8px;
    border: 1px solid #d6e6fb;
    background: #fbfdff;
    font-size: 0.95rem;
    outline: none;
}

.btn {
    cursor: pointer;
    margin-top: 10px;
    padding: 10px 12px;
    border-radius: 8px;
}
.register {
    margin-top: 15px;
    text-align: center;
    color: #3498db;
    text-decoration: none;
}
</style>