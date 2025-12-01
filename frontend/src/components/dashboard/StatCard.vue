<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: String,
  value: [String, Number],
  icon: Object,
  trend: String,
  trendUp: Boolean,
  color: String
})

const iconBgColor = computed(() => {
  const colors = {
    primary: '#10b981',
    blue: '#3b82f6',
    purple: '#8b5cf6',
    orange: '#f97316'
  }
  return colors[props.color] || colors.primary
})
</script>

<template>
  <div class="stat-card">
    <div class="stat-icon" :style="{ backgroundColor: iconBgColor }">
      <component :is="icon" :size="24" />
    </div>
    <div class="stat-content">
      <h3 class="stat-title">{{ title }}</h3>
      <p class="stat-value">{{ value }}</p>
      <span v-if="trend" class="stat-trend" :class="{ 'trend-up': trendUp, 'trend-down': !trendUp }">
        {{ trendUp ? '' : '' }} {{ trend }}
      </span>
    </div>
  </div>
</template>

<style scoped>
.stat-card {
  background: var(--bg-surface);
  border-radius: 1rem;
  padding: 1.5rem;
  display: flex;
  gap: 1rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.stat-title {
  font-size: 0.875rem;
  color: var(--text-muted);
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 0.25rem;
}

.stat-trend {
  font-size: 0.75rem;
  font-weight: 500;
}

.stat-trend.trend-up {
  color: #10b981;
}

.stat-trend.trend-down {
  color: #ef4444;
}
</style>
