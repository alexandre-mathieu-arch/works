import { ref, onMounted, onUnmounted } from 'vue'

export const useParallax = (intensity = 15) => {
  const scrollY = ref(0)
  const windowHeight = ref(0)
  const isEnabled = ref(false)
  let ticking = false

  const updateScroll = () => {
    if (!isEnabled.value || ticking) return

    ticking = true
    requestAnimationFrame(() => {
      scrollY.value = window.scrollY
      ticking = false
    })
  }

  const updateDimensions = () => {
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    isEnabled.value = window.matchMedia('(min-width: 1024px)').matches && !reducedMotion
    windowHeight.value = window.innerHeight
  }

  onMounted(() => {
    updateDimensions()
    window.addEventListener('scroll', updateScroll, { passive: true })
    window.addEventListener('resize', updateDimensions)
  })

  onUnmounted(() => {
    window.removeEventListener('scroll', updateScroll)
    window.removeEventListener('resize', updateDimensions)
  })

  const getParallaxStyle = (el: any) => {
    if (!process.client || typeof window === 'undefined' || !isEnabled.value || !el) return {}

    scrollY.value
    
    // Handle Vue component refs or raw elements
    const element = el.$el || el
    
    if (!element || typeof element.getBoundingClientRect !== 'function') return {}

    const rect = element.getBoundingClientRect()
    const elementCenter = rect.top + rect.height / 2
    const viewportCenter = windowHeight.value / 2
    
    // Calculate distance from center of viewport (-1 to 1)
    const distanceFromCenter = (elementCenter - viewportCenter) / (windowHeight.value / 2)
    
    // Clamp values to prevent excessive motion
    const clampedDistance = Math.max(-1, Math.min(1, distanceFromCenter))
    
    const translateY = clampedDistance * intensity

    return {
      transform: `translate3d(0, ${translateY}px, 0)`,
      willChange: 'transform'
    }
  }

  return {
    getParallaxStyle
  }
}
