import re

file_path = 'frontend/src/components/ReportCard.vue'
content = open(file_path, 'r', encoding='utf-8').read()

# Replace the prose classes with custom class
old_prose_block = """        <div class="prose prose-invert prose-purple max-w-none
          prose-h2:text-xl prose-h2:font-bold prose-h2:text-gray-200 prose-h2:border-b prose-h2:border-white/10 prose-h2:pb-2
          prose-p:text-gray-300 prose-p:leading-relaxed prose-p:text-base
          prose-strong:text-white prose-strong:font-bold
          prose-ul:list-disc prose-ul:text-gray-300 prose-li:my-1
          prose-blockquote:border-l-purple-500 prose-blockquote:bg-purple-500/5 prose-blockquote:py-1 prose-blockquote:px-4 prose-blockquote:rounded-r-lg prose-blockquote:not-italic
          first-line-highlight"
          v-html="parsedReasoning">
        </div>"""

new_prose_block = """        <div class="reasoning-content" v-html="parsedReasoning">
        </div>"""

content = content.replace(old_prose_block, new_prose_block)

# Replace the <style> block
old_style_block = """<style>
/* Prose overrides are handled by Tailwind Typography plugin via prose classes above */
.first-line-highlight > p:first-of-type {
  font-size: 1.25rem;
  font-weight: 900;
  color: #f3f4f6; /* text-gray-100 */
  line-height: 1.6;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-shadow: 0 2px 10px rgba(255,255,255,0.1);
  margin-bottom: 1.5rem;
  border-left: 4px solid var(--color-md-sys-primary, #a855f7);
  padding-left: 1rem;
}
</style>"""

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

content = content.replace(old_style_block, new_style_block)

open(file_path, 'w', encoding='utf-8').write(content)
print("Replaced Tailwind prose classes with raw CSS for Reasoning content.")
