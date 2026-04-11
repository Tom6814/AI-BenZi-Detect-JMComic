<script setup>
import { ref, computed } from 'vue'

const emit = defineEmits(['search-success'])

const searchQuery = ref('')
const loading = ref(false)
const error = ref('')

const isNumber = computed(() => /^\d+$/.test(searchQuery.value))

const handleSearch = async () => {
  if (!searchQuery.value.trim()) return

  loading.value = true
  error.value = ''
  
  try {
    const res = await fetch('http://localhost:8000/api/identify', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        query: searchQuery.value,
      })
    })

    if (res.ok) {
      const data = await res.json()
      emit('search-success', data)
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

<template>
  <div class="max-w-4xl mx-auto space-y-8 animate-fade-in flex flex-col items-center justify-center min-h-[400px]">
    <header class="text-center space-y-4 mb-8">
      <h1 class="text-4xl md:text-5xl font-bold tracking-widest text-neon-tertiary uppercase">数据检索</h1>
      <p class="text-white/60 tracking-widest text-sm">输入 JM 号或关键词进行鉴定</p>
    </header>

    <!-- Search Input -->
    <div class="relative w-full max-w-2xl mx-auto group">
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
          class="w-full bg-transparent border-none px-4 py-3 text-white focus:outline-none focus:ring-0 placeholder-white/30 text-lg"
          placeholder="例如: 123456 或 某个本子名称..."
          :disabled="loading"
        />
        <button
          @click="handleSearch"
          :disabled="loading || !searchQuery.trim()"
          class="bg-[rgba(0,229,255,0.1)] border border-[rgba(0,229,255,0.3)] text-neon-tertiary px-8 py-3 rounded-full hover:bg-[rgba(0,229,255,0.2)] active:scale-95 transition-all duration-300 font-bold whitespace-nowrap disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_15px_rgba(0,229,255,0.2)] hover:shadow-[0_0_25px_rgba(0,229,255,0.4)]"
        >
          <span v-if="loading" class="flex items-center justify-center gap-2">
            <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            鉴定中...
          </span>
          <span v-else>开始鉴定</span>
        </button>
      </div>
    </div>

    <transition name="fade">
      <div v-if="error" class="mt-4 px-6 py-3 rounded-xl border bg-[rgba(255,84,73,0.1)] border-[rgba(255,84,73,0.3)] text-neon-primary shadow-[0_0_15px_rgba(255,84,73,0.2)] text-center">
        {{ error }}
      </div>
    </transition>

    <div v-if="isNumber && searchQuery && !loading" class="mt-8 text-white/50 text-sm font-mono text-center animate-pulse">
      检测到 JM 号输入，将直接请求直接鉴定接口。
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
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
