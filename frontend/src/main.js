import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from './stores/auth.js'
import './style.css'
import App from './App.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: () => import('./views/HomeView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/login',
            component: () => import('./views/LoginView.vue'),
            meta: { requiresAuth: false }
        },
        {
            path: '/assignments',
            component: () => import('./views/AssignmentsView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/notices',
            component: () => import('./views/NoticesView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/class',
            component: () => import('./views/ClassManagementView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/ai',
            component: () => import('./views/AIAssistantView.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/settings',
            component: () => import('./views/SettingsView.vue'),
            meta: { requiresAuth: true }
        },
    ]
})

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)

router.beforeEach((to, _from, next) => {
    const authStore = useAuthStore()

    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next('/login')
    } else if (to.path === '/login' && authStore.isAuthenticated) {
        next('/')
    } else {
        next()
    }
})

app.use(router)
app.mount('#app')
