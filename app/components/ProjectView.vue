<template>
  <div v-if="project" class="w-full relative bg-white dark:bg-[#121212] doux:bg-[#E5E1E0] nuit:bg-[#1A2238] transition-colors duration-300">
    <div :class="isHero ? 'pt-32 pb-24' : 'pt-0 pb-12'">
      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 md:gap-8">
        <!-- Carousel Section -->
        <div class="col-span-1 md:col-span-1 xl:col-span-3 z-0 order-1 md:order-2" :class="isHero ? '' : '-mx-[var(--main-padding)] md:mx-0'">
          <div 
            class="relative w-full aspect-[4/3] sm:aspect-[16/10] md:aspect-[16/9] transition-colors duration-300"
          >
            <ImageCarousel :images="images" :model-value="currentImageIndex" @update:model-value="setCurrentImageIndex" :id="project.path" :alt="project.title" />
          </div>
        </div>

        <!-- Info / Description -->
        <div class="col-span-1 pt-0 z-0 order-2 md:order-1" :style="!isHero ? 'view-transition-name: project-description;' : ''">
          <div class="project-description flex flex-col pr-0 md:pr-8 py-0 bg-white dark:bg-[#121212] doux:bg-[#E5E1E0] nuit:bg-[#1A2238] transition-colors duration-300" :class="!isHero ? 'min-h-0 md:min-h-[calc(100vh-var(--header-height)-120px)]' : ''">
            <div class="flex-grow pb-4 md:pb-6">
              <p v-if="project.description" class="u-body mb-8 font-medium italic opacity-80 leading-relaxed">{{ project.description }}</p>
              <div class="content-renderer">
                <ContentRenderer :value="project" class="prose max-w-none prose-sm md:prose-base dark:prose-invert" />
              </div>
            </div>

            <!-- Metadata -->
            <div class="mt-8 border-t border-[#121212]/10 dark:border-white/10 pt-4">
               <div class="space-y-1">
                <div v-if="project.surface" class="flex gap-4 u-legend">
                  <span class="w-20 opacity-50">Surface:</span>
                  <span>{{ project.surface }}</span>
                </div>
                <div v-if="project.lieu" class="flex gap-4 u-legend">
                  <span class="w-20 opacity-50">Lieu:</span>
                  <span>{{ project.lieu }}</span>
                </div>
                <!-- Additional fields -->
                <div v-if="project.cout" class="flex gap-4 u-legend">
                  <span class="w-20 opacity-50 text-nowrap">Coût:</span>
                  <span>{{ project.cout }}</span>
                </div>
                <div v-if="project.materiaux" class="flex gap-4 u-legend">
                  <span class="w-20 opacity-50 text-nowrap">Matériaux:</span>
                  <span>{{ Array.isArray(project.materiaux) ? project.materiaux.join(', ') : project.materiaux }}</span>
                </div>
                <div v-if="project.collaboration" class="flex gap-4 u-legend">
                  <span class="w-20 opacity-50 text-nowrap">Collaboration:</span>
                  <span>{{ project.collaboration }}</span>
                </div>
                <div v-if="project.logiciels" class="flex gap-4 u-legend">
                  <span class="w-20 opacity-50 text-nowrap">Logiciels:</span>
                  <span>{{ Array.isArray(project.logiciels) ? project.logiciels.join(', ') : project.logiciels }}</span>
                </div>
              </div>
            </div>

            <nav
              v-if="mobilePrevProject || mobileNextProject"
              class="lg:hidden mt-8 grid grid-cols-2 gap-3 border-t border-[#121212]/10 pt-4 dark:border-white/10"
              aria-label="Navigation entre projets"
            >
              <NuxtLink
                v-if="mobilePrevProject"
                :to="mobilePrevProject.path"
                class="min-h-11 border border-[#121212]/15 px-3 py-3 transition-colors duration-500 hover:border-[#121212]/40 dark:border-white/15 doux:border-[#4A4443]/20 nuit:border-[#CDD6F4]/20"
              >
                <span class="u-legend block opacity-50">Precedent</span>
                <span class="u-h4 block truncate !tracking-normal">{{ mobilePrevProject.title }}</span>
              </NuxtLink>
              <span v-else></span>
              <NuxtLink
                v-if="mobileNextProject"
                :to="mobileNextProject.path"
                class="min-h-11 border border-[#121212]/15 px-3 py-3 text-right transition-colors duration-500 hover:border-[#121212]/40 dark:border-white/15 doux:border-[#4A4443]/20 nuit:border-[#CDD6F4]/20"
              >
                <span class="u-legend block opacity-50">Suivant</span>
                <span class="u-h4 block truncate !tracking-normal">{{ mobileNextProject.title }}</span>
              </NuxtLink>
            </nav>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, watchEffect, onMounted } from 'vue';
