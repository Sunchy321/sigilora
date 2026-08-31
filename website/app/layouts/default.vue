<template>
  <div class="flex min-h-dvh flex-col">
    <header class="border-b border-default">
      <div class="container mx-auto flex items-center justify-between px-4 py-3">
        <NuxtLink to="/" class="text-lg font-bold">Sigilora</NuxtLink>
        <nav class="flex items-center gap-4">
          <NuxtLink to="/games" class="hover:text-primary">{{ $t('nav.games') }}</NuxtLink>
          <NuxtLink to="/playground" class="hover:text-primary">{{ $t('nav.playground') }}</NuxtLink>
          <NuxtLink to="/docs/guide/install" class="hover:text-primary">{{ $t('nav.docs') }}</NuxtLink>
          <LanguageSwitcher />
        </nav>
      </div>
    </header>
    <main class="flex-1">
      <slot />
    </main>
  </div>
</template>
