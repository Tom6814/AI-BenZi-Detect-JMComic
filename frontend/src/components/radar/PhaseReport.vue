<script setup>
import { computed, ref, onMounted, nextTick } from 'vue'
import ReportCard from '../ReportCard.vue'
import confetti from 'canvas-confetti'
import * as htmlToImage from 'html-to-image'

const props = defineProps({
  reportData: Object
})
const emit = defineEmits(['reset'])

const reportRef = ref(null)
const isExportMenuOpen = ref(false)

const data = computed(() => {
  if (props.reportData && props.reportData.reasoning) return props.reportData
  return {
    score: 15,
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

onMounted(() => {
  // Add ceremonial effects based on score
  if (data.value.score !== undefined) {
    if (data.value.score >= 55) {
      fireConfetti()
    }
  }
})

const fireConfetti = () => {
  const duration = 3 * 1000
  const animationEnd = Date.now() + duration
  const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 100 }

  function randomInRange(min, max) {
    return Math.random() * (max - min) + min
  }

  const interval = setInterval(function() {
    const timeLeft = animationEnd - Date.now()

    if (timeLeft <= 0) {
      return clearInterval(interval)
    }

    const particleCount = 50 * (timeLeft / duration)
    confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } }))
    confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } }))
  }, 250)
}

const toggleExportMenu = () => {
  isExportMenuOpen.value = !isExportMenuOpen.value
}

const exportJSON = () => {
  const content = JSON.stringify(data.value, null, 2)
  const blob = new Blob([content], { type: 'application/json' })
  downloadBlob(blob, `ai_doujin_report_${new Date().getTime()}.json`)
  isExportMenuOpen.value = false
}

const exportMarkdown = () => {
  let md = `# AI Doujinshi Analysis Report\n\n`
  if (data.value.score !== undefined) {
    md += `## 综合评分: ${data.value.score} / 100\n\n`
  }
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
  downloadBlob(blob, `ai_doujin_report_${new Date().getTime()}.md`)
  isExportMenuOpen.value = false
}

