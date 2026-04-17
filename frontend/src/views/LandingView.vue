<template>
  <div class="landing-container min-h-screen w-full flex flex-col items-center justify-center relative overflow-hidden bg-[#0A0A0A]">
    <!-- Background grid & glow -->
    <div class="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.05)_1px,transparent_1px)] bg-[size:40px_40px] [mask-image:radial-gradient(ellipse_60%_60%_at_50%_50%,#000_10%,transparent_100%)] pointer-events-none opacity-50"></div>
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-purple-600/20 rounded-full blur-[120px] pointer-events-none mix-blend-screen"></div>

    <div class="relative z-10 flex flex-col items-center max-w-3xl mx-auto px-6 text-center">
      <!-- Icon/Logo -->
      <div class="w-24 h-24 bg-white/5 rounded-2xl border border-white/10 flex items-center justify-center mb-8 shadow-[0_0_30px_rgba(168,85,247,0.2)]">
        <svg class="w-12 h-12 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path></svg>
      </div>

      <h1 class="text-5xl md:text-6xl font-black text-transparent bg-clip-text bg-gradient-to-br from-white via-gray-200 to-gray-500 mb-6 tracking-tight">
        AI Doujinshi Radar
      </h1>
      
      <p class="text-lg md:text-xl text-gray-400 mb-12 max-w-2xl leading-relaxed">
        An advanced threat-assessment system for analyzing doujinshi content. Connect your AI, define your red flags, and scan JM/Reddit data to ensure a safe reading experience.
      </p>

      <button @click="$router.push('/radar')" class="group relative px-8 py-4 bg-purple-600 hover:bg-purple-500 text-white font-bold rounded-xl text-lg transition-all duration-300 shadow-[0_0_20px_rgba(147,51,234,0.4)] hover:shadow-[0_0_30px_rgba(147,51,234,0.6)] active:scale-[0.98] overflow-hidden">
        <span class="relative z-10 flex items-center gap-2">
          Start Analysis Sequence
          <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path></svg>
        </span>
        <div class="absolute inset-0 bg-gradient-to-r from-purple-400 to-purple-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
      </button>

      <div class="mt-16 flex items-center gap-6 text-sm text-gray-500 flex-wrap justify-center">
        <div class="flex items-center gap-2">
          <svg class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
          OpenAI / Gemini Support
        </div>
        <div class="flex items-center gap-2">
          <svg class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
          Reddit Context Integration
        </div>
        <div class="flex items-center gap-2">
          <svg class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
          Exportable Reports
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>
