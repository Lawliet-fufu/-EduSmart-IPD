<script setup>
import { ref, onMounted, watch } from 'vue'
import { Users, BookOpen, Bell, Clock, RefreshCcw } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth.js'
import { getDashboardSummary } from '../api/dashboard.js'
import { getClasses, getClassGradeDistribution } from '../api/classes.js'
import { getNotice } from '../api/notices.js'
import StatCard from '../components/dashboard/StatCard.vue'
import RecentNotices from '../components/dashboard/RecentNotices.vue'

// chart.js
import { Line } from 'vue-chartjs'
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Filler,
  Legend,
  Tooltip,
  Title,
} from 'chart.js'
Chart.register(LineController, LineElement, PointElement, LinearScale, CategoryScale, Filler, Legend, Tooltip, Title)

const authStore = useAuthStore()

// 统计数字
const totalStudents = ref(0)
const pendingAssignments = ref(0)
const totalNotices = ref(0)
const classCount = ref(0)
const recentNotices = ref([])

// 班级与分布
const classOptions = ref([]) // {id, name}
const selectedClassId = ref(null)
const isChartLoading = ref(false)

const labels = ref([])
const datasets = ref([])

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  plugins: {
    legend: { position: 'top', labels: { usePointStyle: true } },
    title: { display: false }
  },
  scales: {
    x: {
      title: { display: true, text: 'Score (0-100)' },
      ticks: { maxTicksLimit: 11 }
    },
    y: {
      beginAtZero: true,
      title: { display: true, text: 'Students' },
      ticks: { stepSize: 1 }
    }
  }
})

const buildDatasets = (dist) => {
  const palette = {
    chinese: '#10b981',
    math: '#3b82f6',
    english: '#f59e0b',
    average: '#8b5cf6',
  }
  return [
    { key: 'chinese', label: 'Chinese', color: palette.chinese },
    { key: 'math', label: 'Math', color: palette.math },
    { key: 'english', label: 'English', color: palette.english },
    { key: 'average', label: 'Average', color: palette.average }
  ].map(s => ({
    label: s.label,
    data: dist[s.key] || [],
    borderColor: s.color,
    backgroundColor: s.color + '33',
    tension: 0.35,
    fill: false,
    pointRadius: 0,
    borderWidth: 2
  }))
}

const loadDistribution = async () => {
  if (!selectedClassId.value) return
  isChartLoading.value = true
  try {
    const dist = await getClassGradeDistribution(selectedClassId.value)
    labels.value = dist.labels
    datasets.value = buildDatasets(dist)
  } catch (e) {
    console.error('Failed to load grade distribution:', e)
  } finally {
    isChartLoading.value = false
  }
}

onMounted(async () => {
  try {
    const data = await getDashboardSummary()
    totalStudents.value = data.total_students || 0
    pendingAssignments.value = data.pending_assignments || 0
    totalNotices.value = data.total_notices || 0
    classCount.value = data.class_count || 0
    recentNotices.value = Array.isArray(data.recent_notices) ? data.recent_notices : []
  } catch (e) {
    console.error('Failed to load dashboard summary:', e)
  }

  // 加载班级
  try {
    const classes = await getClasses()
    classOptions.value = classes.map(c => ({ id: c.id, name: c.name }))
    selectedClassId.value = classes[0]?.id || null
    await loadDistribution()
  } catch (e) {
    console.error('Failed to load classes:', e)
  }
})

watch(selectedClassId, () => loadDistribution())

// 通知详情弹窗
const showNoticeModal = ref(false)
const viewingNotice = ref(null)
const isNoticeLoading = ref(false)

const handleOpenNotice = async (short) => {
  isNoticeLoading.value = true
  try {
    const full = await getNotice(short.id)
    viewingNotice.value = full
    showNoticeModal.value = true
  } catch (e) {
    console.error('Failed to load notice detail:', e)
  } finally {
    isNoticeLoading.value = false
  }
}

const closeNotice = () => {
  showNoticeModal.value = false
  viewingNotice.value = null
}

// Get welcome message based on user role
const getWelcomeMessage = () => {
  const name = authStore.user?.name || 'User'
  const role = authStore.user?.role || 'user'
  
  if (role === 'teacher') {
    return `Welcome back, ${name}! 👋`
  } else if (role === 'student') {
    return `Welcome back, ${name}! 📚`
  } else if (role === 'admin') {
    return `Welcome back, ${name}! 🔧`
  }
  return `Welcome back, ${name}! 👋`
}

const getSubMessage = () => {
  const role = authStore.user?.role || 'user'
  
  if (role === 'teacher') {
    return "Here's what's happening in your classes today."
  } else if (role === 'student') {
    return "Here's your learning progress and upcoming assignments."
  } else if (role === 'admin') {
    return "Here's an overview of the platform."
  }
  return "Here's what's happening today."
}
</script>

