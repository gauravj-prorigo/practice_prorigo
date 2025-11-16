// stores/blogs.js
import { defineStore } from 'pinia'
import { useToast } from 'vue-toastification'
import { useAuthStore } from '#imports'

export const useBlogStore = defineStore('blog', {
  state: () => ({
    blogs: [],
    editingBlog: null
  }),
  actions: {
    // Fetch all blogs from backend and normalize author shape
    async fetchBlogs(apiBase) {
      const toast = useToast()
      const auth = useAuthStore()

      try {
        // ensure caller passes apiBase like 'http://127.0.0.1:8000/api'
        const data = await $fetch(`${apiBase}/blogs/`, {
          headers: { Authorization: `Bearer ${auth.token}` }
        })

        // normalize each blog so author becomes object { id, username? }
        this.blogs = (Array.isArray(data) ? data : []).map(b => {
          const authorValue = b?.author
          let authorObj = null
          if (authorValue === null || authorValue === undefined) {
            authorObj = null
          } else if (typeof authorValue === 'object') {
            authorObj = authorValue
          } else {
            // numeric id -> convert to object { id: <num> }
            authorObj = { id: Number(authorValue) }
          }
          return { ...b, author: authorObj }
        })
      } catch (err) {
        console.error('fetchBlogs error', err)
        toast.error('Failed to load blogs')
      }
    },

    // Create blog (backend should set author automatically)
    async addBlog(apiBase, title, content) {
      const toast = useToast()
      const auth = useAuthStore()

      try {
        const created = await $fetch(`${apiBase}/blogs/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${auth.token}`
          },
          body: JSON.stringify({ title, content })
        })

        // normalize author for the created blog too
        const authorValue = created?.author
        const authorObj = (typeof authorValue === 'object') ? authorValue : { id: Number(authorValue) }
        this.blogs.unshift({ ...created, author: authorObj })
        toast.success('Blog created')
      } catch (err) {
        console.error('addBlog error', err)
        toast.error('Failed to create blog')
      }
    },

    startEditing(blog) { this.editingBlog = { ...blog } },
    cancelEditing() { this.editingBlog = null },

    // Update blog
    async updateBlog(apiBase, id, title, content) {
      const toast = useToast()
      const auth = useAuthStore()

      try {
        const updated = await $fetch(`${apiBase}/blogs/${id}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${auth.token}`
          },
          body: JSON.stringify({ title, content })
        })

        // normalize author
        const authorValue = updated?.author
        const authorObj = (typeof authorValue === 'object') ? authorValue : { id: Number(authorValue) }

        const idx = this.blogs.findIndex(b => b.id === id)
        if (idx !== -1) this.blogs.splice(idx, 1, { ...updated, author: authorObj })
        this.editingBlog = null
        toast.success('Blog updated')
      } catch (err) {
        console.error('updateBlog error', err)
        toast.error('Failed to update blog')
      }
    },

    // Delete blog
    async deleteBlog(apiBase, id) {
      const toast = useToast()
      const auth = useAuthStore()

      try {
        await $fetch(`${apiBase}/blogs/${id}/`, {
          method: 'DELETE',
          headers: { Authorization: `Bearer ${auth.token}` }
        })
        this.blogs = this.blogs.filter(b => b.id !== id)
        toast.info('Blog deleted')
      } catch (err) {
        console.error('deleteBlog error', err)
        toast.error('Failed to delete blog')
      }
    }
  },
  getters: {
    allBlogs: (s) => s.blogs,
    currentEdit: (s) => s.editingBlog
  }
})
