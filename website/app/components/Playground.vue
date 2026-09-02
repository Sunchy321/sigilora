<script setup lang="ts">
defineOptions({ name: 'Playground' })

// Embedded in a per-game page: the game and the active style (variant) come
// from the page (the style is switched by the page's own selector), so the
// playground only offers font size and the full/lite family choice.
const props = defineProps<{
  game: string
  activeStyle?: string
  invertable?: boolean
  seed?: string
}>()

const input = ref(props.seed ?? '')
const family = ref<'full' | 'lite'>('full')
const fontSize = ref(24)

const gameLabel = computed(() => props.game.charAt(0).toUpperCase() + props.game.slice(1))
const fontFamily = computed(() => (family.value === 'full' ? `Sigilora ${gameLabel.value}` : `Sigilora ${gameLabel.value} Lite`))
// Lite ships the default style only; a page-level style set applies to full.
const resolvedStyle = computed(() => (family.value === 'lite' ? 'default' : (props.activeStyle ?? 'default')))
</script>

<template>
  <div class="flex flex-col gap-4">
    <UTextarea v-model="input" :rows="4" :placeholder="$t(`playground.placeholder.${game}`)" />
    <div class="flex flex-wrap items-center justify-between gap-4">
      <UButtonGroup>
        <UButton :variant="family === 'full' ? 'solid' : 'ghost'" @click="family = 'full'">
          {{ $t('playground.full') }}
        </UButton>
        <UButton :variant="family === 'lite' ? 'solid' : 'ghost'" @click="family = 'lite'">
          {{ $t('playground.lite') }}
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
      <SymbolText :text="input" :family="fontFamily" :active-style="resolvedStyle" :has-inverted="invertable" />
    </div>
  </div>
</template>
