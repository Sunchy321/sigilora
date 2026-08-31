<script setup lang="ts">
const { locale, switchTo } = useLanguage()
const value = computed({
  get: () => locale.value,
  set: (v: string) => switchTo(v),
})
</script>

<template>
  <USelect
    v-model="value"
    :items="[{ label: 'English', value: 'en' }, { label: '简体中文', value: 'zhs' }]"
    class="w-36"
  />
</template>
