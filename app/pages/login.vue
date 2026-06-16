<template>
  <div class="fixed inset-0 z-[100] bg-white dark:bg-[#121212] flex items-center justify-center p-6">
    <div class="w-full max-w-lg space-y-12">
      <div class="text-center space-y-4">
        <h1 class="u-h1 !text-[24px] md:!text-[32px] uppercase tracking-[0.3em] leading-tight">Alexandre MATHIEU</h1>
        <div class="h-px w-12 bg-[#121212]/20 dark:border-white/20 mx-auto"></div>
        <p class="u-h4 opacity-40 uppercase tracking-[0.2em]">PORTFOLIO — Espace Protégé</p>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div class="relative">
          <input
            v-model="password"
            type="password"
            placeholder="Mot de passe"
            class="w-full bg-transparent border-b border-[#121212]/20 dark:border-white/20 py-3 u-h4 focus:outline-none focus:border-primary-900 dark:focus:border-primary-400 transition-colors duration-(--duration-hover) ease-(--ease-atelier) text-center"
            autofocus
          />
          <p v-if="error" class="absolute top-full left-0 right-0 text-center text-red-500 text-[10px] uppercase tracking-widest mt-2 animate-pulse">
            Accès refusé
          </p>
        </div>

        <button
          type="submit"
          class="w-full h-[45px] border border-[#121212] dark:border-white u-h4 uppercase tracking-[0.2em] hover:bg-[#121212] hover:text-white dark:hover:bg-white dark:hover:text-[#121212] transition-all duration-(--duration-hover) ease-(--ease-atelier)"
        >
          Entrer
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const { login } = useAuth()
const password = ref('')
const error = ref(false)

const handleSubmit = () => {
  if (login(password.value)) {
    navigateTo('/')
  } else {
    error.value = true
    password.value = ''
    setTimeout(() => {
      error.value = false
    }, 3000)
  }
}

useHead({
  title: 'Alexandre MATHIEU — PORTFOLIO'
})

definePageMeta({
  layout: false,
  hideHeader: true,
  hideLayoutTitle: true
})
</script>
