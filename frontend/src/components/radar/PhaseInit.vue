<script setup>
import { ref, onMounted } from 'vue'
import { getApiUrl } from '../../lib/utils.js'

const emit = defineEmits(['next'])

const provider = ref('openai')
const apiKey = ref('')
const baseUrl = ref('')
const model = ref('')
const enableReddit = ref(false)

const loading = ref(false)
const testing = ref(false)
const testResult = ref(null)

onMounted(async () => {
  try {
    const res = await fetch(getApiUrl('/api/config'))
    if (res.ok) {
      const data = await res.json()
      if (data.provider) provider.value = data.provider
      if (data.api_key) apiKey.value = data.api_key
      if (data.base_url) baseUrl.value = data.base_url
      if (data.model) model.value = data.model
      if (data.enable_reddit !== undefined) enableReddit.value = data.enable_reddit
    }
  } catch (e) {
    console.error('Failed to load config:', e)
  }
})

const testConnection = async () => {
  if (!apiKey.value) return
  testing.value = true
  testResult.value = null
  try {
    const res = await fetch(getApiUrl('/api/config/test'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        provider: provider.value,
        api_key: apiKey.value,
        base_url: baseUrl.value,
        model: model.value
      })
    })
    if (res.ok) {
      testResult.value = { success: true, msg: 'Connection Successful' }
    } else {
      const err = await res.json().catch(() => ({}))
      testResult.value = { success: false, msg: err.detail || 'Connection Failed' }
    }
  } catch (err) {
    testResult.value = { success: false, msg: err.message }
  } finally {
    testing.value = false
  }
}

