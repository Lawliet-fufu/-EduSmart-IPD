import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/index.js'

// User roles definition
export const UserRoles = {
    ADMIN: 'admin',
    TEACHER: 'teacher',
    STUDENT: 'student'
}

export const useAuthStore = defineStore('auth', () => {
    // State
    const user = ref(null)
    const token = ref(localStorage.getItem('token'))
    const preferences = ref({
        darkMode: localStorage.getItem('pref_darkMode') === 'true',
        language: localStorage.getItem('pref_language') || 'en',
        notifications: localStorage.getItem('pref_notifications') !== 'false',
        emailAlerts: localStorage.getItem('pref_emailAlerts') === 'true'
    })

    // Getters
    const isAuthenticated = computed(() => !!token.value)
    const userRole = computed(() => user.value?.role || null)
    const isAdmin = computed(() => userRole.value === UserRoles.ADMIN)
    const isTeacher = computed(() => userRole.value === UserRoles.TEACHER)
    const isStudent = computed(() => userRole.value === UserRoles.STUDENT)

    const applyDarkMode = (isDark) => {
        if (isDark) {
            document.documentElement.style.setProperty('--bg-body', '#1e293b')
            document.documentElement.style.setProperty('--bg-surface', '#0f172a')
            document.documentElement.style.setProperty('--text-main', '#f1f5f9')
            document.documentElement.style.setProperty('--text-muted', '#cbd5e1')
            document.documentElement.style.setProperty('--text-light', '#64748b')
            document.documentElement.style.setProperty('--border-color', '#334155')
            document.body.style.background = 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)'
            document.body.style.backgroundAttachment = 'fixed'
        } else {
            document.documentElement.style.setProperty('--bg-body', '#f8fafc')
            document.documentElement.style.setProperty('--bg-surface', 'rgba(255, 255, 255, 0.95)')
            document.documentElement.style.setProperty('--text-main', '#0f172a')
            document.documentElement.style.setProperty('--text-muted', '#64748b')
            document.documentElement.style.setProperty('--text-light', '#94a3b8')
            document.documentElement.style.setProperty('--border-color', '#e2e8f0')
            // 还原到全局样式（去除行内背景），使用 style.css 中定义的绿色渐变和几何纹理
            document.body.style.background = 
                'repeating-linear-gradient(45deg, transparent, transparent 60px, rgba(16, 185, 129, 0.02) 60px, rgba(16, 185, 129, 0.02) 120px), ' +
                'repeating-linear-gradient(-45deg, transparent, transparent 60px, rgba(5, 150, 105, 0.015) 60px, rgba(5, 150, 105, 0.015) 120px), ' +
                'linear-gradient(135deg, #ecfdf5 0%, #d1fae5 25%, #a7f3d0 50%, #6ee7b7 75%, #34d399 100%)'
            document.body.style.backgroundAttachment = 'fixed'
        }
    }

    // Actions
    const loadPreferences = async () => {
        if (!token.value) return
        try {
            const res = await api.get('/auth/preferences')
            if (res.data) {
                preferences.value = {
                    darkMode: res.data.dark_mode,
                    language: res.data.language,
                    notifications: res.data.notifications,
                    emailAlerts: res.data.email_alerts
                }
                // Persist locally for faster boot
                localStorage.setItem('pref_darkMode', String(preferences.value.darkMode))
                localStorage.setItem('pref_language', preferences.value.language)
                localStorage.setItem('pref_notifications', String(preferences.value.notifications))
                localStorage.setItem('pref_emailAlerts', String(preferences.value.emailAlerts))
                applyDarkMode(preferences.value.darkMode)
            }
        } catch (e) {
            // Ignore, fall back to localStorage
            applyDarkMode(preferences.value.darkMode)
        }
    }

    const login = async (username, password) => {
        try {
            const response = await api.post('/auth/login', {
                username: username.trim(),
                password: password.trim()
            })

            if (response.data && response.data.access_token) {
                token.value = response.data.access_token
                user.value = {
                    id: response.data.user.id,
                    name: response.data.user.full_name,
                    role: response.data.user.role,
                    username: response.data.user.username,
                    email: response.data.user.email,
                    avatar: response.data.user.avatar || '👤'
                }
                localStorage.setItem('token', token.value)
                localStorage.setItem('user', JSON.stringify(user.value))

                await loadPreferences()
                return { success: true }
            }
            return { success: false, message: 'Invalid response from server' }
        } catch (error) {
            const message = error.response?.data?.message || 'Login failed. Please try again.'
            return { success: false, message }
        }
    }

    const logout = () => {
        token.value = null
        user.value = null
        localStorage.removeItem('token')
        localStorage.removeItem('user')
    }

    // Restore user from localStorage on init
    const storedUser = localStorage.getItem('user')
    if (storedUser && token.value) {
        try {
            user.value = JSON.parse(storedUser)
            // Apply dark mode preference on boot
            applyDarkMode(preferences.value.darkMode)
        } catch (e) {
            localStorage.removeItem('user')
            localStorage.removeItem('token')
        }
    }

    return { user, token, preferences, isAuthenticated, userRole, isAdmin, isTeacher, isStudent, login, logout, loadPreferences, applyDarkMode }
})
