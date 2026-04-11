<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['next', 'back'])
const avoidInput = ref('')
const likeInput = ref('')
const avoidList = ref([])
const likeList = ref([])
const loading = ref(false)

const loadRules = async () => {
  try {
    const res = await fetch('http://localhost:8000/api/rules')
    if (res.ok) {
      const data = await res.json()
      avoidList.value = data.avoid || []
      likeList.value = data.like || []
    }
  } catch (err) {
    console.warn('Failed to load existing rules.')
  }
}

onMounted(() => {
  loadRules()
})

const addAvoid = () => {
  if (!avoidInput.value.trim()) return
  const items = avoidInput.value.split(',').map(s => s.trim()).filter(Boolean)
  avoidList.value.push(...items)
  avoidList.value = [...new Set(avoidList.value)]
  avoidInput.value = ''
}

const addLike = () => {
  if (!likeInput.value.trim()) return
  const items = likeInput.value.split(',').map(s => s.trim()).filter(Boolean)
  likeList.value.push(...items)
  likeList.value = [...new Set(likeList.value)]
  likeInput.value = ''
}

const removeAvoid = (item) => {
  avoidList.value = avoidList.value.filter(i => i !== item)
}

const removeLike = (item) => {
  likeList.value = likeList.value.filter(i => i !== item)
}

const lockCalibration = async () => {
  loading.value = true
  try {
    await fetch('http://localhost:8000/api/rules', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        avoid: avoidList.value,
        like: likeList.value
      })
    })
    emit('next')
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex flex-col w-full h-full p-8 pt-16 relative">
    <button @click="emit('back')" class="absolute top-6 left-8 text-white/40 hover:text-white/80 transition-colors uppercase text-xs font-bold tracking-widest flex items-center gap-2">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
      Revert
    </button>

    <div class="text-center mb-10">
      <h2 class="text-3xl font-extrabold tracking-[0.2em] uppercase text-white/90 mb-2 drop-shadow-[0_0_15px_rgba(255,255,255,0.3)]">Sensor Calibration</h2>
      <p class="text-white/40 tracking-widest text-xs uppercase">Define interference patterns & resonance frequencies</p>
    </div>

    <div class="flex flex-1 gap-8 max-h-[50vh] min-h-[300px]">
      
      <!-- Interference (Avoid) -->
      <div class="flex-1 flex flex-col bg-black/20 border border-rose-500/20 rounded-3xl p-6 relative overflow-hidden group hover:border-rose-500/40 transition-colors duration-500">
        <div class="absolute inset-0 bg-gradient-to-b from-rose-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
        <h3 class="text-rose-400 font-bold tracking-widest uppercase text-sm mb-4 flex items-center gap-3">
          <div class="w-2 h-2 rounded-full bg-rose-500 shadow-[0_0_10px_rgba(244,63,94,0.8)] animate-pulse"></div>
          Interference (Avoid)
        </h3>
        
        <input 
          v-model="avoidInput" 
          @keyup.enter="addAvoid"
          type="text" 
          class="w-full bg-black/40 border border-rose-500/30 rounded-xl px-5 py-3 text-white placeholder-rose-200/20 focus:outline-none focus:border-rose-500/60 focus:bg-black/60 transition-all duration-300 text-sm mb-4"
          placeholder="e.g. NTR, Gore... (Press Enter)"
        />
        
        <div class="flex-1 overflow-y-auto flex flex-wrap content-start gap-2 pr-2 scrollbar-thin">
          <transition-group name="pill">
            <span 
              v-for="item in avoidList" :key="item"
              class="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-medium tracking-wide shadow-[0_0_10px_rgba(244,63,94,0.1)] hover:bg-rose-500/20 transition-all"
            >
              {{ item }}
              <button @click="removeAvoid(item)" class="text-rose-400 hover:text-rose-200">×</button>
            </span>
          </transition-group>
        </div>
      </div>

      <!-- Resonance (Like) -->
      <div class="flex-1 flex flex-col bg-black/20 border border-emerald-500/20 rounded-3xl p-6 relative overflow-hidden group hover:border-emerald-500/40 transition-colors duration-500">
        <div class="absolute inset-0 bg-gradient-to-b from-emerald-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
        <h3 class="text-emerald-400 font-bold tracking-widest uppercase text-sm mb-4 flex items-center gap-3">
          <div class="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.8)] animate-pulse"></div>
          Resonance (Like)
        </h3>
        
        <input 
          v-model="likeInput" 
          @keyup.enter="addLike"
          type="text" 
          class="w-full bg-black/40 border border-emerald-500/30 rounded-xl px-5 py-3 text-white placeholder-emerald-200/20 focus:outline-none focus:border-emerald-500/60 focus:bg-black/60 transition-all duration-300 text-sm mb-4"
          placeholder="e.g. Pure Love, Vanilla... (Press Enter)"
        />
        
        <div class="flex-1 overflow-y-auto flex flex-wrap content-start gap-2 pr-2 scrollbar-thin">
          <transition-group name="pill">
            <span 
              v-for="item in likeList" :key="item"
              class="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-medium tracking-wide shadow-[0_0_10px_rgba(16,185,129,0.1)] hover:bg-emerald-500/20 transition-all"
            >
              {{ item }}
              <button @click="removeLike(item)" class="text-emerald-400 hover:text-emerald-200">×</button>
            </span>
          </transition-group>
        </div>
      </div>

    </div>

    <div class="mt-8 flex justify-center">
      <button 
        @click="lockCalibration" 
        :disabled="loading"
        class="w-64 py-4 rounded-2xl font-bold tracking-[0.2em] uppercase transition-all duration-300 overflow-hidden relative bg-white/5 border border-white/20 text-white hover:bg-white/10 hover:shadow-[0_0_30px_rgba(255,255,255,0.15)] active:scale-95"
      >
        <span v-if="loading" class="animate-pulse">Locking...</span>
        <span v-else>Lock Calibration</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.pill-enter-active,
.pill-leave-active {
  transition: all 0.4s ease;
}
.pill-enter-from,
.pill-leave-to {
  opacity: 0;
  transform: translateY(10px) scale(0.9);
}

.scrollbar-thin::-webkit-scrollbar {
  width: 4px;
}
.scrollbar-thin::-webkit-scrollbar-thumb {
  background: rgba(255,255,255,0.1);
  border-radius: 4px;
}
</style>
