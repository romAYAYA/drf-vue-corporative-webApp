<template>
  <div class="card flex justify-content-center">
    <Button @click="visible = true" label="Изменить профиль" severity="secondary" size="small" text/>
    <Dialog v-model:visible="visible" modal header="Найстроки" :style="{ width: '25rem' }">
      <div v-if="userData" class="flex flex-col gap-3 mt-5">

        <div class="flex flex-col gap-2">
          <label for="username">Имя пользователя</label>
          <InputText id="username" v-model="userData.username"/>
        </div>

        <div>
          <label for="userBio">Обо мне</label>
          <Textarea id="userBio" v-if="userData.profile" v-model="userData.profile.bio" rows="5" cols="30"/>
        </div>

        <p>Новый аватар:</p>
        <input
            class="relative m-0 block w-full min-w-0 flex-auto cursor-pointer rounded border border-solid border-secondary-500 bg-transparent bg-clip-padding px-3 py-[0.32rem] text-base font-normal text-surface transition duration-300 ease-in-out file:-mx-3 file:-my-[0.32rem] file:me-3 file:cursor-pointer file:overflow-hidden file:rounded-none file:border-0 file:border-e file:border-solid file:border-inherit file:bg-transparent file:px-3  file:py-[0.32rem] file:text-surface focus:border-primary focus:text-gray-700 focus:shadow-inset focus:outline-none"
            type="file"
            @change="onFileChanged($event)"
            accept="image/*"
        />

        <Button class="w-full" @click="changeUserData()">Сохранить</Button>
        <Button class="w-full" severity="danger" @click="logoutUser()">Выйти</Button>
      </div>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useUserStore } from '../stores/user.ts'
import axios from 'axios'
import { useMutation } from '@tanstack/vue-query'
import { useToast } from 'primevue/usetoast'
import { User } from '../types/user.interface.ts'
import { errorDetail, errorSummary } from '../utils/constants.ts'
import Cookies from 'js-cookie'
import { useRouter } from 'vue-router'

const router = useRouter()
const toast = useToast()
const userStore = useUserStore()

const visible = ref(false)
const userData = ref<User | null>(null)

watch(
    () => userStore.user,
    (newUser) => {
      if (newUser) {
        userData.value = {
          username: newUser.username,
          profile: {
            bio: newUser.profile?.bio || '',
            avatar: newUser.profile?.avatar || ''
          }
        }
      }
    },
    { immediate: true }
)

const avatar = ref<File | null>()

function onFileChanged($event: Event) {
  const target = $event.target as HTMLInputElement
  if (target && target.files) {
    avatar.value = target.files[0]
  }
}

const { mutate: changeUserData, status: changeUserDataStatus } = useMutation({
  mutationKey: ['userInfoChange'],
  mutationFn: async () => {
    const formData = new FormData()
    if (userData.value && userData.value.profile) {
      formData.append('username', userData.value.username)
      formData.append('profile.bio', userData.value.profile.bio)
    }

    if (avatar.value) {
      formData.append('profile.avatar', avatar.value)
    }
    await axios.put('/users/update', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
})

const { mutate: logoutUser } = useMutation({
  mutationKey: ['logoutUser'],
  mutationFn: async () => {
    const res = await axios.post('/users/logout')
    if (res.status === 205) {
      Cookies.remove('refresh_token')
      Cookies.remove('access_token')
      userStore.user = {}
      visible.value = false
      await router.push('/')
    }
  }
})

watch(changeUserDataStatus, async (newVal) => {
  if (newVal === 'error') {
    toast.add({
      severity: 'error',
      summary: errorSummary,
      detail: errorDetail,
      life: 3000
    })
  }
  if (newVal === 'success') {
    toast.add({
      severity: 'success',
      summary: 'Данные обновлены',
      life: 3000
    })
    await userStore.getUser()
    visible.value = false
  }
})

</script>