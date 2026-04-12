<script setup>
import { computed } from 'vue'
import ReportCard from '../ReportCard.vue'

const props = defineProps({
  reportData: Object
})
const emit = defineEmits(['reset'])

// Provide mock if needed
const data = computed(() => {
  if (props.reportData && props.reportData.reasoning) return props.reportData
  return {
    avoid: [
      { tag: "NTR", contains: false, probability: 0.05, reasoning: "None found" },
      { tag: "Gore", contains: true, probability: 0.99, reasoning: "Blood visible" }
    ],
    like: [
      { tag: "Pure Love", contains: false, probability: 0.10, reasoning: "Not matching" }
    ],
    reasoning: "核弹级雷区，快跑！\n\n- **画风与作者**：作者履历充满了黑暗猎奇元素...\n- **剧情推测**：封面血迹斑斑..."
  }
})
</script>

<template>
  <div class="flex flex-col items-center w-full h-full p-8 relative overflow-y-auto">
    <div class="absolute top-6 left-8 z-20">
      <button @click="emit('reset')" class="text-white/40 hover:text-white/80 transition-colors uppercase text-xs font-bold tracking-widest flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
        New Scan
      </button>
    </div>

    <div class="text-center mb-8 mt-4 relative z-10">
      <h2 class="text-3xl font-extrabold tracking-[0.2em] uppercase text-white/90 drop-shadow-[0_0_15px_rgba(255,255,255,0.3)]">Analysis Complete</h2>
      <p class="text-cyan-400/80 tracking-widest text-xs uppercase mt-2 drop-shadow-[0_0_5px_rgba(0,229,255,0.5)]">Review Threat Assessment</p>
    </div>

    <div class="w-full max-w-4xl relative z-10">
      <ReportCard :data="data" />
    </div>
  </div>
</template>

<style scoped>
.scrollbar-thin::-webkit-scrollbar {
  width: 4px;
}
.scrollbar-thin::-webkit-scrollbar-thumb {
  background: rgba(255,255,255,0.1);
  border-radius: 4px;
}
</style>
