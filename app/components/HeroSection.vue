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
        class="relative px-8 py-10 md:px-16 md:py-12 flex flex-col items-center space-y-2 transition-colors duration-1000"
      >
        <div class="u-h4 text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] tracking-[0.3em] group-hover/text:opacity-100 transition-opacity">
          Alexandre MATHIEU
        </div>
        <p class="u-body max-w-[34rem] pt-4 text-center opacity-70">
          Architecture, design, rehabilitation et recherche constructive.
        </p>
        <div class="flex flex-col sm:flex-row items-center gap-3 pt-5">
          <button
            type="button"
            class="u-h4 min-h-11 border border-[#121212]/25 px-5 py-3 text-[#121212] transition-all duration-500 hover:border-[#121212] hover:bg-[#121212] hover:text-white dark:border-white/25 dark:text-white dark:hover:bg-white dark:hover:text-[#121212] doux:text-[#4A4443] nuit:text-[#CDD6F4]"
            @click="$emit('scroll-to-projects')"
          >
            Voir les projets
          </button>
          <button
            type="button"
            class="u-h4 min-h-11 px-5 py-3 text-[#121212]/60 transition-colors duration-500 hover:text-[#121212] dark:text-white/60 dark:hover:text-white doux:text-[#4A4443]/70 nuit:text-[#CDD6F4]/70"
            @click="$emit('scroll-to-contact')"
          >
            Contact
          </button>
        </div>
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
  (e: 'scroll-to-contact'): void;
}>();
</script>

<style scoped>
@reference "../assets/css/main.css";
</style>
