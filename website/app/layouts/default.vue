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
          <a
            href="https://github.com/Sunchy321/sigilora"
            target="_blank"
            rel="noopener"
            class="flex items-center text-muted transition hover:text-primary"
            aria-label="GitHub"
          >
            <UIcon name="i-simple-icons-github" class="size-5" />
          </a>
        </nav>
      </div>
    </header>
    <main class="flex-1">
      <slot />
    </main>
  </div>
</template>
