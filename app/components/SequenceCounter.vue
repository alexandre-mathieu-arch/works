<template>
  <div class="sequence-navigation flex items-center min-h-11 md:h-[30px] md:min-h-0 border border-[#121212]/30 dark:border-white/20 bg-white/50 dark:bg-white/5 -mt-[1px] overflow-x-auto whitespace-nowrap scrollbar-hide">
    <!-- Previous Project Button -->
    <NuxtLink 
      v-if="prevProject" 
      :to="prevProject.path" 
      class="u-h4 h-full px-3 flex-shrink-0 flex items-center justify-center border-r border-[#121212]/10 dark:border-white/10 atelier-hover-surface text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4]"
      @click="$emit('nav', 'prev')"
      aria-label="Projet precedent"
    >
      &lt;
    </NuxtLink>
    <span v-else class="u-h4 h-full px-3 flex-shrink-0 flex items-center justify-center border-r border-[#121212]/10 dark:border-white/10 text-gray-300 dark:text-gray-600 cursor-default">&lt;</span>

    <!-- Image Counter Buttons -->
    <button
      v-for="index in total"
      :key="index"
      @click="$emit('update:modelValue', index - 1)"
      class="u-h4 h-full px-2 sm:px-3 flex-shrink-0 flex items-center justify-center transition-[color,background-color,opacity] duration-(--duration-hover) ease-(--ease-atelier) border-r border-[#121212]/10 dark:border-white/10 bg-transparent"
      :aria-label="`Afficher l'image ${index}`"
      :class="[
        modelValue === index - 1 
          ? 'font-bold text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] opacity-100' 
          : 'font-normal text-[#121212]/20 dark:text-white/20 doux:text-[#4A4443]/20 nuit:text-[#CDD6F4]/20 hover:text-[#121212] dark:hover:text-white doux:hover:text-[#4A4443] nuit:hover:text-[#CDD6F4] hover:opacity-100 hover:bg-[#121212]/5 dark:hover:bg-white/5 doux:hover:bg-[#4A4443]/5 nuit:hover:bg-[#CDD6F4]/5'
      ]"
    >
      {{ index }}
    </button>

    <!-- Next Project Button -->
    <NuxtLink 
      v-if="nextProject" 
      :to="nextProject.path" 
      class="u-h4 h-full px-3 flex-shrink-0 flex items-center justify-center atelier-hover-surface text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4]"
      @click="$emit('nav', 'next')"
      title="Projet suivant"
      aria-label="Projet suivant"
    >
      &gt;
    </NuxtLink>
    <span v-else class="u-h4 h-full px-3 flex-shrink-0 flex items-center justify-center text-gray-300 dark:text-gray-600 cursor-default">&gt;</span>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: number;
  total: number;
  prevProject?: any;
  nextProject?: any;
}>();

defineEmits(['update:modelValue', 'nav']);
</script>

<style scoped>
.sequence-navigation {
  user-select: none;
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.sequence-navigation::-webkit-scrollbar {
  display: none;
}
</style>
