<template>
  <div class="pt-0 pb-6">
    <section class="mb-12 max-w-3xl">
      <h1 class="u-h2 text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4]">À propos</h1>
      <p class="u-body mt-5 max-w-2xl text-[#121212]/70 dark:text-white/70 doux:text-[#4A4443]/75 nuit:text-[#CDD6F4]/75">
        Une pratique attentive aux lieux, aux usages et aux atmosphères, avec une exigence constructive simple et durable.
      </p>
    </section>

    <!-- Content: Integrated desktop grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8 items-start">
      <!-- Column 1: Equipe -->
      <div class="opacity-100 pt-0 order-1">
        <div v-if="equipe" class="prose dark:prose-invert max-w-none pb-4">
          <ContentRenderer :value="equipe" />
        </div>
      </div>

      <!-- Column 2: Pratique -->
      <div class="opacity-100 order-3 md:order-2">
        <div v-if="pratique" class="prose dark:prose-invert max-w-none pb-4">
          <ContentRenderer :value="pratique" />
        </div>
      </div>

      <!-- Column 3: Portrait -->
      <div class="opacity-100 order-2 md:order-3 md:sticky md:top-24">
        <div class="overflow-hidden w-full aspect-[4/5]">
          <NuxtImg 
            src="/profil.jpg" 
            alt="Alexandre Mathieu" 
            class="w-full h-full object-cover scale-125 origin-center"
          />
        </div>
      </div>
    </div>

    <!-- Bottom section: Parcours & Downloads, breaks free from columns -->
    <div class="mt-20 pt-8 border-t border-primary-900/10 flex flex-col gap-12">
      <!-- Parcours -->
      <div v-if="parcours">
        <div class="prose dark:prose-invert max-w-none">
          <ContentRenderer :value="parcours" />
        </div>
      </div>

      <!-- Downloads -->
      <div class="flex flex-col md:flex-row items-start gap-x-12 gap-y-4">
        <a 
          :href="cvFrUrl" 
          target="_blank" 
          download 
          class="inline-flex items-center gap-2 px-0 py-1 u-h4 hover:text-[#121212]/65 dark:hover:text-white/70 transition-all duration-(--duration-hover) ease-(--ease-atelier) no-underline group"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mb-[2px] opacity-30 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span class="whitespace-nowrap">Télécharger le CV (FR)</span>
        </a>
        <a 
          :href="cvEnUrl" 
          target="_blank" 
          download 
          class="inline-flex items-center gap-2 px-0 py-1 u-h4 hover:text-[#121212]/65 dark:hover:text-white/70 transition-all duration-(--duration-hover) ease-(--ease-atelier) no-underline group"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mb-[2px] opacity-30 group-hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span class="whitespace-nowrap">Download CV (EN)</span>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const runtimeConfig = useRuntimeConfig()
const assetPath = (path: string) => `${runtimeConfig.app.baseURL}${path.replace(/^\//, '')}`
const cvFrUrl = assetPath('/cv-alexandre-mathieu-fr.pdf')
const cvEnUrl = assetPath('/cv-alexandre-mathieu-en.pdf')

const { data: pratique } = await useAsyncData('about-pratique', () => {
  return queryCollection('content').path('/about/pratique').first()
})

const { data: equipe } = await useAsyncData('about-equipe', () => {
  return queryCollection('content').path('/about/equipe').first()
})

const { data: parcours } = await useAsyncData('about-parcours', () => {
  return queryCollection('content').path('/about/parcours').first()
})

definePageMeta({
  layout: 'default',
  displayTitle: "À propos",
  hideLayoutTitle: true
})

useHead({
  title: 'À propos — Alexandre Mathieu'
})
useSeoMeta({
  description: "Presentation de la pratique, du parcours et des references d'Alexandre Mathieu.",
  ogTitle: 'A propos - Alexandre Mathieu',
  ogDescription: "Presentation de la pratique, du parcours et des references d'Alexandre Mathieu."
})
</script>

<style scoped>
@reference "../assets/css/main.css";
</style>
