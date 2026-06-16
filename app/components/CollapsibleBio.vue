<template>
  <div class="collapsible-bio mb-[10px]">
    <button 
      @click="toggleLocal" 
      class="u-h3 flex items-center gap-4 text-left hover:text-primary-900 transition-colors duration-(--duration-hover) ease-(--ease-atelier) w-full group tracking-widest"
    >
      <span>{{ name }}</span>
      <svg 
        viewBox="0 0 20 20" 
        fill="currentColor" 
        class="w-5 h-5 transform transition-transform duration-(--duration-menu) ease-(--ease-atelier)"
        :class="{ 'rotate-180': isOpen }"
      >
        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
      </svg>
    </button>
    
    <div 
      class="grid transition-all duration-(--duration-menu) ease-(--ease-atelier)"
      :class="isOpen ? 'grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-0'"
    >
      <div class="overflow-hidden">
        <div class="pt-1 pb-1 prose dark:prose-invert max-w-none">
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useAgenceState } from '~/composables/useAgenceState'

const props = defineProps<{
  name: string,
  slug?: string
}>()

const { activeSections, isSectionActive } = useAgenceState()
const isOpen = ref(false)

const toggleLocal = () => {
  isOpen.value = !isOpen.value
}

// Sync with global state if slug is provided
if (props.slug) {
  watch(activeSections, () => {
    isOpen.value = isSectionActive(props.slug!)
  }, { immediate: true })
}
</script>

<style scoped>
.collapsible-bio button {
  cursor: pointer;
  border: none;
  background: none;
  padding: 0;
}
</style>
