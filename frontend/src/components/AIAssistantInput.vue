<template>
  <div class="ai-assistant-input">
    <h3>AI Assistant</h3>
    <textarea v-model="prompt" placeholder="Post math homework..."></textarea>
    <button @click="submitPrompt">Send</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const prompt = ref('');

const submitPrompt = () => {
  console.log('Submitting prompt:', prompt.value);
  // Call API to send prompt to backend
};
</script>
