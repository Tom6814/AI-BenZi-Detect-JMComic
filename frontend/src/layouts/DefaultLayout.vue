<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="min-h-screen p-4 md:p-8 flex items-center justify-center">
    <!-- Main Glass Container -->
    <div class="liquid-glass w-full max-w-5xl mx-auto flex flex-col md:flex-row overflow-hidden shadow-2xl min-h-[80vh]">
      
      <!-- Sidebar / Navigation -->
      <nav class="md:w-64 p-6 border-b md:border-b-0 md:border-r border-[rgba(255,255,255,0.1)] flex flex-col gap-8 bg-[rgba(0,0,0,0.2)]">
        <div class="text-2xl font-bold tracking-wider text-neon-tertiary">
          Aurora<span class="text-neon-primary">Vue</span>
        </div>
        
        <div class="flex md:flex-col gap-4">
          <RouterLink
            to="/"
            class="px-4 py-2 rounded-lg transition-all duration-300 hover:bg-[rgba(255,255,255,0.1)] active:scale-95 text-white/80 hover:text-white"
            active-class="bg-[rgba(255,255,255,0.15)] text-neon-primary font-medium"
          >
            Home
          </RouterLink>
          <RouterLink
            to="/search"
            class="px-4 py-2 rounded-lg transition-all duration-300 hover:bg-[rgba(255,255,255,0.1)] active:scale-95 text-white/80 hover:text-white"
            active-class="bg-[rgba(255,255,255,0.15)] text-neon-primary font-medium"
          >
            Search
          </RouterLink>
          <RouterLink
            to="/rules"
            class="px-4 py-2 rounded-lg transition-all duration-300 hover:bg-[rgba(255,255,255,0.1)] active:scale-95 text-white/80 hover:text-white"
            active-class="bg-[rgba(255,255,255,0.15)] text-neon-primary font-medium"
          >
            Rules
          </RouterLink>
          <RouterLink
            to="/config"
            class="px-4 py-2 rounded-lg transition-all duration-300 hover:bg-[rgba(255,255,255,0.1)] active:scale-95 text-white/80 hover:text-white"
            active-class="bg-[rgba(255,255,255,0.15)] text-neon-primary font-medium"
          >
            Config
          </RouterLink>
          <RouterLink
            to="/about"
            class="px-4 py-2 rounded-lg transition-all duration-300 hover:bg-[rgba(255,255,255,0.1)] active:scale-95 text-white/80 hover:text-white"
            active-class="bg-[rgba(255,255,255,0.15)] text-neon-primary font-medium"
          >
            About
          </RouterLink>
        </div>
      </nav>

      <!-- Main Content Area -->
      <main class="flex-1 p-6 md:p-10 relative overflow-y-auto">
        <RouterView v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </RouterView>
      </main>

    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
