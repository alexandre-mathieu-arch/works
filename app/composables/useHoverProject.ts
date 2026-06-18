import { computed } from 'vue';

interface ProjectHoverData {
  title: string;
  typologies?: string[];
  tailles?: string[];
  date?: string | number | Date;
  pays?: string[];
}

export const useHoverProject = () => {
  const hoveredProject = useState<ProjectHoverData | null>('hovered-project', () => null);

  const setHoveredProject = (project: ProjectHoverData | null) => {
    hoveredProject.value = project;
  };

  const hoveredProjectTitle = computed(() => hoveredProject.value?.title || null);

  return {
    hoveredProject,
    hoveredProjectTitle,
    setHoveredProject,
  };
};
