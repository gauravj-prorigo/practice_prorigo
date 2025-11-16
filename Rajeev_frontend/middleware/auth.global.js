import { useAuthStore } from '#imports'
import { defineNuxtRouteMiddleware, navigateTo } from '#imports'

export default defineNuxtRouteMiddleware((to) => {
  // Define public routes that don't require authentication
  const publicRoutes = ['/', '/register']
  const isPublicRoute = publicRoutes.includes(to.path)
  
  // Initialize auth state
  const auth = useAuthStore()
  
  // Only run on client side
  if (process.server) return
  
  // Initialize from storage (if your app needs this)
  auth.initFromStorage()
  
  // Scenario 1: User is authenticated but trying to access public routes
  if (auth.isAuthenticated && isPublicRoute) {
    return navigateTo('/')
  }
  
  // Scenario 2: User is not authenticated and trying to access protected routes
  if (!auth.isAuthenticated && !isPublicRoute) {
    // Redirect to login with return URL
    return navigateTo(`/?next=${encodeURIComponent(to.fullPath)}`)
  }
  
  // Scenario 3: User is authenticated and accessing protected routes → ALLOW
  // Scenario 4: User is not authenticated and accessing public routes → ALLOW
})