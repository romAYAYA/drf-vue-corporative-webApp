import { createApp } from 'vue'
import PrimeVue from 'primevue/config'

import App from './App.vue'
import './style.css'
import Lara from './presets/ts/lara/index.ts'
import { router } from './router.ts'

import Button from 'primevue/button'
import InputText from 'primevue/inputtext'

const app = createApp(App)

document.documentElement.classList.remove('dark')

app.component('Button', Button)
app.component('InputText', InputText)

app.use(PrimeVue, { ripple: true, unstyled: true, pt: Lara })
app.use(router)
app.mount('#app')