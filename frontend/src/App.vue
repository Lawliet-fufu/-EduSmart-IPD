<script setup>
import { useRoute } from 'vue-router'
import Sidebar from './components/layout/Sidebar.vue'
import Header from './components/layout/Header.vue'

const route = useRoute()
</script>

<template>
  <div class="app-layout">
    <Sidebar v-if="route.meta.requiresAuth" />
    <div :class="{ 'main-wrapper': route.meta.requiresAuth, 'full-width': !route.meta.requiresAuth }">
      <Header v-if="route.meta.requiresAuth" />
      <main class="main-content">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
}

.main-wrapper {
  flex: 1;
  margin-left: 260px; /* Sidebar width */
  display: flex;
  flex-direction: column;
}

.full-width {
  width: 100%;
}

.main-content {
  flex: 1;
  padding: 2rem;
  /* Slightly darker green tinted background */
  background: rgba(236, 253, 245, 0.75);
}
</style>
