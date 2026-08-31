<script setup lang="ts">
defineOptions({ name: 'Playground' })

const input = ref('{W}{U}{R} Lightning Bolt deals {3} damage.')
const family = ref<'full' | 'lite'>('full')
const shadow = ref(true)
const flat = ref(false)

const fontFamily = computed(() => (family.value === 'full' ? "'Sigilora Magic'" : "'Sigilora Magic Lite'"))
const featureStyle = computed(() => {
  const features: string[] = []
  if (family.value === 'full') {
    if (shadow.value) features.push("'ss01'")
    if (flat.value) features.push("'ss02'")
  }
  return features.length ? { fontFeatureSettings: features.join(', ') } : {}
})
</script>

<template>
  <div class="flex flex-col gap-4">
    <UTextarea v-model="input" :rows="4" :placeholder="$t('playground.placeholder')" />
    <div class="flex flex-wrap items-center gap-4">
      <UButtonGroup>
        <UButton :variant="family === 'full' ? 'solid' : 'ghost'" @click="family = 'full'">
          {{ $t('playground.full') }}
        </UButton>
        <UButton :variant="family === 'lite' ? 'solid' : 'ghost'" @click="family = 'lite'">
          {{ $t('playground.lite') }}
        </UButton>
      </UButtonGroup>
      <UCheckbox v-model="shadow" :disabled="family === 'lite'" :label="$t('playground.shadow')" />
      <UCheckbox v-model="flat" :disabled="family === 'lite'" :label="$t('playground.flat')" />
    </div>
    <div
      class="rounded-xl border border-default bg-elevated p-6 text-3xl leading-relaxed"
      :style="{ fontFamily, ...featureStyle }"
    >
      {{ input }}
    </div>
  </div>
</template>