const saveAndNext = async () => {
  if (!apiKey.value) return
  loading.value = true
  try {
    await fetch(getApiUrl('/api/config'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        provider: provider.value,
        api_key: apiKey.value,
        base_url: baseUrl.value,
        model: model.value,
        enable_reddit: enableReddit.value
      })
    })
    emit('next')
  } catch (e) {
    console.error('Failed to save config:', e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex flex-col items-center justify-center w-full h-full p-8 md:p-12 relative overflow-y-auto scrollbar-thin">
    <!-- Title Area -->
    <div class="text-center mb-8">
      <div class="inline-flex items-center justify-center w-16 h-16 rounded-[16px] bg-[var(--color-md-sys-primary-container)] text-[var(--color-md-sys-on-primary-container)] mb-6 md-elevation-1">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
      </div>
      <h2 class="text-3xl font-normal text-[var(--color-md-sys-on-surface)] mb-2 tracking-tight" style="font-family: 'Google Sans', 'Roboto', sans-serif;">
        System Configuration
      </h2>
      <p class="text-[var(--color-md-sys-on-surface-variant)] text-sm tracking-wide">
        Initialize AI Core & API Access
      </p>
    </div>

    <!-- Form Area -->
    <div class="w-full max-w-sm flex flex-col gap-5">
      <!-- Provider Selection -->
      <div class="flex bg-[var(--color-md-sys-surface-variant)] p-1 rounded-2xl md-elevation-1">
        <button
          @click="provider = 'openai'"
          class="flex-1 py-3 text-sm font-bold uppercase tracking-wider rounded-xl transition-all duration-300 md-ripple"
          :class="provider === 'openai' ? 'bg-[var(--color-md-sys-surface)] text-[var(--color-md-sys-primary)] shadow-sm' : 'text-[var(--color-md-sys-on-surface-variant)] hover:text-[var(--color-md-sys-on-surface)]'"
        >
          OpenAI
        </button>
        <button
          @click="provider = 'gemini'"
          class="flex-1 py-3 text-sm font-bold uppercase tracking-wider rounded-xl transition-all duration-300 md-ripple"
          :class="provider === 'gemini' ? 'bg-[var(--color-md-sys-surface)] text-[var(--color-md-sys-primary)] shadow-sm' : 'text-[var(--color-md-sys-on-surface-variant)] hover:text-[var(--color-md-sys-on-surface)]'"
        >
          Gemini
        </button>
      </div>

      <!-- Inputs -->
      <div class="space-y-4">
        <div>
          <input
            v-model="apiKey"
            type="password"
            placeholder="API Key (Required)"
            class="w-full bg-[var(--color-md-sys-surface-variant)] text-[var(--color-md-sys-on-surface-variant)] px-6 py-4 rounded-2xl border-none focus:ring-2 focus:ring-[var(--color-md-sys-primary)] outline-none placeholder-[var(--color-md-sys-outline)] transition-all duration-300 hover:bg-[var(--color-md-sys-surface-variant-hover)]"
          />
        </div>
        <div>
          <input
            v-model="baseUrl"
            type="text"
            placeholder="Base URL (Optional proxy)"
            class="w-full bg-[var(--color-md-sys-surface-variant)] text-[var(--color-md-sys-on-surface-variant)] px-6 py-4 rounded-2xl border-none focus:ring-2 focus:ring-[var(--color-md-sys-primary)] outline-none placeholder-[var(--color-md-sys-outline)] transition-all duration-300 hover:bg-[var(--color-md-sys-surface-variant-hover)]"
          />
        </div>
        <div>
          <input
            v-model="model"
            type="text"
            :placeholder="provider === 'openai' ? 'Model (e.g. gpt-4o)' : 'Model (e.g. gemini-1.5-pro)'"
            class="w-full bg-[var(--color-md-sys-surface-variant)] text-[var(--color-md-sys-on-surface-variant)] px-6 py-4 rounded-2xl border-none focus:ring-2 focus:ring-[var(--color-md-sys-primary)] outline-none placeholder-[var(--color-md-sys-outline)] transition-all duration-300 hover:bg-[var(--color-md-sys-surface-variant-hover)]"
          />
        </div>
      </div>

      <!-- Settings Toggle -->
      <div class="flex items-center justify-between bg-[var(--color-md-sys-surface-variant)] px-6 py-4 rounded-2xl">
        <div class="flex flex-col">
          <span class="text-[var(--color-md-sys-on-surface)] font-medium text-sm">Reddit Context (Beta)</span>
          <span class="text-[var(--color-md-sys-on-surface-variant)] text-xs">Search Reddit for reader feedback</span>
        </div>
        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" v-model="enableReddit" class="sr-only peer">
          <div class="w-11 h-6 bg-[var(--color-md-sys-outline-variant)] peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[var(--color-md-sys-primary)]"></div>
        </label>
      </div>

      <!-- Connection Test -->
      <div class="flex flex-col gap-2 mt-2">
        <button
          @click="testConnection"
          :disabled="testing || !apiKey"
          class="text-sm font-medium text-[var(--color-md-sys-primary)] hover:text-[var(--color-md-sys-primary-container)] transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <svg v-if="testing" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.906 14.142 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"></path></svg>
          Test Connection
        </button>

        <transition name="fade">
          <div v-if="testResult" class="text-center text-sm p-3 rounded-xl border" :class="testResult.success ? 'bg-[var(--color-md-sys-safe-container)] text-[var(--color-md-sys-on-safe-container)] border-[var(--color-md-sys-safe)]' : 'bg-[var(--color-md-sys-error-container)] text-[var(--color-md-sys-on-error-container)] border-[var(--color-md-sys-error)]'">
            {{ testResult.msg }}
          </div>
        </transition>
      </div>

      <!-- Next Button -->
      <button
        @click="saveAndNext"
        :disabled="loading || !apiKey"
        class="w-full py-4 bg-[var(--color-md-sys-primary)] text-[var(--color-md-sys-on-primary)] rounded-full text-lg font-bold tracking-widest uppercase hover:bg-[var(--color-md-sys-primary)] hover:shadow-[0_4px_12px_rgba(var(--color-md-sys-primary-rgb),0.3)] active:scale-[0.98] transition-all duration-300 flex items-center justify-center gap-2 mt-4 disabled:opacity-50 disabled:cursor-not-allowed md-ripple"
      >
        <span v-if="!loading">Initialize</span>
        <svg v-else class="w-6 h-6 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.scrollbar-thin::-webkit-scrollbar {
  width: 4px;
}
.scrollbar-thin::-webkit-scrollbar-thumb {
  background: rgba(255,255,255,0.1);
  border-radius: 4px;
}
</style>
