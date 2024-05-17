import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import type  { AxiosError } from 'axios'
import { useToast } from 'primevue/usetoast'
import { User } from '../types/user.interface.ts'
import Cookies from 'js-cookie'

export const useUserStore = defineStore('user', () => {
  const user = ref()
  const toast = useToast()

  const isUserLoaded = computed(() => !!user.value)
  const setUser = (data?: any) => (user.value = data)

  const getUser = async () => {
    try {
      const { data } = await axios.get<User>('/users/me')
      setUser(data)
    } catch (error) {
      const err = error as AxiosError

      if (err.response && err.response.status !== 400) {
        toast.add({
          severity: 'error',
          summary: 'Произошла ошибка',
          detail: 'Если все сломалось, попробуйте перезагрузить страницу или повторить попытку позже',
          life: 3000
        })
      }
    }
  }

  const registerUser = async (userData: User) => {
    if (!user.value) {
      try {
        const { data } = await axios.post('/register', {
          username: userData.username,
          email: userData.email,
          password: userData.password
        })
        setUser(data)
        Cookies.set('access_token', data.access_token)
        Cookies.set('refresh_token', data.refresh_token)
        await getUser()
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
        const { data } = await axios.post('/login', {
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

  return { user, isUserLoaded, getUser, registerUser, loginUser }
})