<script setup lang="ts">
defineOptions({ name: 'Playground' })

const game = ref<'magic' | 'lorcana' | 'riftbound'>('magic')
const input = ref('{W}{U}{R} Lightning Bolt deals {3} damage.')
const family = ref<'full' | 'lite'>('full')
const style = ref<'default' | 'shadow' | 'flat'>('default')
const fontSize = ref(24)

const defaults: Record<string, string> = {
  magic: '{W}{U}{R} Lightning Bolt deals {3} damage.',
  lorcana: 'Play this character for {3}{I}. It has {4}{S} and {2}{L}.',
  riftbound: 'When I attack, you may pay [R] to give me +2 [M] this turn.',
}

function onGameChange() {
  input.value = defaults[game.value]!
  style.value = 'default'
}

const gameLabel = computed(() => game.value.charAt(0).toUpperCase() + game.value.slice(1))
const fontFamily = computed(() => (family.value === 'full' ? `Sigilora ${gameLabel.value}` : `Sigilora ${gameLabel.value} Lite`))
const activeStyle = computed(() => (family.value === 'lite' ? 'default' : style.value))
const isLorcana = computed(() => game.value === 'lorcana')
const isRiftbound = computed(() => game.value === 'riftbound')
const gameStyles: Record<string, string[]> = {
  magic: ['default', 'shadow', 'flat'],
  lorcana: ['default'],
  riftbound: ['default', 'inverted'],
}
const hasInverted = computed(() => gameStyles[game.value]!.includes('inverted'))
</script>

<template>
  <div class="flex flex-col gap-4">
    <div class="flex flex-wrap items-center gap-4">
      <USelect v-model="game" :items="[{ label: $t('game-name.magic'), value: 'magic' }, { label: $t('game-name.lorcana'), value: 'lorcana' }, { label: $t('game-name.riftbound'), value: 'riftbound' }]" class="w-44" @update:model-value="onGameChange" />
    </div>
    <UTextarea v-model="input" :rows="4" :placeholder="$t(`playground.placeholder.${game}`)" />
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
          :disabled="family === 'lite' || isLorcana || isRiftbound"
          @click="style = 'default'"
        >
          {{ $t('playground.default') }}
        </UButton>
        <UButton :variant="style === 'shadow' ? 'solid' : 'ghost'" :disabled="family === 'lite' || isLorcana || isRiftbound" @click="style = 'shadow'">
          {{ $t('playground.shadow') }}
        </UButton>
        <UButton :variant="style === 'flat' ? 'solid' : 'ghost'" :disabled="family === 'lite' || isLorcana || isRiftbound" @click="style = 'flat'">
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
      <SymbolText :text="input" :family="fontFamily" :active-style="activeStyle" :has-inverted="hasInverted" />
    </div>
  </div>
</template>
