<template>
  <form @submit.prevent="add">
    <input v-model="title" placeholder="New task..." />
    <button type="submit">Add</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useTasksStore } from '~/stores/tasks'
const store = useTasksStore()
const config = useRuntimeConfig()
const title = ref('')

const add = async () => {
  const t = title.value.trim()
  if (!t) return
  await store.addTask(config.public.apiBase, t)
  title.value = ''
}
</script>

<style scoped>
input{ padding:.5rem; border-radius:8px; border:1px solid #ddd; width:70% }
button{ padding:.5rem; border-radius:8px; background:#667eea; color:#fff; border:none }
</style>
