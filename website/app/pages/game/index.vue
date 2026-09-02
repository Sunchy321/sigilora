<script setup lang="ts">
import magicJson from '~/data/magic.json'
import lorcanaJson from '~/data/lorcana.json'
import riftboundJson from '~/data/riftbound.json'
import pokemonJson from '~/data/pokemon.json'

const { t } = useI18n()
const manifests = [magicJson, lorcanaJson, riftboundJson, pokemonJson]

const columns = computed(() => [
  { accessorKey: 'family', header: t('games.family') },
  { accessorKey: 'file', header: 'File' },
  { accessorKey: 'styles', header: t('games.style') },
])

function rows(manifest: { fonts: Array<{ family: string; file: string; styles: string[] }> }) {
  return manifest.fonts.map((f) => ({
    family: f.family,
    file: f.file,
    styles: f.styles.join(', '),
  }))
}
</script>

<template>
  <div class="container mx-auto px-4 py-12">
    <h1 class="text-3xl font-bold">{{ $t('games.title') }}</h1>
    <p class="mt-2 text-muted">{{ $t('games.subtitle') }}</p>

    <UCard v-for="manifest in manifests" :key="manifest.game" class="mt-8">
      <div class="flex items-center justify-between">
        <NuxtLink :to="`/game/${manifest.game}`" class="text-xl font-semibold hover:text-primary">
          {{ $t(`game-name.${manifest.game}`) }}
        </NuxtLink>
        <UBadge>{{ manifest['colr-version'] }}</UBadge>
      </div>
      <dl class="mt-4 grid grid-cols-2 gap-4 text-sm">
        <div>
          <dt class="text-muted">{{ $t('games.version') }}</dt>
          <dd>{{ manifest['font-version'] }}</dd>
        </div>
        <div>
          <dt class="text-muted">{{ $t('games.symbols') }}</dt>
          <dd>{{ manifest.symbols }}</dd>
        </div>
      </dl>
      <UTable :data="rows(manifest)" :columns="columns" class="mt-6" />
    </UCard>
  </div>
</template>
