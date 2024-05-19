import {  useMutation, useQuery } from '@tanstack/vue-query'
import axios from 'axios'
import { useToast } from 'primevue/usetoast'
import { Ref, watch } from 'vue'
import { errorDetail, errorSummary } from '../utils/constants.ts'
import { Project } from '../types/project.interface.ts'


export const useProjects = () => {
  const toast = useToast()

  const { data: projectsData, status: projectsDataStatus, refetch: projectsDataRefetch } = useQuery({
    queryKey: ['projects'],
    queryFn: async () => await axios.get('/projects'),
    select: ({ data }) => data,
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

  return { projectsData, projectsDataStatus, projectsDataRefetch }
}


export const useProject = (projectId: number) => {
  const toast = useToast()

  const { data: projectData, status: projectDataStatus } = useQuery({
    queryKey: ['project'],
    queryFn: async () => await axios.get(`/projects/${ projectId }`),
    select: ({ data }) => data
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





















