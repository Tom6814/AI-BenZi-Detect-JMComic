<script setup>
import { getApiUrl } from '../lib/utils.js'
import { ref, onMounted } from 'vue'

const avoidRules = ref('')
const likeRules = ref('')
const loading = ref(false)
const saveStatus = ref(null)

const fetchRules = async () => {
  try {
    const res = await fetch(getApiUrl('/api/rules'))
    if (res.ok) {
      const data = await res.json()
      avoidRules.value = Array.isArray(data.avoid) ? data.avoid.join(', ') : (data.avoid || '')
      likeRules.value = Array.isArray(data.like) ? data.like.join(', ') : (data.like || '')
    }
  } catch (error) {
    console.error('Failed to fetch rules:', error)
  }
}

const saveRules = async () => {
  loading.value = true
  saveStatus.value = null
  
  const avoidArray = avoidRules.value.split(',').map(s => s.trim()).filter(Boolean)
  const likeArray = likeRules.value.split(',').map(s => s.trim()).filter(Boolean)

  try {
    const res = await fetch(getApiUrl('/api/rules'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        avoid: avoidArray,
        like: likeArray
      })
    })

    if (res.ok) {
      saveStatus.value = { success: true, message: 'Rules synchronized successfully.' }
    } else {
      saveStatus.value = { success: false, message: 'Failed to synchronize rules.' }
    }
  } catch (error) {
    saveStatus.value = { success: false, message: 'Network error during synchronization.' }
  } finally {
    loading.value = false
    setTimeout(() => {
      if (saveStatus.value?.success) saveStatus.value = null
    }, 3000)
  }
}

onMounted(() => {
  fetchRules()
})
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <header class="flex justify-between items-end border-b border-white/10 pb-6">
      <div>
        <h1 class="text-3xl font-bold tracking-widest text-white mb-2 uppercase">Neural Constraints</h1>
        <p class="text-white/50 font-mono text-sm">Define positive and negative attraction parameters</p>
      </div>
      
      <button 
        @click="saveRules"
        :disabled="loading"
        class="bg-[rgba(231,180,255,0.1)] border border-[rgba(231,180,255,0.3)] text-[color:var(--md-sys-color-secondary)] px-8 py-3 rounded-xl hover:bg-[rgba(231,180,255,0.2)] hover:shadow-[0_0_20px_rgba(231,180,255,0.4)] active:scale-95 transition-all duration-300 font-bold tracking-widest disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <span v-if="loading" class="flex items-center gap-2">
          <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          SYNCING...
        </span>
        <span v-else>SYNC RULES</span>
      </button>
    </header>

    <transition name="fade">
      <div v-if="saveStatus" 
           :class="['p-4 rounded-xl border font-mono text-sm text-center', 
                   saveStatus.success ? 'bg-[rgba(0,255,100,0.1)] border-[rgba(0,255,100,0.3)] text-green-400 shadow-[0_0_15px_rgba(0,255,100,0.2)]' : 
                                        'bg-[rgba(255,84,73,0.1)] border-[rgba(255,84,73,0.3)] text-neon-primary shadow-[0_0_15px_rgba(255,84,73,0.2)]']">
        {{ saveStatus.message }}
      </div>
    </transition>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      
      <!-- Like Rules (Neon Green) -->
      <div class="liquid-glass p-8 rounded-3xl relative overflow-hidden group border-[rgba(0,255,100,0.2)] hover:border-[rgba(0,255,100,0.4)] transition-colors duration-500">
        <div class="absolute -top-24 -right-24 w-48 h-48 bg-green-500/20 blur-[50px] rounded-full group-hover:bg-green-500/30 transition-colors duration-500"></div>
        
        <div class="relative z-10">
          <div class="flex items-center gap-3 mb-6">
            <div class="w-10 h-10 rounded-full bg-[rgba(0,255,100,0.1)] border border-[rgba(0,255,100,0.3)] flex items-center justify-center text-green-400 shadow-[0_0_15px_rgba(0,255,100,0.2)]">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
            </div>
            <h2 class="text-2xl font-bold text-green-400 tracking-wider text-shadow-sm shadow-green-400/50">ATTRACTION (LIKE)</h2>
          </div>
          
          <p class="text-white/50 text-sm mb-4 font-mono">Comma-separated keywords to prioritize.</p>
          
          <textarea 
            v-model="likeRules"
            rows="8"
            class="w-full bg-[rgba(0,0,0,0.4)] border border-[rgba(0,255,100,0.2)] rounded-xl p-4 text-green-100 focus:outline-none focus:border-green-400 focus:ring-1 focus:ring-green-400 transition-all duration-300 resize-none font-mono placeholder-green-900/50"
            placeholder="cyberpunk, neon, futuristic, neural..."
          ></textarea>
        </div>
      </div>

      <!-- Avoid Rules (Neon Red) -->
      <div class="liquid-glass p-8 rounded-3xl relative overflow-hidden group border-[rgba(255,84,73,0.2)] hover:border-[rgba(255,84,73,0.4)] transition-colors duration-500">
        <div class="absolute -bottom-24 -left-24 w-48 h-48 bg-red-500/20 blur-[50px] rounded-full group-hover:bg-red-500/30 transition-colors duration-500"></div>
        
        <div class="relative z-10">
          <div class="flex items-center gap-3 mb-6">
            <div class="w-10 h-10 rounded-full bg-[rgba(255,84,73,0.1)] border border-[rgba(255,84,73,0.3)] flex items-center justify-center text-neon-primary shadow-[0_0_15px_rgba(255,84,73,0.2)]">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </div>
            <h2 class="text-2xl font-bold text-neon-primary tracking-wider text-shadow-sm shadow-red-500/50">REPULSION (AVOID)</h2>
          </div>
          
          <p class="text-white/50 text-sm mb-4 font-mono">Comma-separated keywords to filter out.</p>
          
          <textarea 
            v-model="avoidRules"
            rows="8"
            class="w-full bg-[rgba(0,0,0,0.4)] border border-[rgba(255,84,73,0.2)] rounded-xl p-4 text-red-100 focus:outline-none focus:border-neon-primary focus:ring-1 focus:ring-neon-primary transition-all duration-300 resize-none font-mono placeholder-red-900/50"
            placeholder="legacy, deprecated, obsolete, organic..."
          ></textarea>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.text-shadow-sm {
  text-shadow: 0 0 10px var(--tw-shadow-color);
}
</style>
