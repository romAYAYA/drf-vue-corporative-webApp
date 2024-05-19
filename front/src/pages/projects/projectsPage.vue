<template>
  <ProjectCreationModal :projectsDataRefetch="projectsDataRefetch"/>
  <div v-if="projectsDataStatus === 'success'">
    <CardComponent v-for="project in projectsData" :key="project.id" :project="project" />
  </div>


  <div class="text-red-500" v-if="projectsDataStatus === 'error'">
    Произошла ошибка. Пожалуйста, попробуйте перезагрузить страницу
  </div>
</template>

<script setup lang="ts">
import { useProjects } from '../../composables/useProjects.ts'
import ProjectCreationModal from '../../components/ProjectCreationModal.vue'
import CardComponent from '../../components/CardComponent.vue'

const { projectsData, projectsDataStatus, projectsDataRefetch } = useProjects()

</script>