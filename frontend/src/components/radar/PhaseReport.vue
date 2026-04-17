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

const exportReport = () => {
  const content = JSON.stringify(data.value, null, 2)
  const blob = new Blob([content], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `ai_doujin_report_${new Date().getTime()}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const exportMarkdown = () => {
  let md = `# AI Doujinshi Analysis Report\n\n`
  md += `## 避雷警告 (Avoid)\n`
  data.value.avoid.forEach(item => {
    md += `- **${item.tag}**: ${item.contains ? '⚠️ 存在' : '✅ 安全'} (概率: ${(item.probability * 100).toFixed(0)}%)\n  - 理由: ${item.reasoning}\n`
  })
  
  md += `\n## 喜好匹配 (Like)\n`
  data.value.like.forEach(item => {
    md += `- **${item.tag}**: ${item.contains ? '💖 匹配' : '❌ 未匹配'} (概率: ${(item.probability * 100).toFixed(0)}%)\n  - 理由: ${item.reasoning}\n`
  })
  
  md += `\n## 整体分析 (Reasoning)\n\n`
  md += data.value.reasoning + "\n"

  const blob = new Blob([md], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `ai_doujin_report_${new Date().getTime()}.md`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
</script>

<template>
  <div class="flex flex-col items-center w-full h-full p-8 relative overflow-y-auto">
    <div class="absolute top-6 left-8 z-20 flex gap-4">
      <button @click="emit('reset')" class="text-[var(--color-md-sys-on-surface-variant)] hover:text-[var(--color-md-sys-primary)] transition-all active:scale-[0.95] uppercase text-xs font-bold tracking-widest flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-[var(--color-md-sys-surface-variant)]">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
        New Scan
      </button>
    </div>

    <div class="absolute top-6 right-8 z-20 flex gap-2">
      <button @click="exportMarkdown" class="text-[var(--color-md-sys-on-surface-variant)] hover:text-[var(--color-md-sys-primary)] transition-all active:scale-[0.95] uppercase text-xs font-bold tracking-widest flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-[var(--color-md-sys-surface-variant)]">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
        Export MD
      </button>
      <button @click="exportReport" class="text-[var(--color-md-sys-on-surface-variant)] hover:text-[var(--color-md-sys-primary)] transition-all active:scale-[0.95] uppercase text-xs font-bold tracking-widest flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-[var(--color-md-sys-surface-variant)]">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
        JSON
      </button>
    </div>

    <div class="text-center mb-8 mt-4 relative z-10">
      <h2 class="text-3xl font-extrabold tracking-[0.2em] uppercase text-[var(--color-md-sys-on-surface)] drop-shadow-[0_0_15px_rgba(255,255,255,0.1)]">Analysis Complete</h2>
      <p class="text-[var(--color-md-sys-primary)] tracking-widest text-xs uppercase mt-2">Review Threat Assessment</p>
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
