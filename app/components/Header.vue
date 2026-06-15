<template>
  <header 
    class="fixed top-0 left-0 right-0 z-50 glass-fluted transition-all duration-[1500ms] ease-in-out"
    :class="[
      transparent ? 'opacity-0 -translate-y-4 pointer-events-none' : 'opacity-100 translate-y-0'
    ]"
  >
    <div class="main-container h-[var(--header-height)] flex items-center gap-[20px] relative">
      <!-- Logo -->
      <NuxtLink 
        :to="projectsLinkTarget" 
        class="text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] whitespace-nowrap u-h4 logo-link px-2 py-1 transition-all duration-500 hover:bg-[#121212] dark:hover:bg-white doux:hover:bg-[#4A4443] nuit:hover:bg-[#CDD6F4] hover:!text-white dark:hover:!text-[#121212] doux:hover:!text-[#E5E1E0] nuit:hover:!text-[#1A2238]"
        @click.prevent="handleProjectsClick"
        @mouseenter="emit('linkHover', 'Projets')"
        @mouseleave="emit('linkHover', '')"
      >
        Alexandre MATHIEU
      </NuxtLink>

      <!-- Desktop Navigation -->
      <nav class="hidden md:flex items-center ml-10 flex-grow group/nav">
        <div class="flex items-center gap-[30px]">
          <NuxtLink 
            v-for="link in links" 
            :key="link.to" 
            :to="link.to === '/' ? projectsLinkTarget : link.to"
            class="u-h4 transition-all duration-500 px-2 py-1 text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] hover:bg-[#121212] dark:hover:bg-white doux:hover:bg-[#4A4443] nuit:hover:bg-[#CDD6F4] hover:!text-white dark:hover:!text-[#121212] doux:hover:!text-[#E5E1E0] nuit:hover:!text-[#1A2238] relative flex flex-col items-center group/link"
            :class="[
              (link.to === '/' ? route.path === '/' : route.path.startsWith(link.to)) ? 'is-active' : 'group-hover/nav:opacity-50 hover:!opacity-100'
            ]"
            @click="handleDesktopLinkClick(link, $event)"
            @mouseenter="emit('linkHover', link.label)"
            @mouseleave="emit('linkHover', '')"
          >
            {{ link.label }}
            <!-- Active Dot -->
            <span 
              class="absolute -bottom-1 w-1 h-1 rounded-full bg-current transition-all duration-500 scale-0"
              :class="{ 'scale-100': (link.to === '/' ? route.path === '/' : route.path.startsWith(link.to)) }"
            ></span>
          </NuxtLink>
        </div>
      </nav>

      <!-- Large Space -->
      <div class="flex-grow"></div>

      <!-- Desktop Search Bar & Theme Toggle -->
      <div class="hidden md:flex items-center gap-[20px]">
        <!-- Theme Toggle -->
        <button 
          type="button"
          @click="cycleTheme" 
          class="p-2 text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] transition-all duration-500 flex items-center justify-center hover:bg-[#121212] dark:hover:bg-white doux:hover:bg-[#4A4443] nuit:hover:bg-[#CDD6F4] hover:!text-white dark:hover:!text-[#121212] doux:hover:!text-[#E5E1E0] nuit:hover:!text-[#1A2238]"
          :title="themeTitle"
          :aria-label="themeTitle"
        >
          <!-- Light: Empty Circle -->
          <svg v-if="colorMode.preference === 'light'" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="9" />
          </svg>
          <!-- Dark: Half-filled Circle -->
          <svg v-else-if="colorMode.preference === 'dark'" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="9" />
            <path d="M12 3v18c4.97 0 9-4.03 9-9s-4.03-9-9-9z" fill="currentColor" />
          </svg>
          <!-- Doux: Small Dot in Circle -->
          <svg v-else-if="colorMode.preference === 'doux'" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="9" />
            <circle cx="12" cy="12" r="3" fill="currentColor" />
          </svg>
          <!-- Nuit: Filled Circle -->
          <svg v-else-if="colorMode.preference === 'nuit'" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="9" fill="currentColor" />
          </svg>
        </button>

        <!-- Search Bar -->
        <div class="flex items-center relative">
          <div 
            class="flex items-center transition-all duration-700 ease-in-out overflow-hidden"
            :class="isSearchExpanded ? 'w-64 opacity-100' : 'w-0 opacity-0'"
          >
            <UInput 
              ref="searchInput"
              v-model="searchTerm" 
              id="site-search"
              placeholder="Rechercher..." 
              icon="i-heroicons-magnifying-glass-20-solid" 
              class="header-search-input text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4]"
              color="[#121212]"
              variant="none"
              size="md"
              @blur="handleSearchBlur"
            />
          </div>
          <button 
            v-if="!isSearchExpanded"
            type="button"
            @click="isSearchExpanded = true"
            class="p-2 text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] hover:bg-[#121212] dark:hover:bg-white doux:hover:bg-[#4A4443] nuit:hover:bg-[#CDD6F4] hover:!text-white dark:hover:!text-[#121212] doux:hover:!text-[#E5E1E0] nuit:hover:!text-[#1A2238] transition-all duration-500 flex items-center justify-center"
            aria-label="Ouvrir la recherche"
            :aria-expanded="isSearchExpanded"
            aria-controls="site-search"
          >
            <UIcon name="i-heroicons-magnifying-glass-20-solid" class="w-5 h-5" />
          </button>

          <!-- Search Results Dropdown -->
          <div 
            v-if="isSearchExpanded && searchTerm && searchResults.length > 0" 
            class="absolute top-full mt-2 right-0 w-64 glass-fluted bg-white/70 dark:bg-[#121212]/70 border border-gray-100 dark:border-gray-800 shadow-xl z-[100] max-h-80 overflow-y-auto"
          >
            <NuxtLink 
              v-for="result in searchResults" 
              :key="result.path" 
              :to="result.path"
              class="block px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-900 border-b border-gray-50 dark:border-gray-800 last:border-0 group"
              @click="clearSearch"
            >
              <div class="text-[12px] font-bold text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] tracking-wider group-hover:text-black dark:group-hover:text-gray-300 transition-colors">{{ result.title }}</div>
              <div v-if="result.description" class="text-[10px] text-gray-400 mt-1 line-clamp-1">{{ result.description }}</div>
            </NuxtLink>
          </div>
          <div 
            v-else-if="isSearchExpanded && searchTerm && !isSearching" 
            class="absolute top-full mt-2 right-0 w-64 bg-white dark:bg-[#121212] border border-gray-100 dark:border-gray-800 p-4 shadow-xl z-[100] text-[10px] text-gray-400 tracking-widest text-center"
          >
            Aucun résultat
          </div>        
        </div>
      </div>

      <!-- Mobile Toggle Button -->
      <div class="md:hidden flex items-center gap-2">
        <button 
          type="button"
          @click="cycleTheme" 
          class="p-1 text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4]"
          :title="themeTitle"
          :aria-label="themeTitle"
        >
          <!-- Light: Empty Circle -->
          <svg v-if="colorMode.preference === 'light'" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="9" />
          </svg>
          <!-- Dark: Half-filled Circle -->
          <svg v-else-if="colorMode.preference === 'dark'" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="9" />
            <path d="M12 3v18c4.97 0 9-4.03 9-9s-4.03-9-9-9z" fill="currentColor" />
          </svg>
          <!-- Doux: Small Dot in Circle -->
          <svg v-else-if="colorMode.preference === 'doux'" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="9" />
            <circle cx="12" cy="12" r="3" fill="currentColor" />
          </svg>
          <!-- Nuit: Filled Circle -->
          <svg v-else-if="colorMode.preference === 'nuit'" class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="9" fill="currentColor" />
          </svg>
        </button>
        <button 
          type="button"
          @click.stop="toggleMenu" 
          class="p-2 rounded-md text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] hover:bg-gray-200 dark:hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-gray-500"
          :aria-expanded="isMenuOpen"
          aria-controls="mobile-menu"
          :aria-label="isMenuOpen ? 'Fermer le menu' : 'Ouvrir le menu'"
        >
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path :class="{ 'hidden': isMenuOpen, 'block': !isMenuOpen }" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path :class="{ 'hidden': !isMenuOpen, 'block': isMenuOpen }" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Mobile Navigation Overlay -->
      <div
        v-if="isMenuOpen"
        id="mobile-menu"
        class="md:hidden fixed inset-0 h-screen w-screen glass-fluted bg-white dark:bg-[#121212] doux:bg-[#E5E1E0] nuit:bg-[#1A2238] z-[70] flex flex-col items-end justify-start pt-24 px-6 space-y-4"
        role="dialog"
        aria-modal="true"
        @click.stop
      >
        <button
          type="button"
          @click.stop="closeMenu"
          class="absolute top-4 right-6 p-3 text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] focus:outline-none focus:ring-2 focus:ring-inset focus:ring-gray-500"
          aria-label="Fermer le menu"
        >
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <!-- Search Bar (Mobile) -->
        <div class="w-full max-w-xs mb-8">
          <UInput 
            v-model="searchTerm" 
            id="mobile-site-search"
            placeholder="Rechercher..." 
            icon="i-heroicons-magnifying-glass-20-solid" 
            class="header-search-input"
            color="[#121212]"
            variant="none"
            size="lg"
          />
          <div 
            v-if="searchTerm && searchResults.length > 0" 
            class="mt-3 w-full glass-fluted bg-white/80 dark:bg-[#121212]/80 border border-gray-100 dark:border-gray-800 shadow-xl max-h-64 overflow-y-auto"
          >
            <NuxtLink 
              v-for="result in searchResults" 
              :key="result.path" 
              :to="result.path"
              class="block px-4 py-3 hover:bg-gray-50 dark:hover:bg-gray-900 border-b border-gray-50 dark:border-gray-800 last:border-0"
              @click="handleMobileSearchResultClick"
            >
              <div class="text-[12px] font-bold text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] tracking-wider">{{ result.title }}</div>
              <div v-if="result.description" class="text-[10px] text-gray-400 mt-1 line-clamp-1">{{ result.description }}</div>
            </NuxtLink>
          </div>
          <div 
            v-else-if="searchTerm && !isSearching" 
            class="mt-3 w-full bg-white/80 dark:bg-[#121212]/80 border border-gray-100 dark:border-gray-800 p-4 shadow-xl text-[10px] text-gray-400 tracking-widest text-center"
          >
            Aucun resultat
          </div>
        </div>

        <nav class="flex flex-col items-end space-y-4 w-full">
          <NuxtLink 
            v-for="link in links" 
            :key="link.to" 
            :to="link.to === '/' ? projectsLinkTarget : link.to"
            class="u-h2 text-[24px] text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] mobile-link px-4 py-3 min-h-11 border border-[#121212]/10 dark:border-white/10 w-fit"
            @click="handleMobileLinkClick(link, $event)"
          >
            {{ link.label }}
          </NuxtLink>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, computed, onUnmounted } from 'vue';