const exportHTML = () => {
  const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AI Doujinshi Report</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0A0A0A; color: #fff; padding: 40px; }
    .container { max-w-4xl; margin: 0 auto; background: #1A1A1A; padding: 40px; border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    h1 { color: #A855F7; text-align: center; }
    .score { text-align: center; font-size: 48px; font-weight: 900; margin: 20px 0; color: ${data.value.score >= 80 ? '#10B981' : data.value.score >= 50 ? '#F59E0B' : '#EF4444'}; }
    .section { margin-top: 30px; }
    .section h2 { border-bottom: 1px solid #333; padding-bottom: 10px; color: #E5E7EB; }
    .tag-list { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; }
    .tag { padding: 8px 12px; border-radius: 8px; font-size: 14px; font-weight: bold; }
    .tag.avoid-true { background: #450a0a; color: #fca5a5; border: 1px solid #ef4444; }
    .tag.avoid-false { background: #262626; color: #9ca3af; }
    .tag.like-true { background: #064e3b; color: #6ee7b7; border: 1px solid #10b981; }
    .tag.like-false { background: #262626; color: #9ca3af; }
    .reasoning { background: #262626; padding: 20px; border-radius: 16px; line-height: 1.6; margin-top: 20px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>AI Doujinshi Radar Report</h1>
    ${data.value.score !== undefined ? `<div class="score">${data.value.score} / 100</div>` : ''}
    
    <div class="section">
      <h2>Avoid (Red Flags)</h2>
      <div class="tag-list">
        ${data.value.avoid.map(i => `<div class="tag avoid-${i.contains}">${i.tag} (${(i.probability * 100).toFixed(0)}%) - ${i.reasoning}</div>`).join('')}
      </div>
    </div>
    
    <div class="section">
      <h2>Like (Favorites)</h2>
      <div class="tag-list">
        ${data.value.like.map(i => `<div class="tag like-${i.contains}">${i.tag} (${(i.probability * 100).toFixed(0)}%) - ${i.reasoning}</div>`).join('')}
      </div>
    </div>
    
    <div class="section">
      <h2>AI Reasoning</h2>
      <div class="reasoning">
        ${data.value.reasoning.replace(/\n/g, '<br/>')}
      </div>
    </div>
  </div>
</body>
</html>
`
  const blob = new Blob([htmlContent], { type: 'text/html' })
  downloadBlob(blob, `ai_doujin_report_${new Date().getTime()}.html`)
  isExportMenuOpen.value = false
}

const exportImage = async () => {
  if (!reportRef.value) return
  isExportMenuOpen.value = false

  // Wait for dropdown to close visually
  await nextTick()

  try {
    const el = reportRef.value.$el || reportRef.value
    const dataUrl = await htmlToImage.toPng(el, {
      backgroundColor: '#121212',
      pixelRatio: 2,
      skipFonts: false
    })

    // Create a temporary link to download
    const a = document.createElement('a')
    a.href = dataUrl
    a.download = `ai_doujin_report_${new Date().getTime()}.png`
    
    // For iOS Safari compatibility: open in new tab if download fails or if it's Safari
    const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent)
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)
    
    // Attempt native share API first for mobile devices
    if ((isIOS || /Android/i.test(navigator.userAgent)) && navigator.canShare) {
      try {
        const response = await fetch(dataUrl)
        const blob = await response.blob()
        const file = new File([blob], a.download, { type: 'image/png' })
        if (navigator.canShare({ files: [file] })) {
          await navigator.share({
            files: [file],
            title: 'AI 本子雷达分析报告',
            text: '这是我用 AI 生成的本子雷达鉴定报告，快来看看吧！'
          })
          return
        }
      } catch (shareErr) {
        console.warn('Share API failed or cancelled', shareErr)
        // Fallthrough to manual download
      }
    }

    if (isIOS || isSafari) {
      // In iOS Safari, triggering download via a tag with base64 dataUrl sometimes fails silently
      // Opening in a new window/tab allows the user to long-press and save
      const win = window.open()
      if (win) {
        win.document.write(`<img src="${dataUrl}" style="width: 100%; height: auto;" />`)
        win.document.title = "Long press to save"
      } else {
        // Fallback if popup blocker is active
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
      }
    } else {
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
    }
  } catch (err) {
    console.error('Failed to export image', err)
    alert('Failed to generate image.')
  }
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
</script>

<template>
  <div class="flex flex-col items-center w-full h-full p-8 relative overflow-y-auto overflow-x-hidden bg-[#0a0a0a]">
    
    <!-- Red Alert Overlay -->
    <div 
      v-if="data.score !== undefined && data.score < 30" 
      class="fixed inset-0 pointer-events-none z-0 animate-red-alert mix-blend-screen"
    ></div>

    <!-- Controls Bar -->
    <div class="w-full max-w-4xl flex justify-between items-center z-50 mb-8 mt-2 relative">
      <button @click="emit('reset')" class="group px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-gray-300 hover:text-white transition-all flex items-center gap-2 text-sm font-medium backdrop-blur-sm">
        <svg class="w-4 h-4 group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
        New Scan
      </button>

      <!-- Export Dropdown -->
      <div class="relative">
        <button 
          @click="toggleExportMenu" 
          class="px-5 py-2 bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/30 rounded-xl text-purple-300 hover:text-purple-200 transition-all flex items-center gap-2 text-sm font-medium backdrop-blur-sm shadow-[0_0_15px_rgba(168,85,247,0.15)]"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
          Export Report
          <svg class="w-4 h-4 transition-transform" :class="isExportMenuOpen ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
        </button>

        <!-- Dropdown Menu -->
        <transition name="dropdown">
          <div v-if="isExportMenuOpen" class="absolute right-0 mt-2 w-48 bg-[#1a1a1a] border border-white/10 rounded-xl shadow-2xl overflow-hidden z-50 origin-top-right">
            <button @click="exportImage" class="w-full text-left px-4 py-3 text-sm text-gray-300 hover:bg-purple-500/20 hover:text-purple-300 transition-colors flex items-center gap-2 border-b border-white/5">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
              Save as Image (PNG)
            </button>
            <button @click="exportHTML" class="w-full text-left px-4 py-3 text-sm text-gray-300 hover:bg-purple-500/20 hover:text-purple-300 transition-colors flex items-center gap-2 border-b border-white/5">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path></svg>
              Save as HTML
            </button>
            <button @click="exportMarkdown" class="w-full text-left px-4 py-3 text-sm text-gray-300 hover:bg-purple-500/20 hover:text-purple-300 transition-colors flex items-center gap-2 border-b border-white/5">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
              Save as Markdown
            </button>
            <button @click="exportJSON" class="w-full text-left px-4 py-3 text-sm text-gray-300 hover:bg-purple-500/20 hover:text-purple-300 transition-colors flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
              Save as JSON
            </button>
          </div>
        </transition>
      </div>
    </div>

    <!-- Title Header -->
    <div class="text-center mb-10 z-10 animate-fade-in-up">
      <h2 class="text-4xl md:text-5xl font-black tracking-tight text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-400 drop-shadow-[0_0_15px_rgba(255,255,255,0.1)]">
        Analysis Complete
      </h2>
      <p class="text-purple-400 tracking-[0.2em] text-sm uppercase mt-3 font-semibold">Review Threat Assessment</p>
    </div>

    <!-- Report Card Container -->
    <div class="w-full max-w-4xl relative z-10 animate-fade-in-up" style="animation-delay: 0.1s;">
      <ReportCard ref="reportRef" :data="data" />
    </div>

    <!-- Click outside handler overlay -->
    <div v-if="isExportMenuOpen" @click="isExportMenuOpen = false" class="fixed inset-0 z-40"></div>
  </div>
</template>

<style scoped>
.animate-fade-in-up {
  animation: fadeInUp 0.6s cubic-bezier(0.2, 0, 0, 1) both;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s cubic-bezier(0.2, 0, 0, 1);
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}

.animate-red-alert {
  animation: redAlert 2s ease-in-out infinite alternate;
  box-shadow: inset 0 0 150px rgba(239, 68, 68, 0.4);
  border: 4px solid rgba(239, 68, 68, 0.2);
}

@keyframes redAlert {
  0% { opacity: 0.2; }
  100% { opacity: 0.8; box-shadow: inset 0 0 250px rgba(239, 68, 68, 0.6); }
}

.scrollbar-thin::-webkit-scrollbar {
  width: 4px;
}
.scrollbar-thin::-webkit-scrollbar-thumb {
  background: rgba(255,255,255,0.1);
  border-radius: 4px;
}
</style>
