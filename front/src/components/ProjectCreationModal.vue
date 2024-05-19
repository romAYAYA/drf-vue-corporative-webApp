<template>
  <div class="card flex justify-content-center">
    <Button @click="visible = true" label="Опубликовать проект" severity="secondary" size="small" text/>
    <Dialog v-model:visible="visible" modal header="Публикация проекта" :style="{ width: '25rem' }">
      <div class="flex flex-col gap-3 mt-5">

        <div class="flex flex-col gap-2">
          <label for="projectName">Название проекта</label>
          <InputText id="projectName" v-model="projectData.name"/>
        </div>

        <div>
          <label for="projectDescription">Описание проекта</label>
          <Textarea id="projectDescription" v-model="projectData.description" rows="5" cols="30"/>
        </div>

        <input
            class="relative m-0 block w-full min-w-0 flex-auto cursor-pointer rounded border border-solid border-secondary-500 bg-transparent bg-clip-padding px-3 py-[0.32rem] text-base font-normal text-surface transition duration-300 ease-in-out file:-mx-3 file:-my-[0.32rem] file:me-3 file:cursor-pointer file:overflow-hidden file:rounded-none file:border-0 file:border-e file:border-solid file:border-inherit file:bg-transparent file:px-3  file:py-[0.32rem] file:text-surface focus:border-primary focus:text-gray-700 focus:shadow-inset focus:outline-none"
            type="file"
            @change="onFileChanged($event)"
        />

        <Button class="w-full" @click="createProject()">Опубликовать</Button>
      </div>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { handleCreateProject } from '../composables/useProjects.ts'

const { projectsDataRefetch } = defineProps({
  projectsDataRefetch: {
    type: Function
  }
})

const visible = ref(false)
const projectData = ref({ name: '', description: '' })
const file = ref<File | null>(null)

const { createProject } = handleCreateProject(projectData, file, projectsDataRefetch)

function onFileChanged($event: Event) {
  const target = $event.target as HTMLInputElement
  if (target && target.files) {
    file.value = target.files[0]
  }
}

</script>

