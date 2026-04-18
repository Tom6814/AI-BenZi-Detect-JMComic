import re

file_path = 'frontend/src/components/ReportCard.vue'
content = open(file_path, 'r', encoding='utf-8').read()

old_btn_style = """const buttonStyle = computed(() => {
  const s = props.data.score
  if (s === undefined) return 'bg-purple-600 hover:bg-purple-500 shadow-[0_0_20px_rgba(147,51,234,0.4)]'
  if (s >= 80) return 'bg-emerald-600 hover:bg-emerald-500 shadow-[0_0_20px_rgba(16,185,129,0.4)] border-emerald-400'
  if (s >= 31) return 'bg-amber-600 hover:bg-amber-500 shadow-[0_0_20px_rgba(245,158,11,0.4)] border-amber-400'
  return 'bg-red-600 hover:bg-red-500 shadow-[0_0_20px_rgba(239,68,68,0.4)] border-red-400'
})

const buttonText = computed(() => {"""

new_btn_style = """const buttonStyle = computed(() => {
  const s = props.data.score
  if (s === undefined) return 'bg-purple-600 hover:bg-purple-500 shadow-[0_0_20px_rgba(147,51,234,0.4)] border-purple-400'
  if (s >= 80) return 'bg-emerald-600 hover:bg-emerald-500 shadow-[0_0_20px_rgba(16,185,129,0.4)] border-emerald-400'
  if (s >= 31) return 'bg-amber-600 hover:bg-amber-500 shadow-[0_0_20px_rgba(245,158,11,0.4)] border-amber-400'
  return 'bg-red-600 hover:bg-red-500 shadow-[0_0_20px_rgba(239,68,68,0.4)] border-red-400'
})

const buttonText = computed(() => {"""

content = content.replace(old_btn_style, new_btn_style)

open(file_path, 'w', encoding='utf-8').write(content)
print("Button CSS Fixed")
