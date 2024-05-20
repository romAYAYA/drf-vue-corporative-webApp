<template>
  <section class="bg-blue-500 text-white py-16">
    <div class="container mx-auto text-center">
      <h1 class="text-4xl font-bold mb-4">Добро пожаловать в корпоративное приложение</h1>
      <p class="text-lg">Здесь вы можете публиковать свои проекты, ставить лайки и комментировать.</p>
    </div>
  </section>

  <main class="container mx-auto mt-8" v-if="isUserLoaded">
    <section>
      <h2 class="text-2xl font-bold mb-4">Топ проектов</h2>

      <div class="flex justify-center gap-12 items-center mb-5">
        <div class="flex items-center gap-2">
          <label for="searchQuery">Поиск:</label>
          <InputText class="h-8" id="searchQuery" v-model="searchQuery"/>
        </div>
        <Button class="w-fit p-2" @click="projectsDataRefetch()">Поиск</Button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <ProjectCard v-for="project in projects" :key="project.id" :project="project"
                     :projectsDataRefetch="projectsDataRefetch"/>
      </div>
      <Paginator
          v-if="isUserLoaded && projectsCount && projectsCount > 9"
          v-model:first="projectsOffset"
          v-model:rows="projectsPerPage"
          :totalRecords="projectsCount"
          @page="onProjectsPaginate"
      />


    </section>
  </main>
  <main class="container mx-auto mt-8 text-red-500" v-else>
    Войдите, чтобы увидеть лучшие проекты

  </main>

</template>

<script setup lang="ts">
import { useUserStore } from '../stores/user.ts'
import { computed, ref } from 'vue'
import { useProjects } from '../composables/useProjects.ts'
import ProjectCard from '../components/ProjectCard.vue'


const userStore = useUserStore()

const isUserLoaded = computed(() => userStore.isUserLoaded)

const projectsPage = ref(1)
const projectsOffset = ref(0)
const projectsPerPage = (9)

const searchQuery = ref('')
const sortCriteria = ref('ratings')


const {
  projectsData,
  projectsDataRefetch,
  projectsCount
} = useProjects(isUserLoaded, projectsPage, searchQuery, sortCriteria)
const projects = computed(() => projectsData?.value?.results)

const onProjectsPaginate = ({ rows, page }: { rows: number, page: number }) => {
  projectsOffset.value = rows * page
  projectsPage.value = page + 1
  console.log(projectsPage.value)
}
</script>
