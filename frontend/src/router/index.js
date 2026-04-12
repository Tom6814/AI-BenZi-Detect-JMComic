import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '../layouts/DefaultLayout.vue'
import RadarView from '../views/RadarView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'radar',
      component: RadarView
    },
    // Keep old routes under a layout for reference/testing if needed
    {
      path: '/classic',
      component: DefaultLayout,
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('../views/Home.vue')
        },
        {
          path: 'config',
          name: 'config',
          component: () => import('../views/ConfigView.vue')
        },
        {
          path: 'rules',
          name: 'rules',
          component: () => import('../views/RulesView.vue')
        },
        {
          path: 'search',
          name: 'search',
          component: () => import('../views/SearchView.vue')
        },
        {
          path: 'identify',
          name: 'identify',
          component: () => import('../views/IdentifyView.vue')
        },
        {
          path: 'about',
          name: 'about',
          component: () => import('../views/About.vue')
        }
      ]
    }
  ]
})

export default router
