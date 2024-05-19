<template>
  <ProjectCreationModal :projectsDataRefetch="projectsDataRefetch"/>
  <div v-if="projectsDataStatus === 'success'">
    {{ projectsData }}
  </div>
</template>

<script setup lang="ts">
import { useProjects } from '../../composables/useProjects.ts'
import ProjectCreationModal from '../../components/ProjectCreationModal.vue'

const { projectsData, projectsDataStatus, projectsDataRefetch } = useProjects()

</script>