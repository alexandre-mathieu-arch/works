<template>
  <NuxtLink 
    :to="project.path" 
    class="block w-full group"
    :class="{ 'pointer-events-none': !isRevealed }"
    @mouseenter="isRevealed ? setHoveredProject(project) : null"
    @mouseleave="isRevealed ? setHoveredProject(null) : null"
    @click="isRevealed ? addVisited(project.path) : (e) => e.preventDefault()"
  >
    <div class="relative w-full aspect-square overflow-hidden" ref="parallaxRef">
      <template v-if="displayImage">
        <!-- Parallax Wrapper -->
        <div 
          class="absolute inset-0 w-full h-full transition-transform duration-700 ease-out"
          :style="getParallaxStyle(parallaxRef)"
        >
          <!-- Image with smooth zoom and grayscale -->
          <NuxtImg
            :src="displayImage"
            :alt="project.title"
            format="webp"
            width="800"
            height="800"
            class="w-full h-full object-cover transition-all duration-1000 ease-in-out scale-110 group-hover:scale-115 grayscale-[0.4] group-hover:grayscale-0"
            :style="{ 
              viewTransitionName: 'image-' + project.path.replace(/\//g, '-') 
            }"
          />
        </div>
      </template>
      <!-- Placeholder si pas d'image -->
      <div v-else class="absolute inset-0 w-full h-full bg-gray-100 dark:bg-gray-800 doux:bg-[#DED9D8] nuit:bg-[#131929] flex items-center justify-center">
        <UIcon name="i-heroicons-photo" class="w-12 h-12 text-gray-400" />
      </div>
      
      <!-- Infos affichées en permanence (avant uniquement au survol) -->
      <div v-if="isRevealed" class="absolute inset-0 z-10">
        <div class="absolute top-0 left-0 w-full border border-[#121212]/10 group-hover:border-[#121212]/30 dark:border-white/10 dark:group-hover:border-white/20 px-2 h-[30px] flex items-center gap-3 bg-white dark:bg-[#121212] doux:bg-[#E5E1E0] nuit:bg-[#1A2238] transition-all duration-700 overflow-hidden">
          <h3 
            class="u-h3 normal-case dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] whitespace-nowrap overflow-hidden text-ellipsis flex-shrink"
            :style="{ viewTransitionName: 'title-' + project.path.replace(/\//g, '-') }"
          >
            {{ project.title }}
          </h3>
          <p 
            class="text-[12px] font-light text-[#121212] dark:text-gray-300 doux:text-[#4A4443]/70 nuit:text-[#CDD6F4]/70 tracking-[0.1em] whitespace-nowrap flex-shrink-0 opacity-100 lg:opacity-0 lg:group-hover:opacity-100 transition-opacity duration-700"
            :style="{ viewTransitionName: 'year-' + project.path.replace(/\//g, '-') }"
          >
            {{ projectYear }}
          </p>
          <p 
            class="text-[12px] font-light text-[#121212] dark:text-gray-400 doux:text-[#4A4443]/60 nuit:text-[#CDD6F4]/60 tracking-[0.1em] whitespace-nowrap overflow-hidden text-ellipsis flex-shrink-0 opacity-100 lg:opacity-0 lg:group-hover:opacity-100 transition-opacity duration-700"
            :style="{ viewTransitionName: 'location-' + project.path.replace(/\//g, '-') }"
          >
            {{ formattedLocation }}
          </p>
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
const { getParallaxStyle } = useParallax(15);
const { isRevealed } = useRevealedState();

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

const formattedLocation = computed(() => {
  const parts = [];
  if (props.project.lieu) parts.push(props.project.lieu);
  if (props.project.region) parts.push(props.project.region);
  if (props.project.pays && props.project.pays.length > 0) {
    parts.push(props.project.pays.join(', '));
  }
  return parts.join(', ');
});

const projectYear = computed(() => {
  const d = props.project.date;
  if (!d) return '';
  
  if (typeof d === 'number' || (typeof d === 'string' && /^\d{4}$/.test(d))) {
    return d.toString();
  }
  
  const dateObj = new Date(d);
  if (isNaN(dateObj.getTime())) return d.toString();
  return dateObj.getFullYear().toString();
});
</script>

<style scoped>
/* Styles personnalisés si nécessaire */
</style>
