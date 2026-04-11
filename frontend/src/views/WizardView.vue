<script setup>
import { ref } from 'vue'
import Step1Config from '../components/wizard/Step1Config.vue'
import Step2Rules from '../components/wizard/Step2Rules.vue'
import Step3Search from '../components/wizard/Step3Search.vue'
import Step4Report from '../components/wizard/Step4Report.vue'

const currentStep = ref(1)
const searchResult = ref(null)

const nextStep = () => {
  if (currentStep.value < 4) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const handleSearchSuccess = (data) => {
  searchResult.value = data
  currentStep.value = 4
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center p-4 md:p-8 relative overflow-hidden">
    <!-- Main Full-Screen Centered Glass Card -->
    <div class="w-full max-w-5xl h-[85vh] min-h-[600px] bg-white/10 backdrop-blur-2xl border border-white/20 shadow-[0_8px_32px_0_rgba(0,0,0,0.37)] rounded-3xl flex flex-col relative z-10 overflow-hidden">
      
      <!-- Wizard Header (Progress indicator) -->
      <div class="px-8 py-6 border-b border-white/10 flex items-center justify-between bg-black/5">
        <h2 class="text-2xl font-bold tracking-wider text-white">Aurora Nexus</h2>
        <div class="flex items-center gap-2">
          <div v-for="step in 4" :key="step" class="flex items-center">
            <div 
              :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-colors duration-500', 
                currentStep >= step ? 'bg-neon-tertiary text-black shadow-[0_0_15px_rgba(0,229,255,0.5)]' : 'bg-white/10 text-white/50 border border-white/20']"
            >
              {{ step }}
            </div>
            <div v-if="step < 4" :class="['w-10 h-[2px] mx-2 transition-colors duration-500', currentStep > step ? 'bg-neon-tertiary shadow-[0_0_8px_rgba(0,229,255,0.5)]' : 'bg-white/20']"></div>
          </div>
        </div>
      </div>

      <!-- Step Content Area -->
      <div class="flex-1 overflow-y-auto relative p-8">
        <transition name="step" mode="out-in">
          <Step1Config v-if="currentStep === 1" @next="nextStep" />
          <Step2Rules v-else-if="currentStep === 2" @next="nextStep" />
          <Step3Search v-else-if="currentStep === 3" @search-success="handleSearchSuccess" />
          <Step4Report v-else-if="currentStep === 4" :report-data="searchResult" />
        </transition>
      </div>

      <!-- Footer Buttons -->
      <div class="p-6 border-t border-white/10 flex justify-between items-center bg-black/10">
        <button 
          @click="prevStep" 
          :class="['px-6 py-2.5 rounded-lg border font-medium transition-all duration-300', 
            currentStep > 1 
              ? 'border-white/30 text-white/80 hover:bg-white/10 hover:text-white active:scale-95' 
              : 'border-transparent text-transparent pointer-events-none']"
        >
          上一步
        </button>

        <button 
          v-if="currentStep < 3" 
          @click="nextStep" 
          class="px-8 py-2.5 rounded-lg bg-[rgba(0,229,255,0.15)] border border-[rgba(0,229,255,0.3)] text-[#00e5ff] font-medium hover:bg-[rgba(0,229,255,0.25)] hover:shadow-[0_0_15px_rgba(0,229,255,0.4)] active:scale-95 transition-all duration-300"
        >
          下一步
        </button>
        
        <button 
          v-else-if="currentStep === 4" 
          @click="currentStep = 3" 
          class="px-8 py-2.5 rounded-lg bg-[rgba(0,255,100,0.15)] border border-[rgba(0,255,100,0.3)] text-green-400 font-medium hover:bg-[rgba(0,255,100,0.25)] hover:shadow-[0_0_15px_rgba(0,255,100,0.4)] active:scale-95 transition-all duration-300"
        >
          重新鉴定
        </button>
        <div v-else></div>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* Transition for steps */
.step-enter-active,
.step-leave-active {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.step-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.step-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.text-neon-tertiary {
  color: var(--md-sys-color-tertiary, #00e5ff);
}
.bg-neon-tertiary {
  background-color: var(--md-sys-color-tertiary, #00e5ff);
}
</style>
