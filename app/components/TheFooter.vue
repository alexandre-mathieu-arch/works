<template>
  <footer class="hidden md:block fixed bottom-0 left-0 right-0 z-40 glass-fluted transition-colors duration-300 pointer-events-none">
    <div class="main-container h-[45px] flex justify-between md:justify-end items-center gap-2 md:gap-12 pointer-events-auto">
      <a 
        href="mailto:alexandre.mat+w@protonmail.com" 
        class="u-h4 text-[10px] sm:text-[12px] md:text-[14px] text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] transition-colors hover:text-gray-500 dark:hover:text-gray-400 truncate max-w-[65vw] md:max-w-none"
      >
        alexandre.mat+w@protonmail.com
      </a>
      <button 
        @click="handleContactClick"
        class="u-h4 text-[10px] sm:text-[11px] md:text-[13px] text-[#121212] dark:text-white doux:text-[#4A4443] nuit:text-[#CDD6F4] uppercase transition-colors hover:text-gray-500 dark:hover:text-gray-400 cursor-pointer whitespace-nowrap"
      >
        Contact
      </button>
    </div>
  </footer>
</template>

<script setup lang="ts">
const router = useRouter();

const handleContactClick = async () => {
  // If we're already on the projects page, just scroll
  if (router.currentRoute.value.path === '/') {
    const el = document.getElementById('contact');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  } else {
    // Navigate with a query param to trigger scroll on mount
    await router.push({ path: '/', query: { scroll: 'contact' } });
  }
};
</script>
