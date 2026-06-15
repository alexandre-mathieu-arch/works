<template>
  <ProjectView v-if="page" :project="page" />
</template>

<script setup lang="ts">
import ProjectView from '~/components/ProjectView.vue';
import { useHoverProject } from '~/composables/useHoverProject';

definePageMeta({
  layout: 'default',
  showFilters: true,
  readonlyFilters: true
})

const route = useRoute()
const { data: page } = await useAsyncData('page-' + route.path, () => {
  const cleanPath = route.path.replace(/^\/works/, '') || '/'
  return queryCollection('content').path(cleanPath).first()
})

if (!page.value) {
  throw createError({ statusCode: 404, statusMessage: 'Page not found', fatal: true })
}

useSeoMeta({
  title: () => page.value?.title ? `${page.value.title} - Alexandre Mathieu` : 'Alexandre Mathieu',
  description: () => page.value?.description || "Projet d'architecture et de design par Alexandre Mathieu.",
  ogTitle: () => page.value?.title ? `${page.value.title} - Alexandre Mathieu` : 'Alexandre Mathieu',
  ogDescription: () => page.value?.description || "Projet d'architecture et de design par Alexandre Mathieu.",
  twitterTitle: () => page.value?.title ? `${page.value.title} - Alexandre Mathieu` : 'Alexandre Mathieu',
  twitterDescription: () => page.value?.description || "Projet d'architecture et de design par Alexandre Mathieu."
})

const { setHoveredProject } = useHoverProject();
watchEffect(() => {
  if (page.value) {
    route.meta.dynamicTitle = page.value.title;
    setHoveredProject(page.value as any);
  }
});

onMounted(() => {
  if (page.value) {
    setHoveredProject(page.value as any);
  }
});
</script>
