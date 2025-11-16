<template>
  <div class="page">
    <h1>ℹ️ About Page</h1>
    <p>This is the About page of our Nuxt.js app.</p>

    <nav>
      <NuxtLink to="/">Home</NuxtLink> |
      <NuxtLink to="/about">About</NuxtLink> |
      <NuxtLink to="/contact">Contact</NuxtLink>
    </nav>
  </div>
</template>
<script>
import auth from '~/middleware/auth';

</script>
<style scoped>
.page {
  text-align: center;
  padding: 50px;
}
</style>
