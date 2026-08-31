<script setup lang="ts">
const { locale } = useI18n()
const route = useRoute()
const slug = computed(() => (route.params.slug as string[] || []).join('/'))
const path = computed(() => `/${locale.value}/guide/${slug.value || 'install'}`)
</script>

<template>
  <div class="container mx-auto max-w-3xl px-4 py-12">
    <ContentDoc :path="path" />
  </div>
</template>
