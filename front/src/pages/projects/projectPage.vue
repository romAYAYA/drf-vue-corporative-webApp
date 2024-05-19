<template>
  <div v-if="projectDataStatus === 'success'">
    {{ projectData }}
  </div>
</template>

<script setup lang="ts">
import { useProject } from '../../composables/useProjects.ts'
import { useRoute } from 'vue-router'

const route = useRoute()
const { projectData, projectDataStatus } = useProject(Number(route.params.projectId))
console.log(route.params.projectId)

</script>
