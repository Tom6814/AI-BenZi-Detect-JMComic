<script setup>
import { useMainStore } from '../store'
import { ref } from 'vue'

const store = useMainStore()
const count = ref(0)
</script>

<template>
  <div class="space-y-8 animate-fade-in">
    <header class="space-y-4">
      <h1 class="text-4xl md:text-6xl font-extrabold tracking-tight text-neon-primary drop-shadow-lg">
        Aurora Neon
      </h1>
      <p class="text-lg md:text-xl text-white/80 max-w-2xl font-light">
        A breathtaking visual experience powered by Vue 3, Vite, and Tailwind CSS. Embrace the fusion of <span class="text-neon-tertiary font-medium">Material 3 Expressive</span> colors and liquid glassmorphism.
      </p>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Pinia Card -->
      <div class="liquid-glass p-6 hover:-translate-y-1 transition-transform duration-300">
        <h3 class="text-xl font-semibold mb-3 text-neon-tertiary">Pinia Store</h3>
        <p class="text-white/70 mb-4 text-sm">{{ store.message }}</p>
        <button 
          @click="store.updateMessage('State updated via Pinia!')"
          class="px-4 py-2 rounded bg-gradient-to-r from-[var(--color-primary-container)] to-[var(--color-primary)] text-[var(--color-on-primary)] font-medium shadow-lg hover:opacity-90 active:scale-95 transition-all"
        >
          Update State
        </button>
      </div>

      <!-- Counter Card -->
      <div class="liquid-glass p-6 hover:-translate-y-1 transition-transform duration-300 flex flex-col items-start justify-between">
        <div>
          <h3 class="text-xl font-semibold mb-3 text-neon-tertiary">Interactive</h3>
          <p class="text-white/70 mb-4 text-sm">Vue's reactivity makes this counter feel instantaneous.</p>
        </div>
        <button 
          @click="count++"
          class="px-4 py-2 rounded bg-gradient-to-r from-[var(--color-tertiary)] to-cyan-400 text-[#00363d] font-bold shadow-[0_0_15px_rgba(0,229,255,0.4)] hover:shadow-[0_0_25px_rgba(0,229,255,0.6)] active:scale-95 transition-all"
        >
          Count is {{ count }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}
</style>
