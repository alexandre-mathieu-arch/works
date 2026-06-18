<template>
  <NuxtLink 
    :to="project.path" 
    class="block w-full group/card"
    :class="{ 'pointer-events-none': !isRevealed }"
    @pointerenter="handleProjectPointerEnter"
    @pointerleave="handleProjectPointerLeave"
    @focus="handleProjectFocus"
    @blur="handleProjectBlur"
    @click.capture="handleProjectClick"
  >
    <div class="relative w-full aspect-square overflow-hidden" ref="parallaxRef">
      <template v-if="displayImage">
        <div
          data-project-media
          class="absolute inset-0 overflow-hidden"
          :class="{ '[view-transition-name:project-media]': isTransitionTarget }"
        >
          <!-- Parallax Wrapper -->
          <div
            class="absolute inset-0 w-full h-full"
            :style="getParallaxStyle(parallaxRef)"
          >
            <!-- Image with smooth zoom and grayscale -->
            <div class="h-full w-full origin-center will-change-transform [transform:translate3d(0,0,0)_scale(1)] transition-transform duration-(--duration-zoom-card) ![transition-duration:var(--duration-zoom-card)] ease-(--ease-atelier-soft) group-hover/card:[transform:translate3d(0,0,0)_scale(1.14)]">
              <NuxtImg
                :src="displayImage"
                :alt="project.title"
                format="webp"
                width="800"
                height="800"
                class="w-full h-full object-cover grayscale-[0.28] transition-[filter] duration-(--duration-zoom-card) ![transition-duration:var(--duration-zoom-card)] ease-(--ease-atelier-soft) group-hover/card:grayscale-0"
              />
            </div>
          </div>
        </div>
      </template>
      <!-- Placeholder si pas d'image -->
      <div v-else class="absolute inset-0 w-full h-full bg-gray-100 dark:bg-gray-800 doux:bg-[#DED9D8] nuit:bg-[#131929] flex items-center justify-center">
        <UIcon name="i-heroicons-photo" class="w-12 h-12 text-gray-400" />
      </div>
      
      <!-- Infos affichees en permanence -->
      <div v-if="isRevealed" class="absolute inset-0 z-10">
        <div class="absolute top-0 left-0 w-full border border-[#121212]/10 group-hover/card:border-[#121212]/30 dark:border-white/10 dark:group-hover/card:border-white/20 px-2 h-[30px] flex items-center bg-white dark:bg-[#121212] doux:bg-[#E5E1E0] nuit:bg-[#1A2238] transition-colors duration-(--duration-menu) ease-(--ease-atelier) overflow-hidden">
          <h3 
            class="u-h3 normal-case dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] whitespace-nowrap overflow-hidden text-ellipsis flex-shrink"
          >
            {{ project.title }}
          </h3>
        </div>
      </div>
    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useVisitedProjects } from '~/composables/useVisitedProjects';
import { useHoverProject } from '~/composables/useHoverProject';
import { useParallax } from '~/composables/useParallax';
import { useRevealedState } from '~/composables/useRevealedState';

const { setHoveredProject } = useHoverProject();
const { addVisited } = useVisitedProjects();
const { getParallaxStyle } = useParallax(10);
const { isRevealed } = useRevealedState();
const { state: projectTransition, openProject } = useProjectTransition();
const SHARED_MEDIA_CLASS = '[view-transition-name:project-media]';

const parallaxRef = ref<HTMLElement | null>(null);

const props = defineProps<{
  project: {
    path: string;
    title: string;
    description: string;
    thumbnail?: string;
    image?: string;
    images?: string[];
    tags?: string[];
    typologies?: string[];
    tailles?: string[];
    pays?: string[];
    lieu?: string;
    region?: string;
    date?: string | number | Date;
    ratio?: string;
  };
}>();

const displayImage = computed(() => {
  if (props.project.thumbnail) {
    const thumb = props.project.thumbnail;
    return thumb.startsWith('/') ? thumb : '/' + thumb;
  }

  let imagePath: string | undefined;
  if (props.project.images && Array.isArray(props.project.images)) {
    imagePath = props.project.images.find(img => typeof img === 'string' && img.length > 0);
  }
  
  if (!imagePath) {
    imagePath = props.project.image;
  }
  
  if (imagePath && typeof imagePath === 'string' && !imagePath.startsWith('/')) {
    return '/' + imagePath;
  }
  return imagePath;
});

const isTransitionTarget = computed(() => {
  return projectTransition.value.targetProjectPath === props.project.path;
});

const handleProjectClick = (event: MouseEvent) => {
  if (!isRevealed.value) {
    event.preventDefault();
    event.stopPropagation();
    return;
  }

  document.querySelectorAll<HTMLElement>('[data-project-media]').forEach(element => {
    element.classList.remove(SHARED_MEDIA_CLASS);
  });
  const selectedMedia = (event.currentTarget as HTMLElement)
    .querySelector<HTMLElement>('[data-project-media]');
  selectedMedia?.classList.add(SHARED_MEDIA_CLASS);

  openProject(props.project.path);
  addVisited(props.project.path);
};

const canUseFineHover = () => {
  if (!import.meta.client) return false;

  return window.matchMedia('(hover: hover) and (pointer: fine)').matches;
};

const handleProjectPointerEnter = () => {
  if (!isRevealed.value || !canUseFineHover()) return;

  setHoveredProject(props.project);
};

const handleProjectPointerLeave = () => {
  if (!canUseFineHover()) return;

  setHoveredProject(null);
};

const handleProjectFocus = () => {
  if (!isRevealed.value) return;

  setHoveredProject(props.project);
};

const handleProjectBlur = () => {
  setHoveredProject(null);
};
</script>
