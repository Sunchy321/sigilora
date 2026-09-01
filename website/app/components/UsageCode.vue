<script setup lang="ts">
defineOptions({ name: 'UsageCode' })

const { t } = useI18n()
const props = defineProps<{ title: string; code: string }>()

const copied = ref(false)
let timer: ReturnType<typeof setTimeout> | undefined

async function copy() {
  await navigator.clipboard.writeText(props.code)
  copied.value = true
  clearTimeout(timer)
  timer = setTimeout(() => { copied.value = false }, 1200)
}
</script>

<template>
  <div class="overflow-hidden rounded-xl border border-default bg-elevated">
    <div class="flex items-center justify-between border-b border-default px-4 py-2">
      <span class="text-sm font-medium">{{ title }}</span>
      <UButton icon="i-lucide-copy" size="xs" variant="ghost" @click="copy">
        <span v-if="copied" class="text-success">{{ $t('playground.copied') }}</span>
      </UButton>
    </div>
    <pre class="overflow-x-auto p-4 text-sm"><code>{{ code }}</code></pre>
  </div>
</template>
