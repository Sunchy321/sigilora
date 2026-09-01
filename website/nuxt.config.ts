export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@nuxtjs/i18n', '@nuxt/ui', '@nuxt/content'],
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
