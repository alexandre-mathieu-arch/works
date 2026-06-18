<template>
  <div v-if="project" class="w-full relative bg-white dark:bg-[#121212] doux:bg-[#E5E1E0] nuit:bg-[#1A2238] transition-colors duration-(--duration-menu) ease-(--ease-atelier)">
    <div :class="isHero ? 'pt-32 pb-24' : 'pt-0 pb-12'">
      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 md:gap-8">
        <!-- Carousel Section -->
        <div class="col-span-1 md:col-span-1 xl:col-span-3 z-0 order-1 md:order-2" :class="isHero ? '' : '-mx-[var(--main-padding)] md:mx-0'">
          <div 
            class="relative w-full aspect-[4/3] sm:aspect-[16/10] md:aspect-[16/9] transition-colors duration-(--duration-menu) ease-(--ease-atelier)"
            :class="{ '[view-transition-name:project-media]': usesSharedMediaTransition }"
          >
            <ImageCarousel :images="images" :model-value="currentImageIndex" @update:model-value="setCurrentImageIndex" :id="project.path" :alt="project.title" />
          </div>
        </div>

        <!-- Info / Description -->
        <div class="col-span-1 pt-0 z-0 order-2 md:order-1">
          <div
            class="project-description flex w-full max-w-[280px] flex-col py-0 md:max-w-[300px] xl:max-w-[320px] bg-white dark:bg-[#121212] doux:bg-[#E5E1E0] nuit:bg-[#1A2238] transition-colors duration-(--duration-menu) ease-(--ease-atelier)"
            :class="[
              !isHero ? 'min-h-0 md:min-h-[calc(100vh-var(--header-height)-120px)]' : '',
              !isHero ? '[view-transition-name:project-description]' : ''
            ]"
          >
            <div class="flex-grow pb-4 md:pb-6">
              <div
                class="content-renderer will-change-[opacity,transform] transition-[opacity,transform] duration-(--duration-detail-copy) ease-(--ease-atelier-soft)"
                :class="contentReady ? 'translate-y-0 opacity-100' : 'translate-y-2 opacity-0'"
              >
                <ContentRenderer :value="project" class="prose max-w-none prose-sm md:prose-base dark:prose-invert" />
              </div>

              <!-- Metadata -->
              <dl
                v-if="projectMetadata.length"
                class="mt-8 border-t border-[#121212]/12 pt-4 will-change-[opacity,transform] transition-[opacity,transform] duration-(--duration-detail-copy) delay-100 ease-(--ease-atelier-soft) dark:border-white/12 doux:border-[#4A4443]/12 nuit:border-[#CDD6F4]/12"
                :class="contentReady ? 'translate-y-0 opacity-100' : 'translate-y-2 opacity-0'"
              >
                <div class="space-y-2">
                  <div
                    v-for="item in projectMetadata"
                    :key="item.label"
                    class="grid grid-cols-[6.5rem_1fr] gap-4 font-(family-name:--font-primary) text-[12px] font-[450] leading-[1.5] tracking-[0.07em] md:text-[13px]"
                  >
                    <dt class="text-[#121212]/60 dark:text-white/60 doux:text-[#4A4443]/62 nuit:text-[#CDD6F4]/62">{{ item.label }}</dt>
                    <dd class="min-w-0 text-[#121212]/85 dark:text-white/85 doux:text-[#4A4443]/88 nuit:text-[#CDD6F4]/88">{{ item.value }}</dd>
                  </div>
                </div>
              </dl>

              <div
                v-if="projectWorkflow"
                class="mt-6 border-t border-[#121212]/12 pt-4 will-change-[opacity,transform] transition-[opacity,transform] duration-(--duration-detail-copy) delay-200 ease-(--ease-atelier-soft) dark:border-white/12 doux:border-[#4A4443]/12 nuit:border-[#CDD6F4]/12"
                :class="contentReady ? 'translate-y-0 opacity-100' : 'translate-y-2 opacity-0'"
              >
                <div class="grid grid-cols-[6.5rem_1fr] gap-4 font-(family-name:--font-primary) text-[12px] font-[450] leading-[1.5] tracking-[0.07em] md:text-[13px]">
                  <p class="text-[#121212]/60 dark:text-white/60 doux:text-[#4A4443]/62 nuit:text-[#CDD6F4]/62">Workflow</p>
                  <p class="min-w-0 text-[#121212]/85 dark:text-white/85 doux:text-[#4A4443]/88 nuit:text-[#CDD6F4]/88">{{ projectWorkflow }}</p>
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
                class="min-h-11 border border-[#121212]/15 px-3 py-3 transition-colors duration-(--duration-hover) ease-(--ease-atelier) hover:border-[#121212]/40 dark:border-white/15 doux:border-[#4A4443]/20 nuit:border-[#CDD6F4]/20"
                @click.capture="prepareMobileProjectNavigation(mobilePrevProject.path, 'prev')"
              >
                <span class="u-legend block opacity-50">Precedent</span>
                <span class="u-h4 block truncate !tracking-normal">{{ mobilePrevProject.title }}</span>
              </NuxtLink>
              <span v-else></span>
              <NuxtLink
                v-if="mobileNextProject"
                :to="mobileNextProject.path"
                class="min-h-11 border border-[#121212]/15 px-3 py-3 text-right transition-colors duration-(--duration-hover) ease-(--ease-atelier) hover:border-[#121212]/40 dark:border-white/15 doux:border-[#4A4443]/20 nuit:border-[#CDD6F4]/20"
                @click.capture="prepareMobileProjectNavigation(mobileNextProject.path, 'next')"
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
import { ref, computed, watch, watchEffect, onMounted, onBeforeUnmount } from 'vue';
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
const { state: projectTransition, navigateBetweenProjects } = useProjectTransition();
const contentReady = ref(!import.meta.client || projectTransition.value.mode === null);
let contentRevealTimer: ReturnType<typeof setTimeout> | null = null;

