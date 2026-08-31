<script setup lang="ts">
const { locale } = useI18n()
const route = useRoute()
const slug = computed(() => (route.params.slug as string[] || []).join('/'))
const path = computed(() => `/${locale.value}/guide/${slug.value || 'install'}`)

const { data: doc } = await useAsyncData(
  'doc',
  () => queryContent(path.value).findOne(),
  { watch: [path] },
)
</script>

<template>
  <div class="container mx-auto max-w-3xl px-4 py-12">
    <article v-if="doc" class="prose prose-slate max-w-none dark:prose-invert">
      <ContentRenderer :value="doc" />
    </article>
    <p v-else class="text-muted">{{ $t('docs.not-found') }}</p>
  </div>
</template>
