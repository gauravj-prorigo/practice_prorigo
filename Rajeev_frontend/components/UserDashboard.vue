<template>
  <section class="user-dashboard">
    <!-- Welcome Section -->
    <div class="welcome-section">
      <div class="welcome-content">
        <h1 class="welcome-title">Welcome to Our Blog Platform! 📝</h1>
        <p class="welcome-subtitle">
          Discover amazing stories, share your thoughts, and connect with our community of readers and writers.
        </p>
        <div class="welcome-features">
          <div class="feature-item">
            <span class="feature-icon">📚</span>
            <span class="feature-text">Read inspiring content</span>
          </div>
          <div class="feature-item">
            <span class="feature-icon">🔍</span>
            <span class="feature-text">Discover new perspectives</span>
          </div>
          <div class="feature-item">
            <span class="feature-icon">💬</span>
            <span class="feature-text">Join the conversation</span>
          </div>
        </div>
      </div>
      <div class="welcome-stats">
        <div class="stat-item">
          <div class="stat-number">{{ totalBlogs }}</div>
          <div class="stat-label">Total Posts</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ activeWriters }}</div>
          <div class="stat-label">Active Writers</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ communityMembers }}</div>
          <div class="stat-label">Community Members</div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="quick-actions">
      <h2 class="section-title">Get Started</h2>
      <div class="action-buttons">
        <button class="action-btn primary" @click="scrollToBlogs">
          <span class="action-icon">📖</span>
          <span class="action-text">Browse All Posts</span>
        </button>
        <button class="action-btn" @click="showFeatured">
          <span class="action-icon">⭐</span>
          <span class="action-text">Featured Posts</span>
        </button>
        <button class="action-btn" @click="showCategories">
          <span class="action-icon">📂</span>
          <span class="action-text">Browse Categories</span>
        </button>
      </div>
    </div>

    <!-- Latest Posts Preview -->
    <div class="preview-section">
      <div class="section-header">
        <h2 class="section-title">Latest from Our Community</h2>
        <p class="section-subtitle">Fresh content from our talented writers</p>
      </div>
      <div class="preview-grid">
        <div v-for="blog in latestBlogs" :key="blog.id" class="preview-card">
          <div class="preview-content">
            <h3 class="blog-title">{{ blog.title }}</h3>
            <p class="blog-excerpt">{{ getExcerpt(blog.content) }}</p>
            <div class="blog-meta">
              <span class="blog-author">By {{ blog.author?.username || 'Anonymous' }}</span>
              <span class="blog-date">{{ formatDate(blog.created_at) }}</span>
            </div>
          </div>
          <button class="btn btn-read" @click="viewBlog(blog)">Read More</button>
        </div>
      </div>
    </div>

    <!-- Main Blog List -->
    <!-- <div class="blog-list-section" ref="blogListSection">
      <div class="section-header">
        <h2 class="section-title">All Blog Posts</h2>
        <p class="section-subtitle">Explore our complete collection of stories and articles</p>
      </div>
      <BlogList />
    </div> -->

    <!-- Community Info -->
    <div class="community-section">
      <div class="community-content">
        <h2 class="section-title">Join Our Growing Community</h2>
        <p class="community-description">
          Be part of a vibrant community of readers and writers. Share your thoughts, 
          engage with others, and discover content that matters to you.
        </p>
        <div class="community-stats">
          <div class="community-stat">
            <div class="stat-value">99%</div>
            <div class="stat-label">Reader Satisfaction</div>
          </div>
          <div class="community-stat">
            <div class="stat-value">24/7</div>
            <div class="stat-label">Content Updates</div>
          </div>
          <div class="community-stat">
            <div class="stat-value">1000+</div>
            <div class="stat-label">Monthly Readers</div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '#imports'
import BlogList from './BlogList.vue'

const auth = useAuthStore()
const API_BASE = 'http://127.0.0.1:8000'
const blogListSection = ref(null)

const blogs = ref([])
const loading = ref(false)

// Mock data for demonstration
const totalBlogs = ref(156)
const activeWriters = ref(42)
const communityMembers = ref(1284)

onMounted(() => { 
  fetchBlogs() 
})

const latestBlogs = computed(() => {
  return blogs.value.slice(0, 3) // Show latest 3 blogs in preview
})

