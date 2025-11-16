<template>
  <div class="task-container">
    <draggable
      v-model="tasks"
      item-key="id"
      @end="onReorder"
      class="task-list"
    >
      <template #item="{ element: task }">
        <div class="task-item" :class="{ done: task.completed }">
          <label>
            <input type="checkbox" :checked="task.completed" @change="toggle(task.id)" />
            <span>{{ task.title }}</span>
          </label>
          <button class="delete" @click="remove(task.id)">🗑</button>
        </div>
      </template>
    </draggable>

    <p v-if="!tasks.length" class="empty">No tasks yet.</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTasksStore } from '~/stores/tasks'
import draggable from 'vuedraggable'

const store = useTasksStore()
const config = useRuntimeConfig()
const tasks = computed(() => store.allTasks)

const toggle = (id) => store.toggleTask(config.public.apiBase, id)
const remove = (id) => {
  if (confirm('Delete this task?')) store.deleteTask(config.public.apiBase, id)
}
const onReorder = (event) => {
  store.reorderTasks(tasks.value)
}
</script>

<style scoped>
.task-container {
  margin-top: 1rem;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f7fafc;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.task-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.task-item.done {
  opacity: 0.6;
  text-decoration: line-through;
}

.delete {
  background: none;
  border: none;
  font-size: 1rem;
  cursor: pointer;
}

.empty {
  text-align: center;
  color: #777;
  margin-top: 1rem;
}
</style>
