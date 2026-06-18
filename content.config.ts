import { defineContentConfig, defineCollection, z } from '@nuxt/content'

export default defineContentConfig({
  collections: {
    content: defineCollection({
      type: 'page',
      source: '**',
      schema: z.object({
        title: z.string(),
        description: z.string(),
        thumbnail: z.string().optional(),
        image: z.string().optional(),
        images: z.array(z.string()).optional(),
        heroImages: z.array(z.string()).optional(),
        details: z.array(z.string()).optional(),
        date: z.date().or(z.string()).optional(),
        tags: z.array(z.string()).optional(),
        gallery: z.array(z.string()).optional(),
        draft: z.boolean().default(false),
        typologies: z.array(z.string()).optional(),
        tailles: z.array(z.string()).optional(),
        pays: z.array(z.string()).optional(),
        lieu: z.string().optional(),
        surface: z.string().optional(),
        cout: z.string().optional(),
        phase: z.string().optional(),
        'phase réalisées': z.string().optional(),
        statut: z.string().optional(),
        workflow: z.array(z.string()).or(z.string()).optional(),
        ratio: z.string().optional(),
        order: z.number().optional(),
        collaboration: z.string().optional(),
        logiciels: z.array(z.string()).or(z.string()).optional(),
        materiaux: z.array(z.string()).or(z.string()).optional(),
        systeme_constructif: z.array(z.string()).or(z.string()).optional(),
      })
    }),
  },
})
