<script setup lang="ts">
const { locale, t } = useI18n()
const route = useRoute()
const slug = computed(() => (route.params.slug as string[] || []).join('/'))
const path = computed(() => `/${locale.value}/${slug.value || 'guide/install'}`)

// Reactive key per path so client-side navigation between doc pages re-fetches;
// a static key + watch hangs when the same [...slug] component is reused.
const { data: doc, pending } = useAsyncData(
  () => `doc-${path.value}`,
  () => queryCollection('content').path(path.value).first(),
)

const navSections = computed(() => [
  {
    label: t('docs.nav.guide'),
    items: [
      { label: t('docs.nav.install'), to: '/docs/guide/install' },
      { label: t('docs.nav.installNpm'), to: '/docs/guide/install-npm' },
      { label: t('docs.nav.installDesktop'), to: '/docs/guide/install-desktop' },
      { label: t('docs.nav.knownLimitations'), to: '/docs/guide/known-limitations' },
    ],
  },
  {
    label: t('docs.nav.changelog'),
    items: [
      { label: t('game-name.magic'), to: '/docs/guide/changelog-magic' },
      { label: t('game-name.lorcana'), to: '/docs/guide/changelog-lorcana' },
      { label: t('game-name.riftbound'), to: '/docs/guide/changelog-riftbound' },
    ],
  },
])

const activePath = computed(() => route.path)
</script>

<template>
  <div class="container mx-auto flex gap-8 px-4 py-12">
    <aside class="hidden w-52 shrink-0 md:block">
      <nav class="sticky top-6 flex flex-col gap-6">
        <div v-for="section in navSections" :key="section.label">
          <p class="mb-2 text-xs font-semibold uppercase tracking-wide text-muted">{{ section.label }}</p>
          <NuxtLink
            v-for="item in section.items"
            :key="item.to"
            :to="item.to"
            class="block rounded-md px-2 py-1.5 text-sm transition hover:bg-elevated hover:text-primary"
            :class="activePath === item.to ? 'bg-elevated font-medium text-primary' : 'text-muted'"
          >
            {{ item.label }}
          </NuxtLink>
        </div>
      </nav>
    </aside>
    <article v-if="doc" class="prose prose-slate max-w-3xl flex-1 dark:prose-invert">
      <ContentRenderer :value="doc" />
    </article>
    <p v-else-if="!pending" class="text-muted">{{ $t('docs.not-found') }}</p>
  </div>
</template>
