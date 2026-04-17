<template>
  <div class="min-h-screen w-full bg-[#030303] text-white selection:bg-purple-500/30 font-sans overflow-x-hidden">
    <!-- Background Effects -->
    <div class="fixed inset-0 pointer-events-none z-0">
      <!-- Noise Texture -->
      <div class="absolute inset-0 opacity-[0.03] mix-blend-overlay" style="background-image: url('data:image/svg+xml,%3Csvg viewBox=%220 0 200 200%22 xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cfilter id=%22noiseFilter%22%3E%3CfeTurbulence type=%22fractalNoise%22 baseFrequency=%220.65%22 numOctaves=%223%22 stitchTiles=%22stitch%22/%3E%3C/filter%3E%3Crect width=%22100%25%22 height=%22100%25%22 filter=%22url(%23noiseFilter)%22/%3E%3C/svg%3E');"></div>
      <!-- Radial Gradients -->
      <div class="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-purple-600/20 blur-[120px] rounded-full mix-blend-screen animate-pulse-slow"></div>
      <div class="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-indigo-600/10 blur-[120px] rounded-full mix-blend-screen animate-pulse-slow" style="animation-delay: 2s;"></div>
      <!-- Grid -->
      <div class="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:64px_64px] [mask-image:radial-gradient(ellipse_80%_80%_at_50%_0%,#000_20%,transparent_100%)]"></div>
    </div>

    <!-- Main Content -->
    <div class="relative z-10 max-w-6xl mx-auto px-6 pt-32 pb-24 flex flex-col items-center">
      
      <!-- Hero Section -->
      <div class="flex flex-col items-center text-center animate-fade-in-up">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-purple-300 text-sm font-medium mb-8 backdrop-blur-md shadow-[0_0_20px_rgba(168,85,247,0.15)]">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-purple-500"></span>
          </span>
          System v2.0 Online
        </div>

        <h1 class="text-5xl md:text-7xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-b from-white via-gray-200 to-gray-500 mb-6 leading-tight">
          AI 智能本子鉴定雷达
        </h1>
        
        <p class="text-lg md:text-xl text-gray-400 mb-12 max-w-3xl leading-relaxed font-light">
          接入你的多模态大模型，全网自动扫描 JM 与 Reddit 评论区。<br class="hidden md:block" />
          以极其严苛的法则为你精准排除牛头人与猎奇毒点，保卫纯爱阅读体验。
        </p>

        <!-- CTA Button -->
        <button @click="$router.push('/radar')" class="group relative inline-flex items-center justify-center px-8 py-4 font-bold text-white transition-all duration-300 bg-purple-600 rounded-2xl hover:bg-purple-500 hover:scale-[1.02] active:scale-[0.98] shadow-[0_0_40px_rgba(147,51,234,0.4)] hover:shadow-[0_0_60px_rgba(147,51,234,0.6)] overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-r from-purple-400/0 via-white/20 to-purple-400/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
          <span class="relative flex items-center gap-3 text-lg tracking-wide">
            启动鉴定序列
            <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 7l5 5m0 0l-5 5m5-5H6"></path></svg>
          </span>
        </button>
      </div>

      <!-- Feature Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-32 w-full animate-fade-in-up" style="animation-delay: 0.2s;">
        
        <!-- Feature 1 -->
        <div class="group relative p-8 rounded-3xl bg-white/[0.02] border border-white/5 hover:border-purple-500/30 transition-colors duration-500 backdrop-blur-sm overflow-hidden">
          <div class="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-purple-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative z-10">
            <div class="w-14 h-14 rounded-2xl bg-purple-500/20 flex items-center justify-center text-purple-400 mb-6 border border-purple-500/20 shadow-[0_0_15px_rgba(168,85,247,0.2)]">
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-100 mb-3">多模态大模型引擎</h3>
            <p class="text-gray-400 leading-relaxed">
              支持接入 OpenAI / Gemini 视觉大模型。自动抓取图集封面并转为 Base64 编码喂给 AI，结合文本简介与用户补充要求，实现全方位深度剧情推演。
            </p>
          </div>
        </div>

        <!-- Feature 2 -->
        <div class="group relative p-8 rounded-3xl bg-white/[0.02] border border-white/5 hover:border-blue-500/30 transition-colors duration-500 backdrop-blur-sm overflow-hidden">
          <div class="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-blue-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative z-10">
            <div class="w-14 h-14 rounded-2xl bg-blue-500/20 flex items-center justify-center text-blue-400 mb-6 border border-blue-500/20 shadow-[0_0_15px_rgba(59,130,246,0.2)]">
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-100 mb-3">全网舆情深度扫描</h3>
            <p class="text-gray-400 leading-relaxed">
              打破信息孤岛。不仅自动提取 JM 平台最新精选评论，更通过第三方接口检索 Reddit 英文社区相关讨论，将被坑网友的真实反馈作为最高裁决证据。
            </p>
          </div>
        </div>

        <!-- Feature 3 -->
        <div class="group relative p-8 rounded-3xl bg-white/[0.02] border border-white/5 hover:border-red-500/30 transition-colors duration-500 backdrop-blur-sm overflow-hidden">
          <div class="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-red-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative z-10">
            <div class="w-14 h-14 rounded-2xl bg-red-500/20 flex items-center justify-center text-red-400 mb-6 border border-red-500/20 shadow-[0_0_15px_rgba(239,68,68,0.2)]">
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-100 mb-3">极度严苛排雷法则</h3>
            <p class="text-gray-400 leading-relaxed">
              内置“处女默认假设”与严格的“纯女”定义限制（绝不允许任何男主以外的触碰暗示）。拒绝教条主义与作者滤镜，宁可错杀绝不放过，只为你呈现绝对纯净。
            </p>
          </div>
        </div>

        <!-- Feature 4 -->
        <div class="group relative p-8 rounded-3xl bg-white/[0.02] border border-white/5 hover:border-emerald-500/30 transition-colors duration-500 backdrop-blur-sm overflow-hidden">
          <div class="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-emerald-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative z-10">
            <div class="w-14 h-14 rounded-2xl bg-emerald-500/20 flex items-center justify-center text-emerald-400 mb-6 border border-emerald-500/20 shadow-[0_0_15px_rgba(16,185,129,0.2)]">
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-100 mb-3">AI 综合评分与可视化</h3>
            <p class="text-gray-400 leading-relaxed">
              分析完成后提供 0-100 的综合安全度评分，配合极具现代感的数据可视化图表。附带 300 字以上的深情感排雷长文，支持一键导出 Markdown 或 JSON 报告。
            </p>
          </div>
        </div>

      </div>

      <!-- Footer Elements -->
      <div class="mt-24 flex items-center justify-center gap-6 text-gray-500 text-sm animate-fade-in-up" style="animation-delay: 0.4s;">
        <span class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-gray-500"></div> 100% 隐私安全 (本地保存)</span>
        <span class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-gray-500"></div> 支持配置云端同步导出</span>
        <span class="flex items-center gap-2"><div class="w-1.5 h-1.5 rounded-full bg-gray-500"></div> MD3 Expressive 架构</span>
      </div>
    </div>
  </div>
</template>

<script setup>
// Landing View - fully static frontend
</script>

<style scoped>
.animate-fade-in-up {
  animation: fadeInUp 0.8s cubic-bezier(0.2, 0, 0, 1) both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-pulse-slow {
  animation: pulseSlow 8s ease-in-out infinite alternate;
}

@keyframes pulseSlow {
  0% { opacity: 0.3; transform: scale(1); }
  100% { opacity: 0.7; transform: scale(1.05); }
}
</style>
