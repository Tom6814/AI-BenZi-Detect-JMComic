file_path = 'frontend/src/components/radar/PhaseTarget.vue'
content = open(file_path, 'r', encoding='utf-8').read()

# Enhance waiting animation
old_overlay = """    <!-- Analyzing Overlay (Inspired by Tom6814's approach) -->
    <div v-if="analyzing" class="absolute inset-0 z-40 bg-[var(--color-md-sys-surface)]/95 backdrop-blur-sm flex flex-col items-center justify-center p-8 transition-all">
      <div class="bg-[var(--color-md-sys-surface-variant)] border border-[var(--color-md-sys-outline-variant)] rounded-3xl p-10 flex flex-col items-center justify-center max-w-md w-full md-elevation-3">
        <div class="relative w-20 h-20 mb-8">
          <div class="absolute inset-0 border-4 border-[var(--color-md-sys-primary)]/20 rounded-full"></div>
          <div class="absolute inset-0 border-4 border-[var(--color-md-sys-primary)] border-t-transparent rounded-full animate-spin"></div>
          <svg class="absolute inset-0 m-auto w-8 h-8 text-[var(--color-md-sys-primary)] animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
        </div>
        <h3 class="text-2xl font-medium text-[var(--color-md-sys-on-surface)] mb-3">AI 正在深度分析中...</h3>
        <p class="text-[var(--color-md-sys-on-surface-variant)] text-center text-sm">
          正在检索全网同人设定与评论数据<br/>
          <span class="opacity-70">（思考过程已隐藏，请耐心等待结果）</span>
        </p>
      </div>
    </div>"""

new_overlay = """    <!-- Analyzing Overlay (MD3 Expressive Radar Glow) -->
    <div v-if="analyzing" class="absolute inset-0 z-40 bg-[#0a0a0a]/80 backdrop-blur-md flex flex-col items-center justify-center p-8 transition-all duration-500 overflow-hidden">
      <!-- Glows -->
      <div class="absolute w-[600px] h-[600px] bg-[var(--color-md-sys-primary)]/10 rounded-full blur-[100px] animate-[pulse_4s_ease-in-out_infinite]"></div>
      
      <div class="relative z-10 flex flex-col items-center">
        <!-- Radar Spinner -->
        <div class="relative w-32 h-32 mb-10 flex items-center justify-center">
          <div class="absolute inset-0 border border-[var(--color-md-sys-primary)]/30 rounded-full scale-[1.5] animate-[ping_2s_cubic-bezier(0,0,0.2,1)_infinite]"></div>
          <div class="absolute inset-0 border-2 border-[var(--color-md-sys-primary)]/50 rounded-full scale-[1.2] animate-[ping_2s_cubic-bezier(0,0,0.2,1)_infinite_0.5s]"></div>
          <div class="absolute inset-0 border-[3px] border-[var(--color-md-sys-primary)] rounded-full animate-[spin_3s_linear_infinite]" style="border-right-color: transparent; border-top-color: transparent;"></div>
          <div class="absolute inset-0 border-[3px] border-[var(--color-md-sys-tertiary)] rounded-full animate-[spin_2s_linear_infinite_reverse]" style="border-left-color: transparent; border-bottom-color: transparent; scale: 0.8;"></div>
          
          <div class="bg-[var(--color-md-sys-surface)] rounded-full p-4 shadow-[0_0_30px_rgba(var(--color-md-sys-primary-rgb),0.5)] z-10">
            <svg class="w-10 h-10 text-[var(--color-md-sys-primary)] animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
          </div>
        </div>

        <h3 class="text-3xl font-bold text-white tracking-wide mb-4 drop-shadow-[0_0_10px_rgba(255,255,255,0.5)]">AI 正在深度分析中</h3>
        <p class="text-white/70 text-center text-base max-w-md leading-relaxed">
          正在读取图集信息及精选评论...<br/>
          正在连接大模型进行成分推演...<br/>
          <span class="text-[var(--color-md-sys-primary)] text-sm font-medium mt-2 inline-block animate-pulse">Please wait while the neural network processes...</span>
        </p>
      </div>
    </div>"""

content = content.replace(old_overlay, new_overlay)

# Add Settings button to PhaseTarget
settings_btn = """    <div class="absolute top-8 right-8 md:top-12 md:right-12 z-20">
      <button @click="$emit('back', 'INIT')" class="p-3 rounded-full text-[var(--color-md-sys-on-surface-variant)] hover:bg-[var(--color-md-sys-surface-variant)] transition-all hover:text-[var(--color-md-sys-primary)] md-ripple active:scale-[0.95] flex items-center justify-center shadow-sm">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
      </button>
    </div>"""

# Insert settings button near the back button
back_btn = """    <div class="absolute top-8 left-8 md:top-12 md:left-12 z-20">"""
content = content.replace(back_btn, settings_btn + "\n" + back_btn)

open(file_path, 'w', encoding='utf-8').write(content)
print("Updated PhaseTarget.vue.")
