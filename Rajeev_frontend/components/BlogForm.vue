<template>
  <div class="overlay" @keydown.esc="onCancel" tabindex="-1">
    <form @submit.prevent="submit" class="blog-form" role="dialog" aria-modal="true">
      <input v-model="title" placeholder="Title" />
      <textarea v-model="content" rows="6" placeholder="Content"></textarea>

      <div class="controls">
        <button type="button" class="btn-cancel" @click="onCancel">Cancel</button>
        <button type="submit" class="btn-primary">Publish</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useBlogStore } from '~/stores/blogs'

const emit = defineEmits(['close', 'created'])
const store = useBlogStore()
const config = useRuntimeConfig()

// local fields
const title = ref('')
const content = ref('')

// submit handler: create new blog
const submit = async () => {
  const t = title.value.trim()
  const c = content.value.trim()
  if (!t || !c) {
    alert('Please provide title and content')
    return
  }

  try {
    // create via store (store should push created blog into its blogs list)
    const created = await store.addBlog(config.public.apiBase, t, c)
    // clear local fields
    title.value = ''
    content.value = ''
    // emit created (parent can react if needed)
    emit('created', created ?? null)
    // tell parent to close the modal
    emit('close')
  } catch (err) {
    console.error('submit error', err)
    alert('Failed to create post')
  }
}

// cancel handler
const onCancel = () => {
  // clear inputs (optional)
  title.value = ''
  content.value = ''
  emit('close')
}
</script>

<style scoped>
/* same styling as you had */
.overlay { position: fixed; top:0; left:0; right:0; bottom:0; background: rgba(0,0,0,0.5); display:flex; align-items:center; justify-content:center; z-index:1000; }
.blog-form { background: white; max-width: 600px; width: 90%; margin: 20px; padding: 24px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
input, textarea { width:100%; padding:12px; border:1px solid #ccc; border-radius:4px; margin-bottom:16px; box-sizing:border-box; font-family:inherit; font-size:14px; }
.controls { display:flex; justify-content:flex-end; gap:12px; }
.btn-primary { background:#2563eb; color:#fff; padding:10px 20px; border-radius:4px; border:none; cursor:pointer; }
.btn-cancel { background:#6b7280; color:#fff; padding:10px 20px; border-radius:4px; border:none; cursor:pointer; }
</style>
