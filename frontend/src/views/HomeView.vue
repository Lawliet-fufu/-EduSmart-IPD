<script setup>
import { Users, BookOpen, CheckCircle, Clock } from 'lucide-vue-next'
import StatCard from '../components/dashboard/StatCard.vue'
import RecentNotices from '../components/dashboard/RecentNotices.vue'
</script>

<template>
  <div class="dashboard">
    <div class="welcome-section">
      <h1>Welcome back, Teacher Lawliet! 👋</h1>
      <p>Here's what's happening in your classes today.</p>
    </div>

    <div class="stats-grid">
      <StatCard 
        title="Total Students" 
        value="1,234" 
        trend="12%" 
        :trendUp="true"
        :icon="Users"
        color="#3b82f6"
      />
      <StatCard 
        title="Pending Assignments" 
        value="23" 
        trend="5" 
        :trendUp="false"
        :icon="BookOpen"
        color="#f59e0b"
      />
      <StatCard 
        title="Avg. Attendance" 
        value="95%" 
        trend="2%" 
        :trendUp="true"
        :icon="CheckCircle"
        color="#10b981"
      />
      <StatCard 
        title="Upcoming Classes" 
        value="4" 
        :icon="Clock"
        color="#8b5cf6"
      />
    </div>

    <div class="dashboard-content">
      <div class="main-column">
        <!-- Placeholder for a chart or main widget -->
        <div class="chart-placeholder">
          <h3>Student Performance Overview</h3>
          <div class="placeholder-box">
            <span>Chart Component Coming Soon</span>
          </div>
        </div>
      </div>
      <div class="side-column">
        <RecentNotices />
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

.chart-placeholder {
  background-color: var(--bg-surface);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
  height: 100%;
  min-height: 400px;
  display: flex;
  flex-direction: column;
}

.chart-placeholder h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-main);
  margin-bottom: 1.5rem;
}

.placeholder-box {
  flex: 1;
  background-color: var(--bg-body);
  border: 2px dashed var(--border-color);
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-weight: 500;
}

@media (max-width: 1024px) {
  .dashboard-content {
    grid-template-columns: 1fr;
  }
}
</style>
