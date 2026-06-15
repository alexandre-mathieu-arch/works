<template>
  <div 
    id="wrapper" 
    :class="[
      !isRevealed ? 'h-screen overflow-hidden cursor-pointer' : '',
    ]"
    @click="!isRevealed ? reveal() : null"
  >
    <Header 
      v-if="!route.meta.hideHeader"
      :class="[isRevealed ? 'opacity-100' : 'opacity-0 pointer-events-none', 'transition-opacity duration-[1400ms] ease-[var(--motion-luxury-ease)]']"
      @linkClick="handleLinkClick" 
      @linkHover="handleLinkHover" 
    />
    
    <!-- Curtain Overlay (Top) -->
    <div 
      class="fixed inset-x-0 top-0 h-1/2 z-[60] glass-fluted transition-transform duration-[1800ms] ease-curtain pointer-events-none"
      :class="[
        isRevealed ? '-translate-y-full' : 'translate-y-0'
      ]"
      :style="!isRevealed ? { transform: `translateY(-${revealProgress * 100}%)` } : {}"
    ></div>
    <!-- Curtain Overlay (Bottom) -->
    <div 
      class="fixed inset-x-0 bottom-0 h-1/2 z-[60] glass-fluted transition-transform duration-[1800ms] ease-curtain pointer-events-none"
      :class="[
        isRevealed ? 'translate-y-full' : 'translate-y-0'
      ]"
      :style="!isRevealed ? { transform: `translateY(${revealProgress * 100}%)` } : {}"
    ></div>

    <!-- UI Overlay (Title & Info) -->
    <div 
      class="fixed inset-0 z-[70] flex flex-col items-center justify-center pointer-events-none transition-all duration-[1800ms] ease-curtain"
      :class="isRevealed ? 'opacity-0 scale-105' : 'opacity-100 scale-100'"
      :style="!isRevealed ? { opacity: 1 - revealProgress, transform: `scale(${1 + revealProgress * 0.05})` } : {}"
    >
      <!-- Centralized three-line info -->
      <div 
        class="main-container w-full flex flex-col items-center group/text"
      >
        <div class="relative border border-[#121212]/10 dark:border-white/10 px-8 py-10 md:px-16 md:py-12 flex flex-col items-center space-y-2 transition-colors duration-[1400ms] ease-[var(--motion-luxury-ease)] group-hover/text:border-[#121212]/30 dark:group-hover/text:border-white/30">
          <div class="u-h4 text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] uppercase tracking-[0.3em] group-hover/text:opacity-100 transition-opacity duration-[1200ms] ease-[var(--motion-luxury-ease)]">
            Alexandre MATHIEU
          </div>
          <span class="u-h4 text-white motion-luxury-pulse uppercase tracking-[0.5em] pt-4 group-hover/text:text-primary-900 dark:group-hover/text:text-primary-400 transition-colors duration-[1200ms] ease-[var(--motion-luxury-ease)] text-[14px] md:text-[16px]">works</span>
          <svg 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="1.5" 
            class="w-5 h-5 text-white group-hover/text:text-primary-900 dark:group-hover/text:text-primary-400 transition-colors duration-[1200ms] ease-[var(--motion-luxury-ease)] motion-luxury-drift mt-2 opacity-60"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
          </svg>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div 
      class="transition-all duration-[1400ms] ease-[var(--motion-luxury-ease)]"
      :class="[!isRevealed ? 'h-screen overflow-hidden' : 'min-h-screen']"
    >
      <main class="pb-12 main-container" :style="{ paddingTop: 'var(--header-height)' }">
        <PageTitle 
          v-if="!route.meta.hideLayoutTitle"
          :class="[isRevealed ? 'opacity-100' : 'opacity-0 pointer-events-none', 'transition-opacity duration-[1400ms] ease-[var(--motion-luxury-ease)]']"
          :title="pageTitle" 
          :show-filters="route.meta.showFilters === true" 
          :readonly-filters="route.meta.readonlyFilters === true"
        />
        <div :class="[isRevealed ? 'opacity-100' : 'opacity-0 pointer-events-none', 'transition-opacity duration-[1400ms] ease-[var(--motion-luxury-ease)] delay-300']">
          <slot />
        </div>
      </main>
      <TheFooter :class="[isRevealed ? 'opacity-100' : 'opacity-0 pointer-events-none', 'transition-opacity duration-[1400ms] ease-[var(--motion-luxury-ease)]']" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { useRevealedState } from '~/composables/useRevealedState';

const { isRevealed, reveal, resetReveal } = useRevealedState();
const route = useRoute();
const router = useRouter();
const hoveredTitle = ref<string | object>('');
const clickedTitle = ref<string | object>('');
const revealProgress = ref(0);
let autoRevealTimer: any = null;

const triggerReveal = () => {
  reveal();
  if (route.path === '/') {
    router.push({ path: '/', query: { view: 'grid' } });
  }
};

const handleScroll = (e: WheelEvent) => {
  if (isRevealed.value) return;

  // Sensitivity adjustment
  revealProgress.value += e.deltaY * 0.001;
  revealProgress.value = Math.max(0, Math.min(1, revealProgress.value));

  if (revealProgress.value >= 0.8) {
    triggerReveal();
    window.removeEventListener('wheel', handleScroll);
  }
};

onMounted(() => {
  // Always reset on home page entry
  resetReveal();
  revealProgress.value = 0;

  if (!isRevealed.value) {
    window.addEventListener('wheel', handleScroll, { passive: true });
    
    autoRevealTimer = setTimeout(() => {
      if (!isRevealed.value) triggerReveal();
    }, 5000);
  }
});

onUnmounted(() => {
  window.removeEventListener('wheel', handleScroll);
  if (autoRevealTimer) clearTimeout(autoRevealTimer);
});

// Reset titles on route change
watch(() => route.fullPath, () => {
  clickedTitle.value = '';
  hoveredTitle.value = '';
}, { immediate: true });

const handleLinkHover = (title: string) => {
  hoveredTitle.value = title;
};

const handleLinkClick = (title: string) => {
  clickedTitle.value = title;
  hoveredTitle.value = title; 
};

const pageTitle = computed(() => {
  // Priority: hover, then click, then static meta
  if (hoveredTitle.value) {
    return hoveredTitle.value;
  }
  if (clickedTitle.value) {
    return clickedTitle.value;
  }
  if (route.meta.displayTitle) {
    return route.meta.displayTitle;
  }
  return '';
});
</script>
