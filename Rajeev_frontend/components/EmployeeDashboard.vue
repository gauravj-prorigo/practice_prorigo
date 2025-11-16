<template>
  <section class="employee-dashboard">
    <div class="dashboard-grid">
      <!-- Profile Section -->
      <div class="profile-section">
        <div class="profile-card">
          <div class="profile-header">
            <div class="profile-avatar">
              {{ getInitials(auth.user.username) }}
            </div>
            <div class="profile-info">
              <h2 class="profile-name">{{ auth.user.username }}</h2>
              <span class="profile-role">{{ auth.user.role }}</span>
            </div>
          </div>
          
          <div class="profile-details">
            <div class="detail-item">
              <span class="detail-label">Username:</span>
              <span class="detail-value">{{ auth.user.username }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Email:</span>
              <span class="detail-value">{{ auth.user.email }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Role:</span>
              <span class="role-badge">{{ auth.user.role }}</span>
            </div>
          </div>
        </div>
        
        <!-- Quick Actions -->
        <div class="quick-actions">
          <button class="action-btn primary" @click="showBlogForm = true">
            <span class="action-icon">✏️</span>
            <span class="action-text">Create New Post</span>
          </button>
          <button class="action-btn" @click="fetchBlogs">
            <span class="action-icon">🔄</span>
            <span class="action-text">Refresh Posts</span>
          </button>
          <button class="action-btn" @click="viewMyStats">
            <span class="action-icon">📊</span>
            <span class="action-text">My Stats</span>
          </button>
        </div>

        <!-- Quick Stats -->
        <div class="quick-stats">
          <div class="stat-card">
            <div class="stat-icon">📝</div>
            <div class="stat-info">
              <div class="stat-number">{{ myBlogsCount }}</div>
              <div class="stat-label">My Posts</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📅</div>
            <div class="stat-info">
              <div class="stat-number">{{ recentPostsCount }}</div>
              <div class="stat-label">This Week</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="main-content">
        <!-- Header -->
        <div class="content-header">
          <h2 class="section-title">My Blog Posts</h2>
          <div class="filter-options">
            <select v-model="filterStatus" class="filter-select">
              <option value="all">All Posts</option>
              <option value="published">Published</option>
              <option value="draft">Drafts</option>
            </select>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading your posts...</p>
        </div>

        <!-- Blog Posts -->
        <div v-else class="blog-posts">
          <div v-if="filteredBlogs.length === 0" class="empty-state">
            <div class="empty-icon">📝</div>
            <h3>No posts yet</h3>
            <p>Start by creating your first blog post!</p>
            <button class="btn btn-primary" @click="showBlogForm = true">
              Create Your First Post
            </button>
          </div>

          <div v-else class="posts-grid">
            <div v-for="blog in filteredBlogs" :key="blog.id" class="blog-card">
              <div class="blog-header">
                <h3 class="blog-title">{{ blog.title }}</h3>
                <span class="blog-status" :class="blog.status || 'published'">
                  {{ blog.status || 'published' }}
                </span>
              </div>
              
              <div class="blog-content">
                <p class="blog-excerpt">{{ getExcerpt(blog.content) }}</p>
                <div class="blog-meta">
                  <span class="blog-date">{{ formatDate(blog.created_at) }}</span>
                  <span class="blog-views" v-if="blog.views">👁️ {{ blog.views }} views</span>
                </div>
              </div>

              <div class="blog-actions">
                <button class="btn btn-sm btn-edit" @click="editBlog(blog)">
                  ✏️ Edit
                </button>
                <button class="btn btn-sm btn-view" @click="viewBlog(blog)">
                  👁️ View
                </button>
                <button class="btn btn-sm btn-delete" @click="deleteBlog(blog)">
                  🗑️ Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Blog Form Modal -->
    <BlogForm 
      v-if="showBlogForm" 
      :blog="editingBlog"
      @close="closeBlogForm" 
      @saved="onBlogSaved"
    />
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '#imports'
import BlogForm from './BlogForm.vue'

const showBlogForm = ref(false)
const editingBlog = ref(null)
const auth = useAuthStore()
const API_BASE = 'http://127.0.0.1:8000'

const blogs = ref([])
const loading = ref(false)
const filterStatus = ref('all')

onMounted(() => { 
  fetchBlogs() 
})

// Computed properties
const myBlogsCount = computed(() => blogs.value.length)
const recentPostsCount = computed(() => {
  const oneWeekAgo = new Date()
  oneWeekAgo.setDate(oneWeekAgo.getDate() - 7)
  return blogs.value.filter(blog => new Date(blog.created_at) > oneWeekAgo).length
})

const filteredBlogs = computed(() => {
  if (filterStatus.value === 'all') return blogs.value
  return blogs.value.filter(blog => (blog.status || 'published') === filterStatus.value)
})

async function fetchBlogs() {
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/api/blogs/`, { 
      headers: { Authorization: `Bearer ${auth.token}` } 
    })
    const allBlogs = await res.json()
    // Filter to show only current user's blogs for employee dashboard
    blogs.value = allBlogs.filter(blog => blog.author?.id === auth.user.id)
  } catch (e) { 
    console.error('Failed to fetch blogs:', e) 
  } finally { 
    loading.value = false 
  }
}

function editBlog(blog) {
  editingBlog.value = { ...blog }
  showBlogForm.value = true
}

function viewBlog(blog) {
  // Navigate to blog view page or open in modal
  console.log('View blog:', blog)
  // You can implement navigation: router.push(`/blogs/${blog.id}`)
}

async function deleteBlog(blog) {
  if (!confirm('Are you sure you want to delete this post?')) return
  
  try {
    await fetch(`${API_BASE}/api/blogs/${blog.id}/`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    await fetchBlogs() // Refresh the list
  } catch (e) {
    console.error('Failed to delete blog:', e)
  }
}

function viewMyStats() {
  // Implement stats view
  console.log('View my stats')
  alert(`Your Blog Stats:\n\nTotal Posts: ${myBlogsCount.value}\nPosts This Week: ${recentPostsCount.value}`)
}

function closeBlogForm() {
  showBlogForm.value = false
  editingBlog.value = null
}

function onBlogSaved() {
  closeBlogForm()
  fetchBlogs()
}

function getExcerpt(content, length = 120) {
  if (!content) return 'No content'
  return content.length > length ? content.substring(0, length) + '...' : content
}

function formatDate(dateString) {
  if (!dateString) return 'Unknown date'
  const options = { year: 'numeric', month: 'short', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

function getInitials(username) {
  if (!username) return '??'
  return username
    .split(' ')
    .map(name => name.charAt(0))
    .join('')
    .toUpperCase()
    .substring(0, 2)
}
</script>

<style scoped>
.employee-dashboard {
  padding: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
  min-height: 100vh;
  background: #f8fafc;
}

/* Main Grid Layout */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: 380px 1fr;
  }
}

/* Profile Section */
.profile-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.profile-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.profile-header {
  padding: 1.75rem;
  background: linear-gradient(135deg, #0f0f0f 0%, #14222f 100%);
  color: white;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.profile-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.375rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 1.375rem;
  font-weight: 700;
  margin: 0 0 0.375rem 0;
}

.profile-role {
  font-size: 0.875rem;
  background: rgba(255, 255, 255, 0.15);
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  text-transform: capitalize;
}

.profile-details {
  padding: 1.75rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid #f1f5f9;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.detail-value {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.95rem;
}

.role-badge {
  background: #f1f5f9;
  color: #475569;
  padding: 0.375rem 1rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
}

/* Quick Actions */
.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  width: 100%;
}

.action-btn:hover {
  background: #f8fafc;
  border-color: #3b82f6;
  transform: translateY(-1px);
}

.action-btn.primary {
  background: linear-gradient(135deg, #3f4959 0%, #182855 100%);
  color: white;
  border: none;
}

.action-btn.primary:hover {
  background: linear-gradient(135deg, #292c33 0%, #0b0e17 100%);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.action-icon {
  font-size: 1.25rem;
  width: 24px;
  text-align: center;
}

.action-text {
  font-weight: 600;
  font-size: 0.95rem;
}

/* Quick Stats */
.quick-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 1rem;
  border: 1px solid #f1f5f9;
}

.stat-icon {
  font-size: 1.5rem;
  opacity: 0.8;
}

.stat-info {
  flex: 1;
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
  margin-top: 0.25rem;
}

/* Main Content */
.main-content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  overflow: hidden;
  min-height: 600px;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #f1f5f9;
  background: #fafbfc;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.filter-options {
  display: flex;
  gap: 1rem;
}

.filter-select {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;
  background: white;
  cursor: pointer;
}

/* Blog Posts */
.blog-posts {
  padding: 1.5rem;
}

.posts-grid {
  display: grid;
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .posts-grid {
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  }
}

.blog-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
}

.blog-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.blog-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.blog-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
  flex: 1;
  margin-right: 1rem;
}

.blog-status {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.blog-status.published {
  background: #f0fdf4;
  color: #059669;
}

.blog-status.draft {
  background: #fffbeb;
  color: #d97706;
}

.blog-content {
  margin-bottom: 1.5rem;
}

.blog-excerpt {
  color: #64748b;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.blog-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  color: #94a3b8;
}

.blog-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  gap: 0.5rem;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.75rem;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-edit {
  background: #f0f9ff;
  color: #0369a1;
  border: 1px solid #bae6fd;
}

.btn-edit:hover {
  background: #e0f2fe;
}

.btn-view {
  background: #f8fafc;
  color: #475569;
  border: 1px solid #e2e8f0;
}

.btn-view:hover {
  background: #f1f5f9;
}

.btn-delete {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.btn-delete:hover {
  background: #fee2e2;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  color: #64748b;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid transparent;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #64748b;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  color: #475569;
}

.empty-state p {
  margin: 0 0 1.5rem 0;
}

/* Responsive */
@media (max-width: 768px) {
  .employee-dashboard {
    padding: 1rem;
  }
  
  .content-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .filter-options {
    justify-content: flex-start;
  }
  
  .blog-header {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .blog-actions {
    justify-content: stretch;
  }
  
  .blog-actions .btn {
    flex: 1;
  }
  
  .quick-stats {
    grid-template-columns: 1fr;
  }
}
</style>