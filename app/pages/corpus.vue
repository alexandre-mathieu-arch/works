<template>
  <div class="pt-8 pb-24">
    <div v-if="articles?.length" class="max-w-4xl mx-auto flex flex-col space-y-16">
      <article 
        v-for="article in articles" 
        :key="article.path" 
        class="group flex flex-col md:flex-row gap-4 md:gap-12 items-baseline border-t border-[#121212]/10 dark:border-white/10 pt-8"
      >
        <!-- Date / Metadata Column -->
        <div class="w-full md:w-48 shrink-0">
          <time v-if="article.date" class="u-legend opacity-60">
            {{ new Date(article.date).toLocaleDateString('fr-FR', { year: 'numeric', month: 'long' }) }}
          </time>
          <div v-if="article.tags" class="mt-2 flex gap-2">
            <span v-for="tag in article.tags" :key="tag" class="u-legend uppercase tracking-widest opacity-40">
              {{ tag }}
            </span>
          </div>
        </div>

        <!-- Content Column -->
        <div class="flex-grow">
          <NuxtLink :to="article.path" class="block">
            <h2 class="u-h2 mb-4 group-hover:opacity-70 transition-opacity duration-700">
              {{ article.title }}
            </h2>
            <p class="u-body opacity-80 leading-relaxed max-w-2xl">
              {{ article.description }}
            </p>
            <div class="mt-6 inline-flex items-center gap-2 u-h4 uppercase tracking-widest text-[#121212] dark:text-white group-hover:gap-4 transition-all duration-700">
              <span>Lire l'article</span>
              <span class="opacity-0 group-hover:opacity-100 transition-opacity duration-700">→</span>
            </div>
          </NuxtLink>
        </div>
      </article>
    </div>
    
    <div v-else class="text-center py-20 max-w-2xl mx-auto">
      <p class="u-body opacity-60 italic">Le corpus est en cours de constitution. Cet espace accueillera prochainement des essais sur la théorie architecturale, le design et les nouvelles technologies.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const { data: allArticles } = await useAsyncData('corpus-articles', () => {
  return queryCollection('content')
    .where('path', 'LIKE', '/corpus/%')
    .where('draft', '<>', true)
    .all()
})

const articles = computed(() => {
  if (!allArticles.value) return []
  return [...allArticles.value].sort((a, b) => {
    const dateA = new Date(a.date || 0).getTime()
    const dateB = new Date(b.date || 0).getTime()
    return dateB - dateA // Latest first
  })
})

definePageMeta({
  layout: 'default',
  displayTitle: 'Corpus'
})

useHead({
  title: 'Corpus — Alexandre Mathieu'
})
useSeoMeta({
  description: "Essais et notes sur l'architecture, le design, la conception parametrique et les pratiques constructives.",
  ogTitle: 'Corpus - Alexandre Mathieu',
  ogDescription: "Essais et notes sur l'architecture, le design, la conception parametrique et les pratiques constructives."
})
</script>
