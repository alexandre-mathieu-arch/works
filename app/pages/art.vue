<template>
  <div class="pt-8 pb-40 relative">
    <div v-if="filteredArt?.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 md:gap-12">
      <div 
        v-for="(item, index) in filteredArt" 
        :key="item.path"
        class="flex flex-col group transition-all duration-1000"
      >
        <div 
          class="relative overflow-hidden cursor-zoom-in transition-all duration-700 rounded-none bg-gray-50 dark:bg-gray-900 flex items-center justify-center min-h-[200px]"
          @click="selectedImage = item"
        >
          <img
            v-if="item.image"
            :src="formatImagePath(item.image)"
            :alt="item.title"
            class="w-full h-auto transition-transform duration-[1.5s] ease-out rounded-none"
            @error="(e) => console.error('Image load error:', formatImagePath(item.image))"
          />
          <div v-else class="flex flex-col items-center gap-2 opacity-20">
            <UIcon name="i-heroicons-photo" class="w-10 h-10" />
            <span class="u-legend">{{ item.title }}</span>
          </div>
          <!-- Subtle overlay for texture -->
          <div class="absolute inset-0 opacity-0 group-hover:opacity-10 dark:bg-white bg-black transition-opacity duration-700 pointer-events-none"></div>
        </div>
        
        <!-- Sober Legend -->
        <div class="mt-4 flex flex-col space-y-0.5 opacity-80 group-hover:opacity-100 transition-opacity duration-500">
          <span class="u-h4 font-medium tracking-wider text-[#121212] dark:text-white">{{ item.title }}</span>
          <p v-if="item.description" class="u-legend font-normal opacity-50 max-w-[300px] leading-tight">
            {{ item.description }}
          </p>
        </div>
      </div>
    </div>
    
    <div v-else class="text-center py-20">
      <p class="u-body opacity-60 italic">La section Art est en cours de chargement ou sera bientôt disponible...</p>
      <div v-if="allContentItems?.length" class="mt-4 text-[10px] opacity-20">
        {{ allContentItems.length }} items total en base
      </div>
    </div>

    <!-- Exhibition Lightbox -->
    <Transition
      enter-active-class="transition duration-500 ease-curtain"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition duration-400 ease-curtain"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div 
        v-if="selectedImage" 
        class="fixed inset-0 z-[100] bg-white/95 dark:bg-[#121212]/95 backdrop-blur-md flex items-center justify-center p-6 md:p-16 cursor-zoom-out"
        @click="selectedImage = null"
      >
        <div class="relative w-full h-full flex flex-col items-center justify-center">
          <img
            :src="formatImagePath(selectedImage.image)"
            :alt="selectedImage.title"
            class="max-w-full max-h-[85vh] object-contain rounded-none"
          />
          
          <div class="mt-12 text-center max-w-2xl">
            <h3 class="u-h2 uppercase tracking-[0.4em] mb-4">{{ selectedImage.title }}</h3>
            <p v-if="selectedImage.description" class="u-body italic opacity-70">
              {{ selectedImage.description }}
            </p>
          </div>
        </div>
        
        <!-- Close button (minimal) -->
        <button class="absolute top-8 right-8 u-h4 opacity-40 hover:opacity-100 transition-opacity">FERMER</button>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'

const selectedImage = ref<any>(null)

const formatImagePath = (path: string) => {
  if (!path) return ''
  if (path.startsWith('http')) return path
  
  // Try relative path (no leading slash)
  // If we are at /works/art, images/art/vague.jpg resolves to /works/images/art/vague.jpg
  return path.startsWith('/') ? path.slice(1) : path
}

// Robust data fetching for Art section
const { data: allContentItems } = await useAsyncData('all-content-for-art-v3', () => {
  return queryCollection('content').all()
})

const filteredArt = computed(() => {
  if (!allContentItems.value) return []
  // Match any path that contains 'art/' to be safe with different indexing styles
  return allContentItems.value
    .filter(item => item.path && item.path.toLowerCase().includes('art/'))
    .filter(item => !item.draft)
    .sort((a, b) => (a.order || 999) - (b.order || 999))
})

definePageMeta({
  layout: 'default',
  displayTitle: 'Art'
})

useHead({
  title: 'Art — Alexandre Mathieu'
})

useSeoMeta({
  description: "Dessins, croquis, aquarelles et recherches graphiques d'Alexandre Mathieu.",
  ogTitle: 'Art - Alexandre Mathieu',
  ogDescription: "Dessins, croquis, aquarelles et recherches graphiques d'Alexandre Mathieu."
})

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') selectedImage.value = null
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
/* Studio wall layout styles */
</style>
