<template>
  <div class="page">
    <h1> Contact Page</h1>
    <p>Feel free to reach out via this page!</p>

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
