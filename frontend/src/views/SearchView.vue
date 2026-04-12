<script setup>
import { ref, computed } from 'vue'

const searchQuery = ref('')
const isNumber = computed(() => /^\d+$/.test(searchQuery.value))
const hasSearched = ref(false)

const handleSearch = () => {
  if (!searchQuery.value.trim()) return
  hasSearched.value = true
}

// Mock data for grid
const mockResults = Array.from({ length: 6 }).map((_, i) => ({
  id: i + 1,
  title: `Neural Node ${i + 1}`,
  description: `Quantum data fragment ${Math.random().toString(36).substring(7)}`,
  status: Math.random() > 0.5 ? 'Active' : 'Standby'
}))

</script>

<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <header class="text-center space-y-4 mb-12">
      <h1 class="text-4xl md:text-5xl font-bold tracking-widest text-neon-tertiary uppercase">Data Nexus</h1>
      <p class="text-white/60 tracking-widest text-sm">QUANTUM SEARCH INTERFACE</p>
    </header>

    <!-- Search Input -->
    <div class="relative max-w-2xl mx-auto group">
      <div class="absolute inset-0 bg-neon-tertiary/20 blur-xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
      <div class="relative liquid-glass rounded-full flex items-center p-2">
        <div class="pl-4 text-neon-tertiary">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <input 
          v-model="searchQuery"
          @keyup.enter="handleSearch"
          type="text" 
          class="w-full bg-transparent border-none px-4 py-3 text-white focus:outline-none focus:ring-0 placeholder-white/30"
          placeholder="Enter access code or text query..."
        />
        <button 
          @click="handleSearch"
          class="bg-[rgba(0,229,255,0.1)] border border-[rgba(0,229,255,0.3)] text-neon-tertiary px-6 py-2 rounded-full hover:bg-[rgba(0,229,255,0.2)] active:scale-95 transition-all duration-300 font-medium whitespace-nowrap"
        >
          Initialize
        </button>
      </div>
    </div>

    <!-- Results Area -->
    <transition name="fade" mode="out-in">
      <div v-if="hasSearched && searchQuery" class="mt-12">
        
        <!-- Direct Lock UI (Numbers Only) -->
        <div v-if="isNumber" class="flex justify-center items-center py-12">
          <div class="liquid-glass p-12 rounded-3xl text-center space-y-8 relative overflow-hidden group w-full max-w-md">
            <div class="absolute inset-0 bg-neon-primary/5 blur-3xl rounded-full opacity-50"></div>
            
            <div class="relative z-10">
              <div class="w-24 h-24 mx-auto border-4 border-[rgba(255,84,73,0.3)] rounded-full flex items-center justify-center mb-6 shadow-[0_0_30px_rgba(255,84,73,0.2)]">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-neon-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h2 class="text-2xl font-bold text-neon-primary tracking-widest mb-2">DIRECT LOCK</h2>
              <p class="text-white/60 mb-8 font-mono">ID: {{ searchQuery }}</p>
              
              <button class="w-full bg-[rgba(255,84,73,0.1)] border border-[rgba(255,84,73,0.3)] text-neon-primary py-3 rounded-lg hover:bg-[rgba(255,84,73,0.2)] hover:shadow-[0_0_20px_rgba(255,84,73,0.3)] transition-all duration-300 tracking-widest">
                ENGAGE OVERRIDE
              </button>
            </div>
          </div>
        </div>

        <!-- Grid UI (Text Search) -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="item in mockResults" 
            :key="item.id"
            class="liquid-glass p-6 rounded-2xl hover:-translate-y-2 transition-transform duration-300 cursor-pointer group"
          >
            <div class="flex justify-between items-start mb-4">
              <h3 class="text-xl font-bold text-neon-tertiary group-hover:text-white transition-colors">{{ item.title }}</h3>
              <span 
                class="px-2 py-1 text-xs rounded border"
                :class="item.status === 'Active' ? 'bg-[rgba(0,255,100,0.1)] border-[rgba(0,255,100,0.3)] text-green-400' : 'bg-[rgba(255,255,255,0.1)] border-[rgba(255,255,255,0.2)] text-white/60'"
              >
                {{ item.status }}
              </span>
            </div>
            <p class="text-white/50 text-sm font-mono mb-6">{{ item.description }}</p>
            <div class="h-1 w-full bg-white/5 rounded overflow-hidden">
              <div class="h-full bg-neon-tertiary/50 w-1/3 group-hover:w-full transition-all duration-700"></div>
            </div>
          </div>
        </div>

      </div>
    </transition>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
