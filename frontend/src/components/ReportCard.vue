<template>
  <div class="report-card liquid-glass p-6 rounded-xl">
    <div class="mb-8">
      <h3 class="text-xl font-bold mb-4 text-white tracking-wide">需要避免 (Avoid)</h3>
      <div class="flex flex-wrap gap-3">
        <span 
          v-for="info in data.avoid" 
          :key="info.tag"
          :class="['px-4 py-1.5 rounded-full text-sm font-medium transition-all duration-300', 
            info.contains 
              ? 'bg-[rgba(255,0,0,0.1)] text-[#ff4d4d] border border-[#ff4d4d] shadow-[0_0_12px_rgba(255,77,77,0.8)]' 
              : 'liquid-glass text-white/70 hover:text-white']"
          :title="info.reasoning"
        >
          {{ info.tag }} <span v-if="info.probability" class="opacity-80 ml-1 text-[10px]">{{ (info.probability * 100).toFixed(0) }}%</span>
        </span>
      </div>
    </div>

    <div class="mb-8">
      <h3 class="text-xl font-bold mb-4 text-white tracking-wide">推荐 (Like)</h3>
      <div class="flex flex-wrap gap-3">
        <span 
          v-for="info in data.like" 
          :key="info.tag"
          :class="['px-4 py-1.5 rounded-full text-sm font-medium transition-all duration-300', 
            info.contains 
              ? 'bg-[rgba(0,255,0,0.1)] text-[#00ff00] border border-[#00ff00] shadow-[0_0_12px_rgba(0,255,0,0.8)]' 
              : 'liquid-glass text-white/70 hover:text-white']"
          :title="info.reasoning"
        >
          {{ info.tag }} <span v-if="info.probability" class="opacity-80 ml-1 text-[10px]">{{ (info.probability * 100).toFixed(0) }}%</span>
        </span>
      </div>
    </div>

    <div>
      <h3 class="text-xl font-bold mb-4 text-white tracking-wide">原因分析 (Reasoning)</h3>
      <div 
        class="reasoning-content text-white/90"
        v-html="parsedReasoning"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { marked } from 'marked'

const props = defineProps({
  data: {
    type: Object,
    required: true,
    default: () => ({ avoid: {}, like: {}, reasoning: '' })
  }
})

const parsedReasoning = computed(() => {
  if (!props.data.reasoning) return ''
  
  const sentenceRegex = /^([^.!?。！？]+[.!?。！？]+)(?:\s|\n|$)([\s\S]*)$/
  const match = props.data.reasoning.match(sentenceRegex)
  
  let html = ''
  if (match) {
    const firstSentence = match[1]
    const rest = match[2]
    
    const markdownStr = `<div class="first-sentence-blockquote">${firstSentence}</div>\n\n${rest}`
    html = marked.parse(markdownStr)
  } else {
    const markdownStr = `<div class="first-sentence-blockquote">${props.data.reasoning}</div>`
    html = marked.parse(markdownStr)
  }
  
  return html
})
</script>

<style>
/* Base styles for markdown content */
.reasoning-content p {
  margin-bottom: 1rem;
  line-height: 1.7;
}
.reasoning-content ul {
  list-style-type: disc;
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}
.reasoning-content ol {
  list-style-type: decimal;
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}
.reasoning-content strong {
  color: #fff;
  font-weight: 600;
}
.reasoning-content code {
  background: rgba(255, 255, 255, 0.1);
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-family: monospace;
  font-size: 0.9em;
}

/* CSS to style the first sentence as enlarged bold Blockquote */
.reasoning-content .first-sentence-blockquote {
  display: block;
  font-size: 1.3rem;
  font-weight: 700;
  padding: 1.2rem 1.5rem;
  margin-bottom: 1.5rem;
  border-left: 4px solid var(--md-sys-color-tertiary, #00e5ff);
  color: #ffffff;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0 0.5rem 0.5rem 0;
  box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.02);
  line-height: 1.6;
}
</style>
