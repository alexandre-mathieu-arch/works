<template>
  <div>
    <!-- Hero Section -->
    <div class="-mt-[var(--header-height)]">
      <HeroSection 
        :scroll-progress="scrollProgress" 
        @scroll-to-projects="scrollToProjectsFromHero"
      />
    </div>

    <!-- Project Grid (from architecture.vue) -->
    <div id="projects-grid" class="pt-0 pb-0 min-h-screen scroll-mt-40">
      <div 
        v-if="filteredProjects?.length" 
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-4 gap-4 md:gap-8 items-center mt-3"
      >
        <template v-for="(project, index) in filteredProjects" :key="project.path">
          <template v-if="index % 6 === 5">
            <button 
              @click="scrollToContact"
              class="hidden xl:block aspect-square border border-[#121212]/30 relative group transition-colors duration-(--duration-menu) ease-(--ease-atelier) hover:border-[#121212] dark:border-white/20 dark:hover:border-white/45 doux:border-[#4A4443]/25 nuit:border-[#CDD6F4]/20 nuit:hover:border-[#CDD6F4]/45 text-left"
            >
              <div class="absolute top-0 left-0 w-full px-2 h-[30px] flex items-center opacity-0 group-hover:opacity-100 transition-opacity duration-(--duration-menu) ease-(--ease-atelier)">
                <span class="u-h3 dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4]">Parlons de votre projet</span>
              </div>
            </button>
            <ProjectCard :project="project" />
            <button 
              @click="scrollToContact"
              class="hidden xl:block aspect-square border border-[#121212]/30 relative group transition-colors duration-(--duration-menu) ease-(--ease-atelier) hover:border-[#121212] dark:border-white/20 dark:hover:border-white/45 doux:border-[#4A4443]/25 nuit:border-[#CDD6F4]/20 nuit:hover:border-[#CDD6F4]/45 text-left"
            >
              <div class="absolute top-0 left-0 w-full px-2 h-[30px] flex items-center opacity-0 group-hover:opacity-100 transition-opacity duration-(--duration-menu) ease-(--ease-atelier)">
                <span class="u-h3 dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4]">Parlons de votre projet</span>
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
        class="xl:hidden mt-8 flex min-h-11 w-full items-center justify-between border border-[#121212]/20 px-4 py-3 text-left transition-colors duration-(--duration-hover) ease-(--ease-atelier) hover:border-[#121212]/50 dark:border-white/20 dark:hover:border-white/45 doux:border-[#4A4443]/20 nuit:border-[#CDD6F4]/20"
      >
        <span class="u-h3 dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4]">Parlons de votre projet</span>
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
          <a href="mailto:alexandre.mat+w@protonmail.com" class="u-h3 text-[13px] sm:text-[15px] font-normal tracking-[0.08em] sm:tracking-[0.2em] hover:text-[#121212]/55 dark:hover:text-white/65 transition-colors duration-(--duration-hover) ease-(--ease-atelier) w-fit break-all sm:break-normal">
            alexandre.mat+w@protonmail.com
          </a>
          <a href="tel:+33658215300" class="u-h3 font-normal tracking-[0.2em] hover:text-[#121212]/55 dark:hover:text-white/65 transition-colors duration-(--duration-hover) ease-(--ease-atelier) w-fit">
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
const { state: projectTransition } = useProjectTransition();
const scrollProgress = ref(0);
const PROJECTS_GRID_SCROLL_OFFSET = 160;
const HERO_SCROLL_DURATION = 1900;
let activeScrollFrame: number | null = null;
let restoreScrollBehavior: (() => void) | null = null;
const isHeroScrollRunning = ref(false);

