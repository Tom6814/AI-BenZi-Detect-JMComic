<script setup>
import { getApiUrl } from '../../lib/utils.js'
import { ref, onMounted } from 'vue'

const emit = defineEmits(['next', 'back'])
const avoidInput = ref('')
const likeInput = ref('')
const avoidList = ref([])
const likeList = ref([])
const additionalPrompt = ref('')
const loading = ref(false)

const loadRules = async () => {
  try {
    const res = await fetch(getApiUrl('/api/rules'))
    if (res.ok) {
      const data = await res.json()
      avoidList.value = data.avoid || []
      likeList.value = data.like || []
      additionalPrompt.value = data.additional_prompt || ''
    }
  } catch (err) {
    console.warn('Failed to load existing rules.')
  }
}

onMounted(() => {
  loadRules()
})

const addAvoid = () => {
  if (!avoidInput.value.trim()) return
  const items = avoidInput.value.split(',').map(s => s.trim()).filter(Boolean)
  avoidList.value.push(...items)
  avoidList.value = [...new Set(avoidList.value)]
  avoidInput.value = ''
}

const addLike = () => {
  if (!likeInput.value.trim()) return
  const items = likeInput.value.split(',').map(s => s.trim()).filter(Boolean)
  likeList.value.push(...items)
  likeList.value = [...new Set(likeList.value)]
  likeInput.value = ''
}

const removeAvoid = (item) => {
  avoidList.value = avoidList.value.filter(i => i !== item)
}

const removeLike = (item) => {
  likeList.value = likeList.value.filter(i => i !== item)
}

