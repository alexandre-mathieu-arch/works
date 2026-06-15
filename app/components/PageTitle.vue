<template>
  <div 
    class="relative z-40 transition-colors duration-700"
    :class="[
      isProjectPage ? 'pb-1' : 'pb-2',
      { 'glass-fluted -mx-[var(--main-padding)] px-[var(--main-padding)]': showFilters || $slots.triggers },
      { 'sticky top-[var(--header-height)]': (showFilters || $slots.triggers) && !noSticky }
    ]"
  >
    <!-- Project Title Slot: Permanent height to avoid folding effect -->
    <div class="h-9 md:h-[30px] relative flex items-center"> 
      <Transition
        enter-active-class="transition duration-700 ease-out"
        enter-from-class="opacity-0 translate-y-1"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition duration-200 ease-in absolute top-0 left-0"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0 -translate-y-1"
      >
        <div 
          v-if="hoveredProjectTitle || (!hideMainTitle && title) || (hideMainTitle && title)" 
          :key="hoveredProjectTitle || (typeof title === 'string' ? title : title.main)"
          class="text-[18px] sm:text-[20px] font-bold leading-none text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] whitespace-nowrap overflow-hidden text-ellipsis w-full md:w-[calc((100%-32px)/2)] xl:w-[calc((100%-96px)/4)] h-full flex items-center"
          :style="{ viewTransitionName: route.path.startsWith('/projets/') ? 'title-' + route.path.replace(/\//g, '-') : 'project-title-continuity' }"
        >
          <template v-if="hoveredProjectTitle">
            {{ hoveredProjectTitle }}
          </template>
          <template v-else-if="!hideMainTitle && title">
            {{ typeof title === 'string' ? title : title.main }}
          </template>
          <template v-else-if="hideMainTitle && title">
            {{ typeof title === 'string' ? title : '' }}
          </template>
        </div>
      </Transition>
    </div>
    
    <div v-if="showFilters || $slots.triggers" class="mt-0 relative" ref="filterContainer">
      <div v-if="showFilters && !readonlyFilters && !isProjectPage" class="md:hidden">
        <div class="flex items-center gap-2">
          <button
            type="button"
            @click="isMobileFiltersOpen = true"
            class="flex min-h-11 flex-1 items-center justify-between border border-[#121212]/30 bg-white/50 px-3 text-left u-h4 !tracking-normal text-[#121212] transition-colors duration-500 dark:border-white/20 dark:bg-white/5 dark:text-white doux:text-[#4A4443] nuit:bg-[#161D2F] nuit:text-[#CDD6F4]"
            :aria-expanded="isMobileFiltersOpen"
            aria-controls="mobile-filters-panel"
          >
            <span>Filtres</span>
            <span v-if="activeFilterCount" class="ml-3 flex h-5 min-w-5 items-center justify-center rounded-full bg-[#121212] px-1.5 text-[10px] leading-none text-white dark:bg-white dark:text-[#121212]">
              {{ activeFilterCount }}
            </span>
          </button>
          <button
            v-if="hasActiveFilters"
            type="button"
            @click="resetFilters"
            class="flex h-11 w-11 shrink-0 items-center justify-center border border-primary-900/30 bg-white/50 text-primary-900 transition-colors duration-500 dark:border-primary-400/30 dark:bg-white/5 dark:text-primary-400 nuit:bg-[#161D2F]"
            aria-label="Réinitialiser les filtres"
          >
            <svg viewBox="0 0 20 20" fill="currentColor" class="h-4 w-4">
              <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
            </svg>
          </button>
        </div>

        <Teleport to="body">
          <Transition
            enter-active-class="transition duration-300 ease-out"
            enter-from-class="opacity-0"
            enter-to-class="opacity-100"
            leave-active-class="transition duration-200 ease-in"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
          >
            <div
              v-if="isMobileFiltersOpen"
              class="fixed inset-0 z-[90] md:hidden"
              role="dialog"
              aria-modal="true"
              aria-labelledby="mobile-filters-title"
            >
              <button
                type="button"
                class="absolute inset-0 bg-[#121212]/35"
                aria-label="Fermer les filtres"
                @click="isMobileFiltersOpen = false"
              />
              <div
                id="mobile-filters-panel"
                class="absolute inset-x-0 bottom-0 max-h-[82dvh] overflow-y-auto border-t border-[#121212]/10 bg-white px-[var(--main-padding)] pb-[calc(env(safe-area-inset-bottom)+1rem)] pt-4 shadow-2xl dark:border-white/10 dark:bg-[#121212] doux:bg-[#E5E1E0] nuit:bg-[#1A2238]"
              >
                <div class="mb-5 flex items-center justify-between gap-4">
                  <h2 id="mobile-filters-title" class="u-h3 text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4]">
                    Filtres
                  </h2>
                  <button
                    type="button"
                    @click="isMobileFiltersOpen = false"
                    class="flex h-11 w-11 items-center justify-center border border-[#121212]/20 text-[#121212] dark:border-white/20 dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4]"
                    aria-label="Fermer les filtres"
                  >
                    <svg viewBox="0 0 20 20" fill="currentColor" class="h-4 w-4">
                      <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
                    </svg>
                  </button>
                </div>

                <div class="space-y-6">
                  <section v-for="group in mobileFilterGroups" :key="group.id">
                    <div class="mb-2 u-h4 text-[#121212]/60 dark:text-white/60 doux:text-[#4A4443]/70 nuit:text-[#CDD6F4]/70">
                      {{ group.label }}
                    </div>
                    <div class="flex flex-wrap gap-2">
                      <button
                        type="button"
                        @click="selectMobileFilter(group.id, null)"
                        class="min-h-10 border px-3 py-2 u-h4 !tracking-normal transition-colors duration-300"
                        :class="isMobileFilterActive(group.id, null) ? 'border-primary-900 bg-primary-900 text-white dark:border-primary-400 dark:bg-primary-400 dark:text-[#121212]' : 'border-[#121212]/20 text-[#121212]/70 dark:border-white/20 dark:text-white/70 doux:text-[#4A4443]/70 nuit:text-[#CDD6F4]/70'"
                      >
                        {{ group.emptyLabel }}
                      </button>
                      <button
                        v-for="option in group.options"
                        :key="option"
                        type="button"
                        @click="selectMobileFilter(group.id, option)"
                        class="min-h-10 border px-3 py-2 u-h4 !tracking-normal transition-colors duration-300"
                        :class="isMobileFilterActive(group.id, option) ? 'border-primary-900 bg-primary-900 text-white dark:border-primary-400 dark:bg-primary-400 dark:text-[#121212]' : 'border-[#121212]/20 text-[#121212]/70 dark:border-white/20 dark:text-white/70 doux:text-[#4A4443]/70 nuit:text-[#CDD6F4]/70'"
                      >
                        {{ option }}
                      </button>
                    </div>
                  </section>
                </div>

                <div class="sticky bottom-0 -mx-[var(--main-padding)] mt-6 flex gap-2 border-t border-[#121212]/10 bg-white px-[var(--main-padding)] py-3 dark:border-white/10 dark:bg-[#121212] doux:bg-[#E5E1E0] nuit:bg-[#1A2238]">
                  <button
                    v-if="hasActiveFilters"
                    type="button"
                    @click="resetFilters"
                    class="min-h-11 flex-1 border border-[#121212]/20 px-3 u-h4 !tracking-normal text-[#121212] dark:border-white/20 dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4]"
                  >
                    Tout effacer
                  </button>
                  <button
                    type="button"
                    @click="isMobileFiltersOpen = false"
                    class="min-h-11 flex-1 border border-[#121212] bg-[#121212] px-3 u-h4 !tracking-normal text-white dark:border-white dark:bg-white dark:text-[#121212] doux:border-[#4A4443] doux:bg-[#4A4443] doux:text-[#E5E1E0] nuit:border-[#CDD6F4] nuit:bg-[#CDD6F4] nuit:text-[#1A2238]"
                  >
                    Voir les projets
                  </button>
                </div>
              </div>
            </div>
          </Transition>
        </Teleport>
      </div>

      <!-- Custom triggers slot -->
      <slot name="triggers">
        <!-- Grid aligned triggers -->
        <div 
          class="hidden md:grid grid-cols-1 sm:grid-cols-3 xl:grid-cols-4 gap-x-2 gap-y-3 md:gap-8 items-start"
          style="view-transition-name: page-triggers;"
        >
          <!-- Standard Filters (Grid) or Project Info (Detail) -->
          <template v-if="showFilters">
            <div 
              v-for="filter in filters" 
              :key="filter.id"
              class="relative col-span-1"
            >
              <button 
                @click="!readonlyFilters ? toggleMenu(filter.id) : null"
                class="flex items-center justify-between gap-2 u-h4 transition-all duration-700 px-3 min-h-11 md:h-[30px] md:min-h-0 -mt-[1px] w-full group !tracking-normal capitalize"
                :aria-expanded="activeMenu === filter.id"
                :aria-controls="'filter-menu-' + filter.id"
                :class="[
                  readonlyFilters 
                    ? 'bg-transparent border border-primary-900 text-primary-900 dark:border-primary-400 dark:text-primary-400 cursor-default pointer-events-none' 
                    : 'bg-white/50 dark:bg-white/5 nuit:bg-[#161D2F] border border-[#121212]/30 dark:border-white/20',
                  activeMenu === filter.id ? 'text-primary-900 border-primary-900 dark:text-primary-400 dark:border-primary-400 z-50' : (!readonlyFilters ? 'text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4]' : ''),
                  filter.active ? '!text-primary-900 !border-primary-900 dark:!text-primary-400 dark:!border-primary-400 z-50' : '',
                  !readonlyFilters ? 'hover:border-primary-900 hover:text-primary-900 dark:hover:border-primary-400 dark:hover:text-primary-400' : ''
                ]"
              >
                <div class="flex items-center gap-2 truncate">
                  <span class="truncate">{{ filter.selection }}</span>
                </div>
                
                <template v-if="!readonlyFilters">
                  <svg 
                    viewBox="0 0 20 20" 
                    fill="currentColor" 
                    class="w-4 h-4 flex-shrink-0 transition-transform duration-700"
                    :class="{ 'rotate-180': activeMenu === filter.id }"
                  >
                    <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clip-rule="evenodd" />
                  </svg>
                </template>
              </button>

              <!-- Local Dropdown Menu (Vertical List) -->
              <Transition
                mode="out-in"
                enter-active-class="transition duration-400 ease-out"
                enter-from-class="opacity-0 -translate-y-2"
                enter-to-class="opacity-100 translate-y-0"
                leave-active-class="transition duration-300 ease-in"
                leave-from-class="opacity-100 translate-y-0"
                leave-to-class="opacity-0 -translate-y-2"
              >
                <div 
                  v-if="activeMenu === filter.id" 
                  :id="'filter-menu-' + filter.id"
                  class="absolute left-0 top-full mt-1 z-50 bg-white dark:bg-[#1A1A1A] doux:bg-[#E5E1E0] nuit:bg-[#1E2538] border border-[#121212]/10 dark:border-white/10 shadow-lg min-w-full w-[min(22rem,calc(100vw-2rem))] max-h-[60vh] overflow-y-auto"
                  :class="{ 'right-0 left-auto': filter.id === 'country' && !isProjectPage }"
                >
                  <div class="flex flex-col py-1">
                    <template v-if="activeMenu === 'typology'">
                      <button 
                        @click="selectedTypology = null; activeMenu = null" 
                        class="u-h4 min-h-11 md:min-h-[34px] px-4 flex items-center transition-colors duration-300 whitespace-nowrap hover:bg-[#121212]/5 dark:hover:bg-white/5" 
                        :class="selectedTypology === null ? 'text-primary-900 dark:text-primary-400 font-bold bg-[#121212]/5 dark:bg-white/5' : 'text-[#121212]/60 dark:text-white/60 doux:text-[#4A4443]/60 nuit:text-[#CDD6F4]/60'"
                      >
                        Toutes
                      </button>
                      <button 
                        v-for="opt in typologyOptions" 
                        :key="opt" 
                        @click="selectedTypology = opt; activeMenu = null" 
                        class="u-h4 min-h-11 md:min-h-[34px] px-4 flex items-center transition-colors duration-300 whitespace-nowrap hover:bg-[#121212]/5 dark:hover:bg-white/5" 
                        :class="selectedTypology === opt ? 'text-primary-900 dark:text-primary-400 font-bold bg-[#121212]/5 dark:bg-white/5' : 'text-[#121212]/60 dark:text-white/60 doux:text-[#4A4443]/60 nuit:text-[#CDD6F4]/60'"
                      >
                        {{ opt }}
                      </button>
                    </template>
                    <template v-if="activeMenu === 'year'">
                      <button 
                        @click="selectedYear = null; activeMenu = null" 
                        class="u-h4 min-h-11 md:min-h-[34px] px-4 flex items-center transition-colors duration-300 whitespace-nowrap hover:bg-[#121212]/5 dark:hover:bg-white/5" 
                        :class="selectedYear === null ? 'text-primary-900 dark:text-primary-400 font-bold bg-[#121212]/5 dark:bg-white/5' : 'text-[#121212]/60 dark:text-white/60 doux:text-[#4A4443]/60 nuit:text-[#CDD6F4]/60'"
                      >
                        Toutes
                      </button>
                      <button 
                        v-for="opt in yearOptions" 
                        :key="opt" 
                        @click="selectedYear = opt; activeMenu = null" 
                        class="u-h4 min-h-11 md:min-h-[34px] px-4 flex items-center transition-colors duration-300 whitespace-nowrap hover:bg-[#121212]/5 dark:hover:bg-white/5" 
                        :class="selectedYear === opt ? 'text-primary-900 dark:text-primary-400 font-bold bg-[#121212]/5 dark:bg-white/5' : 'text-[#121212]/60 dark:text-white/60 doux:text-[#4A4443]/60 nuit:text-[#CDD6F4]/60'"
                      >
                        {{ opt }}
                      </button>
                    </template>
                    <template v-if="activeMenu === 'country'">
                      <button 
                        @click="selectedCountry = null; activeMenu = null" 
                        class="u-h4 min-h-11 md:min-h-[34px] px-4 flex items-center transition-colors duration-300 whitespace-nowrap hover:bg-[#121212]/5 dark:hover:bg-white/5" 
                        :class="selectedCountry === null ? 'text-primary-900 dark:text-primary-400 font-bold bg-[#121212]/5 dark:bg-white/5' : 'text-[#121212]/60 dark:text-white/60 doux:text-[#4A4443]/60 nuit:text-[#CDD6F4]/60'"
                      >
                        Tous
                      </button>
                      <button 
                        v-for="opt in countryOptions" 
                        :key="opt" 
                        @click="selectedCountry = opt; activeMenu = null" 
                        class="u-h4 min-h-11 md:min-h-[34px] px-4 flex items-center transition-colors duration-300 whitespace-nowrap hover:bg-[#121212]/5 dark:hover:bg-white/5" 
                        :class="selectedCountry === opt ? 'text-primary-900 dark:text-primary-400 font-bold bg-[#121212]/5 dark:bg-white/5' : 'text-[#121212]/60 dark:text-white/60 doux:text-[#4A4443]/60 nuit:text-[#CDD6F4]/60'"
                      >
                        {{ opt }}
                      </button>
                    </template>
                  </div>
                </div>
              </Transition>
            </div>
          </template>

          <!-- Project Navigation Triggers (Specific to Detail Page) -->
          <template v-if="isProjectPage">
            <!-- Column 2+: Sequence Navigation (Arrows + Counters) -->
            <!-- We allow this column to span across the rest of the grid to accommodate many images -->
            <div class="hidden lg:flex min-h-11 md:h-[30px] items-center col-span-full md:col-span-2 xl:col-span-3 w-full md:w-fit">
              <SequenceCounter
                v-if="totalImages > 0"
                :model-value="carouselCurrentImageIndex"
                :total="totalImages"
                :prev-project="prevProject"
                :next-project="nextProject"
                @update:model-value="newIndex => setCurrentImageIndex(newIndex)"
                @nav="direction => setTransitionDirection(direction)"
              />
            </div>
          </template>

          <!-- Reset Buttons Column -->
          <div class="flex justify-start sm:justify-end sm:col-start-3 xl:col-start-4 gap-2">
            <button 
              v-if="hasActiveFilters"
              @click="resetFilters"
              class="flex items-center gap-2 u-h4 px-3 min-h-11 md:h-[30px] md:min-h-0 border border-primary-900/30 dark:border-primary-400/30 text-primary-900 dark:text-primary-400 bg-white/50 dark:bg-white/5 nuit:bg-[#161D2F] hover:bg-primary-900 hover:text-white dark:hover:bg-primary-400 dark:hover:text-[#121212] transition-all duration-700 -mt-[1px] whitespace-nowrap group/reset !tracking-normal"
              title="Réinitialiser les filtres"
            >
              <span class="text-[9px] md:text-[10px] capitalize font-medium">Tout effacer</span>
              <svg viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4 opacity-50 group-hover/reset:opacity-100 transition-opacity">
                <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 101.06 1.06L10 11.06l3.72 3.72a.75.75 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
              </svg>
            </button>
          </div>
        </div>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted, onUnmounted } from 'vue';
