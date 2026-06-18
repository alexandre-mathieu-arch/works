export type ProjectTransitionMode = 'open' | 'close' | 'next' | 'prev' | 'generic' | null;

interface ProjectTransitionState {
  sourceProjectPath: string | null;
  targetProjectPath: string | null;
  gridScrollY: number;
  hasGridScrollPosition: boolean;
  shouldRestoreGridScroll: boolean;
  mode: ProjectTransitionMode;
}

export const useProjectTransition = () => {
  const state = useState<ProjectTransitionState>('project-transition', () => ({
    sourceProjectPath: null,
    targetProjectPath: null,
    gridScrollY: 0,
    hasGridScrollPosition: false,
    shouldRestoreGridScroll: false,
    mode: null
  }));

  const rememberGridScroll = () => {
    if (!import.meta.client) return;
    state.value.gridScrollY = window.scrollY;
    state.value.hasGridScrollPosition = true;
  };

  const beginTransition = (
    sourceProjectPath: string | null,
    targetProjectPath: string | null,
    mode: ProjectTransitionMode
  ) => {
    state.value.sourceProjectPath = sourceProjectPath;
    state.value.targetProjectPath = targetProjectPath;
    state.value.mode = mode;
  };

  const openProject = (projectPath: string) => {
    rememberGridScroll();
    state.value.shouldRestoreGridScroll = false;
    beginTransition(projectPath, projectPath, 'open');
  };

  const navigateBetweenProjects = (
    sourceProjectPath: string,
    targetProjectPath: string,
    direction: 'next' | 'prev'
  ) => {
    state.value.shouldRestoreGridScroll = false;
    beginTransition(sourceProjectPath, targetProjectPath, direction);
  };

  const closeProject = (projectPath: string) => {
    state.value.shouldRestoreGridScroll = state.value.hasGridScrollPosition;
    beginTransition(projectPath, projectPath, 'close');
  };

  const restoreGridScroll = () => {
    if (!import.meta.client || !state.value.shouldRestoreGridScroll) return false;

    state.value.shouldRestoreGridScroll = false;
    window.scrollTo({ top: state.value.gridScrollY, behavior: 'auto' });
    return true;
  };

  const settleOnProject = (projectPath: string) => {
    state.value.sourceProjectPath = projectPath;
    state.value.targetProjectPath = projectPath;
    state.value.mode = null;
  };

  const clearTransition = () => {
    state.value.sourceProjectPath = null;
    state.value.targetProjectPath = null;
    state.value.mode = null;
  };

  return {
    state,
    rememberGridScroll,
    beginTransition,
    openProject,
    navigateBetweenProjects,
    closeProject,
    restoreGridScroll,
    settleOnProject,
    clearTransition
  };
};
