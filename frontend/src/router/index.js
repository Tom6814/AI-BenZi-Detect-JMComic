import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Wizard',
    component: () => import('../views/WizardView.vue')
  },
  {
    path: '/old',
    component: () => import('../layouts/DefaultLayout.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('../views/Home.vue')
      },
      {
        path: 'search',
        name: 'Search',
        component: () => import('../views/SearchView.vue')
      },
      {
        path: 'rules',
        name: 'Rules',
        component: () => import('../views/RulesView.vue')
      },
      {
        path: 'config',
        name: 'Config',
        component: () => import('../views/ConfigView.vue')
      },
      {
        path: 'identify',
        name: 'Identify',
        component: () => import('../views/IdentifyView.vue')
      },
      {
        path: 'about',
        name: 'About',
        component: () => import('../views/About.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
