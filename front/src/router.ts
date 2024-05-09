import { createMemoryHistory, createRouter } from 'vue-router'

import homePage from './pages/homePage.vue'
import aboutPage from './pages/aboutPage.vue'


const routes = [
  { path: '/', component: homePage },
  { path: '/about', component: aboutPage }
]

export const router = createRouter({
  history: createMemoryHistory(),
  routes
})