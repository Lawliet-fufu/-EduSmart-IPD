import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const routes = [
  {
    path: '/',
    component: () => import('../views/HomeView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    component: () => import('../views/LoginView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/assignments',
    component: () => import('../views/AssignmentsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/notices',
    component: () => import('../views/NoticesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/class',
    component: () => import('../views/ClassManagementView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/ai',
    component: () => import('../views/AIAssistantView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    component: () => import('../views/SettingsView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  
  // 确保从 localStorage 恢复 token 和 user（如果存在）
  const storedToken = localStorage.getItem('token')
  const storedUser = localStorage.getItem('user')
  
  if (storedToken && !authStore.token) {
    // 如果 localStorage 有 token 但 store 中没有，恢复它
    authStore.token = storedToken
    if (storedUser) {
      try {
        authStore.user = JSON.parse(storedUser)
      } catch (e) {
        console.error('Failed to parse user from localStorage:', e)
        localStorage.removeItem('user')
        localStorage.removeItem('token')
      }
    }
  }
  
  // 检查认证状态
  const isAuthenticated = authStore.isAuthenticated || !!storedToken
  
  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      next('/login')
    } else {
      next()
    }
  } else if (to.path === '/login' && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
