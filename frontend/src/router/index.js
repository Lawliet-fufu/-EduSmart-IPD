import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue')
    },
    {
        path: '/teacher-dashboard',
        name: 'TeacherDashboard',
        component: () => import('../views/TeacherDashboard.vue'),
        meta: { requiresAuth: true, role: 'teacher' }
    },
    {
        path: '/student-dashboard',
        name: 'StudentDashboard',
        component: () => import('../views/StudentDashboard.vue'),
        meta: { requiresAuth: true, role: 'student' }
    },
    {
        path: '/',
        redirect: '/login'
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    // Placeholder for authentication logic
    const isAuthenticated = false; // Replace with actual auth check
    const userRole = null; // Replace with actual user role

    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login');
    } else if (to.meta.role && to.meta.role !== userRole) {
        // Handle unauthorized access
        next('/login');
    } else {
        next();
    }
})

export default router
