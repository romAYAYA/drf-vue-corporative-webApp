<template>
  <div v-if="project">
    Название: {{ project.name }}
    Опубликовано: {{ new Date(project.creation_date).toLocaleString() }}
    Описание: {{ project.description }}
    <img :src="`http://localhost:8000/${project.author.profile.avatar}`" alt="zdf">
  </div>
</template>

<script setup lang="ts">

const {project} = defineProps({
  project: {
    type: Object,
    default: null
  }
})


</script>
