import re

file_path = 'frontend/src/components/radar/PhaseReport.vue'
content = open(file_path, 'r', encoding='utf-8').read()

# Fix the z-index issue
# Change Controls Bar z-index to z-50
content = content.replace('class="w-full max-w-4xl flex justify-between items-center z-20 mb-8 mt-2"', 'class="w-full max-w-4xl flex justify-between items-center z-50 mb-8 mt-2 relative"')

# Change the click outside handler overlay z-index to z-40, which is below z-50
# It's already z-40.

open(file_path, 'w', encoding='utf-8').write(content)
print("Fixed export menu z-index.")
