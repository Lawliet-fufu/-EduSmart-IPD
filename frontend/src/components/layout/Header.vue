<script setup>
import { Search, Bell, User, LogOut, Settings } from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth.js'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const authStore = useAuthStore()
const router = useRouter()
const showUserMenu = ref(false)

const handleUserMenuClick = () => {
  showUserMenu.value = !showUserMenu.value
}

const handleSettings = () => {
  showUserMenu.value = false
  router.push('/settings')
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

// Close menu when clicking outside
const handleClickOutside = () => {
  showUserMenu.value = false
}
</script>

<template>
  <header class="header" @click="handleClickOutside">
    <div class="search-bar">
      <Search :size="20" class="search-icon" />
      <input type="text" placeholder="Search for anything..." />
    </div>

    <div class="header-actions">
      <button class="icon-btn">
        <Bell :size="20" />
        <span class="badge"></span>
      </button>

      <div class="user-profile" @click.stop="handleUserMenuClick">
        <div class="avatar">
          <span v-if="authStore.user?.avatar">{{ authStore.user.avatar }}</span>
          <User v-else :size="20" />
        </div>
        <div class="user-info">
          <span class="name">{{ authStore.user?.name || 'User' }}</span>
          <span class="role">{{ authStore.user?.role || 'User' }}</span>
        </div>

        <!-- User Menu Dropdown -->
        <div v-if="showUserMenu" class="user-menu" @click.stop>
          <div class="menu-item" @click="handleSettings">
            <Settings :size="18" />
            <span>Settings</span>
          </div>
          <div class="menu-divider"></div>
          <div class="menu-item logout" @click="handleLogout">
            <LogOut :size="18" />
            <span>Logout</span>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  height: 70px;
  background-color: var(--bg-surface);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  position: sticky;
  top: 0;
  z-index: 10;
}

.search-bar {
  position: relative;
  width: 400px;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-light);
}

.search-bar input {
  width: 100%;
  padding: 0.625rem 1rem 0.625rem 2.75rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  background-color: var(--bg-body);
  color: var(--text-main);
  font-size: 0.875rem;
  transition: border-color 0.2s;
}

.search-bar input:focus {
  outline: none;
  border-color: var(--primary);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.icon-btn {
  position: relative;
  color: var(--text-muted);
  padding: 0.5rem;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.icon-btn:hover {
  background-color: var(--bg-body);
  color: var(--text-main);
}

.badge {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 8px;
  height: 8px;
  background-color: #ef4444;
  border-radius: 50%;
  border: 2px solid var(--bg-surface);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding-left: 1.5rem;
  border-left: 1px solid var(--border-color);
  position: relative;
  cursor: pointer;
  transition: opacity 0.2s;
}

.user-profile:hover {
  opacity: 0.8;
}

.avatar {
  width: 36px;
  height: 36px;
  background-color: #e0f2fe;
  /* Sky 100 */
  color: #0284c7;
  /* Sky 600 */
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-main);
}

.role {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: capitalize;
}

.user-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 0.75rem;
  box-shadow: var(--shadow-lg);
  min-width: 180px;
  z-index: 1000;
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: var(--text-main);
  cursor: pointer;
  transition: background-color 0.2s;
}

.menu-item:hover {
  background-color: var(--bg-body);
}

.menu-item.logout {
  color: #ef4444;
}

.menu-item.logout:hover {
  background-color: rgba(239, 68, 68, 0.1);
}

.menu-divider {
  height: 1px;
  background-color: var(--border-color);
}
</style>
