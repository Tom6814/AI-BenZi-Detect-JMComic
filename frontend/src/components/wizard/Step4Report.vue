<script setup>
import { computed } from 'vue'
import ReportCard from '../ReportCard.vue'

const props = defineProps({
  reportData: {
    type: Object,
    default: () => null
  }
})
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-8 animate-fade-in flex flex-col items-center">
    <header class="text-center space-y-4 w-full mb-8">
      <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-[rgba(0,255,100,0.1)] border border-[rgba(0,255,100,0.3)] text-green-400 shadow-[0_0_15px_rgba(0,255,100,0.2)] mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
      </div>
      <h1 class="text-3xl md:text-4xl font-bold tracking-widest text-neon-tertiary uppercase">鉴定报告</h1>
      <p class="text-white/60 tracking-widest text-sm font-mono">NEURAL ANALYSIS COMPLETE</p>
    </header>

    <div v-if="reportData" class="w-full">
      <ReportCard :data="reportData" />
    </div>
    <div v-else class="w-full text-center text-white/50 p-12 liquid-glass rounded-xl font-mono">
      暂无数据，请返回上一步重新鉴定。
    </div>
  </div>
</template>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
