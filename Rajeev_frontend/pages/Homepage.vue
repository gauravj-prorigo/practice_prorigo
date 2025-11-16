<template>
  <main class="page">
    <div class="container">
      <header class="header">
        <h1>My App — Blogs & Tasks</h1>
        
        <nav>
          <button :class="{ active: view==='blogs' }" @click="view='blogs'">Blogs</button>
          <button :class="{ active: view==='tasks' }" @click="view='tasks'">Tasks</button>
          <button @click="logout">Logout</button>
        </nav>
      </header>
      <section v-if="view==='blogs'">
     <BlogForm v-if="authStore.user === 'employee' || blogStore.currentEdit" />

        <BlogList />

        <div v-if="authStore.user === 'admin'">
        </div>
      </section>

      <section v-if="view==='tasks'">
        <TaskForm v-if="authStore.user === 'employee'" />

        <TaskList />

        <div v-if="authStore.user === 'admin'">
          <button>Edit Task</button>
          <button>Delete Task</button>

        </div>
      </section>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BlogForm from '~/components/BlogForm.vue'
import BlogList from '~/components/BlogList.vue'
import TaskForm from '~/components/TaskForm.vue'
import TaskList from '~/components/TaskList.vue'
import { useBlogStore } from '~/stores/blogs'
import { useTasksStore } from '~/stores/tasks'
import { useAuthStore } from '#imports'
import { useRouter } from '#imports'

// definePageMeta({
//     middleware: ['auth'],
// })

const view = ref('blogs')
const blogStore = useBlogStore()
const tasksStore = useTasksStore()
const authStore = useAuthStore()

authStore.initFromStorage()

const config = useRuntimeConfig()
const router = useRouter()

onMounted(() => {
  blogStore.fetchBlogs(config.public.apiBase)
  tasksStore.fetchTasks(config.public.apiBase)
  console.log("the user is" , authStore.user)
})

function logout() {
  authStore.logout()
  router.push('/')
}
</script>

<style scoped>
.page{ display:flex; justify-content:center; align-items:flex-start; min-height:100vh; background:linear-gradient(135deg,#74ABE2,#5563DE); padding:3rem 0 }
.container{ width:720px; background:white; padding:1.6rem; border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,.12) }
.header{ display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem }
nav button{ background:transparent; border:1px solid #ddd; padding:.4rem .8rem; border-radius:8px; margin-left:.4rem; cursor:pointer }
nav button.active{ background:#667eea; color:#fff; border-color:transparent }
</style>
