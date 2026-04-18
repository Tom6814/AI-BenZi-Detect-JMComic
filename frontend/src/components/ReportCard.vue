<script setup>
import { computed } from 'vue'
import { marked } from 'marked'

const props = defineProps({
  data: Object
})

const scoreColor = computed(() => {
  const s = props.data.score
  if (s === undefined) return '#a855f7' // Default purple
  if (s >= 80) return '#10b981' // Emerald 500
  if (s >= 50) return '#f59e0b' // Amber 500
  return '#ef4444' // Red 500
})

const scoreLabel = computed(() => {
  const s = props.data.score
  if (s === undefined) return ''
  if (s >= 80) return 'SAFE'
  if (s >= 50) return 'CAUTION'
  return 'DANGER'
})

const parsedReasoning = computed(() => {
  if (!props.data.reasoning) return ''
  // Basic markdown parsing
  return marked.parse(props.data.reasoning)
})

const avoidHits = computed(() => props.data.avoid?.filter(t => t.contains).length || 0)
const likeHits = computed(() => props.data.like?.filter(t => t.contains).length || 0)
const watchUrl = computed(() => {
  if (props.data.album_id) {
    return `https://web.jmcomic.uk/detail/${props.data.album_id}`
  }
  return '#'
})

const buttonStyle = computed(() => {
  const s = props.data.score
  if (s === undefined) return 'bg-purple-600 hover:bg-purple-500 shadow-[0_0_20px_rgba(147,51,234,0.4)] border-purple-400'
  if (s >= 80) return 'bg-emerald-600 hover:bg-emerald-500 shadow-[0_0_20px_rgba(16,185,129,0.4)] border-emerald-400'
  if (s >= 31) return 'bg-amber-600 hover:bg-amber-500 shadow-[0_0_20px_rgba(245,158,11,0.4)] border-amber-400'
  return 'bg-red-600 hover:bg-red-500 shadow-[0_0_20px_rgba(239,68,68,0.4)] border-red-400'
})

const buttonText = computed(() => {
  const s = props.data.score
  if (s === undefined) return '前往观看'
  if (s >= 80) return '火速食用'
  if (s >= 31) return '前往观看'
  return '我已知晓，无视风险继续观看'
})
</script>

