import { createApp } from 'vue'
import PrimeVue from 'primevue/config'

import App from './App.vue'
import './style.css'
import Lara from './presets/ts/lara/index.ts'
import { router } from './router.ts'

import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Toolbar from 'primevue/toolbar'
import Image from 'primevue/image'
import Avatar from 'primevue/avatar'

const app = createApp(App)

document.documentElement.classList.remove('dark')

app.component('Button', Button)
app.component('InputText', InputText)
app.component('Toolbar', Toolbar)
app.component('Image', Image)
app.component('Avatar', Avatar)


app.use(PrimeVue, { ripple: true, unstyled: true, pt: Lara })
app.use(router)
app.mount('#app')