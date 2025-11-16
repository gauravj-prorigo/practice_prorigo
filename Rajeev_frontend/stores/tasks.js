// stores/tasks.js
import { defineStore } from 'pinia'
import { useToast } from 'vue-toastification'

export const useTasksStore = defineStore('tasks', {
  state: () => ({
    tasks: [],
    editingTask: null
  }),

  actions: {
    // ✅ Fetch tasks from Django, completed tasks go to bottom
    async fetchTasks(apiBase) {
      const toast = useToast()
      try {
        const res = await $fetch(`${apiBase}/tasks/`)
        this.tasks = res.sort((a, b) => a.completed - b.completed) // incomplete first
      } catch (err) {
        console.error(err)
        toast.error('⚠️ Failed to load tasks')
      }
    },

    // ✅ Add a new task
    async addTask(apiBase, title) {
      const toast = useToast()
      try {
        const created = await $fetch(`${apiBase}/tasks/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title, completed: false })
        })
        this.tasks.unshift(created)
        toast.success('✅ Task added!')
      } catch (err) {
        console.error(err)
        toast.error('❌ Failed to add task')
      }
    },

    // ✅ Toggle task completion and re-sort
    async toggleTask(apiBase, id) {
      const toast = useToast()
      const task = this.tasks.find(t => t.id === id)
      if (!task) return

      try {
        const updated = await $fetch(`${apiBase}/tasks/${id}/`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            title: task.title,
            completed: !task.completed
          })
        })
        Object.assign(task, updated)
        this.sortTasks()
        toast.success('🔄 Task updated!')
      } catch (err) {
        console.error(err)
        toast.error('❌ Failed to update task')
      }
    },

    // ✅ Delete task
    async deleteTask(apiBase, id) {
      const toast = useToast()
      try {
        await $fetch(`${apiBase}/tasks/${id}/`, { method: 'DELETE' })
        this.tasks = this.tasks.filter(t => t.id !== id)
        toast.info('🗑️ Task deleted!')
      } catch (err) {
        console.error(err)
        toast.error('⚠️ Failed to delete task')
      }
    },

    reorderTasks(newOrder) {
      this.tasks = newOrder
      this.sortTasks()
    },

    sortTasks() {
      this.tasks.sort((a, b) => a.completed - b.completed)
    }
  },

  getters: {
    allTasks: (state) => state.tasks
  }
})
