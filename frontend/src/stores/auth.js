import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// User roles definition
export const UserRoles = {
    ADMIN: 'admin',
    TEACHER: 'teacher',
    STUDENT: 'student'
}

// Demo users with different roles
const demoUsers = {
    'admin': { username: 'admin', password: '123456', role: UserRoles.ADMIN, name: 'Administrator', avatar: '👨‍💼' },
    'teacher': { username: 'teacher', password: '123456', role: UserRoles.TEACHER, name: 'Teacher Lawliet', avatar: '👨‍🏫' },
    'student': { username: 'student', password: '123456', role: UserRoles.STUDENT, name: 'Student Mike', avatar: '👨‍🎓' }
}

export const useAuthStore = defineStore('auth', () => {
    // State
    const user = ref(null)
    const token = ref(localStorage.getItem('token'))

    // Getters
    const isAuthenticated = computed(() => !!token.value)
    const userRole = computed(() => user.value?.role || null)
    const isAdmin = computed(() => userRole.value === UserRoles.ADMIN)
    const isTeacher = computed(() => userRole.value === UserRoles.TEACHER)
    const isStudent = computed(() => userRole.value === UserRoles.STUDENT)

    // Actions
    const login = (username, password) => {
        const normalizedUsername = username.trim().toLowerCase()
        const demoUser = demoUsers[normalizedUsername]

        // Check demo users
        if (demoUser && password.trim() === demoUser.password) {
            token.value = `mock-jwt-token-${demoUser.role}-${Date.now()}`
            user.value = {
                name: demoUser.name,
                role: demoUser.role,
                username: demoUser.username,
                avatar: demoUser.avatar
            }
            localStorage.setItem('token', token.value)
            localStorage.setItem('user', JSON.stringify(user.value))
            return true
        }

        return false
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
        } catch (e) {
            localStorage.removeItem('user')
        }
    }

    return { user, token, isAuthenticated, userRole, isAdmin, isTeacher, isStudent, login, logout }
})
