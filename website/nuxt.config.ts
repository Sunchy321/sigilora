export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@nuxtjs/i18n', '@nuxt/ui', '@nuxt/content'],
  content: {
    experimental: {
      sqliteConnector: 'native',
    },
  },
  // Production is deployed on Cloudflare Workers (cloudflare_module). For local
  // `nuxt dev`, Nuxt Content's client-side SQL dump is only served under its node
  // preset (the cloudflare preset reads it from build storage / ASSETS, which are
  // absent in dev) — without it, client-side queryCollection returns null and the
  // docs show "not found" on internal navigation. Hence the dev script sets
  // NITRO_PRESET=node. Production build is unaffected (env var unset).
  nitro: {
    preset: 'cloudflare_module',
    cloudflare: {
      deployConfig: true,
      nodeCompat: true,
    },
  },
  css: ['~/assets/css/main.css'],
  app: {
    head: {
      htmlAttrs: { lang: 'en' },
      link: [
        { rel: 'stylesheet', href: '/fonts/magic/magic.css' },
        { rel: 'stylesheet', href: '/fonts/lorcana/lorcana.css' },
        { rel: 'stylesheet', href: '/fonts/riftbound/riftbound.css' },
        { rel: 'stylesheet', href: '/fonts/pokemon/pokemon.css' },
      ],
    },
  },
  i18n: {
    defaultLocale: 'en',
    locales: [
      { code: 'en', language: 'en-US', name: 'English', file: 'en/index.ts' },
      { code: 'zhs', language: 'zh-CN', name: 'Chinese (Simplified)', file: 'zhs/index.ts' },
    ],
    strategy: 'no_prefix',
    detectBrowserLanguage: { useCookie: true, redirectOn: 'root' },
  },
  compatibilityDate: '2025-07-15',
})
