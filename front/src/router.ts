import { createRouter, createWebHistory } from 'vue-router'

import homePage from './pages/homePage.vue'
import aboutPage from './pages/aboutPage.vue'
import projectsPage from './pages/projects/projectsPage.vue'
import projectPage from './pages/projects/projectPage.vue'


const routes = [
  { path: '/', component: homePage },
  { path: '/projects', component: projectsPage },
  { path: '/projects/:projectId', component: projectPage },
  { path: '/about', component: aboutPage }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})