<template>
  <div class="relative w-full rounded-[28px] bg-[#121212] border border-white/10 shadow-[0_20px_50px_rgba(0,0,0,0.5)] overflow-hidden backdrop-blur-xl">
    
    <!-- Dynamic Ambient Glow based on Score -->
    <div v-if="data.score !== undefined" class="absolute -top-32 -right-32 w-96 h-96 rounded-full blur-[100px] pointer-events-none transition-colors duration-1000" :style="{ backgroundColor: scoreColor, opacity: 0.15 }"></div>
    <div v-if="data.score !== undefined" class="absolute -bottom-32 -left-32 w-96 h-96 rounded-full blur-[100px] pointer-events-none transition-colors duration-1000" :style="{ backgroundColor: scoreColor, opacity: 0.1 }"></div>

    <div class="relative z-10 p-8 md:p-10 flex flex-col gap-10">
      
      <!-- Header Area -->
      <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-8 border-b border-white/10">
        
        <div class="flex items-center gap-5">
          <div class="w-14 h-14 bg-white/5 border border-white/10 rounded-2xl flex items-center justify-center text-white shadow-inner">
            <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          </div>
          <div>
            <h3 class="text-3xl font-extrabold text-white tracking-tight">AI Evaluation</h3>
            <p class="text-gray-400 text-sm mt-1 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full animate-pulse" :style="{ backgroundColor: scoreColor }"></span>
              Neural Scan Complete
            </p>
          </div>
        </div>

        <!-- Visual Score Gauge -->
        <div v-if="data.score !== undefined" class="flex items-center gap-5 bg-black/40 px-6 py-4 rounded-2xl border border-white/5 shadow-inner backdrop-blur-md">
          <div class="flex flex-col text-right">
            <span class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-300 mb-1">Threat Level</span>
            <span class="text-lg font-black tracking-wider" :style="{ color: scoreColor }">{{ scoreLabel }}</span>
          </div>
          
          <div class="relative w-16 h-16 flex items-center justify-center">
            <!-- Background track -->
            <svg class="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
              <path class="text-gray-800" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" stroke-width="3" />
              <!-- Progress track -->
              <path :style="{ color: scoreColor }" class="transition-all duration-1500 ease-out drop-shadow-[0_0_8px_currentColor]" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" :stroke-dasharray="`${data.score}, 100`" />
            </svg>
            <span class="absolute text-xl font-black" :style="{ color: scoreColor }">{{ data.score }}</span>
          </div>
        </div>
      </div>

      <!-- Tag Sections -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        <!-- Avoid Section -->
        <div v-if="data.avoid && data.avoid.length" class="bg-red-500/5 border border-red-500/10 rounded-3xl p-6 relative overflow-hidden group hover:border-red-500/20 transition-colors">
          <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-red-500 to-transparent opacity-50"></div>
          <div class="flex items-center justify-between mb-6">
            <h4 class="text-sm font-black text-red-400 uppercase tracking-widest flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
              Red Flags (Avoid)
            </h4>
            <span class="text-xs font-bold bg-red-500/20 text-red-400 px-3 py-1 rounded-full border border-red-500/20">
              {{ avoidHits }} Found
            </span>
          </div>
          
          <div class="flex flex-wrap gap-3">
            <div v-for="(item, idx) in data.avoid" :key="idx" 
                 class="relative px-4 py-2.5 rounded-xl border text-sm font-semibold transition-all duration-300 flex items-center gap-2"
                 :class="item.contains 
                    ? 'bg-red-500/20 border-red-500/40 text-red-300 shadow-[0_0_15px_rgba(239,68,68,0.15)]' 
                    : 'bg-black/40 border-white/5 text-gray-300'">
              <svg v-if="item.contains" class="w-4 h-4 text-red-400 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
              <svg v-else class="w-4 h-4 opacity-40" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
              {{ item.tag }}
              <span v-if="item.contains" class="ml-1 text-[10px] bg-red-500/30 px-1.5 py-0.5 rounded text-red-200">{{ (item.probability * 100).toFixed(0) }}%</span>
            </div>
          </div>
        </div>

        <!-- Like Section -->
        <div v-if="data.like && data.like.length" class="bg-emerald-500/5 border border-emerald-500/10 rounded-3xl p-6 relative overflow-hidden group hover:border-emerald-500/20 transition-colors">
          <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-500 to-transparent opacity-50"></div>
          <div class="flex items-center justify-between mb-6">
            <h4 class="text-sm font-black text-emerald-400 uppercase tracking-widest flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
              Favorites (Like)
            </h4>
            <span class="text-xs font-bold bg-emerald-500/20 text-emerald-400 px-3 py-1 rounded-full border border-emerald-500/20">
              {{ likeHits }} Matched
            </span>
          </div>

          <div class="flex flex-wrap gap-3">
            <div v-for="(item, idx) in data.like" :key="idx" 
                 class="relative px-4 py-2.5 rounded-xl border text-sm font-semibold transition-all duration-300 flex items-center gap-2"
                 :class="item.contains 
                    ? 'bg-emerald-500/20 border-emerald-500/40 text-emerald-300 shadow-[0_0_15px_rgba(16,185,129,0.15)]' 
                    : 'bg-black/40 border-white/5 text-gray-300'">
              <svg v-if="item.contains" class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
              <svg v-else class="w-4 h-4 opacity-40" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
              {{ item.tag }}
              <span v-if="item.contains" class="ml-1 text-[10px] bg-emerald-500/30 px-1.5 py-0.5 rounded text-emerald-200">{{ (item.probability * 100).toFixed(0) }}%</span>
            </div>
          </div>
        </div>

      </div>

      <!-- AI Reasoning Section -->
      <div class="mt-4 bg-white/[0.02] border border-white/5 rounded-3xl p-6 md:p-8">
        <h4 class="text-sm font-black text-gray-400 uppercase tracking-widest flex items-center gap-2 mb-6">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
          Neural Network Reasoning
        </h4>
        
        <div class="reasoning-content" v-html="parsedReasoning">
        </div>
      </div>
      
      <!-- Go to Watch Button -->
      <div class="mt-4 flex justify-center w-full relative z-20">
        <a :href="watchUrl" target="_blank" rel="noopener noreferrer" 
           class="group relative inline-flex items-center justify-center px-10 py-4 font-bold text-white transition-all duration-300 rounded-2xl hover:scale-[1.02] active:scale-[0.98] border border-transparent overflow-hidden"
           :class="buttonStyle">
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
          <span class="relative flex items-center gap-3 text-lg tracking-wide">
            <svg class="w-6 h-6 group-hover:-translate-y-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
            {{ buttonText }}
          </span>
        </a>
      </div>

    </div>
  </div>
</template>

<style>
/* Prose overrides are handled by Tailwind Typography plugin via prose classes above */
.first-line-highlight > p:first-of-type {
  font-size: 1.25rem;
  font-weight: 900;
  color: #f3f4f6; /* text-gray-100 */
  line-height: 1.6;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-shadow: 0 2px 10px rgba(255,255,255,0.1);
  margin-bottom: 1.5rem;
  border-left: 4px solid var(--color-md-sys-primary, #a855f7);
  padding-left: 1rem;
}
</style>
