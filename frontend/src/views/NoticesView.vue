<script setup>
import { ref } from 'vue'
import { Bell, Plus, AlertCircle, Info, Calendar, User } from 'lucide-vue-next'

const showCreateModal = ref(false)

const notices = ref([
  {
    id: 1,
    title: 'Final Exam Schedule Released',
    content: 'The final exam schedule for this semester has been released. Please check the student portal for detailed information.',
    author: 'Admin Department',
    date: '2024-02-15',
    priority: 'important',
    category: 'Academic'
  },
  {
    id: 2,
    title: 'Parent-Teacher Meeting',
    content: 'Parent-teacher meeting will be held on February 20th. All parents are encouraged to attend.',
    author: 'Principal Office',
    date: '2024-02-12',
    priority: 'important',
    category: 'Event'
  },
  {
    id: 3,
    title: 'Winter Holiday Homework',
    content: 'Please remind students to complete their winter holiday homework before the new semester starts.',
    author: 'Academic Office',
    date: '2024-02-10',
    priority: 'normal',
    category: 'Academic'
  },
  {
    id: 4,
    title: 'School Festival Announcement',
    content: 'The annual school festival will take place on March 15th. Prepare performances and activities!',
    author: 'Student Affairs',
    date: '2024-02-08',
    priority: 'normal',
    category: 'Event'
  },
  {
    id: 5,
    title: 'Library Hours Extended',
    content: 'The library will now be open until 8 PM on weekdays to support student studying.',
    author: 'Library Department',
    date: '2024-02-05',
    priority: 'normal',
    category: 'Facility'
  }
])

const getPriorityColor = (priority) => {
  return priority === 'important' ? '#ef4444' : '#10b981'
}

const getPriorityIcon = (priority) => {
  return priority === 'important' ? AlertCircle : Info
}
</script>

<template>
  <div class="notices-container">
    <div class="page-header">
      <div>
        <h1>Notices & Announcements</h1>
        <p>Important information and updates</p>
      </div>
      <button @click="showCreateModal = true" class="create-btn">
        <Plus :size="20" />
        Post Notice
      </button>
    </div>

    <!-- Notices List -->
    <div class="notices-list">
      <div 
        v-for="notice in notices" 
        :key="notice.id" 
        class="notice-card"
        :class="{ important: notice.priority === 'important' }"
      >
        <div class="notice-header">
          <div class="priority-indicator">
            <component 
              :is="getPriorityIcon(notice.priority)" 
              :size="20"
              :style="{ color: getPriorityColor(notice.priority) }"
            />
          </div>
          <div class="notice-title-section">
            <h3>{{ notice.title }}</h3>
            <div class="notice-meta">
              <span class="category-badge">{{ notice.category }}</span>
              <span class="separator">•</span>
              <span class="meta-item">
                <Calendar :size="14" />
                {{ notice.date }}
              </span>
              <span class="separator">•</span>
              <span class="meta-item">
                <User :size="14" />
                {{ notice.author }}
              </span>
            </div>
          </div>
        </div>

        <div class="notice-content">
          <p>{{ notice.content }}</p>
        </div>

        <div class="notice-actions">
          <button class="action-btn">View Full Notice</button>
          <button class="action-btn secondary">Edit</button>
          <button class="action-btn secondary text-danger">Delete</button>
        </div>
      </div>
    </div>

    <!-- Create Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click="showCreateModal = false">
      <div class="modal-content" @click.stop>
        <h2>Post New Notice</h2>
        <p class="modal-message">Notice creation form will be implemented here.</p>
        <button @click="showCreateModal = false" class="close-btn">Close</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.notices-container {
  max-width: 900px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 0.5rem;
}

.page-header p {
  color: var(--text-muted);
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: var(--primary);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 600;
  transition: all 0.2s;
}

.create-btn:hover {
  background-color: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.notices-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.notice-card {
  background: var(--bg-surface);
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid var(--border-color);
  border-left-width: 4px;
  transition: all 0.2s;
}

.notice-card.important {
  border-left-color: #ef4444;
  background-color: #fef2f2;
}

.notice-card:not(.important) {
  border-left-color: var(--primary);
}

.notice-card:hover {
  transform: translateX(4px);
  box-shadow: var(--shadow-md);
}

.notice-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.priority-indicator {
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.notice-title-section {
  flex: 1;
}

.notice-title-section h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-main);
  margin-bottom: 0.5rem;
}

.notice-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  font-size: 0.8125rem;
  color: var(--text-muted);
}

.category-badge {
  background-color: var(--primary);
  color: white;
  padding: 0.125rem 0.625rem;
  border-radius: 999px;
  font-weight: 500;
  font-size: 0.75rem;
}

.separator {
  color: var(--border-color);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.notice-content {
  margin-bottom: 1rem;
  padding: 1rem;
  background-color: var(--bg-body);
  border-radius: 0.5rem;
}

.notice-content p {
  color: var(--text-main);
  line-height: 1.6;
  font-size: 0.9375rem;
}

.notice-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  font-size: 0.875rem;
  background-color: var(--primary);
  color: white;
  transition: all 0.2s;
}

.action-btn:hover {
  background-color: var(--primary-hover);
}

.action-btn.secondary {
  background-color: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border-color);
}

.action-btn.secondary:hover {
  background-color: var(--bg-body);
  color: var(--text-main);
}

.action-btn.text-danger {
  color: #ef4444;
}

.action-btn.text-danger:hover {
  background-color: #fef2f2;
  border-color: #ef4444;
  color: #dc2626;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--bg-surface);
  padding: 2rem;
  border-radius: 1rem;
  max-width: 500px;
  width: 90%;
}

.modal-content h2 {
  margin-bottom: 1rem;
  color: var(--text-main);
}

.modal-message {
  color: var(--text-muted);
  margin-bottom: 1.5rem;
}

.close-btn {
  background-color: var(--primary);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
}
</style>
