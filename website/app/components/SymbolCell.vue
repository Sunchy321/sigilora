<script setup lang="ts">
defineOptions({ name: 'SymbolCell' })

const props = defineProps<{
  symbol: { name: string; ligature: string[]; 'display-name': string }
}>()

const copied = ref(false)
let timer: ReturnType<typeof setTimeout> | undefined

async function copy() {
  await navigator.clipboard.writeText(props.symbol.ligature[0])
  copied.value = true
  clearTimeout(timer)
  timer = setTimeout(() => { copied.value = false }, 1200)
}
</script>

<template>
  <button
    class="flex flex-col items-center gap-1.5 rounded-xl border border-default bg-elevated p-4 transition hover:border-primary"
    @click="copy"
  >
    <span class="text-3xl leading-none" style="font-family: 'Sigilora Magic'">
      {{ symbol.ligature[0] }}
    </span>
    <span class="font-mono text-xs text-muted">{{ symbol.ligature[0] }}</span>
    <span class="text-sm">{{ symbol['display-name'] }}</span>
    <span v-if="copied" class="text-xs text-success">{{ $t('playground.copied') }}</span>
  </button>
</template>
