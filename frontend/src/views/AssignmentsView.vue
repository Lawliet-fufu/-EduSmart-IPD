<script setup>
import { ref, computed } from 'vue'
import { BookOpen, Plus, Calendar, Clock, CheckCircle, AlertCircle } from 'lucide-vue-next'

const activeFilter = ref('all')
const showCreateModal = ref(false)

const assignments = ref([
  { id: 1, title: 'Math Homework - Chapter 5', subject: 'Mathematics', dueDate: '2024-02-15', status: 'pending', students: 28, completed: 12 },
  { id: 2, title: 'English Essay - My Dream', subject: 'English', dueDate: '2024-02-12', status: 'grading', students: 28, completed: 28 },
  { id: 3, title: 'Science Project Proposal', subject: 'Science', dueDate: '2024-02-20', status: 'pending', students: 28, completed: 5 },
  { id: 4, title: 'History Timeline Assignment', subject: 'History', dueDate: '2024-02-10', status: 'completed', students: 28, completed: 28 },
  { id: 5, title: 'Geography Map Drawing', subject: 'Geography', dueDate: '2024-02-18', status: 'pending', students: 28, completed: 8 }
])

const filteredAssignments = computed(() => {
  if (activeFilter.value === 'all') return assignments.value
  return assignments.value.filter(a => a.status === activeFilter.value)
})

const getStatusColor = (status) => {
  const colors = {
    pending: '#f97316',
    grading: '#3b82f6',
    completed: '#10b981'
  }
  return colors[status] || '#6b7280'
}

const getStatusText = (status) => {
  const texts = {
    pending: 'Pending',
    grading: 'Grading',
    completed: 'Completed'
  }
  return texts[status] || status
}
</script>

<template>
  <div class="assignments-container">
    <div class="page-header">
      <div>
        <h1>Assignments</h1>
        <p>Manage and track student assignments</p>
      </div>
      <button @click="showCreateModal = true" class="create-btn">
        <Plus :size="20" />
        Create Assignment
      </button>
    </div>

    <!-- Filters -->
    <div class="filters">
      <button 
        @click="activeFilter = 'all'" 
        :class="{ active: activeFilter === 'all' }"
        class="filter-btn"
      >
        All Assignments
      </button>
      <button 
        @click="activeFilter = 'pending'" 
        :class="{ active: activeFilter === 'pending' }"
        class="filter-btn"
      >
        Pending
      </button>
      <button 
        @click="activeFilter = 'grading'" 
        :class="{ active: activeFilter === 'grading' }"
        class="filter-btn"
      >
        Grading
      </button>
      <button 
        @click="activeFilter = 'completed'" 
        :class="{ active: activeFilter === 'completed' }"
        class="filter-btn"
      >
        Completed
      </button>
    </div>

    <!-- Assignments Grid -->
    <div class="assignments-grid">
      <div v-for="assignment in filteredAssignments" :key="assignment.id" class="assignment-card">
        <div class="card-header">
          <div class="title-section">
            <BookOpen :size="20" class="subject-icon" />
            <div>
              <h3>{{ assignment.title }}</h3>
              <span class="subject">{{ assignment.subject }}</span>
            </div>
          </div>
          <span class="status-badge" :style="{ backgroundColor: getStatusColor(assignment.status) }">
            {{ getStatusText(assignment.status) }}
          </span>
        </div>

        <div class="card-body">
          <div class="info-row">
            <Calendar :size="16" />
            <span>Due: {{ assignment.dueDate }}</span>
          </div>
          <div class="progress-section">
            <div class="progress-info">
              <span>{{ assignment.completed }}/{{ assignment.students }} completed</span>
              <span>{{ Math.round((assignment.completed / assignment.students) * 100) }}%</span>
            </div>
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ width: `${(assignment.completed / assignment.students) * 100}%` }"
              ></div>
            </div>
          </div>
        </div>

        <div class="card-actions">
          <button class="action-btn">View Details</button>
          <button class="action-btn secondary">Edit</button>
        </div>
      </div>
    </div>

    <!-- Create Modal Placeholder -->
    <div v-if="showCreateModal" class="modal-overlay" @click="showCreateModal = false">
      <div class="modal-content" @click.stop>
        <h2>Create New Assignment</h2>
        <p class="modal-message">Assignment creation form will be implemented here.</p>
        <button @click="showCreateModal = false" class="close-btn">Close</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.assignments-container {
  max-width: 1200px;
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

.filters {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 0.625rem 1.25rem;
  border-radius: 0.5rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  font-weight: 500;
  transition: all 0.2s;
}

.filter-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.filter-btn.active {
  background-color: var(--primary);
  color: white;
  border-color: var(--primary);
}

.assignments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.assignment-card {
  background: var(--bg-surface);
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid var(--border-color);
  transition: all 0.2s;
}

.assignment-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
}

.title-section {
  display: flex;
  gap: 0.75rem;
  flex: 1;
}

.subject-icon {
  color: var(--primary);
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.title-section h3 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-main);
  margin-bottom: 0.25rem;
  line-height: 1.4;
}

.subject {
  font-size: 0.8125rem;
  color: var(--text-muted);
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
  white-space: nowrap;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-muted);
  font-size: 0.875rem;
}

.progress-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.8125rem;
  color: var(--text-muted);
  font-weight: 500;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #e5e7eb;
  border-radius: 999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: var(--primary);
  border-radius: 999px;
  transition: width 0.3s;
}

.card-actions {
  display: flex;
  gap: 0.75rem;
}

.action-btn {
  flex: 1;
  padding: 0.625rem;
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
