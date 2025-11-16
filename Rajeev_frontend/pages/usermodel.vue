<template>
  <div class="overlay" @click.self="emitClose">
    <div class="card">
      <button class="close-x" @click="emitClose">✕</button>

      <div class="card-content">
        <h3 class="title">User Details</h3>

        <div class="row"><strong>ID:</strong> <span>{{ user.id }}</span></div>
        <div class="row"><strong>Username:</strong> <span>{{ user.username }}</span></div>
        <div class="row"><strong>Email:</strong> <span>{{ user.email ?? '-' }}</span></div>
        <div class="row"><strong>Role:</strong> <span>{{ user.role ?? '-' }}</span></div>

        <!-- optional actions -->
        <div class="actions">
          <!-- <button class="btn" @click="onEdit">Edit</button> -->
          <button class="btn-ghost" @click="emitClose">Close</button>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script setup>
const props = defineProps({
  user: { type: Object, required: true }   // parent passes an object
})
const emit = defineEmits(['close'])

function emitClose() {
  emit('close')
}

// optional: if you want to navigate to a user edit page or open an edit modal
// function onEdit() {
//   // example: $router push to user edit route (if you have one)
//   // const router = useRouter()
//   // router.push(`/users/${props.user.id}/edit`)
//   // or emit('edit', props.user)
//   alert('edit clicked for ' + props.user.username) // placeholder
// }
</script>

<style scoped>
/* backdrop */
.overlay {
  position: fixed; inset: 0; display: flex; align-items: center; justify-content: center;
  background: rgba(2,6,23,0.5); z-index: 1000; padding: 16px;
}

/* card */
.card {
  width: 100%; max-width: 460px; background: white; border-radius: 10px; box-shadow: 0 12px 40px rgba(2,6,23,0.3);
  position: relative;
  overflow: hidden;
}
.card-content { padding: 20px; }
.title { margin: 0 0 12px; font-size: 1.1rem; }
.row { display:flex; justify-content:space-between; padding:6px 0; color:#1f2937 }
.actions { display:flex; gap:8px; justify-content:flex-end; margin-top:14px; }

/* buttons */
.btn { background:#0ea5e9;color:white;padding:8px 12px;border-radius:8px;border:none;cursor:pointer }
.btn-ghost { background:transparent;border:1px solid #e6eef8;padding:8px 12px;border-radius:8px;cursor:pointer }

/* close X */
.close-x { position:absolute; top:8px; right:8px; border:none; background:transparent; font-size:18px; cursor:pointer }
</style>
