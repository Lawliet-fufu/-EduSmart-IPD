<script setup>
import { Bell } from 'lucide-vue-next'

const notices = [
  { id: 1, title: 'Final Exam Schedule Notice', date: '2024-01-15', type: 'important' },
  { id: 2, title: 'Parent Meeting Invitation', date: '2024-01-12', type: 'normal' },
  { id: 3, title: 'Winter Homework Checklist', date: '2024-01-10', type: 'normal' }
]
</script>

<template>
  <div class="notices-card">
    <div class="card-header">
      <h3>Recent Notices</h3>
      <Bell :size="20" />
    </div>
    <div class="notices-list">
      <div v-for="notice in notices" :key="notice.id" class="notice-item" :class="notice.type">
        <div class="notice-content">
          <h4>{{ notice.title }}</h4>
          <span class="notice-date">{{ notice.date }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.notices-card {
  background: var(--bg-surface);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.card-header h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-main);
}

.notices-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.notice-item {
  padding: 1rem;
  border-radius: 0.5rem;
  background: var(--bg-body);
  border-left: 3px solid var(--border-color);
  transition: transform 0.2s;
}

.notice-item:hover {
  transform: translateX(4px);
}

.notice-item.important {
  border-left-color: #ef4444;
  background: #fef2f2;
}

.notice-content h4 {
  font-size: 0.9375rem;
  font-weight: 500;
  color: var(--text-main);
  margin-bottom: 0.25rem;
}

.notice-date {
  font-size: 0.75rem;
  color: var(--text-muted);
}
</style>