import { UInput } from '#components';
import { useHoverProject } from '~/composables/useHoverProject';

const props = defineProps<{
  transparent?: boolean;
}>();

const colorMode = useColorMode();
const cycleTheme = () => {
  const modes = ['light', 'dark', 'doux', 'nuit'];
  const currentIndex = modes.indexOf(colorMode.preference);
  const nextIndex = (currentIndex + 1) % modes.length;
  colorMode.preference = modes[nextIndex];
};

const themeTitle = computed(() => {
  if (colorMode.preference === 'light') return 'Passer au mode sombre';
  if (colorMode.preference === 'dark') return 'Passer au mode doux';
  if (colorMode.preference === 'doux') return 'Passer au mode nuit';
  return 'Passer au mode clair';
});

const { hoveredProjectTitle } = useHoverProject();

type HeaderLink = {
  label: string;
  to: string;
};

const links: HeaderLink[] = [
  { label: 'Projets', to: '/' },
  { label: 'À propos', to: '/about' },
  { label: 'Corpus', to: '/corpus' },
  { label: 'Art', to: '/art' }
];

const projectsLinkTarget = { path: '/', query: { view: 'grid' } };

const emit = defineEmits(['linkClick', 'linkHover']);

const activeLink = ref('');
const isMenuOpen = ref(false); // State for mobile menu
const searchTerm = ref(''); // Reactive search term
const isSearchExpanded = ref(false);
const searchInput = ref<any>(null);
const isSearching = ref(false);
const route = useRoute();
const router = useRouter();
const lockedBodyOverflow = ref<string | null>(null);

