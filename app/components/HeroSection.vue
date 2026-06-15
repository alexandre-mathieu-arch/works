<template>
  <section 
    class="relative h-screen w-full flex flex-col items-center justify-center overflow-hidden"
  >
    <!-- Hero Content -->
    <div 
      class="main-container w-full flex flex-col items-center group/text transition-all duration-1000"
      :style="{ 
        opacity: 1 - scrollProgress * 2,
        transform: `translateY(${-scrollProgress * 100}px) scale(${1 + scrollProgress * 0.05})`
      }"
    >
      <div 
        @click="$emit('scroll-to-projects')"
        class="relative px-8 py-10 md:px-16 md:py-12 flex flex-col items-center space-y-2 transition-colors duration-1000 cursor-pointer"
      >
        <div class="u-h4 text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] tracking-[0.3em] group-hover/text:opacity-100 transition-opacity">
          Alexandre MATHIEU
        </div>
        <span class="u-h4 text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] opacity-40 animate-pulse uppercase tracking-[0.5em] pt-4 group-hover/text:text-primary-900 dark:group-hover/text:text-primary-400 group-hover/text:opacity-100 transition-all duration-700 text-[14px] md:text-[16px]">projets</span>
        <svg 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          stroke-width="1.5" 
          class="w-5 h-5 text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] opacity-40 group-hover/text:opacity-100 transition-all duration-700 animate-bounce mt-2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
        </svg>
      </div>
    </div>

    <!-- Scroll Indicator -->
    <div 
      @click="$emit('scroll-to-projects')"
      class="absolute bottom-10 left-1/2 -translate-x-1/2 transition-opacity duration-500 cursor-pointer group/scroll"
      :style="{ opacity: 1 - scrollProgress * 5 }"
    >
      <div class="w-px h-12 bg-gradient-to-b from-transparent via-[#121212]/20 dark:via-white/20 to-transparent animate-bounce group-hover/scroll:via-[#121212]/40 dark:group-hover/scroll:via-white/40"></div>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  scrollProgress: number;
}>();

defineEmits<{
  (e: 'scroll-to-projects'): void;
}>();
</script>

<style scoped>
@reference "../assets/css/main.css";
</style>
