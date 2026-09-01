<script setup lang="ts">
const colorMode = useColorMode()
const isDark = computed(() => colorMode.value === 'dark')
function toggleDark() {
  colorMode.preference = isDark.value ? 'light' : 'dark'
}
</script>

<template>
  <div class="flex min-h-dvh flex-col">
    <header class="border-b border-default">
      <div class="container mx-auto flex items-center justify-between px-4 py-3">
        <NuxtLink to="/" class="text-lg font-bold">Sigilora</NuxtLink>
        <nav class="flex items-center gap-4">
          <NuxtLink to="/game" class="hover:text-primary">{{ $t('nav.games') }}</NuxtLink>
          <NuxtLink to="/playground" class="hover:text-primary">{{ $t('nav.playground') }}</NuxtLink>
          <NuxtLink to="/docs/guide/install" class="hover:text-primary">{{ $t('nav.docs') }}</NuxtLink>
          <NuxtLink to="/docs/guide/changelog" class="hover:text-primary">{{ $t('nav.changelog') }}</NuxtLink>
          <UButton :icon="isDark ? 'i-lucide-moon' : 'i-lucide-sun'" variant="ghost" square @click="toggleDark" />
          <LanguageSwitcher />
        </nav>
      </div>
    </header>
    <main class="flex-1">
      <slot />
    </main>
  </div>
</template>
