<script setup>
import { ref } from 'vue'

const emit = defineEmits(['next'])
const provider = ref('openai')
const apiKey = ref('')
const baseUrl = ref('')
const model = ref('')
const loading = ref(false)
const errorMsg = ref('')

const toggleProvider = () => {
  provider.value = provider.value === 'openai' ? 'gemini' : 'openai'
  // Clear optional fields when switching
  baseUrl.value = ''
  model.value = ''
}

const testConnection = async () => {
  if (!apiKey.value) {
    errorMsg.value = 'API Key is required.'
    return
  }
  loading.value = true
  errorMsg.value = ''
  
  try {
    const res = await fetch('http://localhost:8000/api/config/test', {
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
  <div class="flex flex-col items-center justify-center w-full h-full p-8 relative">
    <div class="text-center mb-12">
      <h2 class="text-4xl font-extrabold tracking-[0.2em] uppercase text-white/90 mb-3 drop-shadow-[0_0_15px_rgba(255,255,255,0.3)]">Awaken Core</h2>
      <p class="text-white/40 tracking-widest text-sm uppercase">Establish neural uplink to proceed</p>
    </div>

    <!-- Provider Toggle Switch -->
    <div class="flex bg-black/40 rounded-full p-1.5 mb-10 border border-white/5 relative overflow-hidden">
      <div 
        class="absolute top-1.5 left-1.5 bottom-1.5 w-[calc(50%-6px)] rounded-full transition-all duration-500 ease-[cubic-bezier(0.34,1.56,0.64,1)] z-0"
        :class="provider === 'openai' ? 'bg-gradient-to-r from-teal-400 to-emerald-500 translate-x-0 shadow-[0_0_20px_rgba(0,255,170,0.4)]' : 'bg-gradient-to-r from-fuchsia-500 to-purple-600 translate-x-full shadow-[0_0_20px_rgba(200,0,255,0.4)]'"
      ></div>
      <button 
        @click="provider = 'openai'" 
        class="w-40 py-3 text-sm font-bold tracking-widest uppercase relative z-10 transition-colors duration-300"
        :class="provider === 'openai' ? 'text-black' : 'text-white/50 hover:text-white/80'"
      >
        OpenAI
      </button>
      <button 
        @click="provider = 'gemini'" 
        class="w-40 py-3 text-sm font-bold tracking-widest uppercase relative z-10 transition-colors duration-300"
        :class="provider === 'gemini' ? 'text-white drop-shadow-md' : 'text-white/50 hover:text-white/80'"
      >
        Gemini
      </button>
    </div>

    <!-- Form Container -->
    <div class="w-full max-w-md flex flex-col gap-6 relative z-10">
      <div class="relative group">
        <input 
          v-model="apiKey" 
          type="password" 
          class="w-full bg-black/30 border border-white/10 rounded-2xl px-6 py-4 text-white placeholder-white/30 focus:outline-none focus:border-white/30 focus:bg-black/50 transition-all duration-300"
          :placeholder="provider === 'openai' ? 'sk-...' : 'AIzaSy...'"
        />
        <span class="absolute -top-3 left-4 bg-transparent px-2 text-xs font-semibold tracking-widest text-white/50 uppercase">API Key</span>
      </div>

      <div class="relative group">
        <input 
          v-model="baseUrl" 
          type="text" 
          class="w-full bg-black/30 border border-white/10 rounded-2xl px-6 py-4 text-white placeholder-white/30 focus:outline-none focus:border-white/30 focus:bg-black/50 transition-all duration-300"
          :placeholder="provider === 'openai' ? 'https://api.openai.com/v1' : 'https://generativelanguage.googleapis.com/v1beta'"
        />
        <span class="absolute -top-3 left-4 bg-transparent px-2 text-xs font-semibold tracking-widest text-white/50 uppercase">Base URL (Optional)</span>
      </div>

      <div class="relative group">
        <input 
          v-model="model" 
          type="text" 
          class="w-full bg-black/30 border border-white/10 rounded-2xl px-6 py-4 text-white placeholder-white/30 focus:outline-none focus:border-white/30 focus:bg-black/50 transition-all duration-300"
          :placeholder="provider === 'openai' ? 'gpt-4o' : 'gemini-1.5-pro'"
        />
        <span class="absolute -top-3 left-4 bg-transparent px-2 text-xs font-semibold tracking-widest text-white/50 uppercase">Model (Optional)</span>
      </div>

      <p v-if="errorMsg" class="text-red-400 text-sm font-medium tracking-wide text-center mt-2 animate-pulse">{{ errorMsg }}</p>

      <button 
        @click="testConnection" 
        :disabled="loading"
        class="mt-6 w-full py-5 rounded-2xl font-bold tracking-[0.15em] uppercase transition-all duration-300 overflow-hidden relative group"
        :class="loading ? 'bg-white/10 text-white/50 border border-white/10 cursor-not-allowed' : 'bg-white/5 border border-white/20 text-white hover:bg-white/10 hover:shadow-[0_0_30px_rgba(255,255,255,0.1)] active:scale-95'"
      >
        <span v-if="loading" class="flex items-center justify-center gap-3">
          <div class="w-4 h-4 rounded-full border-2 border-white/20 border-t-white/80 animate-spin"></div>
          Uplinking...
        </span>
        <span v-else>Establish Link</span>
        
        <!-- Hover Glint Effect -->
        <div v-if="!loading" class="absolute top-0 -inset-full h-full w-1/2 z-5 block transform -skew-x-12 bg-gradient-to-r from-transparent to-white/10 opacity-0 group-hover:animate-[glint_1s_forwards]"></div>
      </button>
    </div>
  </div>
</template>

<style scoped>
@keyframes glint {
  100% { left: 200%; opacity: 1; }
}
</style>
