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
         <UIcon name="i-heroicons-photo" class="w-12 h-12 text-gray-300 motion-luxury-pulse" />
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
  inset: 0;
  position: absolute;
  transition:
    transform 1.45s var(--motion-luxury-ease),
    opacity 1.45s var(--motion-luxury-ease);
  will-change: transform, opacity;
}

.slide-left-enter-from {
  opacity: 0.98;
  transform: translate3d(100%, 0, 0);
}
.slide-left-enter-to,
.slide-left-leave-from,
.slide-right-enter-to,
.slide-right-leave-from {
  opacity: 1;
  transform: translate3d(0, 0, 0);
}
.slide-left-leave-to {
  opacity: 0.98;
  transform: translate3d(-100%, 0, 0);
}

.slide-right-enter-from {
  opacity: 0.98;
  transform: translate3d(-100%, 0, 0);
}
.slide-right-leave-to {
  opacity: 0.98;
  transform: translate3d(100%, 0, 0);
}

/* Custom cursors using inline SVGs */
.cursor-left {
  cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='15 18 9 12 15 6'%3E%3C/polyline%3E%3C/svg%3E") 16 16, auto;
}

.cursor-right {
  cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='9 18 15 12 9 6'%3E%3C/polyline%3E%3C/svg%3E") 16 16, auto;
}
</style>
