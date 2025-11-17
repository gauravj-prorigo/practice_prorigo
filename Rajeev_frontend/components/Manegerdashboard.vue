<template>
  <section class="manager-dashboard">
    <!-- Dashboard Header -->
    <div class="dashboard-header">
      <div class="header-content">
        <h1 class="dashboard-title">Manager Dashboard</h1>
        <p class="dashboard-subtitle">Manage and monitor all blog posts</p>
      </div>
      <div class="header-stats">
        <div class="stat-card">
          <div class="stat-icon">📝</div>
          <div class="stat-info">
            <div class="stat-number">{{ totalPosts }}</div>
            <div class="stat-label">Total Posts</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">👥</div>
          <div class="stat-info">
            <div class="stat-number">{{ activeAuthors }}</div>
            <div class="stat-label">Active Authors</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📊</div>
          <div class="stat-info">
            <div class="stat-number">{{ thisWeekPosts }}</div>
            <div class="stat-label">This Week</div>
          </div>
        </div>
      </div>
    </div>
 
    <!-- Quick Actions -->
    <div class="quick-actions">
      <h2 class="section-title">Quick Actions</h2>
      <div class="action-grid">
        <button class="action-btn" @click="refreshPosts">
          <span class="action-icon">🔄</span>
          <span class="action-text">Refresh Posts</span>
        </button>
        <button class="action-btn" @click="showBlogForm = true">
          <span class="action-icon">✅</span>
          <span class="action-text">Create post</span>
        </button>
        <!-- <button class="action-btn" @click="filterByStatus('draft')">
          <span class="action-icon">📄</span>
          <span class="action-text">View Drafts</span>
        </button>
        <button class="action-btn" @click="clearFilters">      <button class="btn btn-primary" @click="showBlogForm = true">
              Create Your First Post
            </button>
          <span class="action-icon">📋</span>
          <span class="action-text">View All</span>
        </button> -->
      </div>
    </div>
 
    <!-- Filters and Search -->
    <!-- <div class="filters-section">
      <div class="filter-group">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search posts..."
            class="search-input"
          >
        </div>
        <select v-model="statusFilter" class="filter-select">
          <option value="all">All Status</option>
          <option value="published">Published</option>
          <option value="draft">Draft</option>
        </select>
        <select v-model="authorFilter" class="filter-select">
          <option value="all">All Authors</option>
          <option v-for="author in uniqueAuthors" :key="author" :value="author">
            {{ author }}
          </option>
        </select>
      </div>
      <div class="results-info">
        Showing {{ filteredBlogs.length }} of {{ totalPosts }} posts
      </div>
    </div> -->
 
    <!-- Blog Posts Table -->
    <div class="blog-management">
      <div class="table-header">
        <h2 class="section-title">Blog Posts Management</h2>
      </div>
      
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading posts...</p>
      </div>
 
      <div v-else class="table-container">
        <table class="posts-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Author</th>
              <th>Status</th>
              <th>Created</th>
              <th>Last Updated</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="blog in filteredBlogs" :key="blog.id">
              <td class="post-title">
                <div class="title-content">
                  <h4 class="title-text">{{ blog.title }}</h4>
                  <p class="title-excerpt">{{ getExcerpt(blog.content) }}</p>
                </div>
              </td>
              <td class="post-author">
                <div class="author-info">
                  <span class="author-avatar">
                    {{ getInitials(blog.author?.username || 'Unknown') }}
                  </span>
                  <span class="author-name">{{ blog.author?.username || 'Unknown' }}</span>
                </div>
              </td>
              <td class="post-status">
                <span class="status-badge" :class="blog.status || 'published'">
                  {{ blog.status || 'published' }}
                </span>
              </td>
              <td class="post-date">
                {{ formatDate(blog.created_at) }}
              </td>
              <td class="post-date">
                {{ formatDate(blog.updated_at) }}
              </td>
              <!-- <td class="post-actions">
                <button class="btn btn-edit" @click="editPost(blog)" title="Edit Post">
                  ✏️ Edit
                </button>
                <button class="btn btn-view" @click="viewPost(blog)" title="View Post">
                  👁️ View
                </button>
              </td> -->
            </tr>
          </tbody>
        </table>
 
        <div v-if="filteredBlogs.length === 0" class="empty-state">
          <div class="empty-icon">📝</div>
          <h3>No posts found</h3>
          <p>No blog posts match your current filters.</p>
          <button class="btn btn-primary" @click="clearFilters">
            Clear Filters
          </button>
        </div>
      </div>
    </div>
 
    <BlogForm 
      v-if="showBlogForm" 
      :blog="editingBlog"
      @close="closeBlogForm" 
      @saved="onBlogSaved"
    />
    <!-- Edit Modal (would be implemented separately) -->
    <!-- <BlogEditor v-if="editingPost" :post="editingPost" @close="closeEditor" @saved="onPostSaved" /> -->
  </section>
