// https://nuxt.com/docs/api/configuration/nuxt-config

import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  app: {
    baseURL: '/works/',
    head: {
      htmlAttrs: {
        lang: 'fr'
      },
      meta: [
        {
          name: 'description',
          content: "Portfolio d'Alexandre Mathieu, architecte: projets d'architecture, design, rehabilitation et recherche constructive."
        },
        { property: 'og:type', content: 'website' },
        { property: 'og:site_name', content: 'Alexandre Mathieu' },
        { property: 'og:title', content: 'Alexandre Mathieu - architecture & design' },
        {
          property: 'og:description',
          content: "Portfolio d'Alexandre Mathieu, architecte: projets d'architecture, design, rehabilitation et recherche constructive."
        },
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'theme-color', content: '#1A2238' }
      ]
    },
    pageTransition: {
      name: 'page',
      mode: 'out-in'
    },
    layoutTransition: false,
    viewTransition: false
  },

  modules: ['@nuxt/content', '@nuxt/image', '@nuxt/ui'],

  image: {
    // Default provider (ipx) is used for static generation.
    // We avoid 'static' provider as it caused 500 errors during prerendering.
  },

  colorMode: {
    classSuffix: '',
    preference: 'nuit',
    fallback: 'light',
    modes: {
      light: 'light',
      dark: 'dark',
      doux: 'doux',
      nuit: 'nuit'
    }
  },

  devtools: { enabled: true },

  compatibilityDate: '2024-04-03',

  css: ['./app/assets/css/main.css'],
  
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
})
