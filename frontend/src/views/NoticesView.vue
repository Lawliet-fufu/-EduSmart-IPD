<script setup>
import { ref, computed, onMounted } from 'vue'
import { Bell, Plus, AlertCircle, Info, Calendar, User, X } from 'lucide-vue-next'
import { getNotices, createNotice, updateNotice, deleteNotice } from '../api/notices.js'
import { useAuthStore } from '../stores/auth.js'

const authStore = useAuthStore()
const showCreateModal = ref(false)
const showViewModal = ref(false)
const notices = ref([])
const isLoading = ref(false)
const error = ref('')

// 当前查看/编辑的通知
const viewingNotice = ref(null)
const editingNotice = ref(null)

// 创建/编辑表单数据
const noticeForm = ref({
  title: '',
  content: '',
  date: new Date().toISOString().split('T')[0], // 默认今天
  priority: 'normal',
  category: ''
})

// 加载通知列表
const loadNotices = async () => {
  isLoading.value = true
  error.value = ''
  try {
    const data = await getNotices()
    notices.value = data.map(item => ({
      ...item,
      author: item.author?.full_name || item.author?.username || 'Unknown'
    }))
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load notices'
    console.error('Error loading notices:', err)
  } finally {
    isLoading.value = false
  }
}

// 创建通知
const handleCreateNotice = async () => {
  if (!noticeForm.value.title || !noticeForm.value.content) {
    error.value = 'Title and content are required'
    return
  }

  isLoading.value = true
  error.value = ''
  try {
    await createNotice(noticeForm.value)
    showCreateModal.value = false
    resetForm()
    await loadNotices()
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to create notice'
  } finally {
    isLoading.value = false
  }
}

// 查看通知详情
const handleViewNotice = (notice) => {
  viewingNotice.value = notice
  showViewModal.value = true
}

// 编辑通知
const handleEditNotice = (notice) => {
  editingNotice.value = notice
  noticeForm.value = {
    title: notice.title,
    content: notice.content,
    date: notice.date,
    priority: notice.priority,
    category: notice.category || ''
  }
  showCreateModal.value = true
}

// 更新通知
const handleUpdateNotice = async () => {
  if (!noticeForm.value.title || !noticeForm.value.content) {
    error.value = 'Title and content are required'
    return
  }

  isLoading.value = true
  error.value = ''
  try {
    await updateNotice(editingNotice.value.id, noticeForm.value)
    showCreateModal.value = false
    editingNotice.value = null
    resetForm()
    await loadNotices()
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to update notice'
  } finally {
    isLoading.value = false
  }
}

// 删除通知
const handleDeleteNotice = async (id) => {
  if (!confirm('Are you sure you want to delete this notice?')) {
    return
  }

  isLoading.value = true
  error.value = ''
  try {
    await deleteNotice(id)
    await loadNotices()
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to delete notice'
  } finally {
    isLoading.value = false
  }
}

// 保存通知（创建或更新）
const handleSaveNotice = () => {
  if (editingNotice.value) {
    handleUpdateNotice()
  } else {
    handleCreateNotice()
  }
}

// 重置表单
const resetForm = () => {
  noticeForm.value = {
    title: '',
    content: '',
    date: new Date().toISOString().split('T')[0],
    priority: 'normal',
    category: ''
  }
  editingNotice.value = null
  error.value = ''
}

// 关闭模态框
const closeModal = () => {
  showCreateModal.value = false
  showViewModal.value = false
  viewingNotice.value = null
  resetForm()
}

// 检查是否有权限创建/编辑/删除通知
const canManageNotices = computed(() => {
  return authStore.isAdmin || authStore.isTeacher
})

const getPriorityColor = (priority) => {
  return priority === 'important' ? '#ef4444' : '#10b981'
}

const getPriorityIcon = (priority) => {
  return priority === 'important' ? AlertCircle : Info
}

// 组件挂载时加载数据
onMounted(() => {
  loadNotices()
})
</script>

