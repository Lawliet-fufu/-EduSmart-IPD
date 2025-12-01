<script setup>
import { Search, Bell, User } from 'lucide-vue-next'
</script>

<template>
  <header class="header">
    <div class="search-bar">
      <Search :size="20" class="search-icon" />
      <input type="text" placeholder="Search for anything..." />
    </div>

    <div class="header-actions">
      <button class="icon-btn">
        <Bell :size="20" />
        <span class="badge"></span>
      </button>
      
      <div class="user-profile">
        <div class="avatar">
          <User :size="20" />
        </div>
        <div class="user-info">
          <span class="name">Teacher Lawliet</span>
          <span class="role">Admin</span>
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
}

.avatar {
  width: 36px;
  height: 36px;
  background-color: #e0f2fe; /* Sky 100 */
  color: #0284c7; /* Sky 600 */
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
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
}
</style>
