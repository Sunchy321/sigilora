// Language preference persisted to a cookie, mirrored into the i18n locale.
export function useLanguage() {
  const { locale, setLocale, availableLocales } = useI18n()
  const cookie = useCookie<string | null>('sigilora_lang', {
    default: () => null,
    maxAge: 60 * 60 * 24 * 365,
  })

  watch(cookie, (val) => {
    if (val && val !== locale.value) setLocale(val)
  }, { immediate: true })

  function switchTo(code: string) {
    cookie.value = code
    if (code !== locale.value) setLocale(code)
  }

  return { locale, switchTo, availableLocales }
}