import { useProjectFilters } from '~/composables/useProjectFilters';
import { useHoverProject } from '~/composables/useHoverProject';
import { useVisitedProjects } from '~/composables/useVisitedProjects';
import { useCarouselState } from '~/composables/useCarouselState';
import SequenceCounter from '~/components/SequenceCounter.vue';

const { hoveredProject, hoveredProjectTitle } = useHoverProject();
const { clearVisited, visitedProjects } = useVisitedProjects();
const { currentImageIndex: carouselCurrentImageIndex, totalImages, setCurrentImageIndex } = useCarouselState();

const props = defineProps<{
  title: string | { main: string; sub?: string };
  showFilters?: boolean;
  readonlyFilters?: boolean;
  hideMainTitle?: boolean;
  noSticky?: boolean;
}>();

const route = useRoute();

const { data: allContent } = await useAsyncData('all-projects-nav', () =>
  queryCollection('content')
    .select('path', 'title', 'date')
    .where('path', 'LIKE', '/projets/%')
    .where('draft', '<>', true)
    .all()
);

const projects = computed(() => {
  if (!allContent.value) return [];
  return [...allContent.value].sort((a, b) => {
    const dateA = new Date(a.date || 0).getTime();
    const dateB = new Date(b.date || 0).getTime();
    return dateB - dateA;
  });
});

