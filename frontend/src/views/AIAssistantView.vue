<script setup>
import { ref, nextTick } from 'vue'
import { Send, Bot, User, Sparkles, Upload, Brain, FileText, Lightbulb } from 'lucide-vue-next'

const messageInput = ref('')
const chatContainer = ref(null)
const uploadedFile = ref(null)
const showMindMap = ref(false)
const showAnalysis = ref(false)
const analysisData = ref(null)

const messages = ref([
  {
    id: 1,
    type: 'ai',
    content: 'Hello! I\'m your AI teaching assistant. Upload a courseware file or ask me anything!',
    timestamp: '10:30 AM'
  }
])

const quickQuestions = ref([
  'How can I improve student engagement?',
  'Suggest activities for today\'s math lesson',
  'Help me create a quiz for Grade 3',
  'Best practices for online teaching'
])

// File upload handling
const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  // Check file type
  if (!file.name.endsWith('.docx')) {
    const errorMsg = {
      id: messages.value.length + 1,
      type: 'ai',
      content: '❌ Only .docx files are supported. Please upload a Word document.',
      timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
    }
    messages.value.push(errorMsg)
    scrollToBottom()
    return
  }

  uploadedFile.value = file

  // Show uploading message
  const uploadingMsg = {
    id: messages.value.length + 1,
    type: 'ai',
    content: `📄 Uploading "${file.name}"...\n\nAnalyzing courseware with AI...`,
    timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
  }
  messages.value.push(uploadingMsg)
  scrollToBottom()

  try {
    // Upload and analyze document
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch('http://127.0.0.1:5000/api/ai/analyze-document', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      throw new Error('Analysis failed')
    }

    const data = await response.json()
    analysisData.value = data.analysis

    // Show analysis results
    showAnalysis.value = true

    const successMsg = {
      id: messages.value.length + 1,
      type: 'ai',
      content: `✅ Document analyzed successfully!\n\n📊 Analysis complete! Check the results above.`,
      timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
    }
    messages.value.push(successMsg)
    scrollToBottom()

  } catch (error) {
    console.error('Error analyzing document:', error)
    const errorMsg = {
      id: messages.value.length + 1,
      type: 'ai',
      content: '❌ Sorry, I encountered an error analyzing the document. Please try again.',
      timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
    }
    messages.value.push(errorMsg)
    scrollToBottom()
  }
}

// Generate mind map (demo)
const generateMindMap = () => {
  showMindMap.value = true
  const mindMapMessage = {
    id: messages.value.length + 1,
    type: 'ai',
    content: '🧠 Mind map generated! Check the visualization above.',
    timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
  }
  messages.value.push(mindMapMessage)
  scrollToBottom()
}

// Show courseware analysis
const showCoursewareAnalysis = () => {
  showAnalysis.value = true
  const analysisMsg = {
    id: messages.value.length + 1,
    type: 'ai',
    content: '📊 Detailed courseware analysis displayed above!',
    timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
  }
  messages.value.push(analysisMsg)
  scrollToBottom()
}

const sendMessage = async () => {
  if (!messageInput.value.trim()) return

  const userQuery = messageInput.value
  messageInput.value = ''

  const userMessage = {
    id: messages.value.length + 1,
    type: 'user',
    content: userQuery,
    timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
  }
  messages.value.push(userMessage)

  await nextTick()
  scrollToBottom()

  try {
    const aiResponseContent = await getAIResponse(userQuery)
    
    const aiMessage = {
      id: messages.value.length + 1,
      type: 'ai',
      content: aiResponseContent,
      timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
    }
    messages.value.push(aiMessage)
    scrollToBottom()
  } catch (error) {
    const errorMessage = {
      id: messages.value.length + 1,
      type: 'ai',
      content: 'Sorry, I encountered an error. Please try again.',
      timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
    }
    messages.value.push(errorMessage)
    scrollToBottom()
  }
}

const askQuickQuestion = (question) => {
  messageInput.value = question
  sendMessage()
}

// Call Backend API
const getAIResponse = async (query) => {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/ai/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: query })
    })

    if (!response.ok) {
      throw new Error('Network response was not ok')
    }

    const data = await response.json()
    return data.response
  } catch (error) {
    console.error('Error fetching AI response:', error)
    return "Sorry, the AI service is temporarily unavailable. Please try again later."
  }
}

const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}
</script>

