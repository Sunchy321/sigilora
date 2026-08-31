<script setup lang="ts">
const route = useRoute()
const game = computed(() => route.params.game as string)

const { data: manifest } = await useFetch(() => `/fonts/${game.value}/magic.json`)
const { data: symbols } = await useFetch(() => `/fonts/${game.value}/symbols.json`)
</script>

<template>
  <div class="container mx-auto px-4 py-12">
    <template v-if="manifest">
      <div class="flex flex-wrap items-center gap-3">
        <h1 class="text-3xl font-bold">{{ manifest.name }}</h1>
        <UBadge>{{ manifest['font-version'] }}</UBadge>
        <UBadge variant="soft">{{ manifest['colr-version'] }}</UBadge>
      </div>
      <div class="mt-3 flex flex-wrap gap-2">
        <UBadge v-for="f in manifest.fonts" :key="f.family" color="neutral">{{ f.family }}</UBadge>
      </div>
      <SymbolTable
        v-if="symbols"
        :symbols="symbols"
        :categories="manifest.categories"
        class="mt-10"
      />
    </template>
  </div>
</template>
