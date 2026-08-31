<script setup lang="ts">
import uiEn from '@nuxt/ui/runtime/locale/en.js'
import uiZhCn from '@nuxt/ui/runtime/locale/zh_cn.js'

const { locale } = useI18n()
const uiLocale = computed(() => (locale.value === 'zhs' ? uiZhCn : uiEn))
</script>

<template>
  <UApp :locale="uiLocale">
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </UApp>
</template>
