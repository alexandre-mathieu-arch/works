<template>
  <div
    class="carousel-container group relative w-full h-full overflow-hidden"
    @touchstart.passive="handleTouchStart"
    @touchend.passive="handleTouchEnd"
  >
    <Transition :name="transitionName">
      <NuxtImg
        v-if="images && images.length > 0 && images[currentIndex]"
        :key="currentIndex"
        :src="images[currentIndex]"
        :alt="alt || `Image ${currentIndex + 1}`"
        format="webp"
        width="1600"
        height="900"
        class="w-full h-full object-contain absolute inset-0"
        :style="id && currentIndex === 0 ? { viewTransitionName: 'image-' + id.replace(/\//g, '-') } : {}"
      />
      <div v-else-if="images && images.length > 0" class="w-full h-full flex items-center justify-center bg-transparent">
         <UIcon name="i-heroicons-photo" class="w-12 h-12 text-gray-300 animate-pulse" />
      </div>
    </Transition>

    <!-- Hidden images for the crawler to ensure all images are prerendered -->
    <div class="hidden" aria-hidden="true">
      <NuxtImg
        v-for="img in images"
        :key="'preload-' + img"
        :src="img"
        format="webp"
        width="1600"
        height="900"
      />
    </div>

    <!-- Invisible Click Areas for Navigation -->
    <div class="absolute inset-0 hidden md:flex" aria-hidden="true">
      <div
        class="w-1/2 h-full z-10 cursor-left"
        @click="prev"
        title="Précédent"
      ></div>
      <div
        class="w-1/2 h-full z-10 cursor-right"
        @click="next"
        title="Suivant"
      ></div>
    </div>

    <div class="absolute inset-x-0 top-1/2 z-20 flex -translate-y-1/2 justify-between px-3 pointer-events-none">
      <button
        type="button"
        class="pointer-events-auto flex h-11 w-11 items-center justify-center border border-[#121212]/20 bg-white/80 text-[#121212] transition-all duration-300 hover:border-[#121212]/50 dark:border-white/20 dark:bg-[#121212]/80 dark:text-white doux:bg-[#E5E1E0]/85 nuit:bg-[#1A2238]/85 md:opacity-0 md:group-hover:opacity-100"
        :class="{ 'opacity-30 cursor-default': !canGoPrev }"
        :disabled="!canGoPrev"
        aria-label="Image precedente"
        @click="prev"
      >
        <span aria-hidden="true">&lt;</span>
      </button>
      <button
        type="button"
        class="pointer-events-auto flex h-11 w-11 items-center justify-center border border-[#121212]/20 bg-white/80 text-[#121212] transition-all duration-300 hover:border-[#121212]/50 dark:border-white/20 dark:bg-[#121212]/80 dark:text-white doux:bg-[#E5E1E0]/85 nuit:bg-[#1A2238]/85 md:opacity-0 md:group-hover:opacity-100"
        :class="{ 'opacity-30 cursor-default': !canGoNext }"
        :disabled="!canGoNext"
        aria-label="Image suivante"
        @click="next"
      >
        <span aria-hidden="true">&gt;</span>
      </button>
    </div>

    <div
      v-if="images.length > 1"
      class="absolute bottom-3 right-3 z-20 border border-[#121212]/15 bg-white/80 px-2 py-1 u-legend text-[#121212] dark:border-white/15 dark:bg-[#121212]/80 dark:text-white doux:bg-[#E5E1E0]/85 nuit:bg-[#1A2238]/85"
      aria-live="polite"
    >
      {{ currentIndex + 1 }} / {{ images.length }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';

const props = defineProps<{
  images: string[]
  modelValue: number
  autoplay?: number
  id?: string
  alt?: string
}>()

const emit = defineEmits(['update:modelValue'])

const transitionName = ref('slide-left');

const currentIndex = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const canGoPrev = computed(() => currentIndex.value > 0);
const canGoNext = computed(() => currentIndex.value < props.images.length - 1);

const next = () => {
  if (canGoNext.value) {
    transitionName.value = 'slide-left';
    currentIndex.value++;
  }
}

const prev = () => {
  if (canGoPrev.value) {
    transitionName.value = 'slide-right';
    currentIndex.value--;
  }
}

const touchStartX = ref<number | null>(null);

const handleTouchStart = (event: TouchEvent) => {
  touchStartX.value = event.changedTouches[0]?.clientX ?? null;
};

const handleTouchEnd = (event: TouchEvent) => {
  if (touchStartX.value === null) return;
  const endX = event.changedTouches[0]?.clientX ?? touchStartX.value;
  const delta = endX - touchStartX.value;
  touchStartX.value = null;

  if (Math.abs(delta) < 48) return;
  if (delta < 0) next();
  else prev();
};

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'ArrowRight') next();
  if (e.key === 'ArrowLeft') prev();
}

let intervalId: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  window.addEventListener('keydown', handleKeydown);
  if (props.autoplay) {
    intervalId = setInterval(next, props.autoplay)
  }
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown);
  if (intervalId) {
    clearInterval(intervalId)
  }
})
</script>

<style scoped>
.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-left-enter-from {
  transform: translateX(100%);
}
.slide-left-leave-to {
  transform: translateX(-100%);
}

.slide-right-enter-from {
  transform: translateX(-100%);
}
.slide-right-leave-to {
  transform: translateX(100%);
}

/* Custom cursors using inline SVGs */
.cursor-left {
  cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='15 18 9 12 15 6'%3E%3C/polyline%3E%3C/svg%3E") 16 16, auto;
}

.cursor-right {
  cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='9 18 15 12 9 6'%3E%3C/polyline%3E%3C/svg%3E") 16 16, auto;
}
</style>
