import { keepPreviousData, useMutation, useQuery } from '@tanstack/vue-query'
import axios from 'axios'
import { useToast } from 'primevue/usetoast'
import { computed, ComputedRef, Ref, watch } from 'vue'
import { errorDetail, errorSummary } from '../utils/constants.ts'
import { Project } from '../types/project.interface.ts'
import { useUserStore } from '../stores/user.ts'


export const useProjects = (isUserLoaded: ComputedRef<boolean>, projectsPage: Ref<number>, searchQuery: Ref<string>, sortCriteria: Ref<string>) => {
  const toast = useToast()

  const { data: projectsData, status: projectsDataStatus, refetch: projectsDataRefetch } = useQuery({
    queryKey: ['projects', projectsPage, searchQuery.value, sortCriteria.value],
    queryFn: async () => await axios.get('/projects/', {
      params: {
        page: projectsPage.value,
        search: searchQuery.value,
        sort_by: sortCriteria.value
      }
    }),
    select: ({ data }) => data,
    enabled: isUserLoaded,
    placeholderData: keepPreviousData,
    staleTime: Infinity
  })

  watch(projectsDataStatus, (newVal) => {
    if (newVal === 'error') {
      toast.add({
        severity: 'error',
        summary: errorSummary,
        detail: errorDetail,
        life: 3000
      })
    }
  })

  const projectsCount = computed(() => projectsData?.value?.count)

  return { projectsData, projectsDataStatus, projectsDataRefetch, projectsCount }
}


export const useProject = (projectId: number) => {
  const toast = useToast()
  const userStore = useUserStore()

  const isUserLoaded = computed(() => userStore.isUserLoaded)

  const { data: projectData, status: projectDataStatus } = useQuery({
    queryKey: ['project'],
    queryFn: async () => await axios.get(`/projects/${ projectId }/`),
    select: ({ data }) => data,
    enabled: isUserLoaded
  })

  watch(projectDataStatus, (newVal) => {
    if (newVal === 'error') {
      toast.add({
        severity: 'error',
        summary: errorSummary,
        detail: errorDetail,
        life: 3000
      })
    }
  })

  return { projectData, projectDataStatus }
}


export const handleCreateProject = (projectData: Ref<Project>, file: Ref<File | null>, refetch: any) => {
  const toast = useToast()

  const { mutate: createProject, status: createProjectStatus } = useMutation({
    mutationKey: ['projectCreation'],
    mutationFn: async () => {
      const formData = new FormData()
      if (projectData.value) {
        formData.append('name', projectData.value.name)
        formData.append('description', projectData.value.description)
      }

      if (file.value) {
        formData.append('file', file.value)
      }

      await axios.post(`/projects/create`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    }
  })

  watch(createProjectStatus, (newVal) => {
    if (newVal === 'error') {
      toast.add({
        severity: 'error',
        summary: errorSummary,
        detail: errorDetail,
        life: 3000
      })
    }
    if (newVal === 'success') {
      toast.add({
        severity: 'success',
        summary: 'Проект опубликован',
        life: 3000
      })
      refetch && refetch()
    }
  })


  return { createProject }
}
