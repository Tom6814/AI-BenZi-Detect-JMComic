<script setup>
import { ref, onMounted } from 'vue'
import PhaseInit from '../components/radar/PhaseInit.vue'
import PhaseCalibrate from '../components/radar/PhaseCalibrate.vue'
import PhaseTarget from '../components/radar/PhaseTarget.vue'
import PhaseReport from '../components/radar/PhaseReport.vue'
import { getApiUrl } from '../lib/utils.js'

const phase = ref('INIT') // INIT -> CALIBRATE -> TARGET -> REPORT
const searchResult = ref(null)

onMounted(async () => {
  // Check if configured
  try {
    const configRes = await fetch(getApiUrl('/api/config'))
    const config = await configRes.json()
    
    if (config && config.api_key) {
      // Check if rules exist
      const rulesRes = await fetch(getApiUrl('/api/rules'))
      const rules = await rulesRes.json()
      if (rules && (rules.avoid.length > 0 || rules.like.length > 0)) {
        phase.value = 'TARGET'
        return
      }
      phase.value = 'CALIBRATE'
    }
  } catch (e) {
    console.error("Auto-skip config check failed", e)
  }
})

const toCalibrate = () => phase.value = 'CALIBRATE'
const toTarget = () => phase.value = 'TARGET'
const toInit = () => phase.value = 'INIT'
const handleSearchSuccess = (data) => {
  searchResult.value = data
  phase.value = 'REPORT'
}
</script>

<template>
  <div class="relative w-screen h-screen overflow-hidden bg-[var(--color-md-sys-background)] text-[var(--color-md-sys-on-background)] flex items-center justify-center font-sans">

    <!-- Background Decorator -->
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--color-md-sys-primary-container)_0%,_transparent_50%),radial-gradient(ellipse_at_bottom_left,_var(--color-md-sys-tertiary-container)_0%,_transparent_50%)] opacity-50 z-0"></div>

    <div class="absolute inset-0 flex items-center justify-center p-4 md:p-8 z-10">

      <!-- Main Container (MD3 Surface) -->
      <div
        class="bg-[var(--color-md-sys-surface)] md-elevation-3 relative flex flex-col overflow-hidden transition-all duration-700 ease-[cubic-bezier(0.2,0,0,1)] border border-[var(--color-md-sys-outline-variant)]"
        :class="{
          'w-[500px] h-[650px] md-shape-extra-large': phase === 'INIT',
          'w-[900px] h-[700px] md-shape-extra-large': phase === 'CALIBRATE',
          'w-[600px] h-[500px] md-shape-extra-large': phase === 'TARGET',
          'w-[1000px] h-[85vh] md-shape-extra-large': phase === 'REPORT'
        }"
      >
        <transition name="md-fade" mode="out-in">
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
            @back="toInit"
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
/* MD3 Standard Transition for full-screen changes */
.md-fade-enter-active,
.md-fade-leave-active {
  transition: opacity 0.3s cubic-bezier(0.2, 0, 0, 1), transform 0.4s cubic-bezier(0.2, 0, 0, 1);
}

.md-fade-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.98);
}

.md-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.98);
}
</style>
