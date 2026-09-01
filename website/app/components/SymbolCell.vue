<script setup lang="ts">
defineOptions({ name: 'SymbolCell' })

const { t, te } = useI18n()
const props = defineProps<{
  symbol: { name: string; ligature: string[]; category: string; overflow?: boolean }
  activeStyle?: string
}>()

const glyphStyle = computed(() => {
  const style: Record<string, string> = {
    fontFamily: "'Sigilora Magic'",
    fontFeatureSettings: "'liga'",
  }
  if (props.activeStyle === 'shadow') style.fontFeatureSettings = "'liga', 'ss01'"
  else if (props.activeStyle === 'flat') style.fontFeatureSettings = "'liga', 'ss02'"
  return style
})

const displayName = computed(() => {
  const key = `symbol-name.${props.symbol.name}`
  return te(key) ? t(key) : null
})

const allLigatures = computed(() => props.symbol.ligature.join(', '))

const copied = ref(false)
let timer: ReturnType<typeof setTimeout> | undefined

async function copy() {
  const text = props.symbol.ligature[0]
  if (!text) return
  await navigator.clipboard.writeText(text)
  copied.value = true
  clearTimeout(timer)
  timer = setTimeout(() => { copied.value = false }, 1200)
}
</script>

<template>
  <button
    class="relative flex flex-col items-center gap-1.5 rounded-xl border border-default bg-elevated p-4 transition hover:border-primary"
    @click="copy"
  >
    <UBadge v-if="copied" color="success" class="absolute right-1 top-1" size="xs">
      <UIcon name="i-lucide-check" class="size-3" />
    </UBadge>
    <span class="leading-none" :class="symbol.overflow ? 'text-lg' : 'text-3xl'" :style="glyphStyle">
      {{ symbol.ligature[0] }}
    </span>
    <span class="font-mono text-xs text-muted">{{ allLigatures }}</span>
    <span v-if="displayName" class="text-sm">{{ displayName }}</span>
  </button>
</template>
