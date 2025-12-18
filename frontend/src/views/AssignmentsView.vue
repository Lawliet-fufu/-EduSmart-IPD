<script setup>
import { ref, computed, onMounted } from 'vue'
import { BookOpen, Plus, Calendar } from 'lucide-vue-next'
import { getAssignments, createAssignment, updateAssignment, deleteAssignment } from '../api/assignments.js'

const activeFilter = ref('all')
const showCreateModal = ref(false)
const assignments = ref([])
const isLoading = ref(false)
const error = ref('')


// Subject mapping: Enumerated values returned by the backend -> Display on the frontend (in English)
const subjectLabelMap = {
  'chinese': 'Chinese',
  'math': 'Math',
  'english': 'English'
}

const subjectOptions = [
  { value: 'math', label: 'Math' },
  { value: 'chinese', label: 'Chinese' },
  { value: 'english', label: 'English' }
]

const statusOptions = [
  { value: 'pending', label: 'Pending' },
  { value: 'grading', label: 'Grading' },
  { value: 'completed', label: 'Completed' }
]

// Create job form data
const newAssignment = ref({
  title: '',
  subject: 'math',
  description: '',
  dueDate: '',
  class_id: null
})

// Edit the job data
const editingAssignment = ref(null)

// Create computed properties for each field (for use with v-model)
const formTitle = computed({
  get: () => editingAssignment.value?.title || newAssignment.value.title || '',
  set: (val) => {
    if (editingAssignment.value) {
      editingAssignment.value.title = val
    } else {
      newAssignment.value.title = val
    }
  }
})

const formSubject = computed({
  get: () => editingAssignment.value?.subject || newAssignment.value.subject || 'math',
  set: (val) => {
    if (editingAssignment.value) {
      editingAssignment.value.subject = val
    } else {
      newAssignment.value.subject = val
    }
  }
})

const formDescription = computed({
  get: () => editingAssignment.value?.description || newAssignment.value.description || '',
  set: (val) => {
    if (editingAssignment.value) {
      editingAssignment.value.description = val
    } else {
      newAssignment.value.description = val
    }
  }
})

const formDueDate = computed({
  get: () => editingAssignment.value?.dueDate || newAssignment.value.dueDate || '',
  set: (val) => {
    if (editingAssignment.value) {
      editingAssignment.value.dueDate = val
    } else {
      newAssignment.value.dueDate = val
    }
  }
})

const formStatus = computed({
  get: () => editingAssignment.value?.status || newAssignment.value.status || 'pending',
  set: (val) => {
    if (editingAssignment.value) {
      editingAssignment.value.status = val
    } else {
      newAssignment.value.status = val
    }
  }
})



// Load the job list
const loadAssignments = async () => {
  isLoading.value = true
  error.value = ''
  try {
    const filters = {}
    if (activeFilter.value !== 'all') {
      filters.status = activeFilter.value
    }
    const data = await getAssignments(filters)
    assignments.value = data.map(item => ({
      ...item,
      subjectLabel: subjectLabelMap[item.subject] || item.subject
    }))
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load assignments'
    console.error('Error loading assignments:', err)
  } finally {
    isLoading.value = false
  }
}

// 创建作业
const handleCreateAssignment = async () => {
  if (!newAssignment.value.title || !newAssignment.value.subject) {
    error.value = 'Title and subject are required'
    return
  }

  isLoading.value = true
  error.value = ''
  try {
    await createAssignment({ ...newAssignment.value })
    showCreateModal.value = false
    // 重置表单
    newAssignment.value = {
      title: '',
      subject: 'math',
      description: '',
      dueDate: '',
      status: 'pending',
      class_id: null
    }
    await loadAssignments()
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to create assignment'
  } finally {
    isLoading.value = false
  }
}

// Edit the assignment
const handleEditAssignment = (assignment) => {
  editingAssignment.value = {
    ...assignment,
    subject: assignment.subject // Keep Chinese display
  }
  showCreateModal.value = true
}

// Update the assignment
const handleUpdateAssignment = async () => {
  if (!editingAssignment.value.title || !editingAssignment.value.subject) {
    error.value = 'Title and subject are required'
    return
  }

  isLoading.value = true
  error.value = ''
  try {
    await updateAssignment(editingAssignment.value.id, { ...editingAssignment.value })
    showCreateModal.value = false
    editingAssignment.value = null
    await loadAssignments()
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to update assignment'
  } finally {
    isLoading.value = false
  }
}