const { data: allContent } = await useAsyncData('all-site-content', () =>
  queryCollection('content')
    .select('path', 'title', 'description', 'date')
    .where('draft', '<>', true)
    .all()
);

const searchResults = computed(() => {
  if (!searchTerm.value || !allContent.value) return [];
  const query = searchTerm.value.toLowerCase().trim();
  return allContent.value.filter(item => 
    item.title?.toLowerCase().includes(query) || 
    item.description?.toLowerCase().includes(query)
  ).slice(0, 10); // Limit to 10 results
});

const handleSearchBlur = () => {
  // Delay blurring to allow clicking results
  setTimeout(() => {
    if (searchTerm.value === '') {
      isSearchExpanded.value = false;
    }
  }, 200);
};

const clearSearch = () => {
  searchTerm.value = '';
  isSearchExpanded.value = false;
};

watch(isSearchExpanded, (newValue) => {
  if (newValue) {
    nextTick(() => {
      const input = searchInput.value?.$el?.querySelector('input');
      if (input) input.focus();
    });
  }
});

const handleLinkClick = (label: string) => {
  activeLink.value = label;
  emit('linkClick', label);
};

const setBodyScrollLock = (locked: boolean) => {
  if (import.meta.client) {
    if (locked) {
      if (lockedBodyOverflow.value === null) {
        lockedBodyOverflow.value = document.body.style.overflow;
      }
      document.body.style.overflow = 'hidden';
    } else if (lockedBodyOverflow.value !== null) {
      document.body.style.overflow = lockedBodyOverflow.value;
      lockedBodyOverflow.value = null;
    }
  }
};

