import type { ProjectTransitionMode } from '~/composables/useProjectTransition';

const PROJECT_ROUTE_PATTERN = /^\/projets\/[^/]+$/;
const ROOT_TRANSITION_CLASSES = [
  'route-transition-open',
  'route-transition-close',
  'route-transition-next',
  'route-transition-prev',
  'route-transition-generic'
];

const normalizeRoutePath = (path: string) => {
  const normalizedPath = path.replace(/^\/works(?=\/|$)/, '');
  return normalizedPath || '/';
};

export default defineNuxtPlugin(nuxtApp => {
  const router = useRouter();
  const {
    state,
    rememberGridScroll,
    beginTransition,
    closeProject,
    restoreGridScroll,
    settleOnProject,
    clearTransition
  } = useProjectTransition();

  let settleTimer: ReturnType<typeof setTimeout> | null = null;

  const applyRootTransitionClass = (mode: Exclude<ProjectTransitionMode, null>) => {
    document.documentElement.classList.remove(...ROOT_TRANSITION_CLASSES);
    document.documentElement.classList.add(`route-transition-${mode}`);
  };

  const getTransitionDuration = () => {
    const rawValue = getComputedStyle(document.documentElement)
      .getPropertyValue('--duration-shared-media')
      .trim();
    const parsedValue = Number.parseFloat(rawValue);

    if (Number.isNaN(parsedValue)) return 1400;
    return rawValue.endsWith('ms') ? parsedValue : parsedValue * 1000;
  };

  router.beforeEach((to, from) => {
    if (settleTimer) {
      clearTimeout(settleTimer);
      settleTimer = null;
    }

    const fromPath = normalizeRoutePath(from.path);
    const toPath = normalizeRoutePath(to.path);
    const fromProject = PROJECT_ROUTE_PATTERN.test(fromPath);
    const toProject = PROJECT_ROUTE_PATTERN.test(toPath);
    const toGrid = toPath === '/';

    if (!fromProject && toProject) {
      if (fromPath === '/') rememberGridScroll();
      if (state.value.targetProjectPath !== toPath || state.value.mode !== 'open') {
        beginTransition(toPath, toPath, 'open');
      }
    } else if (fromProject && toProject) {
      if (state.value.targetProjectPath !== toPath) {
        beginTransition(fromPath, toPath, 'generic');
      }
    } else if (fromProject && toGrid) {
      closeProject(fromPath);
    } else {
      beginTransition(null, null, 'generic');
    }

    applyRootTransitionClass(state.value.mode || 'generic');
  });

  router.afterEach((to, from) => {
    const toPath = normalizeRoutePath(to.path);
    const fromPath = normalizeRoutePath(from.path);

    settleTimer = setTimeout(() => {
      if (PROJECT_ROUTE_PATTERN.test(toPath)) {
        settleOnProject(toPath);
      } else if (toPath !== '/' || !PROJECT_ROUTE_PATTERN.test(fromPath)) {
        clearTransition();
      }

      document.documentElement.classList.remove(...ROOT_TRANSITION_CLASSES);
    }, getTransitionDuration() + 120);
  });

  nuxtApp.hook('page:finish', () => {
    if (normalizeRoutePath(router.currentRoute.value.path) === '/') {
      const restoredGridScroll = restoreGridScroll();
      if (!restoredGridScroll && router.currentRoute.value.query.view === 'grid') {
        const projectsGrid = document.getElementById('projects-grid');
        if (projectsGrid) {
          const targetPosition = projectsGrid.getBoundingClientRect().top + window.scrollY - 160;
          window.scrollTo({ top: Math.max(0, targetPosition), behavior: 'auto' });
        }
      }
    }
  });
});