const currentProjectIndex = computed(() => {
  return projects.value.findIndex(p => p.path === route.path);
});

const prevProject = computed(() => {
  if (currentProjectIndex.value > 0) {
    const p = projects.value[currentProjectIndex.value - 1];
    return p;
  }
  return null;
});

const nextProject = computed(() => {
  if (currentProjectIndex.value < projects.value.length - 1) {
    const p = projects.value[currentProjectIndex.value + 1];
    return p;
  }
  return null;
});

const isProjectPage = computed(() => route.path.startsWith('/projets/'));

const setTransitionDirection = (direction: 'next' | 'prev') => {
  if (import.meta.client) {
    document.documentElement.classList.remove('transition-next', 'transition-prev');
    document.documentElement.classList.add(`transition-${direction}`);
  }
};

const filterContainer = ref<HTMLElement | null>(null);

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
  projectTitleOptions,
  resetFilters
} = useProjectFilters();

const activeMenu = ref<string | null>(null);
const isMobileFiltersOpen = ref(false);

type MobileFilterId = 'typology' | 'year' | 'country';

const mobileFilterGroups = computed<Array<{ id: MobileFilterId; label: string; emptyLabel: string; options: string[] }>>(() => [
  {
    id: 'typology',
    label: 'Typologie',
    emptyLabel: 'Toutes',
    options: typologyOptions.value
  },
  {
    id: 'year',
    label: 'Année',
    emptyLabel: 'Toutes',
    options: yearOptions.value
  },
  {
    id: 'country',
    label: 'Pays',
    emptyLabel: 'Tous',
    options: countryOptions.value
  }
]);

