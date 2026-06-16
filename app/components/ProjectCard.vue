<template>
  <NuxtLink 
    :to="project.path" 
    class="block w-full group/card"
    :class="{ 'pointer-events-none': !isRevealed }"
    @mouseenter="isRevealed ? setHoveredProject(project) : null"
    @mouseleave="isRevealed ? setHoveredProject(null) : null"
    @click="isRevealed ? addVisited(project.path) : (e) => e.preventDefault()"
  >
    <div class="relative w-full aspect-square overflow-hidden" ref="parallaxRef">
      <template v-if="displayImage">
        <!-- Parallax Wrapper -->
        <div 
          class="absolute inset-0 w-full h-full transition-transform duration-(--duration-image) ease-(--ease-atelier-soft)"
          :style="getParallaxStyle(parallaxRef)"
        >
          <!-- Image with smooth zoom and grayscale -->
          <NuxtImg
            :src="displayImage"
            :alt="project.title"
            format="webp"
            width="800"
            height="800"
            class="w-full h-full object-cover transition-[transform,filter] duration-(--duration-image) ease-(--ease-atelier-soft) scale-[1.035] group-hover/card:scale-[1.12] grayscale-[0.28] group-hover/card:grayscale-0"
          />
        </div>
      </template>
      <!-- Placeholder si pas d'image -->
      <div v-else class="absolute inset-0 w-full h-full bg-gray-100 dark:bg-gray-800 doux:bg-[#DED9D8] nuit:bg-[#131929] flex items-center justify-center">
        <UIcon name="i-heroicons-photo" class="w-12 h-12 text-gray-400" />
      </div>
      
      <!-- Infos affichees en permanence avec detail editorial au survol -->
      <div v-if="isRevealed" class="absolute inset-0 z-10">
        <div class="absolute top-0 left-0 w-full border border-[#121212]/10 group-hover/card:border-[#121212]/30 dark:border-white/10 dark:group-hover/card:border-white/20 px-2 h-[30px] flex items-center bg-white dark:bg-[#121212] doux:bg-[#E5E1E0] nuit:bg-[#1A2238] transition-colors duration-(--duration-menu) ease-(--ease-atelier) overflow-hidden">
          <h3 
            class="u-h3 normal-case dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] whitespace-nowrap overflow-hidden text-ellipsis flex-shrink"
          >
            {{ project.title }}
          </h3>
        </div>
        <div class="absolute inset-x-0 bottom-0 pointer-events-none px-3 pb-3 pt-10 bg-gradient-to-t from-white/90 via-white/55 to-transparent dark:from-[#121212]/92 dark:via-[#121212]/55 doux:from-[#E5E1E0]/92 doux:via-[#E5E1E0]/55 nuit:from-[#1A2238]/94 nuit:via-[#1A2238]/58 opacity-100 translate-y-0 lg:opacity-0 lg:translate-y-3 lg:group-hover/card:opacity-100 lg:group-hover/card:translate-y-0 transition-[opacity,transform] duration-(--duration-card-copy) ease-(--ease-atelier-soft)">
          <p 
            class="u-legend text-[#121212]/70 dark:text-white/70 doux:text-[#4A4443]/70 nuit:text-[#CDD6F4]/70"
          >
            {{ projectYear }}
          </p>
          <p
            class="mt-1 max-w-[92%] line-clamp-3 text-[12px] leading-[1.35] font-normal tracking-[0.04em] text-[#121212]/82 dark:text-white/78 doux:text-[#4A4443]/82 nuit:text-[#CDD6F4]/82"
          >
            {{ projectTeaser }}
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
const { getParallaxStyle } = useParallax(10);
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

const normalizeCardText = (text: string, maxLength = 150) => {
  const normalized = text.replace(/\s+/g, ' ').trim();
  if (normalized.length <= maxLength) return normalized;

  const truncated = normalized.slice(0, maxLength).replace(/[\s,;:.-]+$/, '');
  return `${truncated}...`;
};

const projectTeaser = computed(() => {
  if (props.project.description) {
    return normalizeCardText(props.project.description);
  }

  return formattedLocation.value;
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
