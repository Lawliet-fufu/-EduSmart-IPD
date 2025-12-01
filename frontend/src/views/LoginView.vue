<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'
import { BookOpen, User, Lock, ArrowRight, UserCog, GraduationCap, Users } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')
const isLoading = ref(false)
const selectedAccount = ref(null)

// Demo accounts with Lucide icons
const demoAccounts = [
  { username: 'admin', role: 'Admin', icon: UserCog },
  { username: 'teacher', role: 'Teacher', icon: GraduationCap },
  { username: 'student', role: 'Student', icon: User }
]

const selectAccount = (account) => {
  selectedAccount.value = account.username
  username.value = account.username
  password.value = '123456'
}

const handleLogin = async () => {
  error.value = ''
  isLoading.value = true
  
  // Simulate network delay
  setTimeout(() => {
    const success = authStore.login(username.value, password.value)
    if (success) {
      router.push('/')
    } else {
      error.value = 'Invalid username or password'
    }
    isLoading.value = false
  }, 800)
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <div class="brand-header">
        <div class="logo-icon">
          <BookOpen class="text-white" :size="32" />
        </div>
        <h1>EduSmart</h1>
        <p>Intelligent Home-School Platform</p>
      </div>

      <!-- Demo Accounts -->
      <div class="demo-accounts">
        <p class="demo-label">Quick Login (Demo Accounts)</p>
        <div class="accounts-grid">
          <div 
            v-for="account in demoAccounts" 
            :key="account.username"
            @click="selectAccount(account)"
            :class="['account-card', { 'selected': selectedAccount === account.username }]"
          >
            <component :is="account.icon" :size="32" class="account-icon-svg" />
            <div class="account-info">
              <span class="account-role">{{ account.role }}</span>
              <span class="account-username">{{ account.username }}</span>
            </div>
          </div>
        </div>
        <p class="demo-hint">Password: <code>123456</code></p>
      </div>

      <div class="divider">
        <span>Or enter manually</span>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label>Username</label>
          <div class="input-wrapper">
            <User :size="18" class="input-icon" />
            <input 
              v-model="username" 
              type="text" 
              placeholder="Enter your username"
              required
            />
          </div>
        </div>

        <div class="form-group">
          <label>Password</label>
          <div class="input-wrapper">
            <Lock :size="18" class="input-icon" />
            <input 
              v-model="password" 
              type="password" 
              placeholder="Enter your password"
              required
            />
          </div>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button type="submit" :disabled="isLoading" class="login-btn">
          <span v-if="!isLoading">Sign In</span>
          <span v-else>Signing in...</span>
          <ArrowRight v-if="!isLoading" :size="18" />
        </button>
      </form>
      
      <div class="login-footer">
        <p>Demo Credentials: admin / 123456</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.login-card {
  width: 100%;
  max-width: 580px;
  background: var(--bg-surface);
  padding: 3rem;
  border-radius: 1.5rem;
  box-shadow: var(--shadow-lg);
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.brand-header {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-icon {
  width: 64px;
  height: 64px;
  background-color: var(--primary);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.3);
}

.brand-header h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 0.25rem;
}

.brand-header p {
  color: var(--text-muted);
  font-size: 0.875rem;
}

.login-form {
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

.login-btn {
  margin-top: 0.5rem;
  background-color: var(--primary);
  color: white;
  padding: 0.875rem;
  border-radius: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.login-btn:hover:not(:disabled) {
  background-color: var(--primary-hover);
  transform: translateY(-1px);
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  text-align: center;
  background-color: #fef2f2;
  padding: 0.5rem;
  border-radius: 0.5rem;
}

.login-footer {
  text-align: center;
  font-size: 0.75rem;
  color: var(--text-light);
  border-top: 1px solid var(--border-color);
  padding-top: 1.5rem;
}

/* Demo Accounts Styles */
.demo-accounts {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.demo-label {
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--text-main);
  text-align: center;
}

.accounts-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
}

.account-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 0.75rem;
  border: 2px solid var(--border-color);
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
  background: var(--bg-surface);
}

.account-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: var(--primary);
}

.account-card.selected {
  background: #f1f5f9;
  border-color: var(--primary);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
}

.account-icon-svg {
  color: var(--primary);
  transition: all 0.2s;
}

.account-card.selected .account-icon-svg {
  color: var(--primary);
}

.account-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.account-role {
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--text-main);
  transition: all 0.2s;
}

.account-card.selected .account-role {
  color: var(--text-main);
}

.account-username {
  font-size: 0.75rem;
  color: var(--text-muted);
  transition: all 0.2s;
}

.account-card.selected .account-username {
  color: var(--text-muted);
}

.demo-hint {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-align: center;
}

.demo-hint code {
  background: #e0e7ff;
  color: #4f46e5;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-family: monospace;
  font-size: 0.6875rem;
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: -0.5rem 0;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid var(--border-color);
}

.divider span {
  padding: 0 1rem;
  font-size: 0.75rem;
  color: var(--text-light);
}
</style>