const usesSharedMediaTransition = computed(() => {
  const projectPath = props.project?.path;
  if (!projectPath) return false;

  return projectTransition.value.sourceProjectPath === projectPath
    || projectTransition.value.targetProjectPath === projectPath;
});

const getMotionDuration = (name: string, fallback: number) => {
  if (!import.meta.client) return fallback;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return 0;

  const rawValue = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  const parsedValue = Number.parseFloat(rawValue);
  if (Number.isNaN(parsedValue)) return fallback;

  return rawValue.endsWith('ms') ? parsedValue : parsedValue * 1000;
};

const revealProjectContent = () => {
  if (contentRevealTimer) clearTimeout(contentRevealTimer);

  if (projectTransition.value.mode === null) {
    contentReady.value = true;
    return;
  }

  contentReady.value = false;
  contentRevealTimer = setTimeout(() => {
    contentReady.value = true;
    contentRevealTimer = null;
  }, getMotionDuration('--duration-page', 1100) * 0.62);
};

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

const formatMetadataValue = (value: unknown) => {
  if (Array.isArray(value)) return value.filter(Boolean).join(', ');
  if (typeof value === 'number') return value.toString();
  if (typeof value === 'string') return value.trim();
  return '';
};

const projectMetadata = computed(() => {
  if (!props.project) return [];

  const fields = [
    { label: 'Typologie', value: props.project.typologies },
    { label: 'Taille', value: props.project.tailles },
    { label: 'Pays', value: props.project.pays },
    { label: 'Agence', value: props.project.agence ?? props.project.meta?.agence },
    { label: 'Lieu', value: props.project.lieu },
    { label: 'Surface', value: props.project.surface },
    { label: 'Phase', value: props.project['phase réalisées'] ?? props.project.phase },
    { label: 'Statut', value: props.project.statut }
  ];

  return fields
    .map(field => ({ label: field.label, value: formatMetadataValue(field.value) }))
    .filter(field => field.value.length > 0);
});

const projectWorkflow = computed(() => {
  const fields = [props.project?.workflow, props.project?.workflows, props.project?.logiciels];
  for (const field of fields) {
    const value = formatMetadataValue(field);
    if (value.length > 0) return value;
  }
  return '';
});

watchEffect(() => {
  if (props.project) {
    setHoveredProject(props.project);
  }
});

onMounted(() => {
  if (props.project) {
    setHoveredProject(props.project);
    setCurrentImageIndex(0);
    revealProjectContent();
  }
});

watch(() => props.project?.path, () => {
  setCurrentImageIndex(0);
  revealProjectContent();
});

onBeforeUnmount(() => {
  if (contentRevealTimer) clearTimeout(contentRevealTimer);
});

const prepareMobileProjectNavigation = (targetPath: string, direction: 'next' | 'prev') => {
  if (!props.project?.path) return;
  navigateBetweenProjects(props.project.path, targetPath, direction);
};

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
