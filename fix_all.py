import re

# 1. PhaseReport.vue (z-index fix)
file_path = 'frontend/src/components/radar/PhaseReport.vue'
content = open(file_path, 'r', encoding='utf-8').read()
content = content.replace('class="w-full max-w-4xl flex justify-between items-center z-20 mb-8 mt-2"', 'class="w-full max-w-4xl flex justify-between items-center z-50 mb-8 mt-2 relative"')
open(file_path, 'w', encoding='utf-8').write(content)
print("Fixed z-index in PhaseReport.vue")

# 2. ReportCard.vue (reasoning-content fix and button css)
file_path = 'frontend/src/components/ReportCard.vue'
content = open(file_path, 'r', encoding='utf-8').read()

# Replace prose block
pattern = r'<div class="prose.*?v-html="parsedReasoning">\n\s*</div>'
new_div = '<div class="reasoning-content" v-html="parsedReasoning">\n        </div>'
content = re.sub(pattern, new_div, content, flags=re.DOTALL)

# Insert new styles
new_style_block = """<style>
.reasoning-content {
  color: #d1d5db; /* text-gray-300 */
  line-height: 1.75;
  font-size: 1rem;
}

.reasoning-content h2 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #e5e7eb; /* text-gray-200 */
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.5rem;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
}

.reasoning-content p {
  margin-bottom: 1rem;
}

.reasoning-content strong {
  color: #ffffff;
  font-weight: 700;
}

.reasoning-content ul {
  list-style-type: disc;
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}

.reasoning-content li {
  margin-bottom: 0.25rem;
}

.reasoning-content blockquote {
  border-left: 4px solid #a855f7; /* purple-500 */
  background-color: rgba(168, 85, 247, 0.05);
  padding: 0.25rem 1rem;
  border-radius: 0 0.5rem 0.5rem 0;
  margin-bottom: 1rem;
  font-style: normal;
}

/* First line highlight */
.reasoning-content > p:first-of-type {
  font-size: 1.25rem;
  font-weight: 900;
  color: #f3f4f6; /* text-gray-100 */
  line-height: 1.6;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-shadow: 0 2px 10px rgba(255, 255, 255, 0.1);
  margin-bottom: 1.5rem;
  border-left: 4px solid #a855f7;
  padding-left: 1rem;
}
</style>"""

content = content.replace("<style scoped>\n/* Prose overrides are handled by Tailwind Typography plugin via prose classes above */\n</style>", new_style_block)
content = content.replace("<style>\n/* Prose overrides are handled by Tailwind Typography plugin via prose classes above */\n</style>", new_style_block)

# Check if old style block exists
if "Prose overrides" not in content and "reasoning-content {" not in content:
    content += "\n" + new_style_block

open(file_path, 'w', encoding='utf-8').write(content)
print("Fixed styles in ReportCard.vue")

# 3. IdentifyResponse album_id
file_path = 'backend/app/routers/identify.py'
content = open(file_path, 'r', encoding='utf-8').read()

content = re.sub(
    r'class IdentifyResponse\(BaseModel\):\n.*?reasoning: str\n.*?title: Optional\[str\] = ""\n.*?cover_url: Optional\[str\] = ""\n.*?author: Optional\[str\] = ""',
    r'class IdentifyResponse(BaseModel):\n    score: int\n    avoid: List[TagResult]\n    like: List[TagResult]\n    reasoning: str\n    title: Optional[str] = ""\n    cover_url: Optional[str] = ""\n    author: Optional[str] = ""\n    album_id: Optional[str] = ""',
    content, flags=re.DOTALL
)

content = re.sub(
    r'"author": "Mock Author"\n    }',
    r'"author": "Mock Author",\n        "album_id": "12345"\n    }',
    content
)

content = re.sub(
    r'result\["author"\] = req\.author\n                return result',
    r'result["author"] = req.author\n                result["album_id"] = req.query\n                return result',
    content
)

open(file_path, 'w', encoding='utf-8').write(content)
print("Added album_id to identify.py")