const selectMobileFilter = (id: MobileFilterId, value: string | null) => {
  if (id === 'typology') selectedTypology.value = value;
  if (id === 'year') selectedYear.value = value;
  if (id === 'country') selectedCountry.value = value;
};

const isMobileFilterActive = (id: MobileFilterId, value: string | null) => {
  if (id === 'typology') return selectedTypology.value === value;
  if (id === 'year') return selectedYear.value === value;
  return selectedCountry.value === value;
};

const activeFilterCount = computed(() => {
  return [
    selectedTypology.value,
    selectedSize.value,
    selectedYear.value,
    selectedCountry.value,
    selectedProjectTitle.value
  ].filter(Boolean).length;
});

const handleClickOutside = (event: MouseEvent) => {
  if (filterContainer.value && !filterContainer.value.contains(event.target as Node)) {
    activeMenu.value = null;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  if (isMobileFiltersOpen.value) {
    document.body.style.overflow = '';
  }
});

watch(() => route.fullPath, () => {
  activeMenu.value = null;
  isMobileFiltersOpen.value = false;
});

watch(isMobileFiltersOpen, (isOpen) => {
  if (import.meta.client) {
    document.body.style.overflow = isOpen ? 'hidden' : '';
  }
});

const filters = computed(() => {
  const hp = hoveredProject.value;

  // Extract year from hp.date if it exists
  let hpYear = null;
  if (hp?.date) {
    const d = hp.date;
    if (typeof d === 'number' || (typeof d === 'string' && /^\d{4}$/.test(d))) {
      hpYear = d.toString();
    } else {
      const dateObj = new Date(d);
      if (!isNaN(dateObj.getTime())) hpYear = dateObj.getFullYear().toString();
    }
  }

  // If readonly mode (Project Detail), we condense everything into one label for the first trigger
  if (props.readonlyFilters) {
    const parts = [];
    if (hp?.typologies?.[0]) parts.push(hp.typologies[0]);
    if (hpYear) parts.push(hpYear);
    if (hp?.pays?.[0]) parts.push(hp.pays[0]);
    
    return [
      { 
        id: 'info', 
        category: 'Info', 
        selection: parts.join(', ') || 'Détails',
        active: false 
      }
    ];
  }

  return [
    { 
      id: 'typology', 
      category: 'Typologie',
      selection: (hp?.typologies && hp.typologies.length > 0) 
        ? hp.typologies[0] 
        : (selectedTypology.value || 'Typologie'),
      active: !!selectedTypology.value
    },
    { 
      id: 'year', 
      category: 'Année',
      selection: hpYear || (selectedYear.value || 'Année'),
      active: !!selectedYear.value
    },
    { 
      id: 'country', 
      category: 'Pays',
      selection: (hp?.pays && hp.pays.length > 0) 
        ? hp.pays[0] 
        : (selectedCountry.value || 'Pays'),
      active: !!selectedCountry.value
    }
  ];
});

const toggleMenu = (id: string) => {
  if (activeMenu.value === id) {
    activeMenu.value = null;
  } else {
    activeMenu.value = id;
  }
};

const hasActiveFilters = computed(() => activeFilterCount.value > 0);
</script>

<style scoped>
@reference "../assets/css/main.css";
</style>
