<script setup>
import { ref, watch, onMounted } from 'vue'
import { User, Mail, Lock, Bell, Globe, Moon } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth.js'
import { useLocaleStore } from '../stores/locale.js'
import api from '../api/index.js'

const authStore = useAuthStore()
const localeStore = useLocaleStore()

// Settings state
const profile = ref({
  name: authStore.user?.name || 'User',
  email: authStore.user?.email || 'user@edusmart.com',
  role: authStore.user?.role || 'User'
})

const preferences = ref({
  notifications: true,
  emailAlerts: false,
  darkMode: false,
  language: localeStore.locale
})

const isLoading = ref(false)
const saveMessage = ref('')

// Load preferences from backend on mount
onMounted(async () => {
  isLoading.value = true
  try {
    const response = await api.get('/auth/preferences')
    if (response.data) {
      preferences.value = {
        notifications: response.data.notifications,
        emailAlerts: response.data.email_alerts,
        darkMode: response.data.dark_mode,
        language: response.data.language
      }
      // Sync locale store
      localeStore.setLocale(preferences.value.language)
      // Apply dark mode if enabled
      if (preferences.value.darkMode) {
        authStore.applyDarkMode(true)
      }
    }
  } catch (error) {
    console.error('Failed to load preferences:', error)
    // Fall back to localStorage
    preferences.value = {
      notifications: localStorage.getItem('pref_notifications') !== 'false',
      emailAlerts: localStorage.getItem('pref_emailAlerts') === 'true',
      darkMode: localStorage.getItem('pref_darkMode') === 'true',
      language: localeStore.locale
    }
    // Apply dark mode if enabled in localStorage
    if (preferences.value.darkMode) {
      authStore.applyDarkMode(true)
    }
  } finally {
    isLoading.value = false
  }
})

// Watch for dark mode changes
watch(() => preferences.value.darkMode, (newVal) => {
  authStore.applyDarkMode(newVal)
})

// Watch for language changes
watch(() => preferences.value.language, (newVal) => {
  localeStore.setLocale(newVal)
})

const saveSettings = async () => {
  isLoading.value = true
  saveMessage.value = ''
  try {
    await api.put('/auth/preferences', {
      notifications: preferences.value.notifications,
      emailAlerts: preferences.value.emailAlerts,
      darkMode: preferences.value.darkMode,
      language: preferences.value.language
    })
    saveMessage.value = localeStore.t.value('settings.saveSuccess')
    setTimeout(() => {
      saveMessage.value = ''
    }, 3000)
  } catch (error) {
    console.error('Failed to save preferences:', error)
    saveMessage.value = localeStore.t.value('settings.saveFailed')
    // Fall back to localStorage
    localStorage.setItem('pref_notifications', preferences.value.notifications)
    localStorage.setItem('pref_emailAlerts', preferences.value.emailAlerts)
    localStorage.setItem('pref_darkMode', preferences.value.darkMode)
    localStorage.setItem('pref_language', preferences.value.language)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="settings-container">
    <div class="settings-header">
      <h1>{{ localeStore.t.value('settings.title') }}</h1>
      <p>{{ localeStore.t.value('settings.description') }}</p>
    </div>

    <!-- Profile Section -->
    <div class="settings-section">
      <div class="section-header">
        <User :size="20" />
        <h2>{{ localeStore.t.value('settings.profile') }}</h2>
      </div>
      <div class="section-content">
        <div class="form-group">
          <label>{{ localeStore.t.value('settings.fullName') }}</label>
          <div class="input-wrapper">
            <User :size="18" class="input-icon" />
            <input v-model="profile.name" type="text" />
          </div>
        </div>

        <div class="form-group">
          <label>{{ localeStore.t.value('settings.email') }}</label>
          <div class="input-wrapper">
            <Mail :size="18" class="input-icon" />
            <input v-model="profile.email" type="email" />
          </div>
        </div>

        <div class="form-group">
          <label>{{ localeStore.t.value('settings.role') }}</label>
          <div class="input-wrapper">
            <User :size="18" class="input-icon" />
            <input v-model="profile.role" type="text" readonly />
          </div>
        </div>
      </div>
    </div>

    <!-- Security Section -->
    <div class="settings-section">
      <div class="section-header">
        <Lock :size="20" />
        <h2>{{ localeStore.t.value('settings.security') }}</h2>
      </div>
      <div class="section-content">
        <div class="form-group">
          <label>{{ localeStore.t.value('settings.currentPassword') }}</label>
          <div class="input-wrapper">
            <Lock :size="18" class="input-icon" />
            <input type="password" placeholder="••••••••" />
          </div>
        </div>

        <div class="form-group">
          <label>{{ localeStore.t.value('settings.newPassword') }}</label>
          <div class="input-wrapper">
            <Lock :size="18" class="input-icon" />
            <input type="password" placeholder="••••••••" />
          </div>
        </div>

        <div class="form-group">
          <label>{{ localeStore.t.value('settings.confirmPassword') }}</label>
          <div class="input-wrapper">
            <Lock :size="18" class="input-icon" />
            <input type="password" placeholder="••••••••" />
          </div>
        </div>
      </div>
    </div>

    <!-- Preferences Section -->
    <div class="settings-section">
      <div class="section-header">
        <Bell :size="20" />
        <h2>{{ localeStore.t.value('settings.preferences') }}</h2>
      </div>
      <div class="section-content">
        <div class="preference-item">
          <div class="preference-info">
            <Bell :size="20" class="preference-icon" />
            <div>
              <h4>{{ localeStore.t.value('settings.pushNotifications') }}</h4>
              <p>{{ localeStore.t.value('settings.pushNotificationsDesc') }}</p>
            </div>
          </div>
          <label class="toggle-switch">
            <input v-model="preferences.notifications" type="checkbox" />
            <span class="toggle-slider"></span>
          </label>
        </div>

        <div class="preference-item">
          <div class="preference-info">
            <Mail :size="20" class="preference-icon" />
            <div>
              <h4>{{ localeStore.t.value('settings.emailAlerts') }}</h4>
              <p>{{ localeStore.t.value('settings.emailAlertsDesc') }}</p>
            </div>
          </div>
          <label class="toggle-switch">
            <input v-model="preferences.emailAlerts" type="checkbox" />
            <span class="toggle-slider"></span>
          </label>
        </div>

        <div class="preference-item">
          <div class="preference-info">
            <Moon :size="20" class="preference-icon" />
            <div>
              <h4>{{ localeStore.t.value('settings.darkMode') }}</h4>
              <p>{{ localeStore.t.value('settings.darkModeDesc') }}</p>
            </div>
          </div>
          <label class="toggle-switch">
            <input v-model="preferences.darkMode" type="checkbox" />
            <span class="toggle-slider"></span>
          </label>
        </div>

        <div class="preference-item">
          <div class="preference-info">
            <Globe :size="20" class="preference-icon" />
            <div>
              <h4>{{ localeStore.t.value('settings.language') }}</h4>
              <p>{{ localeStore.t.value('settings.languageDesc') }}</p>
            </div>
          </div>
          <select v-model="preferences.language" class="language-select">
            <option value="en">English</option>
            <option value="zh">中文</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Save Button -->
    <div class="settings-actions">
      <div v-if="saveMessage" class="save-message" :class="{ 'error': saveMessage.includes('Failed') || saveMessage.includes('失败') }">
        {{ saveMessage }}
      </div>
      <button @click="saveSettings" class="save-btn" :disabled="isLoading">
        {{ isLoading ? localeStore.t.value('settings.saving') : localeStore.t.value('settings.saveChanges') }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.settings-container {
  max-width: 900px;
  margin: 0 auto;
}

.settings-header {
  margin-bottom: 2rem;
}

.settings-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 0.5rem;
}

.settings-header p {
  color: var(--text-muted);
  font-size: 1rem;
}

.settings-section {
  background: var(--bg-surface);
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
  color: var(--primary);
}

.section-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-main);
}

