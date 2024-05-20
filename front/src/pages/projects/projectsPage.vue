<template>
  <div v-if="isUserLoaded">
    <div class="flex justify-center gap-12 items-center">
      <select
          class="block  py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          v-model="selectedSortCriteria" @change="handleSort(selectedSortCriteria)">
        <option value="name">Название</option>
        <option value="ratings">Рейтинг</option>
        <option value="creation_date">Дата публикации</option>
      </select>

      <div class="flex items-center gap-2">
        <label for="searchQuery">Поиск:</label>
        <InputText class="h-8" id="searchQuery" v-model="searchQuery"/>
      </div>
      <Button class="w-fit p-2" @click="projectsDataRefetch()">Поиск</Button>
    </div>

    <ProjectCreationModal class="mb-5" :projectsDataRefetch="projectsDataRefetch"/>
    <div class="grid grid-cols-3 max-[1100px]:grid-cols-2 max-[750px]:grid-cols-1 gap-4"
         v-if="projectsDataStatus === 'success'">
      <ProjectCard v-for="project in projects" :key="project.id" :project="project"
                   :projectsDataRefetch="projectsDataRefetch"/>
    </div>
    <Paginator
        v-if="isUserLoaded && projectsCount && projectsCount > 9"
        v-model:first="projectsOffset"
        v-model:rows="projectsPerPage"
        :totalRecords="projectsCount"
        @page="onProjectsPaginate"
    >
    </Paginator>

    <div class="text-red-500" v-if="projectsDataStatus === 'error'">
      Произошла ошибка. Пожалуйста, попробуйте перезагрузить страницу
    </div>
  </div>
  <div class="text-red-500" v-else>
    Войдите, чтобы увидеть содержимое страницы
  </div>
</template>

<script setup lang="ts">
import { useProjects } from '../../composables/useProjects.ts'
import ProjectCreationModal from '../../components/ProjectCreationModal.vue'
import ProjectCard from '../../components/ProjectCard.vue'
import { useUserStore } from '../../stores/user.ts'
import { computed, ref } from 'vue'

const userStore = useUserStore()
const isUserLoaded = computed(() => userStore.isUserLoaded)

const projectsPage = ref(1)
const projectsOffset = ref(0)
const projectsPerPage = (9)

const searchQuery = ref('')
const sortCriteria = ref('')
const selectedSortCriteria = ref('')

const {
  projectsData,
  projectsDataStatus,
  projectsDataRefetch,
  projectsCount
} = useProjects(isUserLoaded, projectsPage, searchQuery, sortCriteria)
const projects = computed(() => projectsData?.value?.results)

const handleSort = (criteria: string) => {
  sortCriteria.value = criteria
}

const onProjectsPaginate = ({ rows, page }: { rows: number, page: number }) => {
  projectsOffset.value = rows * page
  projectsPage.value = page + 1
  console.log(projectsPage.value)
}
</script>