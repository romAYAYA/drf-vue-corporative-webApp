<template>
  <div v-if="projectDataStatus === 'success'">
    <Card>
      <template #title>
        <h2>{{ projectData.name }}</h2>
      </template>
      <template #content>
        <p><strong>Описание:</strong> {{ projectData.description }}</p>
        <p><strong>Дата публикации:</strong> {{ new Date(projectData.creation_date).toLocaleString() }}</p>

        <div class="flex align-items-center mb-3">
          <img
              class="w-24 rounded-full"
              :src="userStore.isUserLoaded && userStore.user.profile.avatar ? `http://localhost:8000/${userStore.user.profile.avatar}`: '/duck.jpeg'"
              alt="avatar"/>
          <div class="ml-2">
            <p><strong>Автор:</strong> {{ projectData.author.username }}</p>
            <p><strong>Электронная почта:</strong> {{ projectData.author.email }}</p>
            <p><strong>Информация об авторе:</strong> {{ projectData.author.profile.bio }}</p>
          </div>
        </div>

        <p>
          <strong>Проект: </strong>
          <a :href="`http://localhost:8000/${projectData.file}`" target="_blank" rel="noopener noreferrer">Скачать</a>
        </p>
        <p><strong>Рейтинг:</strong> {{ projectData.rating }}</p>
      </template>
    </Card>

    <div class="flex flex-col gap-2 w-full my-5">
      <label for="comment">Оставить комментарий:</label>
      <Textarea id="comment" v-model="message"/>
      <Button class="self-start w-fit p-2" @click="createComment()">Отправить</Button>
    </div>
    {{ message }}
    <div class="flex flex-col gap-2" v-if="CommentDataStatus === 'success'">
      <CommentComponent v-for="comment in commentData" :key="comment.id" :comment="comment"
                        :commentDataRefetch="commentDataRefetch"/>
    </div>
    <div v-else>Произошла ошибка. Попробуйте перезагрузить страницу или повторить попытку позже</div>
  </div>
</template>

<script setup lang="ts">
import { useProject } from '../../composables/useProjects.ts'
import { useRoute } from 'vue-router'
import { handleCommentCreate, useComments } from '../../composables/useComments.ts'
import { ref } from 'vue'
import CommentComponent from '../../components/CommentComponent.vue'
import { useUserStore } from '../../stores/user.ts'

const route = useRoute()
const userStore = useUserStore()

const { projectData, projectDataStatus } = useProject(Number(route.params.projectId))

const message = ref('')

const { commentData, CommentDataStatus, commentDataRefetch } = useComments(Number(route.params.projectId))
const { createComment } = handleCommentCreate(message, Number(route.params.projectId), commentDataRefetch)


</script>