</template>
 
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '#imports'
 
const auth = useAuthStore()
const API_BASE = 'http://127.0.0.1:8000'
 
const blogs = ref([])
const loading = ref(false)
const searchQuery = ref('')
const statusFilter = ref('all')
const authorFilter = ref('all')
const editingPost = ref(null)
const showBlogForm = ref(false) 
const editingBlog = ref(null)
onMounted(() => {
  fetchBlogs()
})
 


// Computed properties
const totalPosts = computed(() => blogs.value.length)
const activeAuthors = computed(() => {
  const authors = new Set(blogs.value.map(blog => blog.author?.username).filter(Boolean))
  return authors.size
})
const thisWeekPosts = computed(() => {
  const oneWeekAgo = new Date()
  oneWeekAgo.setDate(oneWeekAgo.getDate() - 7)
  return blogs.value.filter(blog => new Date(blog.created_at) > oneWeekAgo).length
})
 
const uniqueAuthors = computed(() => {
  const authors = blogs.value.map(blog => blog.author?.username).filter(Boolean)
  return [...new Set(authors)].sort()
})
 
const filteredBlogs = computed(() => {
  let filtered = blogs.value
 
  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(blog =>
      blog.title.toLowerCase().includes(query) ||
      blog.content.toLowerCase().includes(query) ||
      blog.author?.username.toLowerCase().includes(query)
    )
  }
 
  // Status filter
  if (statusFilter.value !== 'all') {
    filtered = filtered.filter(blog => (blog.status || 'published') === statusFilter.value)
  }
 
  // Author filter
  if (authorFilter.value !== 'all') {
    filtered = filtered.filter(blog => blog.author?.username === authorFilter.value)
  }
 
  return filtered
})
 
