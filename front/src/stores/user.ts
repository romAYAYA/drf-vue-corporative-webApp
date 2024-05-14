import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useToast } from 'primevue/usetoast'
import { User } from '../types/user.interface.ts'
import Cookies from 'js-cookie'

export interface UserResponse {
  id: number
  username: string
  first_name: string
  last_name: string
  email: string
  profile: Profile
}

export interface Profile {
  bio: string
  avatar: string
}


export const useUserStore = defineStore('user', () => {
  const user = ref()
  const toast = useToast()

  const isUserLoaded = computed(() => !!user.value)
  const setUser = (data?: any) => (user.value = data)

  const registerUser = async (userData: User) => {
    if (!user.value) {
      try {
        const { data } = await axios.post('/users_register', {
          username: userData.username,
          email: userData.email,
          password: userData.password
        })
        setUser(data)
        Cookies.set('access_token', data.access_token)
        Cookies.set('refresh_token', data.refresh_token)
        toast.add({
          severity: 'success',
          summary: 'Вы успешно зарегистрированы',
          detail: 'Приятного пользования!',
          life: 3000
        })
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Произошла ошибка',
          detail: 'Если все сломалось, попробуйте перезагрузить страницу или повторить попытку позже',
          life: 3000
        })
      }
    }
  }

  const loginUser = async (userData: User) => {
    if (!user.value) {
      try {
        const { data } = await axios.post('/users_login', {
          username: userData.username,
          password: userData.password
        })
        setUser(data)
        Cookies.set('access_token', data.access_token)
        Cookies.set('refresh_token', data.refresh_token)
        toast.add({ severity: 'success', summary: 'Вы успешно вошли', detail: 'Приятного пользования!', life: 3000 })
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Произошла ошибка',
          detail: 'Если все сломалось, попробуйте перезагрузить страницу или повторить попытку позже',
          life: 3000
        })
      }
    }
  }

  const getUser = async () => {
    const { data } = await axios.get<UserResponse>('/user')
    setUser(data)
  }

  return { user, isUserLoaded, getUser, registerUser, loginUser }
})