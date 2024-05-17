import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import axios from 'axios'
import VueAxios from 'vue-axios'
import { createPinia } from 'pinia'
import { VueQueryPlugin } from '@tanstack/vue-query'

import App from './App.vue'
import './style.css'
import Lara from './presets/ts/lara/index.ts'
import { router } from './router.ts'
import ToastService from 'primevue/toastservice'
import Cookies from 'js-cookie'

import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Image from 'primevue/image'
import Avatar from 'primevue/avatar'
import Toast from 'primevue/toast'
import Dialog from 'primevue/dialog'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import Toolbar from 'primevue/toolbar'
import Textarea from 'primevue/textarea'
import FileUpload from 'primevue/fileupload'


const app = createApp(App)
const pinia = createPinia()

document.documentElement.classList.remove('dark')

app.component('Button', Button)
app.component('InputText', InputText)
app.component('Image', Image)
app.component('Avatar', Avatar)
app.component('Toast', Toast)
app.component('Dialog', Dialog)
app.component('TabView', TabView)
app.component('TabPanel', TabPanel)
app.component('Toolbar', Toolbar)
app.component('Textarea', Textarea)
app.component('FileUpload', FileUpload)

axios.defaults.baseURL = import.meta.env.VITE_API_URL

axios.interceptors.request.use(
  (config) => {
    const accessToken = Cookies.get('access_token')
    if (accessToken) {
      config.headers.Authorization = `Bearer ${ accessToken }`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

axios.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    if (originalRequest.url.includes('/token/refresh')) {
      return Promise.reject(error)
    }

    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      try {
        const response = await axios.post('/token/refresh', {
          refresh: Cookies.get('refresh_token')
        })

        const newAccessToken = response.data.access
        const newRefreshToken = response.data.refresh

        Cookies.set('access_token', newAccessToken, { path: '/' })
        Cookies.set('refresh_token', newRefreshToken, { path: '/' })

        originalRequest.headers.Authorization = `Bearer ${ newAccessToken }`

        return axios(originalRequest)
      } catch (refreshError) {
        Cookies.remove('access_token', { path: '/' })
        Cookies.remove('refresh_token', { path: '/' })
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

app.use(PrimeVue, { ripple: true, unstyled: true, pt: Lara })
app.use(router)
app.use(VueAxios, axios)
app.use(VueQueryPlugin)
app.use(pinia)
app.use(ToastService)
app.mount('#app')