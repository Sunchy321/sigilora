<script setup lang="ts">
defineOptions({ name: 'SymbolTable' })

const { t } = useI18n()
const props = defineProps<{
  symbols: Array<{ name: string; category: string; ligature: string[]; overflow?: boolean }>
  categories: string[]
  activeStyle?: string
  family?: string
  hasInverted?: boolean
}>()

const grouped = computed(() => {
  return props.categories.map((cat) => ({
    category: cat,
    items: props.symbols.filter((s) => s.category === cat),
  })).filter((g) => g.items.length)
})
</script>

<template>
  <div class="flex flex-col gap-8">
    <p class="text-muted">{{ $t('symbols.click-to-copy') }}</p>
    <section v-for="group in grouped" :key="group.category">
      <h2 class="mb-3 text-lg font-semibold">{{ t(`category-name.${group.category}`) }}</h2>
      <div class="grid grid-cols-3 gap-3 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8">
        <SymbolCell v-for="s in group.items" :key="s.name" :symbol="s" :active-style="activeStyle" :family="family" :has-inverted="hasInverted" />
      </div>
    </section>
  </div>
</template>
