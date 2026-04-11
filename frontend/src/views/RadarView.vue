<script setup>
import { ref } from 'vue'
import PhaseInit from '../components/radar/PhaseInit.vue'
import PhaseCalibrate from '../components/radar/PhaseCalibrate.vue'
import PhaseTarget from '../components/radar/PhaseTarget.vue'
import PhaseReport from '../components/radar/PhaseReport.vue'

const phase = ref('INIT') // INIT -> CALIBRATE -> TARGET -> REPORT
const searchResult = ref(null)

const toCalibrate = () => phase.value = 'CALIBRATE'
const toTarget = () => phase.value = 'TARGET'
const toInit = () => phase.value = 'INIT'
const handleSearchSuccess = (data) => {
  searchResult.value = data
  phase.value = 'REPORT'
}
</script>

<template>
  <div class="relative w-screen h-screen overflow-hidden font-sans">
    <div class="aurora-bg"></div>

    <div class="absolute inset-0 flex items-center justify-center p-4 md:p-8">
      
      <!-- Main Morphing Glass Panel -->
      <div 
        class="glass-panel relative flex flex-col overflow-hidden transition-all duration-1000 ease-[cubic-bezier(0.25,1,0.5,1)]"
        :class="{
          'w-[500px] h-[600px] rounded-[40px]': phase === 'INIT',
          'w-[900px] h-[700px] rounded-[50px]': phase === 'CALIBRATE',
          'w-[600px] h-[600px] rounded-[40px]': phase === 'TARGET',
          'w-[1000px] h-[85vh] rounded-[40px]': phase === 'REPORT'
        }"
      >
        <!-- Top Left Decorator -->
        <div class="absolute top-8 left-8 w-2 h-2 rounded-full bg-white/30 animate-pulse z-0 pointer-events-none"></div>
        <!-- Top Right Decorator -->
        <div class="absolute top-8 right-8 text-[10px] tracking-[0.3em] text-white/20 uppercase z-0 pointer-events-none">
          SYS.{{ phase }}
        </div>

        <transition name="phase-fade" mode="out-in">
          <PhaseInit 
            v-if="phase === 'INIT'" 
            @next="toCalibrate" 
          />
          <PhaseCalibrate 
            v-else-if="phase === 'CALIBRATE'" 
            @next="toTarget" 
            @back="toInit"
          />
          <PhaseTarget 
            v-else-if="phase === 'TARGET'" 
            @search-success="handleSearchSuccess" 
            @back="toCalibrate"
          />
          <PhaseReport 
            v-else-if="phase === 'REPORT'" 
            :report-data="searchResult" 
            @reset="toTarget"
          />
        </transition>

      </div>
    </div>
  </div>
</template>

<style scoped>
.phase-fade-enter-active,
.phase-fade-leave-active {
  transition: opacity 0.5s ease, transform 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.phase-fade-enter-from {
  opacity: 0;
  transform: scale(0.95);
}

.phase-fade-leave-to {
  opacity: 0;
  transform: scale(1.05);
}
</style>