async function fetchBlogs() {
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/api/blogs/`, {
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    blogs.value = await res.json()
  } catch (error) {
    console.error('Failed to fetch blogs:', error)
  } finally {
    loading.value = false
  }
}
 
function refreshPosts() {
  fetchBlogs()
}
 

function closeBlogForm() {
  showBlogForm.value = false
  editingBlog.value = null
}

function onBlogSaved() {
  closeBlogForm()
  fetchBlogs()
}

function filterByStatus(status) {
  statusFilter.value = status
}
 
function clearFilters() {
  searchQuery.value = ''
  statusFilter.value = 'all'
  authorFilter.value = 'all'
}
 
function editPost(blog) {
  // Implement edit functionality
  console.log('Edit post:', blog)
  editingPost.value = blog
  // You would open an editor modal or navigate to edit page
}
 
function viewPost(blog) {
  // Implement view functionality
  console.log('View post:', blog)
  // Navigate to blog view: router.push(`/blogs/${blog.id}`)
}
 
function getExcerpt(content, length = 80) {
  if (!content) return 'No content'
  return content.length > length ? content.substring(0, length) + '...' : content
}
 
function formatDate(dateString) {
  if (!dateString) return '-'
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
.manager-dashboard {
  padding: 1.5rem;
  max-width: 1500px;
  margin: 0 auto;
  /* background: white; */
  min-height: 100vh;
}
 
/* Dashboard Header */
.dashboard-header {
  margin-bottom: 2rem;
}
 
.header-content {
  margin-bottom: 1.5rem;
}
 
.dashboard-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}
 
.dashboard-subtitle {
  font-size: 1.1rem;
  color: #64748b;
  margin: 0;
}
 
.header-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}
 
.stat-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
}
 
.stat-card:hover {
  border-color: #3b82f6;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
 
.stat-icon {
  font-size: 2rem;
  opacity: 0.8;
}
 
.stat-info {
  flex: 1;
}
 
.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  line-height: 1;
}
 
.stat-label {
  font-size: 0.875rem;
  color: #64748b;
  margin-top: 0.25rem;
}
 
/* Quick Actions */
.quick-actions {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}
 
.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 1rem 0;
}
 
.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 0.75rem;
}
 
.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
  color: #374151;
}
 
.action-btn:hover {
  background: #f1f5f9;
  border-color: #3b82f6;
  color: #3b82f6;
}
 
.action-icon {
  font-size: 1.125rem;
}
 
.action-text {
  font-size: 0.875rem;
  font-weight: 500;
}
 
/* Filters Section */
.filters-section {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}
 
.filter-group {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}
 
.search-box {
  display: flex;
  align-items: center;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  min-width: 250px;
}
 
.search-icon {
  color: #64748b;
  margin-right: 0.5rem;
}
 
.search-input {
  border: none;
  outline: none;
  background: transparent;
  width: 100%;
  font-size: 0.875rem;
}
 
.search-input::placeholder {
  color: #9ca3af;
}
 
.filter-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;
  background: white;
  cursor: pointer;
  min-width: 120px;
}
 
.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
}
 
.results-info {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}
 
/* Blog Management */
.blog-management {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
}
 
.table-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}
 
.table-container {
  overflow-x: auto;
}
 
.posts-table {
  width: 100%;
  border-collapse: collapse;
}
 
.posts-table th {
  background: #f8fafc;
  padding: 1rem;
  text-align: left;
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #e2e8f0;
}
 
.posts-table td {
  padding: 1rem;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: top;
}
 
.posts-table tr:last-child td {
  border-bottom: none;
}
 
.posts-table tr:hover {
  background: #f8fafc;
}
 
/* Table Cell Styles */
.post-title {
  min-width: 300px;
}
 
.title-content {
  max-width: 400px;
}
 
.title-text {
  font-size: 0.95rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  line-height: 1.3;
}
 
.title-excerpt {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
}
 
.post-author {
  min-width: 150px;
}
 
.author-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
 
.author-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #3b82f6;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
  flex-shrink: 0;
}
 
.author-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}
 
.post-status {
  min-width: 100px;
}
 
.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
 
.status-badge.published {
  background: #f0fdf4;
  color: #059669;
}
 
.status-badge.draft {
  background: #fffbeb;
  color: #d97706;
}
 
.post-date {
  min-width: 120px;
  font-size: 0.875rem;
  color: #64748b;
  white-space: nowrap;
}
 
.post-actions {
  min-width: 150px;
  white-space: nowrap;
}
 
/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 0.75rem;
  border: none;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
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
  margin-left: 0.5rem;
}
 
.btn-view:hover {
  background: #f1f5f9;
}
 
.btn-primary {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
}
 
.btn-primary:hover {
  background: #2563eb;
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
  font-size: 3rem;
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
 
/* Responsive Design */
@media (max-width: 768px) {
  .manager-dashboard {
    padding: 1rem;
  }
 
  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }
 
  .filter-group {
    flex-direction: column;
    align-items: stretch;
  }
 
  .search-box {
    min-width: auto;
  }
 
  .header-stats {
    grid-template-columns: 1fr;
  }
 
  .action-grid {
    grid-template-columns: 1fr;
  }
 
  .posts-table {
    display: block;
  }
 
  .posts-table thead {
    display: none;
  }
 
  .posts-table tbody,
  .posts-table tr,
  .posts-table td {
    display: block;
    width: 100%;
  }
 
  .posts-table tr {
    margin-bottom: 1rem;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    overflow: hidden;
  }
 
  .posts-table td {
    padding: 0.75rem;
    border-bottom: 1px solid #f1f5f9;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
 
  .posts-table td:last-child {
    border-bottom: none;
  }
 
  .posts-table td::before {
    content: attr(data-label);
    font-weight: 600;
    color: #64748b;
    margin-right: 1rem;
    flex-shrink: 0;
  }
 
  /* Add data labels for mobile */
  .post-title::before { content: "Title: "; }
  .post-author::before { content: "Author: "; }
  .post-status::before { content: "Status: "; }
  .post-date::before { content: "Created: "; }
  .post-actions::before { content: "Actions: "; }
}
</style>