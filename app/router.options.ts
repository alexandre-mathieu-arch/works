export default {
  scrollBehavior(to: { path: string }, from: { path: string }, savedPosition: { left: number; top: number } | null) {
    if (savedPosition) return savedPosition;

    const normalizeRoutePath = (path: string) => {
      const normalizedPath = path.replace(/^\/works(?=\/|$)/, '');
      return normalizedPath || '/';
    };
    const toPath = normalizeRoutePath(to.path);
    const fromPath = normalizeRoutePath(from.path);
    const fromProject = /^\/projets\/[^/]+$/.test(fromPath);

    if (toPath === '/' && fromProject) {
      return false;
    }

    if (toPath.startsWith('/projets/')) {
      return { left: 0, top: 0, behavior: 'auto' as const };
    }

    if (toPath === fromPath) {
      return false;
    }

    return { left: 0, top: 0, behavior: 'auto' as const };
  }
};