<template>
  <div class="ai-assistant-container">
    <div class="page-header">
      <div class="header-content">
        <div class="ai-icon">
          <Sparkles :size="28" />
        </div>
        <div>
          <h1>AI Teaching Assistant</h1>
          <p>Upload courseware, generate mind maps, and get teaching insights</p>
        </div>
      </div>
      
      <!-- Feature Buttons -->
      <div class="feature-buttons">
        <label class="feature-btn upload-btn">
          <Upload :size="18" />
          Upload Courseware
          <input type="file" @change="handleFileUpload" accept=".pdf,.ppt,.pptx,.doc,.docx" hidden />
        </label>
        <button @click="generateMindMap" class="feature-btn">
          <Brain :size="18" />
          Generate Mind Map
        </button>
        <button @click="showCoursewareAnalysis" class="feature-btn">
          <FileText :size="18" />
          Analyze Content
        </button>
      </div>
    </div>

    <!-- Mind Map Visualization (Demo) -->
    <div v-if="showMindMap" class="visualization-panel">
      <div class="panel-header">
        <Brain :size="20" />
        <h3>Mind Map - Course Structure</h3>
        <button @click="showMindMap = false" class="close-btn">×</button>
      </div>
      <div class="mind-map-container">
        <div class="mind-map-demo">
          <div class="central-node">Math Course</div>
          <div class="branch branch-1">
            <div class="node">Geometry</div>
            <div class="sub-node">Shapes</div>
            <div class="sub-node">Angles</div>
          </div>
          <div class="branch branch-2">
            <div class="node">Algebra</div>
            <div class="sub-node">Equations</div>
            <div class="sub-node">Variables</div>
          </div>
          <div class="branch branch-3">
            <div class="node">Statistics</div>
            <div class="sub-node">Graphs</div>
            <div class="sub-node">Data</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Analysis Panel (Real Data) -->
    <div v-if="showAnalysis && analysisData" class="visualization-panel">
      <div class="panel-header">
        <FileText :size="20" />
        <h3>Courseware Analysis</h3>
        <button @click="showAnalysis = false" class="close-btn">×</button>
      </div>
      <div class="analysis-grid">
        <div class="analysis-card">
          <Lightbulb :size="24" class="card-icon" />
          <h4>Key Topics</h4>
          <ul>
            <li v-for="(topic, index) in analysisData.key_topics" :key="index">{{ topic }}</li>
          </ul>
        </div>
        <div class="analysis-card">
          <Brain :size="24" class="card-icon" />
          <h4>Learning Objectives</h4>
          <ul>
            <li v-for="(objective, index) in analysisData.learning_objectives" :key="index">{{ objective }}</li>
          </ul>
        </div>
        <div class="analysis-card">
          <FileText :size="24" class="card-icon" />
          <h4>Suggested Activities</h4>
          <ul>
            <li v-for="(activity, index) in analysisData.suggested_activities" :key="index">{{ activity }}</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="chat-layout">
      <!-- Quick Questions Sidebar -->
      <div class="quick-questions-panel">
        <h3>Quick Questions</h3>
        <p class="panel-subtitle">Click to ask</p>
        <div class="questions-list">
          <button
            v-for="(question, index) in quickQuestions"
            :key="index"
            @click="askQuickQuestion(question)"
            class="quick-question-btn"
          >
            <Bot :size="16" />
            {{ question }}
          </button>
        </div>
        
        <!-- Upload Status -->
        <div v-if="uploadedFile" class="upload-status">
          <FileText :size="16" />
          <span>{{ uploadedFile.name }}</span>
        </div>
      </div>

      <!-- Chat Area -->
      <div class="chat-panel">
        <div ref="chatContainer" class="messages-container">
          <div
            v-for="message in messages"
            :key="message.id"
            :class="['message', message.type]"
          >
            <div class="message-avatar">
              <Bot v-if="message.type === 'ai'" :size="20" />
              <User v-else :size="20" />
            </div>
            <div class="message-content">
              <div class="message-bubble">
                <p>{{ message.content }}</p>
              </div>
              <span class="message-time">{{ message.timestamp }}</span>
            </div>
          </div>
        </div>

        <!-- Input Area -->
        <div class="input-area">
          <div class="input-wrapper">
            <input
              v-model="messageInput"
              @keyup.enter="sendMessage"
              type="text"
              placeholder="Ask me anything about teaching..."
              class="message-input"
            />
            <button @click="sendMessage" class="send-btn" :disabled="!messageInput.trim()">
              <Send :size="20" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ai-assistant-container {
  max-width: 1400px;
  margin: 0 auto;
  height: calc(100vh - 140px);
  display: flex;
  flex-direction: column;
}

.page-header {
  margin-bottom: 1.5rem;
}

.header-content {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
}

.ai-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, var(--primary) 0%, #059669 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 0.25rem;
}

