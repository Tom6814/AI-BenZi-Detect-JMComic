file_path = 'frontend/src/components/radar/PhaseInit.vue'
content = open(file_path, 'r', encoding='utf-8').read()

# Replace button classes to be more MD3 expressive
content = content.replace(
    'class="w-full py-4 bg-[var(--color-md-sys-primary)] text-[var(--color-md-sys-on-primary)] rounded-full text-lg font-bold tracking-widest uppercase hover:opacity-90 transition-opacity flex items-center justify-center gap-2"',
    'class="w-full py-4 bg-[var(--color-md-sys-primary)] text-[var(--color-md-sys-on-primary)] rounded-full text-lg font-bold tracking-widest uppercase hover:bg-[var(--color-md-sys-primary)] hover:shadow-[0_4px_12px_rgba(var(--color-md-sys-primary-rgb),0.3)] active:scale-[0.98] transition-all duration-300 flex items-center justify-center gap-2"'
)

# Add more subtle scaling and transition to inputs
content = content.replace(
    'class="w-full bg-[var(--color-md-sys-surface-variant)] text-[var(--color-md-sys-on-surface-variant)] px-6 py-4 rounded-2xl border-none focus:ring-2 focus:ring-[var(--color-md-sys-primary)] outline-none placeholder-[var(--color-md-sys-outline)]"',
    'class="w-full bg-[var(--color-md-sys-surface-variant)] text-[var(--color-md-sys-on-surface-variant)] px-6 py-4 rounded-2xl border-none focus:ring-2 focus:ring-[var(--color-md-sys-primary)] outline-none placeholder-[var(--color-md-sys-outline)] transition-all duration-300 hover:bg-[var(--color-md-sys-surface-variant-hover)]"'
)

open(file_path, 'w', encoding='utf-8').write(content)
print("Updated PhaseInit.")
