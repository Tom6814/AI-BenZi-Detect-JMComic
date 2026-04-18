import re

file_path = 'frontend/src/components/ReportCard.vue'
content = open(file_path, 'r', encoding='utf-8').read()

# Replace the div starting with <div class="prose... up to v-html="parsedReasoning">
pattern = r'<div class="prose.*?v-html="parsedReasoning">'
new_div = '<div class="reasoning-content" v-html="parsedReasoning">'

content = re.sub(pattern, new_div, content, flags=re.DOTALL)

open(file_path, 'w', encoding='utf-8').write(content)
print("Replaced prose block with reasoning-content.")
