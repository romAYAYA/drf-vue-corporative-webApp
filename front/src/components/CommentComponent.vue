<template>
  <div class="flex justify-between p-4 border rounded-lg shadow-sm">
    <div class="flex items-start justify-between">
      <div class="w-16 h-16 rounded-full overflow-hidden flex-shrink-0">
        <img
            class="w-full h-full object-cover"
            :src="userStore.isUserLoaded && userStore.user.profile.avatar ? `http://localhost:8000/${userStore.user.profile.avatar}` : '/duck.jpeg'"
            alt="User Avatar"
        >
      </div>
      <div class="ml-4">
        <p class="text-lg font-semibold text-gray-800">Автор: {{ comment.author.username }}</p>
        <p class="mt-2 text-gray-600 flex items-start gap-2"><span class="font-bold">Комментарий:</span>
          <span v-if="!messageEditable">{{ comment.message }}</span>
          <Textarea v-model="newMessage" v-else/>
        </p>
      </div>
    </div>
    <div class="flex gap-2 flex-col">
      <div class="flex items-center gap-2">
        <i @click="rateComment( true)" class="pi pi-thumbs-up cursor-pointer text-xl"></i>
        {{ comment.rating }}
        <i @click="rateComment(false)" class="pi pi-thumbs-down cursor-pointer text-xl"></i>
      </div>
      <div v-if="userStore.user.username === comment.author.username"
           class="flex justify-between gap-2 border-t-2 border-red-500 pt-2">
        <div class="flex items-center gap-2">
          <i @click="messageEditable = !messageEditable" class="pi pi-pencil cursor-pointer text-xl"></i>
          <i v-if="messageEditable" @click="updateComment()" class="pi pi-check cursor-pointer text-xl"></i>
        </div>
        <i @click="deleteComment()" class="pi pi-trash cursor-pointer text-xl"></i>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '../stores/user.ts'
import axios from 'axios'
import { handleCommentDelete, handleCommentUpdate } from '../composables/useComments.ts'
import { ref } from 'vue'

const { comment, commentDataRefetch } = defineProps({
  comment: {
    type: Object,
    default: null
  },
  commentDataRefetch: {
    type: Function
  }
})

const newMessage = ref(comment.message)
const messageEditable = ref(false)

const userStore = useUserStore()

const { updateComment } = handleCommentUpdate(newMessage, comment.id, comment.project, commentDataRefetch, messageEditable)
const { deleteComment } = handleCommentDelete(comment.id, commentDataRefetch)


const rateComment = async (isLiked: boolean) => {
  await axios.post(`/comments/rating/${ comment.id }`, { is_liked: isLiked })
  commentDataRefetch && commentDataRefetch()
}
</script>
