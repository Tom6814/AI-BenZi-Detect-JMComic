<template>
  <div class="space-y-6 animate-fade-in">
    <h2 class="text-3xl font-bold text-neon-tertiary drop-shadow-md">About This Project</h2>
    
    <div class="liquid-glass p-8 space-y-4">
      <p class="text-white/80 leading-relaxed text-lg">
        This template leverages the power of <span class="text-neon-primary font-semibold">Vue 3</span> and <span class="font-semibold text-[#646cff]">Vite</span> for blazing-fast development. 
      </p>
      
      <p class="text-white/80 leading-relaxed">
        Styling is handled by <span class="text-[#38bdf8] font-semibold">Tailwind CSS v4</span>, configured seamlessly with custom properties for a unique visual language.
      </p>

      <ul class="list-disc list-inside text-white/70 space-y-2 mt-4 ml-2">
        <li><strong>Pinia</strong> for intuitive state management</li>
        <li><strong>Vue Router</strong> for smooth client-side navigation</li>
        <li><strong>Material 3 Expressive</strong> color variables mapping</li>
        <li><strong>Aurora Neon & Liquid Glass</strong> aesthetic themes</li>
      </ul>
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