const getMotionDuration = (name: string, fallback: number) => {
  if (!import.meta.client) return fallback;

  const rawValue = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  if (!rawValue) return fallback;

  const value = parseFloat(rawValue);
  if (Number.isNaN(value)) return fallback;

  return rawValue.endsWith('ms') ? value : value * 1000;
};

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
    cancelActiveScroll();
    const targetPosition = target.getBoundingClientRect().top + window.scrollY - PROJECTS_GRID_SCROLL_OFFSET;
    window.scrollTo({ top: targetPosition, behavior: 'auto' });
  } else if (attempt < 10) {
    setTimeout(() => jumpToProjects(attempt + 1), 80);
  }
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  handleScroll();

  const isReturningFromProject = projectTransition.value.mode === 'close'
    && projectTransition.value.hasGridScrollPosition;

  if (shouldOpenProjectsGrid() && !isReturningFromProject) {
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

onUnmounted(() => {
  if (import.meta.client) {
    window.removeEventListener('scroll', handleScroll);
    cancelActiveScroll();
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

const cancelActiveScroll = () => {
  if (!import.meta.client || activeScrollFrame === null) return;

  cancelAnimationFrame(activeScrollFrame);
  activeScrollFrame = null;

  if (restoreScrollBehavior) {
    restoreScrollBehavior();
    restoreScrollBehavior = null;
  }
};

const animateScrollTo = (
  targetPosition: number,
  duration = getMotionDuration('--duration-page', 900),
  onComplete?: () => void
) => {
  if (!import.meta.client) return;

  const scroller = document.scrollingElement || document.documentElement;
  const top = Math.max(0, targetPosition);
  const startPosition = scroller.scrollTop;
  const distance = top - startPosition;
  const scrollDuration = Math.max(1200, duration);
  const shouldAnimate = Math.abs(distance) > 2 && scrollDuration > 0;

  cancelActiveScroll();

  if (!shouldAnimate) {
    scroller.scrollTop = top;
    onComplete?.();
    return;
  }

  const root = document.documentElement;
  const body = document.body;
  const previousRootScrollBehavior = root.style.scrollBehavior;
  const previousBodyScrollBehavior = body.style.scrollBehavior;

  root.style.scrollBehavior = 'auto';
  body.style.scrollBehavior = 'auto';
  restoreScrollBehavior = () => {
    root.style.scrollBehavior = previousRootScrollBehavior;
    body.style.scrollBehavior = previousBodyScrollBehavior;
  };

  const startTime = performance.now();
  const easeInOutSine = (progress: number) => {
    return -(Math.cos(Math.PI * progress) - 1) / 2;
  };

  const step = (currentTime: number) => {
    const progress = Math.min(1, (currentTime - startTime) / scrollDuration);
    const nextPosition = startPosition + distance * easeInOutSine(progress);
    scroller.scrollTop = nextPosition;

    if (progress < 1) {
      activeScrollFrame = requestAnimationFrame(step);
      return;
    }

    scroller.scrollTop = top;
    activeScrollFrame = null;
    if (restoreScrollBehavior) {
      restoreScrollBehavior();
      restoreScrollBehavior = null;
    }
    onComplete?.();
  };

  activeScrollFrame = requestAnimationFrame(step);
};

const scrollToSection = (targetId: string, offset: number = 96, duration = 1300) => {
  const target = document.getElementById(targetId);
  if (!target) return;

  const targetPosition = target.getBoundingClientRect().top + window.scrollY - offset;
  animateScrollTo(targetPosition, duration);
};

const scrollToContact = () => {
  scrollToSection('contact', 80, getMotionDuration('--duration-image', 1200));
};

const scrollToProjects = () => {
  scrollToSection('projects-grid', PROJECTS_GRID_SCROLL_OFFSET, getMotionDuration('--duration-page', 900));
};

const scrollToProjectsFromHero = () => {
  if (isHeroScrollRunning.value) return;

  const target = document.getElementById('projects-grid');
  if (!target) return;

  isHeroScrollRunning.value = true;
  const targetPosition = target.getBoundingClientRect().top + window.scrollY - PROJECTS_GRID_SCROLL_OFFSET;
  animateScrollTo(targetPosition, HERO_SCROLL_DURATION, () => {
    isHeroScrollRunning.value = false;
  });
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
