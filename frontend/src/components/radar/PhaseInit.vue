<script setup>
import { ref } from 'vue'

const emit = defineEmits(['next'])
const provider = ref('openai')
const apiKey = ref('')
const baseUrl = ref('')
const model = ref('')
const loading = ref(false)
const errorMsg = ref('')

const testConnection = async () => {
  if (!apiKey.value) {
    errorMsg.value = 'API Key is required.'
    return
  }
  loading.value = true
  errorMsg.value = ''
  
  try {
    const res = await fetch('/api/config/test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        provider: provider.value,
        api_key: apiKey.value,
        base_url: baseUrl.value || undefined,
        model: model.value || undefined
      })
    })
    
    if (res.ok) {
      // Save config if test passed
      await fetch('/api/config/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          provider: provider.value,
          api_key: apiKey.value,
          base_url: baseUrl.value || undefined,
          model: model.value || undefined
        })
      })
      emit('next')
    } else {
      const data = await res.json()
      errorMsg.value = data.detail || 'Connection failed.'
    }
  } catch (err) {
    errorMsg.value = 'Network error. Backend not running?'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex flex-col items-center justify-center w-full h-full p-8 md:p-12 relative bg-[var(--color-md-sys-surface)]">
    <div class="text-center mb-10 w-full max-w-lg">
      <h2 class="text-4xl font-normal text-[var(--color-md-sys-on-surface)] mb-4 tracking-tight" style="font-family: 'Google Sans', 'Roboto', sans-serif;">
        Setup Connection
      </h2>
      <p class="text-[var(--color-md-sys-on-surface-variant)] text-body-large">
        Configure your AI provider to begin the analysis sequence.
      </p>
    </div>

    <!-- MD3 Segmented Button (Provider Toggle) -->
    <div class="flex border border-[var(--color-md-sys-outline)] rounded-full mb-10 overflow-hidden bg-transparent">
      <button 
        @click="provider = 'openai'" 
        class="px-8 py-2.5 text-sm font-medium transition-colors md-ripple relative z-10"
        :class="provider === 'openai' ? 'bg-[var(--color-md-sys-secondary-container)] text-[var(--color-md-sys-on-secondary-container)]' : 'text-[var(--color-md-sys-on-surface)] hover:bg-[var(--color-md-sys-surface-variant)]'"
      >
        <span class="flex items-center gap-2">
          <svg v-if="provider === 'openai'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
          OpenAI
        </span>
      </button>
      <div class="w-[1px] bg-[var(--color-md-sys-outline)]"></div>
      <button 
        @click="provider = 'gemini'" 
        class="px-8 py-2.5 text-sm font-medium transition-colors md-ripple relative z-10"
        :class="provider === 'gemini' ? 'bg-[var(--color-md-sys-secondary-container)] text-[var(--color-md-sys-on-secondary-container)]' : 'text-[var(--color-md-sys-on-surface)] hover:bg-[var(--color-md-sys-surface-variant)]'"
      >
        <span class="flex items-center gap-2">
          <svg v-if="provider === 'gemini'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
          Gemini
        </span>
      </button>
    </div>

    <!-- Form Container (MD3 Text Fields) -->
    <div class="w-full max-w-sm flex flex-col gap-6 relative z-10">
      
      <!-- Filled Text Field -->
      <div class="relative bg-[var(--color-md-sys-surface-variant)] rounded-t-md border-b border-[var(--color-md-sys-on-surface-variant)] group focus-within:border-[var(--color-md-sys-primary)] focus-within:border-b-2 transition-all">
        <label class="absolute top-2 left-4 text-xs text-[var(--color-md-sys-on-surface-variant)] group-focus-within:text-[var(--color-md-sys-primary)] transition-colors">API Key</label>
        <input 
          v-model="apiKey" 
          type="password" 
          class="w-full bg-transparent px-4 pt-6 pb-2 text-[var(--color-md-sys-on-surface)] focus:outline-none"
          :placeholder="provider === 'openai' ? 'sk-...' : 'AIzaSy...'"
        />
      </div>

      <div class="relative bg-[var(--color-md-sys-surface-variant)] rounded-t-md border-b border-[var(--color-md-sys-on-surface-variant)] group focus-within:border-[var(--color-md-sys-primary)] focus-within:border-b-2 transition-all">
        <label class="absolute top-2 left-4 text-xs text-[var(--color-md-sys-on-surface-variant)] group-focus-within:text-[var(--color-md-sys-primary)] transition-colors">Base URL (Optional)</label>
        <input 
          v-model="baseUrl" 
          type="text" 
          class="w-full bg-transparent px-4 pt-6 pb-2 text-[var(--color-md-sys-on-surface)] focus:outline-none"
        />
      </div>

      <div class="relative bg-[var(--color-md-sys-surface-variant)] rounded-t-md border-b border-[var(--color-md-sys-on-surface-variant)] group focus-within:border-[var(--color-md-sys-primary)] focus-within:border-b-2 transition-all">
        <label class="absolute top-2 left-4 text-xs text-[var(--color-md-sys-on-surface-variant)] group-focus-within:text-[var(--color-md-sys-primary)] transition-colors">Model (Optional)</label>
        <input 
          v-model="model" 
          type="text" 
          class="w-full bg-transparent px-4 pt-6 pb-2 text-[var(--color-md-sys-on-surface)] focus:outline-none"
        />
      </div>

      <div v-if="errorMsg" class="bg-[var(--color-md-sys-error-container)] text-[var(--color-md-sys-on-error-container)] p-4 rounded-md text-sm md-elevation-1">
        {{ errorMsg }}
      </div>

      <div class="flex justify-end mt-4">
        <button 
          @click="testConnection" 
          :disabled="loading"
          class="md-ripple px-6 py-2.5 rounded-full font-medium transition-all flex items-center justify-center gap-2"
          :class="loading ? 'bg-[var(--color-md-sys-surface-variant)] text-[var(--color-md-sys-on-surface-variant)] opacity-50 cursor-not-allowed' : 'bg-[var(--color-md-sys-primary)] text-[var(--color-md-sys-on-primary)] hover:md-elevation-2 active:md-elevation-1'"
        >
          <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
          {{ loading ? 'Connecting...' : 'Connect' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.text-body-large {
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.5px;
}
</style>
