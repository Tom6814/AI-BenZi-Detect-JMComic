import re

file_path = 'frontend/src/components/ReportCard.vue'
content = open(file_path, 'r', encoding='utf-8').read()

# Make the first line of the reasoning stand out
# we can inject a CSS rule into the prose styles
old_prose_styles = """        <div class="prose prose-invert prose-purple max-w-none
          prose-h2:text-xl prose-h2:font-bold prose-h2:text-gray-200 prose-h2:border-b prose-h2:border-white/10 prose-h2:pb-2
          prose-p:text-gray-300 prose-p:leading-relaxed prose-p:text-base
          prose-strong:text-white prose-strong:font-bold
          prose-ul:list-disc prose-ul:text-gray-300 prose-li:my-1
          prose-blockquote:border-l-purple-500 prose-blockquote:bg-purple-500/5 prose-blockquote:py-1 prose-blockquote:px-4 prose-blockquote:rounded-r-lg prose-blockquote:not-italic"
          v-html="parsedReasoning">
        </div>"""

new_prose_styles = """        <div class="prose prose-invert prose-purple max-w-none
          prose-h2:text-xl prose-h2:font-bold prose-h2:text-gray-200 prose-h2:border-b prose-h2:border-white/10 prose-h2:pb-2
          prose-p:text-gray-300 prose-p:leading-relaxed prose-p:text-base
          prose-strong:text-white prose-strong:font-bold
          prose-ul:list-disc prose-ul:text-gray-300 prose-li:my-1
          prose-blockquote:border-l-purple-500 prose-blockquote:bg-purple-500/5 prose-blockquote:py-1 prose-blockquote:px-4 prose-blockquote:rounded-r-lg prose-blockquote:not-italic
          first-line-highlight"
          v-html="parsedReasoning">
        </div>"""

content = content.replace(old_prose_styles, new_prose_styles)

# Add the CSS block at the bottom
css_styles = """<style>
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

content = content.replace("<style>\n/* Prose overrides are handled by Tailwind Typography plugin via prose classes above */\n</style>", css_styles)

# For "修复如图的字体颜色问题" - likely the tags text color which might be too dark or unreadable. Let's make sure the text contrast is good.
# Current tag style:
# bg-red-500/20 border-red-500/40 text-red-300  <-- This is good
# bg-black/40 border-white/5 text-gray-500  <-- This might be the issue. Let's change text-gray-500 to text-gray-400 or gray-300.
content = content.replace("text-gray-500", "text-gray-300")

open(file_path, 'w', encoding='utf-8').write(content)
print("Updated ReportCard.vue styles and first line.")

