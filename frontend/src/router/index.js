import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import Tasks from '@/views/Tasks.vue'
import Traffic from '@/views/Traffic.vue'
import Environments from '@/views/Environments.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', component: Dashboard },
  { path: '/tasks', component: Tasks },
  { path: '/traffic', component: Traffic },
  { path: '/environments', component: Environments },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

