<template>
  <div class="bg-[var(--color-md-sys-surface)] md-elevation-1 rounded-[24px] p-6 md:p-8 flex flex-col gap-8 w-full transition-shadow hover:md-elevation-2 relative overflow-hidden">
    <!-- Background Glow based on score -->
    <div v-if="data.score !== undefined" class="absolute -top-32 -right-32 w-64 h-64 rounded-full blur-[80px] pointer-events-none opacity-20" :style="{ backgroundColor: scoreColor }"></div>
    
    <!-- Header -->
    <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-6 border-b border-[var(--color-md-sys-surface-variant)] relative z-10">
      <div class="flex items-center gap-4">
        <div class="p-3 bg-[var(--color-md-sys-secondary-container)] text-[var(--color-md-sys-on-secondary-container)] rounded-full">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        </div>
        <div>
          <h3 class="text-[22px] font-normal leading-[28px] text-[var(--color-md-sys-on-surface)]" style="font-family: 'Google Sans', sans-serif;">
            Evaluation Report
          </h3>
          <p class="text-sm text-[var(--color-md-sys-on-surface-variant)]">Based on your configured preferences</p>
        </div>
      </div>

      <!-- Score Visualizer -->
      <div v-if="data.score !== undefined" class="flex items-center gap-4 bg-[var(--color-md-sys-surface-variant)] px-5 py-3 rounded-2xl border border-[var(--color-md-sys-outline-variant)] shadow-sm">
        <div class="flex flex-col text-right">
          <span class="text-xs font-bold uppercase tracking-widest text-[var(--color-md-sys-on-surface-variant)]">AI Score</span>
          <span class="text-sm font-medium" :style="{ color: scoreColor }">{{ scoreLabel }}</span>
        </div>
        
        <div class="relative w-14 h-14 flex items-center justify-center">
          <svg class="w-full h-full transform -rotate-90 drop-shadow-md" viewBox="0 0 36 36">
            <path class="text-[var(--color-md-sys-outline-variant)]" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" stroke-width="3.5" />
            <path :style="{ color: scoreColor }" class="transition-all duration-1000 ease-out drop-shadow-lg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" stroke-width="3.5" :stroke-dasharray="`${data.score}, 100`" />
          </svg>
          <span class="absolute text-lg font-black" :style="{ color: scoreColor }">{{ data.score }}</span>
        </div>
      </div>
    </div>

    <!-- Red Flags Section -->
    <div class="flex flex-col gap-4">
      <h4 class="text-sm font-medium tracking-[0.1px] text-[var(--color-md-sys-error)] uppercase">Avoid (Red Flags)</h4>
      <div class="flex flex-wrap gap-2">
        <span
          v-for="info in data.avoid"
          :key="info.tag"
          :class="['inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300',
            info.contains
              ? 'bg-[var(--color-md-sys-error-container)] text-[var(--color-md-sys-on-error-container)] border border-[var(--color-md-sys-error)]'
              : 'bg-[var(--color-md-sys-surface-variant)] text-[var(--color-md-sys-on-surface-variant)] border border-[var(--color-md-sys-outline-variant)]']"
          :title="info.reasoning"
        >
          <svg v-if="info.contains" class="w-4 h-4 text-[var(--color-md-sys-error)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
          <svg v-else class="w-4 h-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
          
          {{ info.tag }} 
          <span v-if="info.probability" class="opacity-70 text-xs font-normal">
            {{ (info.probability * 100).toFixed(0) }}%
          </span>
        </span>
        <div v-if="!data.avoid || data.avoid.length === 0" class="text-sm text-[var(--color-md-sys-on-surface-variant)] italic">No criteria set</div>
      </div>
    </div>

    <!-- Favorites Section -->
    <div class="flex flex-col gap-4">
      <h4 class="text-sm font-medium tracking-[0.1px] text-[var(--color-md-sys-safe)] uppercase">Like (Favorites)</h4>
      <div class="flex flex-wrap gap-2">
        <span
          v-for="info in data.like"
          :key="info.tag"
          :class="['inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300',
            info.contains
              ? 'bg-[var(--color-md-sys-safe-container)] text-[var(--color-md-sys-on-safe-container)] border border-[var(--color-md-sys-safe)]'
              : 'bg-[var(--color-md-sys-surface-variant)] text-[var(--color-md-sys-on-surface-variant)] border border-[var(--color-md-sys-outline-variant)]']"
          :title="info.reasoning"
        >
          <svg v-if="info.contains" class="w-4 h-4 text-[var(--color-md-sys-safe)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
          <svg v-else class="w-4 h-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>
          
          {{ info.tag }} 
          <span v-if="info.probability" class="opacity-70 text-xs font-normal">
            {{ (info.probability * 100).toFixed(0) }}%
          </span>
        </span>
        <div v-if="!data.like || data.like.length === 0" class="text-sm text-[var(--color-md-sys-on-surface-variant)] italic">No criteria set</div>
      </div>
    </div>

    <!-- Reasoning Section -->
    <div class="flex flex-col gap-4 mt-4">
      <h4 class="text-sm font-medium tracking-[0.1px] text-[var(--color-md-sys-on-surface-variant)] uppercase">AI Reasoning</h4>
      <div
        class="reasoning-content text-[var(--color-md-sys-on-surface)] bg-[var(--color-md-sys-surface-variant)] p-6 rounded-[16px]"
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
    default: () => ({ avoid: [], like: [], reasoning: '' })
  }
})

const scoreColor = computed(() => {
  const s = props.data.score
  if (s === undefined) return 'var(--color-md-sys-primary)'
  if (s >= 80) return '#10B981' // Green
  if (s >= 50) return '#F59E0B' // Yellow
  return '#EF4444' // Red
})

const scoreLabel = computed(() => {
  const s = props.data.score
  if (s === undefined) return ''
  if (s >= 80) return 'Safe'
  if (s >= 50) return 'Caution'
  return 'Danger'
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
/* Base styles for markdown content in MD3 */
.reasoning-content p {
  margin-bottom: 1rem;
  line-height: 1.5;
  font-size: 16px;
  letter-spacing: 0.5px;
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
  font-weight: 500;
  color: var(--color-md-sys-primary);
}

/* Styled Blockquote for first sentence (MD3 flair) */
.reasoning-content .first-sentence-blockquote {
  display: block;
  font-family: 'Google Sans', sans-serif;
  font-size: 20px;
  line-height: 28px;
  font-weight: 400;
  padding: 1rem 1.25rem;
  margin-bottom: 1.5rem;
  border-left: 4px solid var(--color-md-sys-primary);
  color: var(--color-md-sys-on-surface);
  background: var(--color-md-sys-surface);
  border-radius: 0 8px 8px 0;
}
</style>