import { useCarouselState } from '~/composables/useCarouselState';
import { useHoverProject } from '~/composables/useHoverProject';
import { useParallax } from '~/composables/useParallax';

const props = defineProps<{
  project: any;
  isHero?: boolean;
}>();

const route = useRoute();
const { currentImageIndex, setCurrentImageIndex, setTotalImages } = useCarouselState();
const { setHoveredProject } = useHoverProject();
const { getParallaxStyle } = useParallax(30);

const { data: mobileProjectNavItems } = await useAsyncData('project-view-mobile-nav', () =>
  queryCollection('content')
    .select('path', 'title', 'date')
    .where('path', 'LIKE', '/projets/%')
    .where('draft', '<>', true)
    .all()
);

const orderedMobileProjects = computed(() => {
  if (!mobileProjectNavItems.value) return [];
  return [...mobileProjectNavItems.value].sort((a, b) => {
    const dateA = new Date(a.date || 0).getTime();
    const dateB = new Date(b.date || 0).getTime();
    return dateB - dateA;
  });
});

const mobileCurrentProjectIndex = computed(() => {
  return orderedMobileProjects.value.findIndex(p => p.path === route.path);
});

const mobilePrevProject = computed(() => {
  if (mobileCurrentProjectIndex.value > 0) {
    return orderedMobileProjects.value[mobileCurrentProjectIndex.value - 1];
  }
  return null;
});

const mobileNextProject = computed(() => {
  if (mobileCurrentProjectIndex.value >= 0 && mobileCurrentProjectIndex.value < orderedMobileProjects.value.length - 1) {
    return orderedMobileProjects.value[mobileCurrentProjectIndex.value + 1];
  }
  return null;
});

const detailImgRefs = ref<HTMLElement[]>([]);
const setDetailImgRef = (el: any, index: number) => {
  if (el) detailImgRefs.value[index] = el.$el || el;
};

watchEffect(() => {
  if (props.project) {
    setHoveredProject(props.project);
  }
});

onMounted(() => {
  if (props.project) {
    setHoveredProject(props.project);
    // Reset carousel and scroll on entry
    setCurrentImageIndex(0);
    if (import.meta.client) {
      window.scrollTo({ top: 0, behavior: 'instant' });
    }
  }
});

// Also reset when the project changes (e.g. via navigation in the same component)
watch(() => props.project?.path, () => {
  setCurrentImageIndex(0);
  if (import.meta.client) {
    window.scrollTo({ top: 0, behavior: 'instant' });
  }
});

const images = computed(() => {
  if (!props.project) return [];
  
  const mainImgs = props.project.images || props.project.image || [];
  const mainList = Array.isArray(mainImgs) ? mainImgs : [mainImgs];
  
  const detailImgs = props.project.details || [];
  const detailList = Array.isArray(detailImgs) ? detailImgs : [detailImgs];
  
  return [...mainList, ...detailList]
    .filter(p => typeof p === 'string' && p.length > 0)
    .map(p => p.startsWith('/') ? p : '/' + p);
});

watch(images, (newImages) => {
  setTotalImages(newImages.length);
}, { immediate: true });
</script>

<style scoped>
.project-description {
  text-align: left;
}
</style>