.section-content {
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

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-light);
}

.input-wrapper input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.75rem;
  border: 1px solid var(--border-color);
  border-radius: 0.75rem;
  font-size: 0.9375rem;
  color: var(--text-main);
  background-color: var(--bg-body);
  transition: all 0.2s;
}

.input-wrapper input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.input-wrapper input:read-only {
  background-color: #f3f4f6;
  cursor: not-allowed;
}

.preference-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: var(--bg-body);
  border-radius: 0.75rem;
  transition: background 0.2s;
}

.preference-item:hover {
  background: #f3f4f6;
}

.preference-info {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.preference-icon {
  color: var(--text-muted);
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.preference-info h4 {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--text-main);
  margin-bottom: 0.25rem;
}

.preference-info p {
  font-size: 0.8125rem;
  color: var(--text-muted);
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 24px;
  flex-shrink: 0;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #cbd5e1;
  border-radius: 24px;
  transition: 0.3s;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  border-radius: 50%;
  transition: 0.3s;
}

.toggle-switch input:checked+.toggle-slider {
  background-color: var(--primary);
}

.toggle-switch input:checked+.toggle-slider:before {
  transform: translateX(24px);
}

.toggle-switch input:disabled+.toggle-slider {
  opacity: 0.5;
  cursor: not-allowed;
}

.language-select {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  background: var(--bg-surface);
  color: var(--text-main);
  font-size: 0.875rem;
  cursor: pointer;
  transition: border-color 0.2s;
}

.language-select:focus {
  outline: none;
  border-color: var(--primary);
}

.settings-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.save-message {
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  background-color: #d1fae5;
  color: #065f46;
  font-size: 0.875rem;
  font-weight: 500;
}

.save-message.error {
  background-color: #fee2e2;
  color: #991b1b;
}

.save-btn {
  background-color: var(--primary);
  color: white;
  padding: 0.875rem 2rem;
  border-radius: 0.75rem;
  font-weight: 600;
  font-size: 0.9375rem;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
}

.save-btn:hover:not(:disabled) {
  background-color: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
