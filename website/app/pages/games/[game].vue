<script setup lang="ts">
import magicJson from '~/data/magic.json'
import symbolsJson from '~/data/symbols.json'

const manifest = magicJson
const symbols = symbolsJson
</script>

<template>
  <div class="container mx-auto px-4 py-12">
    <div class="flex flex-wrap items-center gap-3">
      <h1 class="text-3xl font-bold">{{ $t('game-name.magic') }}</h1>
      <UBadge>{{ manifest['font-version'] }}</UBadge>
      <UBadge variant="soft">{{ manifest['colr-version'] }}</UBadge>
    </div>
    <div class="mt-3 flex flex-wrap gap-2">
      <UBadge v-for="f in manifest.fonts" :key="f.family" color="neutral">{{ f.family }}</UBadge>
    </div>
    <SymbolTable
      :symbols="symbols"
      :categories="manifest.categories"
      class="mt-10"
    />
  </div>
</template>
