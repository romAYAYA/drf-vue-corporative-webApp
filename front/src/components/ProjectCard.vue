<template>
  <div class="grid grid-cols-2 border-2 shadow-lg rounded-xl p-3 gap-3 min-h-[200px]">
    <div>
      <div class="font-bold mb-2">Автор: <span class="font-medium">{{ project.author.username }}</span></div>
      <div class="rounded-lg shadow-sm overflow-hidden">
        <img class="w-full h-full object-cover" :src="project.author.profile.avatar ? `http://localhost:8000/${project.author.profile.avatar}`: 'duck.jpeg'"
             alt="zdf">
      </div>
    </div>
    <div class="h-full relative">
      <div>
        <p class="font-bold text-lg">Название: <span class="capitalize font-medium">{{ project.name }}</span></p>
      </div>
      <div class="max-[750px]:hidden">
        <span class="font-bold">Описание:</span>
        <p class="capitalize">{{ truncateText(project.description, 50) }}</p>
      </div>

      <div class="absolute bottom-0">
        <p class="text-xs mb-3"> Опубликовано: {{ new Date(project.creation_date).toLocaleString() }}</p>


        <div class="flex justify-between items-center">
          <RouterLink class="p-1 border-2 rounded-lg" :to="`/projects/${project.id}`">Перейти</RouterLink>
          <div class="flex gap-2 items-center justify-center">
            <i @click="rateProject(project.id, true)" class="pi pi-thumbs-up cursor-pointer text-xl"></i>
            {{ project.rating }}
            <i @click="rateProject(project.id, false)" class="pi pi-thumbs-down cursor-pointer text-xl"></i>
          </div>
        </div>
      </div>

    </div>

  </div>


</template>

<script setup lang="ts">
import { truncateText } from '../utils/text.ts'
import axios from 'axios'

const { project, projectsDataRefetch } = defineProps({
  project: {
    type: Object,
    default: null
  },
  projectsDataRefetch: {
    type: Function
  }
})

const rateProject = async (projectId: number, isLiked: boolean) => {
  await axios.post(`/projects/rating/${ projectId }`, { is_liked: isLiked })
  projectsDataRefetch && projectsDataRefetch()
}

</script>