.page-header p {
  color: var(--text-muted);
}

/* Feature Buttons */
.feature-buttons {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.feature-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-main);
  transition: all 0.2s;
  cursor: pointer;
}

.feature-btn:hover {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
  transform: translateY(-2px);
}

.upload-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
}

/* Visualization Panels */
.visualization-panel {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 1rem;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  color: var(--primary);
}

.panel-header h3 {
  flex: 1;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-main);
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #fee2e2;
  color: #ef4444;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #ef4444;
  color: white;
}

/* Mind Map Demo */
.mind-map-container {
  min-height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mind-map-demo {
  position: relative;
  width: 100%;
  height: 250px;
}

.central-node {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: linear-gradient(135deg, var(--primary) 0%, #059669 100%);
  color: white;
  padding: 1rem 2rem;
  border-radius: 999px;
  font-weight: 700;
  font-size: 1.125rem;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.branch {
  position: absolute;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.branch-1 {
  top: 10%;
  left: 10%;
}

.branch-2 {
  bottom: 10%;
  left: 15%;
}

.branch-3 {
  top: 15%;
  right: 10%;
}

.node {
  background: #3b82f6;
  color: white;
  padding: 0.625rem 1.25rem;
  border-radius: 999px;
  font-weight: 600;
  font-size: 0.875rem;
}

.sub-node {
  background: var(--bg-body);
  border: 2px solid #3b82f6;
  color: #3b82f6;
  padding: 0.5rem 1rem;
  border-radius: 999px;
  font-size: 0.8125rem;
  margin-left: 1rem;
}

/* Analysis Grid */
.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.analysis-card {
  background: var(--bg-body);
  border: 1px solid var(--border-color);
  border-radius: 0.75rem;
  padding: 1.25rem;
}

.card-icon {
  color: var(--primary);
  margin-bottom: 0.75rem;
}

.analysis-card h4 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-main);
  margin-bottom: 0.75rem;
}

.analysis-card ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.analysis-card li {
  font-size: 0.875rem;
  color: var(--text-muted);
  padding-left: 1.25rem;
  position: relative;
}

.analysis-card li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: var(--primary);
  font-weight: bold;
}

.chat-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 1.5rem;
  flex: 1;
  min-height: 0;
}

.quick-questions-panel {
  background: var(--bg-surface);
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid var(--border-color);
  overflow-y: auto;
}

.quick-questions-panel h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-main);
  margin-bottom: 0.25rem;
}

.panel-subtitle {
  font-size: 0.8125rem;
  color: var(--text-muted);
  margin-bottom: 1rem;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.quick-question-btn {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  background: var(--bg-body);
  border: 1px solid var(--border-color);
  border-radius: 0.75rem;
  text-align: left;
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--text-main);
  transition: all 0.2s;
}

.quick-question-btn:hover {
  background: white;
  border-color: var(--primary);
  transform: translateX(4px);
}

.upload-status {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #ecfdf5;
  border: 1px solid var(--primary);
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  color: var(--primary);
}

.chat-panel {
  background: var(--bg-surface);
  border-radius: 1rem;
  border: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.message {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message.ai .message-avatar {
  background: linear-gradient(135deg, var(--primary) 0%, #059669 100%);
  color: white;
}

.message.user .message-avatar {
  background: #e0f2fe;
  color: #0284c7;
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  max-width: 70%;
}

.message.user .message-content {
  align-items: flex-end;
}

.message-bubble {
  padding: 1rem 1.25rem;
  border-radius: 1rem;
  word-wrap: break-word;
}

.message.ai .message-bubble {
  background: var(--bg-body);
  border: 1px solid var(--border-color);
  border-bottom-left-radius: 0.25rem;
}

.message.user .message-bubble {
  background: var(--primary);
  color: white;
  border-bottom-right-radius: 0.25rem;
}

.message-bubble p {
  line-height: 1.6;
  font-size: 0.9375rem;
  white-space: pre-line;
}

.message-time {
  font-size: 0.75rem;
  color: var(--text-muted);
  padding: 0 0.5rem;
}

.input-area {
  padding: 1.5rem;
  border-top: 1px solid var(--border-color);
  background: var(--bg-body);
}

.input-wrapper {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.message-input {
  flex: 1;
  padding: 0.875rem 1.25rem;
  border: 1px solid var(--border-color);
  border-radius: 999px;
  font-size: 0.9375rem;
  color: var(--text-main);
  background: var(--bg-surface);
  transition: all 0.2s;
}

.message-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.send-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.send-btn:hover:not(:disabled) {
  background: var(--primary-hover);
  transform: scale(1.05);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