const setMenuOpen = (open: boolean) => {
  isMenuOpen.value = open;
  setBodyScrollLock(open);
};

const toggleMenu = () => {
  setMenuOpen(!isMenuOpen.value);
};

const closeMenu = () => {
  setMenuOpen(false);
};

const scrollToProjectsGrid = () => {
  if (!import.meta.client) return;

  const target = document.getElementById('projects-grid');
  if (!target) return;

  const targetPosition = target.getBoundingClientRect().top + window.scrollY - 96;
  window.scrollTo({ top: Math.max(0, targetPosition), behavior: 'smooth' });
};

const handleProjectsClick = async (event?: MouseEvent) => {
  event?.preventDefault();
  handleLinkClick('Projets');
  closeMenu();

  if (route.path === '/') {
    await nextTick();
    scrollToProjectsGrid();
    return;
  }

  await router.push(projectsLinkTarget);
};

const handleDesktopLinkClick = (link: HeaderLink, event: MouseEvent) => {
  if (link.to === '/') {
    void handleProjectsClick(event);
    return;
  }

  handleLinkClick(link.label);
};

const handleMobileLinkClick = (link: HeaderLink, event: MouseEvent) => {
  if (link.to === '/') {
    void handleProjectsClick(event);
    return;
  }

  handleLinkClick(link.label);
  closeMenu();
};

const handleMobileSearchResultClick = () => {
  clearSearch();
  closeMenu();
};

watch(isMenuOpen, (newValue) => {
  setBodyScrollLock(newValue);
});

watch(() => route.fullPath, () => {
  closeMenu();
});

onUnmounted(() => {
  setBodyScrollLock(false);
});
</script>

<style scoped>
@reference "../assets/css/main.css";

.router-link-active:not(.logo-link) {
  @apply text-black dark:text-white opacity-100;
}

.doux .router-link-active:not(.logo-link) {
  color: #4A4443;
}

.nuit .router-link-active:not(.logo-link) {
  color: #CDD6F4;
}

.logo-link.router-link-active {
  @apply text-[#121212] dark:text-white;
}

.doux .logo-link {
  color: #4A4443;
}

.nuit .logo-link {
  color: #CDD6F4;
}

.doux .mobile-link {
  color: #4A4443 !important;
}

.nuit .mobile-link {
  color: #CDD6F4 !important;
}

.header-search-input .icon {
  width: 21px;
  height: 21px;
}
</style>
