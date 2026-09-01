<script setup lang="ts">
import magicJson from '~/data/magic.json'

const { t } = useI18n()
const manifest = magicJson

const columns = computed(() => [
  { id: 'family', label: t('games.family') },
  { id: 'file', label: 'File' },
  { id: 'styles', label: t('games.style') },
])

const rows = computed(() => {
  return manifest.fonts.map((f: { family: string; file: string; styles: string[] }) => ({
    family: f.family,
    file: f.file,
    styles: f.styles.join(', '),
  }))
})
</script>

<template>
  <div class="container mx-auto px-4 py-12">
    <h1 class="text-3xl font-bold">{{ $t('games.title') }}</h1>
    <p class="mt-2 text-muted">{{ $t('games.subtitle') }}</p>

    <UCard class="mt-8">
      <div class="flex items-center justify-between">
        <NuxtLink :to="`/game/${manifest.game}`" class="text-xl font-semibold hover:text-primary">
          {{ $t('game-name.magic') }}
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
      <UTable :data="rows" :columns="columns" class="mt-6" />
    </UCard>
  </div>
</template>
