<template>
  <div v-if="page" class="pt-8 pb-24 max-w-3xl mx-auto">
    <!-- Article Header -->
    <header class="mb-12 border-b border-[#121212]/10 dark:border-white/10 pb-8">
      <div class="flex gap-4 mb-6">
        <time v-if="page.date" class="u-legend opacity-60">
          {{ new Date(page.date).toLocaleDateString('fr-FR', { year: 'numeric', month: 'long', day: 'numeric' }) }}
        </time>
        <span v-if="page.tags" class="u-legend opacity-40 uppercase tracking-widest">
          {{ page.tags.join(' • ') }}
        </span>
      </div>
      
      <h1 class="text-[32px] md:text-[42px] font-bold leading-[1.1] dark:text-white" style="font-family: var(--font-primary);">
        {{ page.title }}
      </h1>
      
      <p v-if="page.description" class="mt-6 u-body text-[18px] md:text-[21px] font-light italic opacity-80 leading-relaxed">
        {{ page.description }}
      </p>
    </header>

    <!-- Article Content -->
    <div class="content-renderer">
      <ContentRenderer 
        :value="page" 
        class="prose prose-lg dark:prose-invert max-w-none 
               prose-p:leading-loose prose-p:opacity-90 
               prose-headings:font-bold prose-headings:tracking-tight 
               prose-a:underline prose-a:underline-offset-4 hover:prose-a:opacity-70"
      />
    </div>

    <!-- Back Navigation -->
    <div class="mt-20 pt-8 border-t border-[#121212]/10 dark:border-white/10">
      <NuxtLink to="/corpus" class="inline-flex items-center gap-4 u-h4 uppercase tracking-widest text-[#121212] dark:text-white group transition-all duration-700">
        <span class="transform transition-transform duration-700 group-hover:-translate-x-2">←</span>
        <span>Retour au Corpus</span>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default',
  hideLayoutTitle: true // Hide the main "Corpus" title to focus on the article title
})

const route = useRoute()
const { data: page } = await useAsyncData('page-' + route.path, () => {
  const cleanPath = route.path.replace(/^\/works/, '') || '/'
  return queryCollection('content').path(cleanPath).first()
})

if (!page.value) {
  throw createError({ statusCode: 404, statusMessage: 'Article not found', fatal: true })
}

useHead({
  title: computed(() => `${page.value?.title} — Corpus`)
})
useSeoMeta({
  title: () => page.value?.title ? `${page.value.title} - Corpus` : 'Corpus',
  description: () => page.value?.description || "Article du corpus d'Alexandre Mathieu.",
  ogTitle: () => page.value?.title ? `${page.value.title} - Corpus` : 'Corpus',
  ogDescription: () => page.value?.description || "Article du corpus d'Alexandre Mathieu."
})
</script>

<style scoped>
/* Scoped overrides to ensure no underlines on the main text, matching global styling */
.prose a {
  text-decoration: none !important;
  border-bottom: 1px solid currentColor;
}
</style>
