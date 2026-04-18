import re

file_path = 'frontend/src/components/ReportCard.vue'
content = open(file_path, 'r', encoding='utf-8').read()

# Add button properties
script_block_end = "</script>"
button_logic = """const watchUrl = computed(() => {
  if (props.data.album_id) {
    return `https://web.jmcomic.uk/detail/${props.data.album_id}`
  }
  return '#'
})

const buttonStyle = computed(() => {
  const s = props.data.score
  if (s === undefined) return 'bg-purple-600 hover:bg-purple-500 shadow-[0_0_20px_rgba(147,51,234,0.4)]'
  if (s >= 80) return 'bg-emerald-600 hover:bg-emerald-500 shadow-[0_0_20px_rgba(16,185,129,0.4)] border-emerald-400'
  if (s >= 31) return 'bg-amber-600 hover:bg-amber-500 shadow-[0_0_20px_rgba(245,158,11,0.4)] border-amber-400'
  return 'bg-red-600 hover:bg-red-500 shadow-[0_0_20px_rgba(239,68,68,0.4)] border-red-400'
})

const buttonText = computed(() => {
  const s = props.data.score
  if (s === undefined) return '前往观看'
  if (s >= 80) return '火速食用'
  if (s >= 31) return '前往观看'
  return '我已知晓，无视风险继续观看'
})
</script>"""

content = content.replace(script_block_end, button_logic)

# Add button HTML at the bottom of the card
html_end = """      </div>

    </div>
  </div>
</template>"""

button_html = """      </div>
      
      <!-- Go to Watch Button -->
      <div class="mt-4 flex justify-center w-full relative z-20">
        <a :href="watchUrl" target="_blank" rel="noopener noreferrer" 
           class="group relative inline-flex items-center justify-center px-10 py-4 font-bold text-white transition-all duration-300 rounded-2xl hover:scale-[1.02] active:scale-[0.98] border border-transparent overflow-hidden"
           :class="buttonStyle">
          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
          <span class="relative flex items-center gap-3 text-lg tracking-wide">
            <svg class="w-6 h-6 group-hover:-translate-y-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
            {{ buttonText }}
          </span>
        </a>
      </div>

    </div>
  </div>
</template>"""

content = content.replace(html_end, button_html)

open(file_path, 'w', encoding='utf-8').write(content)
print("Updated ReportCard.vue with Go to Watch button.")