async function fetchBlogs() {
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/api/blogs/`, { 
      headers: { Authorization: `Bearer ${auth.token}` } 
    })
    blogs.value = await res.json()
    totalBlogs.value = blogs.value.length
  } catch (e) { 
    console.error('Failed to fetch blogs:', e) 
  } finally { 
    loading.value = false 
  }
}

function scrollToBlogs() {
  if (blogListSection.value) {
    blogListSection.value.scrollIntoView({ behavior: 'smooth' })
  }
}

function viewBlog(blog) {
  // Navigate to blog detail page
  console.log('View blog:', blog)
  // router.push(`/blogs/${blog.id}`)
}

function showFeatured() {
  // Implement featured posts filter
  console.log('Show featured posts')
}

function showCategories() {
  // Implement categories view
  console.log('Show categories')
}

function getExcerpt(content, length = 120) {
  if (!content) return 'No content available'
  return content.length > length ? content.substring(0, length) + '...' : content
}

function formatDate(dateString) {
  if (!dateString) return 'Recently'
  const options = { year: 'numeric', month: 'short', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}
</script>

<style scoped>
.user-dashboard {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

/* Welcome Section */
.welcome-section {
  background: white;
  color: rgb(20, 19, 19);
  border-radius: 20px;
  padding: 3rem 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 10px 30px rgba(3, 3, 3, 0.3);
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  align-items: center;
}

.welcome-content {
  text-align: left;
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin: 0 0 1rem 0;
  line-height: 1.2;
  letter-spacing: -0.025em;
}

.welcome-subtitle {
  font-size: 1.25rem;
  opacity: 0.95;
  margin: 0 0 2rem 0;
  line-height: 1.5;
}

.welcome-features {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.1rem;
}

.feature-icon {
  font-size: 1.5rem;
}

.feature-text {
  font-weight: 500;
}

.welcome-stats {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Quick Actions */
.quick-actions {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
}

.section-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 1rem 0;
  text-align: center;
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1.25rem 1.5rem;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  font-size: 1rem;
  color: #475569;
}

.action-btn:hover {
  border-color: #3b82f6;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.action-btn.primary {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border: none;
}

.action-btn.primary:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.3);
}

.action-icon {
  font-size: 1.5rem;
}

.action-text {
  font-weight: 600;
}

/* Preview Section */
.preview-section {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
}

.section-header {
  text-align: center;
  margin-bottom: 2rem;
}

.section-subtitle {
  font-size: 1.1rem;
  color: #64748b;
  margin: 0;
}

.preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.preview-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.preview-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  border-color: #3b82f6;
}

.blog-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 1rem 0;
  line-height: 1.3;
}

.blog-excerpt {
  color: #64748b;
  line-height: 1.5;
  margin: 0 0 1.5rem 0;
  flex: 1;
}

.blog-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
  color: #94a3b8;
  margin-bottom: 1rem;
}

.blog-author {
  font-weight: 500;
}

.blog-date {
  font-style: italic;
}

.btn-read {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
  width: 100%;
}

.btn-read:hover {
  background: #2563eb;
}

/* Blog List Section */
.blog-list-section {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
}

/* Community Section */
.community-section {
  background: white;
  color: black;
  border-radius: 20px;
  padding: 3rem 2rem;
  text-align: center;
   box-shadow: 0 10px 30px rgba(3, 3, 3, 0.3);
}

.community-content {
  max-width: 600px;
  margin: 0 auto;
}

.community-description {
  font-size: 1.1rem;
  line-height: 1.6;
  opacity: 0.9;
  margin: 0 0 2rem 0;
}

.community-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.community-stat {
  text-align: center;
}

.community-stat .stat-value {
  font-size: 2rem;
  font-weight: 800;
  color: #3b82f6;
  margin-bottom: 0.5rem;
}

.community-stat .stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .user-dashboard {
    padding: 1rem;
  }

  .welcome-section {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 2rem 1rem;
  }

  .welcome-title {
    font-size: 2rem;
  }

  .welcome-subtitle {
    font-size: 1.1rem;
  }

  .welcome-stats {
    padding: 1.5rem;
  }

  .preview-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    grid-template-columns: 1fr;
  }

  .community-stats {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}

/* Animation for scroll */
.scroll-indicator {
  text-align: center;
  margin: 1rem 0;
  color: #64748b;
  font-size: 1.5rem;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}
</style>