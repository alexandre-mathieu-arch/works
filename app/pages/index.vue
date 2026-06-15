<template>
  <div>
    <!-- Hero Section -->
    <div class="-mt-[var(--header-height)]">
      <HeroSection 
        :scroll-progress="scrollProgress" 
        @scroll-to-projects="scrollToProjects"
      />
    </div>

    <!-- Project Grid (from architecture.vue) -->
    <div id="projects-grid" class="pt-0 pb-0 min-h-screen scroll-mt-40">
      <div 
        v-if="filteredProjects?.length" 
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-4 gap-4 md:gap-8 items-center mt-3"
        style="view-transition-name: projects-grid;"
      >
        <template v-for="(project, index) in filteredProjects" :key="project.path">
          <template v-if="index % 6 === 5">
            <button 
              @click="scrollToContact"
              class="hidden xl:block aspect-square border border-[#121212]/30 relative group transition-colors duration-700 hover:border-[#121212] text-left"
            >
              <div class="absolute top-0 left-0 w-full px-2 h-[30px] flex items-center opacity-0 group-hover:opacity-100 transition-opacity duration-700">
                <span class="u-h3 dark:text-white doux:text-[#4A4443]">Démarrer un projet ?</span>
              </div>
            </button>
            <ProjectCard :project="project" />
            <button 
              @click="scrollToContact"
              class="hidden xl:block aspect-square border border-[#121212]/30 relative group transition-colors duration-700 hover:border-[#121212] text-left"
            >
              <div class="absolute top-0 left-0 w-full px-2 h-[30px] flex items-center opacity-0 group-hover:opacity-100 transition-opacity duration-700">
                <span class="u-h3 dark:text-white doux:text-[#4A4443]">Démarrer un projet ?</span>
              </div>
            </button>
          </template>
          <ProjectCard 
            v-else 
            :project="project" 
          />
        </template>
      </div>
      <div v-else class="text-center py-10">
        <p class="text-gray-500">Aucun projet ne correspond à votre sélection.</p>
      </div>

      <button
        type="button"
        @click="scrollToContact"
        class="xl:hidden mt-8 flex min-h-11 w-full items-center justify-between border border-[#121212]/20 px-4 py-3 text-left transition-colors duration-500 hover:border-[#121212] dark:border-white/20 doux:border-[#4A4443]/20 nuit:border-[#CDD6F4]/20"
      >
        <span class="u-h3 dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4]">Demarrer un projet ?</span>
        <span class="u-h3 dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4]" aria-hidden="true">-&gt;</span>
      </button>

      <!-- Collaborations & Parcours Section -->
      <CollaborationsList />

      <!-- Contact Section -->
      <div id="contact" class="mt-32 pb-24 border-t border-[#121212]/10 pt-16 scroll-mt-20">
        <div class="mb-10">
          <p class="u-h2 max-w-2xl leading-tight font-light !tracking-[0.15em]">
            Définir un programme, donner forme à une vision, bâtir un futur, engageons le dialogue.
          </p>
        </div>
        <div class="flex flex-col gap-y-6">
          <a href="mailto:alexandre.mat+w@protonmail.com" class="u-h3 text-[13px] sm:text-[15px] font-normal tracking-[0.08em] sm:tracking-[0.2em] hover:text-gray-500 transition-colors w-fit break-all sm:break-normal">
            alexandre.mat+w@protonmail.com
          </a>
          <a href="tel:+33658215300" class="u-h3 font-normal tracking-[0.2em] hover:text-gray-500 transition-colors w-fit">
            +33 6 58 21 53 00
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watchEffect, onMounted, onUnmounted } from 'vue';
import ProjectCard from '~/components/ProjectCard.vue';
import HeroSection from '~/components/HeroSection.vue';
import CollaborationsList from '~/components/CollaborationsList.vue';
import { useProjectFilters } from '~/composables/useProjectFilters';

definePageMeta({
  layout: 'default',
  displayTitle: 'Projets',
  showFilters: true,
  transparentHeader: true
})

useHead({
  title: 'Alexandre Mathieu — architecture & design'
})

useSeoMeta({
  description: "Portfolio d'Alexandre Mathieu: projets d'architecture, design, rehabilitation et recherche constructive.",
  ogTitle: 'Alexandre Mathieu - architecture & design',
  ogDescription: "Portfolio d'Alexandre Mathieu: projets d'architecture, design, rehabilitation et recherche constructive.",
  twitterTitle: 'Alexandre Mathieu - architecture & design',
  twitterDescription: "Portfolio d'Alexandre Mathieu: projets d'architecture, design, rehabilitation et recherche constructive."
})

