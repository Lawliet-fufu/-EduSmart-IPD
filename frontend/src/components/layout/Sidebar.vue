<script setup>
import { computed } from 'vue'
import { 
  Home, 
  BookOpen, 
  Bell, 
  Users, 
  Bot,
  Settings,
  LogOut
} from 'lucide-vue-next'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore, UserRoles } from '../../stores/auth.js'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// All menu items with role restrictions
const allMenuItems = [
  { name: 'Home', path: '/', icon: Home, roles: ['all'] },
  { name: 'Assignments', path: '/assignments', icon: BookOpen, roles: ['all'] },
  { name: 'Notices', path: '/notices', icon: Bell, roles: ['all'] },
  { name: 'Class Mgmt', path: '/class', icon: Users, roles: [UserRoles.TEACHER, UserRoles.ADMIN] },
  { name: 'AI Assistant', path: '/ai', icon: Bot, roles: [UserRoles.TEACHER, UserRoles.ADMIN] },
]

// Filter menu items based on user role
const menuItems = computed(() => {
  const userRole = authStore.userRole
  return allMenuItems.filter(item => {
    if (item.roles.includes('all')) return true
    return item.roles.includes(userRole)
  })
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <aside class="sidebar">
    <div class="logo-container">
      <div class="logo-icon">
        <BookOpen class="text-white" :size="24" />
      </div>
      <span class="logo-text">EduSmart</span>
    </div>

    <nav class="nav-menu">
      <router-link 
        v-for="item in menuItems" 
        :key="item.path" 
        :to="item.path"
        class="nav-item"
        :class="{ active: route.path === item.path }"
      >
        <component :is="item.icon" :size="20" />
        <span>{{ item.name }}</span>
      </router-link>
    </nav>

    <div class="bottom-menu">
      <router-link to="/settings" class="nav-item">
        <Settings :size="20" />
        <span>Settings</span>
      </router-link>
      <button @click="handleLogout" class="nav-item text-danger">
        <LogOut :size="20" />
        <span>Logout</span>
      </button>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 260px;
  height: 100vh;
  /* Dark green gradient with design feel */
  background: linear-gradient(180deg, #047857 0%, #065f46 50%, #064e3b 100%);
  border-right: 1px solid rgba(16, 185, 129, 0.2);
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  position: fixed;
  left: 0;
  top: 0;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15);
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 2.5rem;
  padding: 0 0.5rem;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: rgba(16, 185, 129, 0.25);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.logo-text {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
  transition: all 0.2s;
}

.nav-item:hover {
  background-color: rgba(16, 185, 129, 0.15);
  color: rgba(255, 255, 255, 0.95);
}

.nav-item.active {
  background: rgba(16, 185, 129, 0.3);
  color: white;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
}

.nav-item.active svg {
  color: white;
}

.bottom-menu {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.text-danger {
  color: #fca5a5;
}

.text-danger:hover {
  background-color: rgba(239, 68, 68, 0.15);
  color: #fecaca;
}
</style>
