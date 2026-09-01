<script setup lang="ts">
defineOptions({ name: 'SymbolText' })

const props = defineProps<{ text: string; family?: string; activeStyle?: string }>()

const glyphStyle = computed(() => {
  const style: Record<string, string> = {
    fontFamily: props.family ?? "'Sigilora Magic'",
    fontFeatureSettings: "'liga'",
    display: 'inline-block',
    lineHeight: '1',
    whiteSpace: 'nowrap',
  }
  if (props.activeStyle === 'shadow') style.fontFeatureSettings = "'liga', 'ss01'"
  else if (props.activeStyle === 'flat') style.fontFeatureSettings = "'liga', 'ss02'"
  return style
})

const parts = computed(() => {
  const tokens = props.text.split(/(\{[^}]+\}|\[[^\]]+\])/g)
  return tokens.filter((t) => t !== '')
})
</script>

<template>
  <span>
    <template v-for="(part, i) in parts" :key="i">
      <span v-if="/^(\{[^}]+\}|\[[^\]]+\])$/.test(part)" :style="glyphStyle">{{ part }}</span>
      <template v-else>{{ part }}</template>
    </template>
  </span>
</template>