const route = useRoute();
const scrollProgress = ref(0);
const PROJECTS_GRID_SCROLL_OFFSET = 160;

const handleScroll = () => {
  if (import.meta.client) {
    scrollProgress.value = Math.min(1, window.scrollY / window.innerHeight);
  }
};

const shouldOpenProjectsGrid = () => {
  return route.query.view === 'grid' || route.hash === '#projects-grid';
};

const jumpToProjects = (attempt = 0) => {
  const target = document.getElementById('projects-grid');
  if (target) {
    const targetPosition = target.getBoundingClientRect().top + window.scrollY - PROJECTS_GRID_SCROLL_OFFSET;
    window.scrollTo({ top: targetPosition, behavior: 'auto' });
  } else if (attempt < 10) {
    setTimeout(() => jumpToProjects(attempt + 1), 80);
  }
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  handleScroll();
  
  if (shouldOpenProjectsGrid()) {
    // Immediate jump if view=grid is present
    setTimeout(() => jumpToProjects(), 50);
  } else if (route.query.scroll === 'contact') {
    // Scroll to contact if requested
    setTimeout(scrollToContact, 100);
  }
});

watch(() => route.fullPath, () => {
  if (import.meta.client && shouldOpenProjectsGrid()) {
    setTimeout(() => jumpToProjects(), 50);
  }
});

const { 
  selectedTypology, 
  selectedSize, 
  selectedYear, 
  selectedCountry,
  selectedProjectTitle,
  sortBy,
  typologyOptions,
  sizeOptions,
  yearOptions,
  countryOptions,
  projectTitleOptions
} = useProjectFilters();

// Watch filters and scroll to grid when they change
watch([selectedTypology, selectedYear, selectedCountry], () => {
  if (import.meta.client) {
    // Only scroll if we're not already at the grid or below
    const target = document.getElementById('projects-grid');
    if (target) {
      const rect = target.getBoundingClientRect();
      // If the top of the grid is not visible (scrolled up too far), scroll to it
      if (rect.top > PROJECTS_GRID_SCROLL_OFFSET + 24 || rect.top < PROJECTS_GRID_SCROLL_OFFSET) {
        scrollToProjects();
      }
    }
  }
}, { deep: true });

const { data: projects } = await useAsyncData('home-projects', () =>
  queryCollection('content')
    .where('path', 'LIKE', '/projets/%')
    .where('draft', '<>', true)
    .all()
);

const scrollToSection = (targetId: string, offset: number = 96, behavior: ScrollBehavior = 'smooth') => {
  const target = document.getElementById(targetId);
  if (!target) return;

  const targetPosition = target.getBoundingClientRect().top + window.scrollY - offset;
  window.scrollTo({ top: Math.max(0, targetPosition), behavior });
};

const scrollToContact = () => {
  scrollToSection('contact', 80);
};

const scrollToProjects = () => {
  scrollToSection('projects-grid', PROJECTS_GRID_SCROLL_OFFSET);
};

watchEffect(() => {
  if (projects.value) {
    const typologies = new Set<string>();
    const years = new Set<string>();
    const countries = new Set<string>();
    projects.value.forEach(p => {
      if (Array.isArray(p.typologies)) p.typologies.forEach(t => t && typologies.add(t));
      if (Array.isArray(p.pays)) p.pays.forEach(c => c && countries.add(c));
      if (p.date) {
        const year = new Date(p.date).getFullYear().toString();
        if (year !== 'NaN') years.add(year);
      }
    });
    typologyOptions.value = Array.from(typologies).sort();
    yearOptions.value = Array.from(years).sort((a, b) => b.localeCompare(a));
    countryOptions.value = Array.from(countries).sort();
  }
});

const filteredProjects = computed(() => {
  if (!projects.value) return [];
  let result = projects.value.filter(p => {
    const matchTypology = !selectedTypology.value || (p.typologies && p.typologies.includes(selectedTypology.value));
    const matchCountry = !selectedCountry.value || (p.pays && p.pays.includes(selectedCountry.value));
    const matchYear = !selectedYear.value || (p.date && new Date(p.date).getFullYear().toString() === selectedYear.value);
    return matchTypology && matchCountry && matchYear;
  });
  result.sort((a, b) => {
    const orderA = a.order ?? 999;
    const orderB = b.order ?? 999;
    if (orderA !== orderB) return orderA - orderB;
    return new Date(b.date || 0).getTime() - new Date(a.date || 0).getTime();
  });
  return result;
});
</script>
