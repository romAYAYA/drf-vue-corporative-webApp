<template>
  <div class="flex flex-col gap-3">
    <InputText placeholder="Имя пользователя" v-model="userData.username"/>
    <InputText placeholder="Пароль" v-model="userData.password"/>

    <Button class="w-full" @click="loginUser(userData)">Войти</Button>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '../../stores/user.ts'
import { ref } from 'vue'
import { User } from '../../types/user.interface.ts'
import { useToast } from 'primevue/usetoast'

const visible = defineModel('visible')

const userStore = useUserStore()
const toast = useToast()

const userData = ref<User>({ username: '', password: '' })

const loginUser = (userData: User) => {
  if (userData.username.length >= 3 && userData.password && userData.password.length >= 3) {
    userStore.loginUser(userData, visible)
    visible.value = false
  } else {
    toast.add({
      severity: 'error',
      summary: 'Произошла ошибка',
      detail: 'Проверьте заполненность полей и повторите попытку',
      life: 3000
    })
  }
}
</script>