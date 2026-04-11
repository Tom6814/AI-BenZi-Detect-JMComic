<script setup>
import { ref } from 'vue'

const emit = defineEmits(['search-success', 'back'])
const query = ref('')
const loading = ref(false)
const scanLines = ref(false)

const initiateScan = async () => {
  if (!query.value.trim()) return
  loading.value = true
  scanLines.value = true
  
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
    scanLines.value = false
  }
}
</script>

<template>
  <div class="flex flex-col items-center justify-center w-full h-full p-8 relative overflow-hidden group">
    
    <button @click="emit('back')" class="absolute top-6 left-8 text-white/40 hover:text-white/80 transition-colors uppercase text-xs font-bold tracking-widest flex items-center gap-2 z-20">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
      Revert
    </button>

    <!-- Radar UI Background -->
    <div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-20 transition-opacity duration-1000" :class="{ 'opacity-50': loading }">
      <div class="w-96 h-96 rounded-full border border-cyan-500/30 absolute animate-[ping_3s_cubic-bezier(0,0,0.2,1)_infinite]"></div>
      <div class="w-64 h-64 rounded-full border border-cyan-500/20 absolute"></div>
      <div class="w-[1px] h-96 bg-cyan-500/20 absolute"></div>
      <div class="h-[1px] w-96 bg-cyan-500/20 absolute"></div>
    </div>

    <!-- Scanning Line Effect -->
    <div v-if="scanLines" class="absolute inset-0 pointer-events-none overflow-hidden z-10">
      <div class="w-full h-2 bg-cyan-400/50 shadow-[0_0_20px_rgba(0,229,255,0.8)] absolute top-0 animate-[scan_1.5s_linear_infinite]"></div>
    </div>

    <div class="text-center mb-16 relative z-20">
      <h2 class="text-4xl font-extrabold tracking-[0.2em] uppercase text-white/90 mb-3 drop-shadow-[0_0_15px_rgba(255,255,255,0.3)]">Target Acquisition</h2>
      <p class="text-cyan-400/80 tracking-widest text-sm uppercase drop-shadow-[0_0_5px_rgba(0,229,255,0.5)]">Enter Subject ID or Designation</p>
    </div>

    <div class="w-full max-w-xl relative z-20">
      <div class="relative group mb-12">
        <div class="absolute -inset-1 bg-gradient-to-r from-cyan-500 to-fuchsia-500 rounded-3xl blur opacity-25 group-hover:opacity-40 transition duration-1000 group-hover:duration-200"></div>
        <input 
          v-model="query" 
          @keyup.enter="initiateScan"
          type="text" 
          class="relative w-full bg-black/60 border border-white/20 rounded-2xl px-8 py-6 text-2xl text-center text-white font-mono tracking-widest placeholder-white/20 focus:outline-none focus:border-cyan-400/50 focus:bg-black/80 transition-all duration-500"
          placeholder="e.g. 123456 or Title..."
          :disabled="loading"
        />
        <div class="absolute right-6 top-1/2 -translate-y-1/2 w-4 h-4 rounded-full" :class="query.trim() ? 'bg-cyan-400 shadow-[0_0_10px_rgba(0,229,255,0.8)]' : 'bg-white/10'"></div>
      </div>

      <button 
        @click="initiateScan" 
        :disabled="loading || !query.trim()"
        class="w-full py-5 rounded-2xl font-bold tracking-[0.2em] uppercase transition-all duration-500 overflow-hidden relative"
        :class="(loading || !query.trim()) ? 'bg-white/5 text-white/30 border border-white/10 cursor-not-allowed' : 'bg-cyan-500/10 border border-cyan-400/50 text-cyan-300 hover:bg-cyan-500/20 hover:shadow-[0_0_30px_rgba(0,229,255,0.4)] active:scale-95'"
      >
        <span v-if="loading" class="flex items-center justify-center gap-3">
          <div class="w-4 h-4 rounded-full bg-cyan-400 animate-ping"></div>
          Scanning...
        </span>
        <span v-else>Initiate Deep Scan</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
@keyframes scan {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100vh); }
}
</style>
