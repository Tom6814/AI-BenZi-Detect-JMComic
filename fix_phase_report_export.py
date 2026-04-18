import re

file_path = 'frontend/src/components/radar/PhaseReport.vue'
content = open(file_path, 'r', encoding='utf-8').read()

# Replace downloadBlob arrow function with standard function to hoist it
old_downloadBlob = """const downloadBlob = (blob, filename) => {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}"""

new_downloadBlob = """function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}"""

if old_downloadBlob in content:
    content = content.replace(old_downloadBlob, new_downloadBlob)
    open(file_path, 'w', encoding='utf-8').write(content)
    print("Fixed downloadBlob in PhaseReport.vue")
else:
    print("Could not find downloadBlob")

