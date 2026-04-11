<script setup>
import { ref } from 'vue'

const emit = defineEmits(['search-success', 'back'])
const query = ref('')
const loading = ref(false)

const initiateScan = async () => {
  if (!query.value.trim()) return
  loading.value = true
  
  try {
    // Simulated deep scan delay
    await new Promise(r => setTimeout(r, 1500))
    
    const res = await fetch(`http://localhost:8000/api/identify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query.value })
    })
    
    if (res.ok) {
      const data = await res.json()
      emit('search-success', data)
    } else {
      console.error('Identify failed')
    }
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex flex-col items-center justify-center w-full h-full p-8 md:p-12 relative bg-[var(--color-md-sys-surface)]">
    
    <div class="absolute top-8 left-8 md:top-12 md:left-12 z-20">
      <button @click="emit('back')" class="p-2 rounded-full text-[var(--color-md-sys-on-surface-variant)] hover:bg-[var(--color-md-sys-surface-variant)] transition-colors md-ripple flex items-center justify-center">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
      </button>
    </div>

    <!-- Indeterminate Linear Progress Indicator for loading state -->
    <div v-if="loading" class="absolute top-0 left-0 w-full h-1 bg-[var(--color-md-sys-surface-variant)] overflow-hidden z-30">
      <div class="h-full bg-[var(--color-md-sys-primary)] w-1/3 animate-[md-linear-progress_2s_infinite_linear]"></div>
    </div>

    <div class="text-center mb-12 relative z-20 w-full max-w-lg">
      <div class="inline-flex items-center justify-center w-16 h-16 rounded-[16px] bg-[var(--color-md-sys-primary-container)] text-[var(--color-md-sys-on-primary-container)] mb-6 md-elevation-1">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
      </div>
      <h2 class="text-3xl font-normal text-[var(--color-md-sys-on-surface)] mb-4 tracking-tight" style="font-family: 'Google Sans', 'Roboto', sans-serif;">
        Analyze Content
      </h2>
      <p class="text-[var(--color-md-sys-on-surface-variant)] text-body-large">
        Enter a title, ID, or link to evaluate against your preferences.
      </p>
    </div>

    <!-- MD3 Search Bar -->
    <div class="w-full max-w-2xl relative z-20">
      <div class="relative bg-[var(--color-md-sys-surface-variant)] rounded-[28px] h-[56px] flex items-center px-4 transition-shadow focus-within:md-elevation-1 focus-within:bg-[var(--color-md-sys-surface)]">
        <svg class="w-6 h-6 text-[var(--color-md-sys-on-surface-variant)] ml-2 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
        <input 
          v-model="query" 
          @keyup.enter="initiateScan"
          type="text" 
          class="flex-1 bg-transparent border-none text-[var(--color-md-sys-on-surface)] text-lg focus:outline-none h-full placeholder-[var(--color-md-sys-on-surface-variant)]"
          placeholder="Search by ID or Title..."
          :disabled="loading"
        />
        
        <button 
          v-if="query"
          @click="query = ''" 
          class="p-2 rounded-full text-[var(--color-md-sys-on-surface-variant)] hover:bg-[var(--color-md-sys-outline-variant)] transition-colors mr-1"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>

      <div class="mt-8 flex justify-center">
        <!-- MD3 Filled Button -->
        <button 
          @click="initiateScan" 
          :disabled="loading || !query.trim()"
          class="md-ripple h-[40px] px-6 rounded-full font-medium transition-all flex items-center justify-center gap-2"
          :class="(loading || !query.trim()) ? 'bg-[var(--color-md-sys-surface-variant)] text-[var(--color-md-sys-on-surface-variant)] opacity-[0.38] cursor-not-allowed' : 'bg-[var(--color-md-sys-primary)] text-[var(--color-md-sys-on-primary)] hover:md-elevation-1 active:md-elevation-0'"
        >
          <span>Evaluate</span>
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

@keyframes md-linear-progress {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(300%); }
}
</style>
