<script setup lang="ts">
const { data: manifest } = await useFetch('/fonts/magic/magic.json')
</script>

<template>
  <div class="container mx-auto px-4 py-16">
    <section class="mx-auto max-w-2xl text-center">
      <h1 class="text-4xl font-bold">{{ $t('hero.title') }}</h1>
      <p class="mt-4 text-lg text-muted">{{ $t('hero.subtitle') }}</p>
      <div class="mt-8 flex justify-center gap-3">
        <UButton to="/docs/guide/install" size="lg">{{ $t('hero.cta') }}</UButton>
        <UButton to="/playground" size="lg" variant="soft">{{ $t('nav.playground') }}</UButton>
      </div>
    </section>

    <section v-if="manifest" class="mx-auto mt-16 max-w-2xl">
      <h2 class="mb-4 text-xl font-semibold">{{ $t('nav.games') }}</h2>
      <NuxtLink
        :to="`/games/${manifest.game}`"
        class="flex items-center justify-between rounded-xl border border-default bg-elevated p-4 transition hover:border-primary"
      >
        <span class="text-lg font-medium">{{ manifest.name }}</span>
        <UBadge>{{ manifest['font-version'] }}</UBadge>
      </NuxtLink>
    </section>
  </div>
</template>
