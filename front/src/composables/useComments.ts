import { useMutation, useQuery } from '@tanstack/vue-query'
import axios from 'axios'
import { useUserStore } from '../stores/user.ts'
import { computed, Ref, watch } from 'vue'
import { useToast } from 'primevue/usetoast'

export const useComments = (projectId: number) => {
  const userStore = useUserStore()
  const isUserLoaded = computed(() => userStore.isUserLoaded)

  const { data: commentData, status: CommentDataStatus, refetch: commentDataRefetch } = useQuery({
    queryKey: ['comments'],
    queryFn: async () => await axios.get(`/comments/${ projectId }/`),
    select: ({ data }) => data,
    enabled: isUserLoaded
  })

  return { commentData, CommentDataStatus, commentDataRefetch }
}

export const handleCommentCreate = (message: Ref<string>, projectId: number, commentDataRefetch: any) => {
  const { mutate: createComment } = useMutation({
    mutationKey: ['commentCreation'],
    mutationFn: async () => {
      if (message.value) {
        await axios.post(`/comments/${ projectId }/`, { message: message.value })
        commentDataRefetch && commentDataRefetch()
        message.value = ''
      }
    }
  })

  return { createComment }
}


export const handleCommentUpdate = (message: Ref<string>, commentId: number, projectId: number, commentDataRefetch: any, messageEditable: Ref<boolean>) => {

  const { mutate: updateComment } = useMutation({
    mutationKey: ['commentUpdate'],
    mutationFn: async () => {
      const response = await axios.put(`/comment/${ commentId }/`, {
        message: message.value,
        project: projectId
      })
      if (response.data) {
        messageEditable.value = !messageEditable.value
        commentDataRefetch && commentDataRefetch()
      }
    }
  })

  return { updateComment }
}


export const handleCommentDelete = (commentId: number, commentDataRefetch: any) => {
  const toast = useToast()

  const { mutate: deleteComment, status: deleteCommentStatus } = useMutation({
    mutationKey: ['deleteComment'],
    mutationFn: async () =>  await axios.delete(`/comment/${ commentId }/`)
  })

  watch(deleteCommentStatus, (newVal) => {
    if (newVal === 'success') {
      commentDataRefetch && commentDataRefetch()
      toast.add({severity: 'info', summary: 'Комментарий удален', life: 3000})
    }
  })

  return { deleteComment }
}






