// Delete the assignment
const handleDeleteAssignment = async (id) => {
  if (!confirm('Are you sure you want to delete this assignment?')) {
    return
  }

  isLoading.value = true
  error.value = ''
  try {
    await deleteAssignment(id)
    await loadAssignments()
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to delete assignment'
  } finally {
    isLoading.value = false
  }
}

// Save the assignment (create or update)
const handleSaveAssignment = () => {
  if (editingAssignment.value) {
    handleUpdateAssignment()
  } else {
    handleCreateAssignment()
  }
}

// Close the modal window
const closeModal = () => {
  showCreateModal.value = false
  editingAssignment.value = null
  newAssignment.value = {
    title: '',
    subject: 'math',
    description: '',
    dueDate: '',
    status: 'pending',
    class_id: null
  }
  error.value = ''
}

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

// Loading data during component mounting
onMounted(() => {
  loadAssignments()
})
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

    <!-- Loading State -->
    <div v-if="isLoading && assignments.length === 0" class="loading-state">
      <p>Loading assignments...</p>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="error-banner">
      {{ error }}
    </div>

    <!-- Assignments Grid -->
    <div v-if="!isLoading || assignments.length > 0" class="assignments-grid">
      <div v-for="assignment in filteredAssignments" :key="assignment.id" class="assignment-card">
        <div class="card-header">
          <div class="title-section">
            <BookOpen :size="20" class="subject-icon" />
            <div>
              <h3>{{ assignment.title }}</h3>
              <span class="subject">{{ assignment.subjectLabel || subjectLabelMap[assignment.subject] || assignment.subject }}</span>
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
          <button class="action-btn secondary" @click="handleEditAssignment(assignment)">Edit</button>
          <button class="action-btn danger" @click="handleDeleteAssignment(assignment.id)">Delete</button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h2>{{ editingAssignment ? 'Edit Assignment' : 'Create New Assignment' }}</h2>
        
        <form @submit.prevent="handleSaveAssignment" class="assignment-form">
          <div class="form-group">
            <label>Title *</label>
            <input 
              v-model="formTitle"
              type="text" 
              placeholder="Enter assignment title"
              required
            />
          </div>

          <div class="form-group">
            <label>Subject *</label>
            <select 
              v-model="formSubject"
              required
            >
              <option 
                v-for="option in subjectOptions" 
                :key="option.value" 
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>Description</label>
            <textarea 
              v-model="formDescription"
              placeholder="Enter assignment description"
              rows="3"
            ></textarea>
          </div>

          <div class="form-group">
            <label>Due Date</label>
            <input 
              v-model="formDueDate"
              type="date"
            />
          </div>

          <div class="form-group">
            <label>Status *</label>
            <select 
              v-model="formStatus"
              required
            >
              <option 
                v-for="option in statusOptions" 
                :key="option.value" 
                :value="option.value"
              >
                {{ option.label }}
              </option>
            </select>
          </div>

          <div v-if="error" class="form-error">
            {{ error }}
          </div>

          <div class="modal-actions">
            <button type="button" @click="closeModal" class="btn-secondary">Cancel</button>
            <button type="submit" :disabled="isLoading" class="btn-primary">
              {{ isLoading ? 'Saving...' : (editingAssignment ? 'Update' : 'Create') }}
            </button>
          </div>
        </form>
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

.loading-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-muted);
}

.error-banner {
  background-color: #fef2f2;
  color: #ef4444;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid #fecaca;
}

.assignment-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-main);
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  font-size: 0.9375rem;
  color: var(--text-main);
  background-color: var(--bg-body);
  transition: all 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.form-error {
  color: #ef4444;
  font-size: 0.875rem;
  background-color: #fef2f2;
  padding: 0.75rem;
  border-radius: 0.5rem;
}

.modal-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-top: 1rem;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background-color: var(--primary);
  color: white;
  border: none;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--primary-hover);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover {
  background-color: var(--bg-body);
  color: var(--text-main);
}

.action-btn.danger {
  background-color: #ef4444;
  color: white;
}

.action-btn.danger:hover {
  background-color: #dc2626;
}
</style>
