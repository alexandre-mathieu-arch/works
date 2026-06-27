<template>
  <div class="pt-0 pb-10">
    <section class="mb-8">
      <h1 class="u-h2 text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4]">Portfolio</h1>
    </section>

    <section class="border-y border-[#121212]/12 py-5 dark:border-white/12 doux:border-[#4A4443]/12 nuit:border-[#CDD6F4]/12">
      <div class="grid gap-4 md:grid-cols-3">
        <article
          v-for="document in documents"
          :key="document.label"
          class="border border-[#121212]/18 bg-[#121212]/[0.035] p-5 transition-colors duration-(--duration-hover) ease-(--ease-atelier) dark:border-white/18 dark:bg-white/[0.055] doux:border-[#4A4443]/18 doux:bg-white/20 nuit:border-[#CDD6F4]/18 nuit:bg-white/[0.055]"
        >
          <div class="mb-7 flex items-start justify-between gap-4">
            <div>
              <p class="u-legend uppercase opacity-55">{{ document.kicker }}</p>
              <h3 class="u-h3 mt-1 text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4]">{{ document.label }}</h3>
              <p class="u-body mt-2 text-[13px] leading-[1.5] text-[#121212]/65 dark:text-white/65 doux:text-[#4A4443]/70 nuit:text-[#CDD6F4]/70">{{ document.description }}</p>
            </div>
            <span class="u-legend shrink-0 border border-[#121212]/25 px-2 py-1 text-[#121212]/70 dark:border-white/25 dark:text-white/70 doux:border-[#4A4443]/25 doux:text-[#4A4443]/75 nuit:border-[#CDD6F4]/25 nuit:text-[#CDD6F4]/75">
              {{ document.lang }}
            </span>
          </div>

          <div class="grid grid-cols-1 gap-2 sm:grid-cols-2">
            <a
              :href="document.url"
              target="_blank"
              class="inline-flex min-h-11 items-center justify-center border border-[#121212] bg-[#121212] px-4 py-3 text-center text-[11px] font-semibold uppercase tracking-[0.18em] text-white no-underline transition-colors duration-(--duration-hover) ease-(--ease-atelier) hover:bg-transparent hover:text-[#121212] dark:border-white dark:bg-white dark:text-[#121212] dark:hover:bg-transparent dark:hover:text-white doux:border-[#4A4443] doux:bg-[#4A4443] doux:text-[#F5F1E8] doux:hover:bg-transparent doux:hover:text-[#4A4443] nuit:border-[#CDD6F4] nuit:bg-[#CDD6F4] nuit:text-[#1A2238] nuit:hover:bg-transparent nuit:hover:text-[#CDD6F4]"
            >
              Visualiser
            </a>
            <a
              :href="document.url"
              target="_blank"
              download
              class="inline-flex min-h-11 items-center justify-center border border-[#121212]/28 px-4 py-3 text-center text-[11px] font-semibold uppercase tracking-[0.18em] text-[#121212] no-underline transition-colors duration-(--duration-hover) ease-(--ease-atelier) hover:border-[#121212] hover:bg-[#121212]/7 dark:border-white/28 dark:text-white dark:hover:border-white dark:hover:bg-white/10 doux:border-[#4A4443]/28 doux:text-[#4A4443] doux:hover:border-[#4A4443] doux:hover:bg-[#4A4443]/8 nuit:border-[#CDD6F4]/28 nuit:text-[#CDD6F4] nuit:hover:border-[#CDD6F4] nuit:hover:bg-[#CDD6F4]/10"
            >
              Télécharger
            </a>
          </div>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const runtimeConfig = useRuntimeConfig()
const assetPath = (path: string) => `${runtimeConfig.app.baseURL}${path.replace(/^\//, '')}`
const portfolioLightUrl = assetPath('/Alexandre-MATHIEU_PORTFOLIO-2026-light.pdf')
const cvFrUrl = assetPath('/cv-alexandre-mathieu-fr.pdf')
const cvEnUrl = assetPath('/cv-alexandre-mathieu-en.pdf')
const documents = [
  {
    label: 'Portfolio light',
    kicker: 'Selected works',
    description: 'Version PDF légère, inférieure à 7 Mo.',
    lang: '≤ 7 Mo',
    url: portfolioLightUrl
  },
  {
    label: 'CV français',
    kicker: 'Version complète',
    description: 'Parcours, expériences, collaborations et références en français.',
    lang: 'FR',
    url: cvFrUrl
  },
  {
    label: 'English CV',
    kicker: 'Complete version',
    description: 'Experience, collaborations and references in English.',
    lang: 'EN',
    url: cvEnUrl
  }
]

definePageMeta({
  layout: 'default',
  displayTitle: 'Portfolio',
  hideLayoutTitle: true
})

useHead({
  title: 'Portfolio — Alexandre Mathieu'
})

useSeoMeta({
  description: "Portfolio PDF d'Alexandre Mathieu, architecte : projets d'architecture et design.",
  ogTitle: 'Portfolio - Alexandre Mathieu',
  ogDescription: "Consulter et télécharger le portfolio PDF d'Alexandre Mathieu."
})
</script>

<style scoped>
@reference "../assets/css/main.css";
</style>
