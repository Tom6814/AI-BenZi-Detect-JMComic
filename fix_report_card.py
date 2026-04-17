import re

file_path = 'frontend/src/components/ReportCard.vue'
content = open(file_path, 'r', encoding='utf-8').read()

# For Avoid: false -> minus
old_avoid_svg = """          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>"""
new_avoid_svg = """          <svg v-else class="w-4 h-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>"""

if old_avoid_svg in content:
    content = content.replace(old_avoid_svg, new_avoid_svg)

# For Like: false -> minus
old_like_svg = """          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>"""
new_like_svg = """          <svg v-else class="w-4 h-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"></path></svg>"""

if old_like_svg in content:
    content = content.replace(old_like_svg, new_like_svg)

open(file_path, 'w', encoding='utf-8').write(content)
print("Updated ReportCard.vue icons.")
