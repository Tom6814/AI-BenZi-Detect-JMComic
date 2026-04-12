<template>
  <div class="identify-view w-full max-w-4xl mx-auto space-y-8 animate-fade-in">
    <div class="flex items-center justify-between">
      <h1 class="text-3xl font-bold tracking-wider text-neon-tertiary">成分鉴定报告</h1>
    </div>
    
    <div class="liquid-glass rounded-xl p-6">
      <p class="text-white/80 mb-6 leading-relaxed">
        点击下方按钮，基于Mock数据向后端请求鉴定报告：
      </p>
      
      <div class="flex gap-4">
        <button 
          @click="loadData"
          :disabled="loading"
          class="px-6 py-2.5 rounded-lg font-medium transition-all duration-300 bg-[rgba(0,229,255,0.15)] text-[#00e5ff] hover:bg-[rgba(0,229,255,0.25)] border border-[rgba(0,229,255,0.3)] hover:shadow-[0_0_15px_rgba(0,229,255,0.4)] disabled:opacity-50"
        >
          {{ loading ? '鉴定中...' : '开始鉴定' }}
        </button>
      </div>
      
      <div v-if="error" class="mt-4 text-red-400">
        {{ error }}
      </div>
    </div>

    <!-- Render ReportCard if data is available -->
    <ReportCard v-if="reportData" :data="reportData" />
  </div>
</template>

<script setup>
import { getApiUrl } from '../lib/utils.js'
import { ref } from 'vue'
import ReportCard from '../components/ReportCard.vue'

const reportData = ref(null)
const loading = ref(false)
const error = ref('')

const loadData = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch(getApiUrl('/api/identify'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({}) // Using default mock data in backend
    })
    
    if (res.ok) {
      reportData.value = await res.json()
    } else {
      error.value = `请求失败: ${res.statusText}`
    }
  } catch (err) {
    error.value = `网络错误: ${err.message}`
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