const lockCalibration = async () => {
  loading.value = true
  try {
    await fetch(getApiUrl('/api/rules'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        avoid: avoidList.value,
        like: likeList.value,
        additional_prompt: additionalPrompt.value
      })
    })
    emit('next')
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex flex-col w-full h-full p-8 md:p-12 relative bg-[var(--color-md-sys-surface)]">
    <!-- Top App Bar (simplified) -->
    <div class="flex items-center gap-4 mb-8 text-[var(--color-md-sys-on-surface)]">
      <button @click="emit('back')" class="p-2 rounded-full hover:bg-[var(--color-md-sys-surface-variant)] transition-colors md-ripple flex items-center justify-center">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
      </button>
      <h2 class="text-[22px] font-normal leading-[28px]">Preferences</h2>
    </div>

    <div class="text-center mb-8">
      <p class="text-[var(--color-md-sys-on-surface-variant)] text-body-large">
        Set up the content criteria for your analysis.
      </p>
    </div>

    <!-- Content Area (Cards) -->
    <div class="flex flex-col md:flex-row flex-1 gap-6 max-h-[55vh] min-h-[300px]">
      
      <!-- Avoid Card -->
      <div class="flex-1 flex flex-col bg-[var(--color-md-sys-error-container)] text-[var(--color-md-sys-on-error-container)] rounded-[24px] p-6 md-elevation-1 transition-shadow hover:md-elevation-2 relative overflow-hidden group">
        <h3 class="text-lg font-medium mb-4 flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
          Avoid (Red Flags)
        </h3>
        
        <!-- Outlined Text Field for Error state -->
        <div class="relative border-2 border-[var(--color-md-sys-error)] rounded-[4px] px-4 py-2 focus-within:border-[var(--color-md-sys-error)] transition-colors mb-4 bg-[var(--color-md-sys-surface)] text-[var(--color-md-sys-on-surface)]">
          <label class="absolute -top-3 left-3 px-1 text-xs bg-[var(--color-md-sys-surface)] text-[var(--color-md-sys-error)] font-medium">Add tag</label>
          <input 
            v-model="avoidInput" 
            @keyup.enter="addAvoid"
            type="text" 
            class="w-full bg-transparent border-none focus:outline-none text-sm"
            placeholder="e.g. NTR (Press Enter)"
          />
        </div>
        
        <div class="flex-1 overflow-y-auto flex flex-wrap content-start gap-2 pr-2">
          <transition-group name="chip">
            <!-- MD3 Assist Chip (Error variant) -->
            <span 
              v-for="item in avoidList" :key="item"
              class="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg border border-[var(--color-md-sys-error)] bg-[var(--color-md-sys-surface)] text-[var(--color-md-sys-on-surface)] text-sm font-medium hover:bg-[var(--color-md-sys-error-container)] transition-colors"
            >
              {{ item }}
              <button @click="removeAvoid(item)" class="text-[var(--color-md-sys-on-surface-variant)] hover:text-[var(--color-md-sys-error)]">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
              </button>
            </span>
          </transition-group>
        </div>
      </div>

      <!-- Like Card -->
      <div class="flex-1 flex flex-col bg-[var(--color-md-sys-safe-container)] text-[var(--color-md-sys-on-safe-container)] rounded-[24px] p-6 md-elevation-1 transition-shadow hover:md-elevation-2 relative overflow-hidden group">
        <h3 class="text-lg font-medium mb-4 flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
          Like (Favorites)
        </h3>
        
        <!-- Outlined Text Field for Safe state -->
        <div class="relative border border-[var(--color-md-sys-outline)] rounded-[4px] px-4 py-2 focus-within:border-2 focus-within:border-[var(--color-md-sys-safe)] transition-colors mb-4 bg-[var(--color-md-sys-surface)] text-[var(--color-md-sys-on-surface)]">
          <label class="absolute -top-3 left-3 px-1 text-xs bg-[var(--color-md-sys-surface)] text-[var(--color-md-sys-on-surface-variant)] focus-within:text-[var(--color-md-sys-safe)] font-medium transition-colors">Add tag</label>
          <input 
            v-model="likeInput" 
            @keyup.enter="addLike"
            type="text" 
            class="w-full bg-transparent border-none focus:outline-none text-sm"
            placeholder="e.g. Pure Love (Press Enter)"
          />
        </div>
        
        <div class="flex-1 overflow-y-auto flex flex-wrap content-start gap-2 pr-2">
          <transition-group name="chip">
            <!-- MD3 Assist Chip (Safe variant) -->
            <span 
              v-for="item in likeList" :key="item"
              class="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg border border-[var(--color-md-sys-outline)] bg-[var(--color-md-sys-surface)] text-[var(--color-md-sys-on-surface)] text-sm font-medium hover:bg-[var(--color-md-sys-safe-container)] transition-colors"
            >
              {{ item }}
              <button @click="removeLike(item)" class="text-[var(--color-md-sys-on-surface-variant)] hover:text-[var(--color-md-sys-safe)]">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
              </button>
            </span>
          </transition-group>
        </div>
      </div>

    </div>

    <div class="mt-6 w-full">
      <div class="bg-[var(--color-md-sys-surface-variant)] border border-[var(--color-md-sys-outline-variant)] rounded-[24px] p-5">
        <div class="flex items-center gap-2 mb-3 text-[var(--color-md-sys-on-surface)]">
          <svg class="w-5 h-5 text-[var(--color-md-sys-primary)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
          <h3 class="text-base font-medium">备注 / 补充信息</h3>
        </div>
        <p class="text-[var(--color-md-sys-on-surface-variant)] text-sm mb-3">
          这里的内容会作为你的额外偏好说明一起发给 AI（例如：重点排查某角色是否非处、是否有强制、是否有暗示路人）。
        </p>
        <textarea
          v-model="additionalPrompt"
          rows="3"
          placeholder="输入你的补充提示（可选）"
          class="w-full bg-[var(--color-md-sys-surface)] text-[var(--color-md-sys-on-surface)] px-4 py-3 rounded-xl border border-[var(--color-md-sys-outline-variant)] focus:ring-2 focus:ring-[var(--color-md-sys-primary)] outline-none placeholder-[var(--color-md-sys-on-surface-variant)] resize-none transition-all duration-300"
        ></textarea>
      </div>
    </div>

    <!-- FAB / Floating Action Area -->
    <div class="mt-8 flex justify-end">
      <button 
        @click="lockCalibration" 
        :disabled="loading"
        class="md-ripple px-6 py-4 rounded-[16px] font-medium transition-all flex items-center justify-center gap-3 bg-[var(--color-md-sys-primary-container)] text-[var(--color-md-sys-on-primary-container)] hover:md-elevation-3 active:md-elevation-1"
        :class="loading ? 'opacity-50 cursor-not-allowed' : 'md-elevation-2'"
      >
        <svg v-if="loading" class="animate-spin h-5 w-5 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
        <span>{{ loading ? 'Saving...' : 'Save & Continue' }}</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.chip-enter-active,
.chip-leave-active {
  transition: all 0.3s cubic-bezier(0.2, 0, 0, 1);
}
.chip-enter-from,
.chip-leave-to {
  opacity: 0;
  transform: scale(0.8);
}
.text-body-large {
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.5px;
}
</style>