<template>
  <div class="dashboard">
    <div class="welcome-section">
      <h1>{{ getWelcomeMessage() }}</h1>
      <p>{{ getSubMessage() }}</p>
    </div>

    <div class="stats-grid">
      <StatCard 
        title="Total Students" 
        :value="totalStudents" 
        :icon="Users"
        color="#3b82f6"
      />
      <StatCard 
        title="Pending Assignments" 
        :value="pendingAssignments" 
        :icon="BookOpen"
        color="#f59e0b"
      />
      <StatCard 
        title="Total Notices" 
        :value="totalNotices" 
        :icon="Bell"
        color="#10b981"
      />
      <StatCard 
        title="Class Count" 
        :value="classCount" 
        :icon="Clock"
        color="#8b5cf6"
      />
    </div>

    <div class="dashboard-content">
      <div class="main-column">
        <div class="chart-card">
          <div class="chart-header">
            <h3>Student Performance Overview</h3>
            <div class="chart-actions">
              <select v-model="selectedClassId" class="class-select">
                <option v-for="c in classOptions" :key="c.id" :value="c.id">{{ c.name }}</option>
              </select>
              <button class="icon-btn" @click="loadDistribution" title="Refresh">
                <RefreshCcw :size="18" />
              </button>
            </div>
          </div>
          <div class="chart-body">
            <div v-if="isChartLoading" class="loading">Loading...</div>
            <Line v-else :data="{ labels, datasets }" :options="chartOptions" />
          </div>
        </div>
      </div>
      <div class="side-column">
        <RecentNotices :items="recentNotices" @view="handleOpenNotice" />
      </div>
    </div>

    <!-- 通知详情弹窗 -->
    <div v-if="showNoticeModal" class="modal-overlay" @click="closeNotice">
      <div class="modal-content view-modal" @click.stop>
        <div class="modal-header">
          <h2>{{ viewingNotice?.title }}</h2>
          <button @click="closeNotice" class="close-icon-btn">✕</button>
        </div>
        <div class="view-notice-content">
          <div class="view-notice-meta">
            <span class="category-badge">{{ viewingNotice?.category || 'General' }}</span>
            <span class="separator">•</span>
            <span class="meta-item">{{ viewingNotice?.date }}</span>
            <span class="separator">•</span>
            <span class="priority-badge" :class="{ important: viewingNotice?.priority==='important' }">
              {{ viewingNotice?.priority==='important' ? 'Important' : 'Normal' }}
            </span>
          </div>
          <div class="view-notice-body">
            <p v-if="!isNoticeLoading">{{ viewingNotice?.content }}</p>
            <p v-else class="text-muted">Loading...</p>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="closeNotice" class="btn-primary">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.welcome-section h1 {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 0.5rem;
}

.welcome-section p {
  color: var(--text-muted);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
}

.chart-card {
  background-color: var(--bg-surface);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
  min-height: 420px;
  display: flex;
  flex-direction: column;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 1rem;
}

.chart-header h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-main);
}

.chart-actions { display: flex; gap: .5rem; align-items: center; }
.class-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border-color);
  background: var(--bg-body);
  color: var(--text-main);
  border-radius: 0.5rem;
}
.icon-btn { padding: .5rem; border-radius: .5rem; border:1px solid var(--border-color); }
.icon-btn:hover { background: var(--bg-body); }

.chart-body { flex:1; position: relative; }
.loading { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; color: var(--text-muted); }

/* Modal (borrowed styles from Notices) */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-content { background: var(--bg-surface); padding: 2rem; border-radius: 1rem; max-width: 600px; width: 92%; }
.modal-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem; }
.close-icon-btn { background: transparent; color: var(--text-muted); }
.view-notice-meta { display:flex; gap:.5rem; align-items:center; flex-wrap:wrap; color: var(--text-muted); margin-bottom:1rem; border-bottom:1px solid var(--border-color); padding-bottom: .75rem; }
.category-badge { background: var(--primary); color:#fff; padding: 0.1rem .5rem; border-radius:999px; font-size:.75rem; }
.priority-badge { background: #10b981; color:#fff; padding: 0.1rem .5rem; border-radius:999px; font-size:.75rem; }
.priority-badge.important { background:#ef4444; }
.view-notice-body { background: var(--bg-body); border-radius:.5rem; padding:1rem; }
.btn-primary { background: var(--primary); color:#fff; padding:.6rem 1.2rem; border-radius:.5rem; }

@media (max-width: 1024px) {
  .dashboard-content {
    grid-template-columns: 1fr;
  }
}
</style>
