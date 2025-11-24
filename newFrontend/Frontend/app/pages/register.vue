<template>
    <div class="main-container">
        <div class="main">
            <form @submit.prevent="register" class="form">
                <label for="username" class="username">Username</label>
                <input type="text" class="username" id="username" v-model="form.username" required />
                <label for="password" class="password">Password</label>
                <input type="password" class="password" id="password" v-model="form.password" required />
                <label for="email" class="email">Email</label>
                <input type="email" class="email" id="email" v-model="form.email" required />
                <button type="submit" class="btn">Register</button>
                <nuxt-link to="/" class="register">Login</nuxt-link>
            </form>
        </div>
    </div>
</template>

<script setup>
import { reactive } from 'vue';
import { useAuthStore } from '~/stores/Authostore';
import { useRouter } from 'vue-router';
const authstore = useAuthStore();
const router = useRouter();
const form = reactive({
    username: '',
    password: '',
    email: ''
})

async function register() {
    console.log("Registering user with data:", form);
    try {
        const respose = await authstore.register(form);
        await authstore.login({ username: form.username, password: form.password });
        console.log("Registration and login successful:", respose);
        router.push('/dashboard');
    } catch (error) {
        console.log("Registration failed:", error);
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