<template>
  <div class="notices-container">
    <div class="page-header">
      <div>
        <h1>Notices & Announcements</h1>
        <p>Important information and updates</p>
      </div>
      <button v-if="canManageNotices" @click="showCreateModal = true" class="create-btn">
        <Plus :size="20" />
        Post Notice
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading && notices.length === 0" class="loading-state">
      <p>Loading notices...</p>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="error-banner">
      {{ error }}
    </div>

    <!-- Notices List -->
    <div v-if="!isLoading || notices.length > 0" class="notices-list">
      <div v-for="notice in notices" :key="notice.id" class="notice-card"
        :class="{ important: notice.priority === 'important' }">
        <div class="notice-header">
          <div class="priority-indicator">
            <component :is="getPriorityIcon(notice.priority)" :size="20"
              :style="{ color: getPriorityColor(notice.priority) }" />
          </div>
          <div class="notice-title-section">
            <h3>{{ notice.title }}</h3>
            <div class="notice-meta">
              <span v-if="notice.category" class="category-badge">{{ notice.category }}</span>
              <span v-if="notice.category" class="separator">•</span>
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
          <p>{{ notice.content.length > 150 ? notice.content.substring(0, 150) + '...' : notice.content }}</p>
        </div>

        <div class="notice-actions">
          <button class="action-btn" @click="handleViewNotice(notice)">View Full Notice</button>
          <button v-if="canManageNotices" class="action-btn secondary" @click="handleEditNotice(notice)">
            Edit
          </button>
          <button v-if="canManageNotices" class="action-btn secondary text-danger"
            @click="handleDeleteNotice(notice.id)">
            Delete
          </button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ editingNotice ? 'Edit Notice' : 'Post New Notice' }}</h2>
          <button @click="closeModal" class="close-icon-btn">
            <X :size="24" />
          </button>
        </div>

        <form @submit.prevent="handleSaveNotice" class="notice-form">
          <div class="form-group">
            <label>Title *</label>
            <input v-model="noticeForm.title" type="text" placeholder="Enter notice title" required />
          </div>

          <div class="form-group">
            <label>Content *</label>
            <textarea v-model="noticeForm.content" placeholder="Enter notice content" rows="5" required></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Date</label>
              <input v-model="noticeForm.date" type="date" />
            </div>

            <div class="form-group">
              <label>Priority</label>
              <select v-model="noticeForm.priority">
                <option value="normal">Normal</option>
                <option value="important">Important</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>Category</label>
            <input v-model="noticeForm.category" type="text" placeholder="e.g., Academic, Event, Facility" />
          </div>

          <div v-if="error" class="form-error">
            {{ error }}
          </div>

          <div class="modal-actions">
            <button type="button" @click="closeModal" class="btn-secondary">Cancel</button>
            <button type="submit" :disabled="isLoading" class="btn-primary">
              {{ isLoading ? 'Saving...' : (editingNotice ? 'Update' : 'Create') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- View Notice Modal -->
    <div v-if="showViewModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content view-modal" @click.stop>
        <div class="modal-header">
          <h2>{{ viewingNotice?.title }}</h2>
          <button @click="closeModal" class="close-icon-btn">
            <X :size="24" />
          </button>
        </div>

        <div class="view-notice-content">
          <div class="view-notice-meta">
            <span class="category-badge">{{ viewingNotice?.category || 'General' }}</span>
            <span class="separator">•</span>
            <span class="meta-item">
              <Calendar :size="14" />
              {{ viewingNotice?.date }}
            </span>
            <span class="separator">•</span>
            <span class="meta-item">
              <User :size="14" />
              {{ viewingNotice?.author }}
            </span>
            <span class="separator">•</span>
            <span class="priority-badge" :style="{
              backgroundColor: getPriorityColor(viewingNotice?.priority),
              color: 'white',
              padding: '0.25rem 0.75rem',
              borderRadius: '999px',
              fontSize: '0.75rem',
              fontWeight: '600'
            }">
              {{ viewingNotice?.priority === 'important' ? 'Important' : 'Normal' }}
            </span>
          </div>

          <div class="view-notice-body">
            <p>{{ viewingNotice?.content }}</p>
          </div>
        </div>

        <div class="modal-actions">
          <button @click="closeModal" class="btn-primary">Close</button>
        </div>
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

.close-icon-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.close-icon-btn:hover {
  color: var(--text-main);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.modal-header h2 {
  margin: 0;
}

.notice-form {
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
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
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
  border: none;
}

.btn-primary {
  background-color: var(--primary);
  color: white;
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

.view-modal {
  max-width: 600px;
}

.view-notice-content {
  margin-bottom: 1.5rem;
}

.view-notice-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  font-size: 0.875rem;
  color: var(--text-muted);
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.view-notice-body {
  padding: 1rem;
  background-color: var(--bg-body);
  border-radius: 0.5rem;
}

.view-notice-body p {
  color: var(--text-main);
  line-height: 1.8;
  font-size: 0.9375rem;
  white-space: pre-wrap;
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
</style>
