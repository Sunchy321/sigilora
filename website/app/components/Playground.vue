<script setup lang="ts">
defineOptions({ name: 'Playground' })

const input = ref('{W}{U}{R} Lightning Bolt deals {3} damage.')
const family = ref<'full' | 'lite'>('full')
const style = ref<'default' | 'shadow' | 'flat'>('default')
const fontSize = ref(24)

const fontFamily = computed(() => (family.value === 'full' ? "'Sigilora Magic'" : "'Sigilora Magic Lite'"))
const activeStyle = computed(() => (family.value === 'lite' ? 'default' : style.value))
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
      <UButtonGroup>
        <UButton
          :variant="style === 'default' && family === 'full' ? 'solid' : 'ghost'"
          :disabled="family === 'lite'"
          @click="style = 'default'"
        >
          {{ $t('playground.default') }}
        </UButton>
        <UButton :variant="style === 'shadow' ? 'solid' : 'ghost'" :disabled="family === 'lite'" @click="style = 'shadow'">
          {{ $t('playground.shadow') }}
        </UButton>
        <UButton :variant="style === 'flat' ? 'solid' : 'ghost'" :disabled="family === 'lite'" @click="style = 'flat'">
          {{ $t('playground.flat') }}
        </UButton>
      </UButtonGroup>
      <div class="flex items-center gap-2">
        <UIcon name="i-lucide-type" class="size-4 text-muted" />
        <USlider v-model="fontSize" :min="12" :max="72" class="w-32" />
        <span class="text-sm text-muted">{{ fontSize }}px</span>
      </div>
    </div>
    <div
      class="rounded-xl border border-default bg-elevated p-6 leading-relaxed"
      :style="{ fontSize: `${fontSize}px` }"
    >
      <SymbolText :text="input" :family="fontFamily" :active-style="activeStyle" />
    </div>
  </div>
</template>
