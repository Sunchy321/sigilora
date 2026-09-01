<script setup lang="ts">
import magicJson from '~/data/magic.json'
import symbolsJson from '~/data/symbols.json'

const { t, tm, rt } = useI18n()
const manifest = magicJson
const symbols = symbolsJson

const styleOptions = computed(() => manifest.fonts[0].styles.map((s: string) => ({
  label: t(`style-name.${s}`),
  value: s,
})))
const activeStyle = ref('default')
const examples = computed(() => {
  const list = tm('examples.list') as unknown as unknown[]
  return list.map((item) => rt(item as string))
})

const htmlCode = '<link rel="stylesheet" href="https://cdn.example.com/@sigilora/fonts/magic.css">\n<i class="sigilora-magic">{W}{U}{R} Lightning Bolt</i>'
const cssCode = ".sigilora-magic {\n  font-family: 'Sigilora Magic', serif;\n}"
</script>

<template>
  <div class="container mx-auto px-4 py-12">
    <div class="flex flex-wrap items-center gap-3">
      <h1 class="text-3xl font-bold">{{ $t('game-name.magic') }}</h1>
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
          <SymbolText :text="ex" :active-style="activeStyle" />
        </div>
      </div>
    </section>

    <SymbolTable
      :symbols="symbols"
      :categories="manifest.categories"
      :active-style="activeStyle"
      class="mt-10"
    />
  </div>
</template>
