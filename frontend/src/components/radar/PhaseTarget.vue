<script setup>
import { ref } from 'vue'

const emit = defineEmits(['search-success', 'back'])
const query = ref('')
const loading = ref(false)
const searchResults = ref([])
const hasSearched = ref(false)

const initiateScan = async (targetId = null) => {
  const searchQuery = targetId || query.value.trim()
  if (!searchQuery) return
  
  loading.value = true
  
  // If it's pure number or an explicit ID was passed, identify directly
  if (targetId || /^\d+$/.test(searchQuery)) {
    try {
      const res = await fetch(`/api/identify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchQuery })
      })
      
      if (res.ok) {
        const data = await res.json()
        emit('search-success', data)
      } else {
        console.error('Identify failed')
      }
    } catch (err) {
      console.error(err)
    } finally {
      loading.value = false
    }
  } else {
    // Otherwise, search JM
    try {
      const res = await fetch(`/api/search?query=${encodeURIComponent(searchQuery)}`)
      if (res.ok) {
        const data = await res.json()
        if (data.type === 'list') {
          searchResults.value = data.items
          hasSearched.value = true
        } else if (data.type === 'exact') {
          // Fallback if somehow it returns exact
          initiateScan(data.id.toString())
        }
      }
    } catch (err) {
      console.error(err)
    } finally {
      loading.value = false
    }
  }
}
</script>

<template>
  <div class="flex flex-col items-center w-full h-full p-8 md:p-12 relative bg-[var(--color-md-sys-surface)] overflow-y-auto">

    <div class="absolute top-8 left-8 md:top-12 md:left-12 z-20">
      <button @click="emit('back')" class="p-2 rounded-full text-[var(--color-md-sys-on-surface-variant)] hover:bg-[var(--color-md-sys-surface-variant)] transition-colors md-ripple flex items-center justify-center">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
      </button>
    </div>

    <!-- Indeterminate Linear Progress Indicator for loading state -->
    <div v-if="loading" class="absolute top-0 left-0 w-full h-1 bg-[var(--color-md-sys-surface-variant)] overflow-hidden z-30">
      <div class="h-full bg-[var(--color-md-sys-primary)] w-1/3 animate-[md-linear-progress_2s_infinite_linear]"></div>
    </div>

    <div class="text-center mb-8 relative z-20 w-full max-w-lg mt-4">
      <div class="inline-flex items-center justify-center w-16 h-16 rounded-[16px] bg-[var(--color-md-sys-primary-container)] text-[var(--color-md-sys-on-primary-container)] mb-6 md-elevation-1">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
      </div>
      <h2 class="text-3xl font-normal text-[var(--color-md-sys-on-surface)] mb-4 tracking-tight" style="font-family: 'Google Sans', 'Roboto', sans-serif;">
        Analyze Content
      </h2>
      <p class="text-[var(--color-md-sys-on-surface-variant)] text-body-large">
        Enter a JM ID to scan directly, or a title to search the database.
      </p>
    </div>

    <!-- MD3 Search Bar -->
    <div class="w-full max-w-2xl relative z-20 shrink-0">
      <div class="relative bg-[var(--color-md-sys-surface-variant)] rounded-[28px] h-[56px] flex items-center px-4 transition-shadow focus-within:md-elevation-1 focus-within:bg-[var(--color-md-sys-surface)]">
        <svg class="w-6 h-6 text-[var(--color-md-sys-on-surface-variant)] ml-2 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
        <input
          v-model="query"
          @keyup.enter="initiateScan(null)"
          type="text"
          class="flex-1 bg-transparent border-none text-[var(--color-md-sys-on-surface)] text-lg focus:outline-none h-full placeholder-[var(--color-md-sys-on-surface-variant)]"
          placeholder="Search by ID or Title..."
          :disabled="loading"
        />

        <button
          v-if="query"
          @click="query = ''; hasSearched = false; searchResults = []"
          class="p-2 rounded-full text-[var(--color-md-sys-on-surface-variant)] hover:bg-[var(--color-md-sys-outline-variant)] transition-colors mr-1"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>

      <div class="mt-6 flex justify-center">
        <!-- MD3 Filled Button -->
        <button
          @click="initiateScan(null)"
          :disabled="loading || !query.trim()"
          class="md-ripple h-[40px] px-6 rounded-full font-medium transition-all flex items-center justify-center gap-2"
          :class="(loading || !query.trim()) ? 'bg-[var(--color-md-sys-surface-variant)] text-[var(--color-md-sys-on-surface-variant)] opacity-[0.38] cursor-not-allowed' : 'bg-[var(--color-md-sys-primary)] text-[var(--color-md-sys-on-primary)] hover:md-elevation-1 active:md-elevation-0'"
        >
          <span>{{ /^\d+$/.test(query.trim()) ? 'Evaluate ID' : 'Search Database' }}</span>
        </button>
      </div>
    </div>

    <!-- Search Results Grid -->
    <div v-if="hasSearched" class="w-full max-w-4xl mt-8 pb-8 z-20 flex-1 relative">
      <h3 class="text-lg font-medium text-[var(--color-md-sys-on-surface)] mb-4">Search Results</h3>
      <div v-if="searchResults.length === 0" class="text-center p-8 bg-[var(--color-md-sys-surface-variant)] rounded-2xl text-[var(--color-md-sys-on-surface-variant)]">
        No results found for "{{ query }}"
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div 
          v-for="item in searchResults" :key="item.id"
          @click="initiateScan(item.id.toString())"
          class="bg-[var(--color-md-sys-surface)] border border-[var(--color-md-sys-outline-variant)] rounded-2xl p-4 flex gap-4 cursor-pointer hover:bg-[var(--color-md-sys-surface-variant)] hover:md-elevation-1 transition-all md-ripple"
        >
          <div class="w-20 h-28 bg-[var(--color-md-sys-surface-variant)] rounded-lg overflow-hidden shrink-0">
            <img v-if="item.cover" :src="item.cover" class="w-full h-full object-cover" alt="cover" />
            <div v-else class="w-full h-full flex items-center justify-center text-[var(--color-md-sys-on-surface-variant)]">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
            </div>
          </div>
          <div class="flex flex-col justify-between py-1 overflow-hidden">
            <h4 class="font-medium text-[var(--color-md-sys-on-surface)] line-clamp-3 text-sm" :title="item.title">{{ item.title }}</h4>
            <div class="text-xs text-[var(--color-md-sys-primary)] font-medium mt-2">ID: {{ item.id }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.text-body-large {
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.5px;
}

@keyframes md-linear-progress {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(300%); }
}
</style>
