import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '../layouts/DefaultLayout.vue'
import RadarView from '../views/RadarView.vue'
import LandingView from '../views/LandingView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView
    },
    {
      path: '/radar',
      name: 'radar',
      component: RadarView
    },
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
