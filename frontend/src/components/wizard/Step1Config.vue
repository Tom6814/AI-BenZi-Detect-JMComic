<script setup>
import { ref } from 'vue'

const emit = defineEmits(['next'])

const apiUrl = ref('http://localhost:8000')
const model = ref('gpt-4o')
const apiKey = ref('')
const loading = ref(false)
const result = ref(null)

const testConnection = async () => {
  loading.value = true
  result.value = null
  try {
    const res = await fetch('http://localhost:8000/api/config/test', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        api_url: apiUrl.value,
        model: model.value,
        api_key: apiKey.value
      })
    })

    if (res.ok) {
      const data = await res.json()
      result.value = { success: true, message: data.message || '连接成功！' }
    } else {
      result.value = { success: false, message: `错误: ${res.statusText}` }
    }
  } catch (error) {
    result.value = { success: false, message: error.message || '网络错误' }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto space-y-8 animate-fade-in">
    <header class="text-center mb-8">
      <h1 class="text-3xl font-bold tracking-wide text-neon-tertiary mb-2">系统配置 (API)</h1>
      <p class="text-white/60">配置你的模型和API以用于后续生成。</p>
    </header>

    <div class="liquid-glass p-8 space-y-6 rounded-2xl">
      <div class="space-y-2">
        <label class="block text-sm font-medium text-neon-primary">API URL</label>
        <input
          v-model="apiUrl"
          type="text"
          class="w-full bg-[rgba(0,0,0,0.3)] border border-[rgba(255,255,255,0.1)] rounded-lg px-4 py-3 text-white focus:outline-none focus:border-neon-tertiary focus:ring-1 focus:ring-neon-tertiary transition-colors"
          placeholder="https://api.openai.com/v1"
        />
      </div>

      <div class="space-y-2">
        <label class="block text-sm font-medium text-neon-primary">模型</label>
        <input
          v-model="model"
          type="text"
          class="w-full bg-[rgba(0,0,0,0.3)] border border-[rgba(255,255,255,0.1)] rounded-lg px-4 py-3 text-white focus:outline-none focus:border-neon-tertiary focus:ring-1 focus:ring-neon-tertiary transition-colors"
          placeholder="gpt-4o"
        />
      </div>

      <div class="space-y-2">
        <label class="block text-sm font-medium text-neon-primary">API Key</label>
        <input
          v-model="apiKey"
          type="password"
          class="w-full bg-[rgba(0,0,0,0.3)] border border-[rgba(255,255,255,0.1)] rounded-lg px-4 py-3 text-white focus:outline-none focus:border-neon-tertiary focus:ring-1 focus:ring-neon-tertiary transition-colors"
          placeholder="sk-..."
        />
      </div>

      <div class="pt-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <button
          @click="testConnection"
          :disabled="loading"
          class="w-full sm:w-auto px-8 py-3 rounded-lg bg-[rgba(0,229,255,0.1)] border border-[rgba(0,229,255,0.3)] text-neon-tertiary hover:bg-[rgba(0,229,255,0.2)] active:scale-95 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed font-medium shadow-[0_0_15px_rgba(0,229,255,0.2)] hover:shadow-[0_0_25px_rgba(0,229,255,0.4)]"
        >
          <span v-if="loading" class="flex items-center justify-center gap-2">
            <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            测试中...
          </span>
          <span v-else>测试连接</span>
        </button>

        <transition name="fade">
          <div v-if="result"
               :class="['w-full sm:w-auto px-4 py-3 rounded-lg border text-sm text-center',
                       result.success ? 'bg-[rgba(0,255,100,0.1)] border-[rgba(0,255,100,0.3)] text-green-400' :
                                        'bg-[rgba(255,84,73,0.1)] border-[rgba(255,84,73,0.3)] text-neon-primary']">
            {{ result.message }}
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
