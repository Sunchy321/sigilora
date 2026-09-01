<script setup lang="ts">
import magicJson from '~/data/magic.json'
import lorcanaJson from '~/data/lorcana.json'
import magicSymbols from '~/data/magic-symbols.json'
import lorcanaSymbols from '~/data/lorcana-symbols.json'

interface GameManifest {
  game: string
  name: string
  'font-version': string
  'colr-version': string
  fonts: Array<{ family: string; file: string; styles: string[] }>
  symbols: number
  categories: string[]
}
interface GameSymbol {
  name: string
  ligature: string[]
  category: string
  styles?: string[]
  overflow?: boolean
}

const route = useRoute()
const { t, tm, rt } = useI18n()

const manifests = { magic: magicJson, lorcana: lorcanaJson } as Record<string, GameManifest>
const symbolSets = { magic: magicSymbols, lorcana: lorcanaSymbols } as Record<string, GameSymbol[]>

const game = computed(() => (route.params.game as string) || 'magic')
const manifest = computed(() => manifests[game.value]!)
const symbols = computed(() => symbolSets[game.value]!)

const family = computed(() => manifest.value.fonts[0]!.family)
const code = computed(() => manifest.value.game)

const styleOptions = computed(() => manifest.value.fonts[0]!.styles.map((s: string) => ({
  label: t(`style-name.${s}`),
  value: s,
})))
const activeStyle = ref('default')
const examples = computed(() => {
  const list = tm(`examples.${game.value}.list`) as unknown as unknown[]
  return list.map((item) => rt(item as string))
})

const htmlSamples: Record<string, { sym: string; plain: string }> = {
  magic: { sym: '{W}{U}{R}', plain: 'Lightning Bolt' },
  lorcana: { sym: '{S}{W}', plain: 'A character' },
}
const htmlCode = computed(() => {
  const s = htmlSamples[game.value] ?? { sym: '', plain: '' }
  return `<link rel="stylesheet" href="https://cdn.example.com/@sigilora/fonts/${code.value}.css">\n<i class="sigilora-${code.value}">${s.sym}</i> ${s.plain}`
})
const cssCode = computed(() => `.sigilora-${code.value} {\n  font-family: '${family.value}', serif;\n}`)
</script>

<template>
  <div class="container mx-auto px-4 py-12">
    <div class="flex flex-wrap items-center gap-3">
      <h1 class="text-3xl font-bold">{{ $t(`game-name.${game}`) }}</h1>
      <UBadge>{{ manifest['font-version'] }}</UBadge>
      <UBadge variant="soft">{{ manifest['colr-version'] }}</UBadge>
    </div>
    <div class="mt-3 flex flex-wrap items-center justify-between gap-3">
      <div class="flex flex-wrap gap-2">
        <UBadge v-for="f in manifest.fonts" :key="f.family" color="neutral">{{ f.family }}</UBadge>
      </div>
      <USelect v-model="activeStyle" :items="styleOptions" class="w-32" />
    </div>

    <section class="mt-10 flex flex-col gap-4">
      <h2 class="text-xl font-semibold">{{ $t('usage.title') }}</h2>
      <div class="grid gap-4 lg:grid-cols-2">
        <UsageCode :title="$t('usage.html')" :code="htmlCode" />
        <UsageCode :title="$t('usage.css')" :code="cssCode" />
      </div>
    </section>

    <section class="mt-10 flex flex-col gap-4">
      <h2 class="text-xl font-semibold">{{ $t('examples.title') }}</h2>
      <div class="flex flex-col gap-3">
        <div
          v-for="(ex, i) in examples"
          :key="i"
          class="rounded-xl border border-default bg-elevated p-4 text-xl leading-relaxed"
        >
          <SymbolText :text="ex" :family="family" :active-style="activeStyle" />
        </div>
      </div>
    </section>

    <SymbolTable
      :symbols="symbols"
      :categories="manifest.categories"
      :active-style="activeStyle"
      :family="family"
      class="mt-10"
    />
  </div>
</template>
