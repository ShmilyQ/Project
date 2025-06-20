import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/',
    component: () => import('@/components/common/layout.vue'), // 修正大小写
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/Dashboard.vue')
      },
      {
        path: 'warehouse',
        name: 'WarehouseList',
        component: () => import('@/views/warehouse/WarehouseList.vue')
      },
      {
        path: 'warehouse/:id',
        name: 'WarehouseDetail',
        component: () => import('@/views/warehouse/WarehouseDetail.vue')
      },
      {
        path: 'product',
        name: 'ProductList',
        component: () => import('@/views/product/ProductList.vue')
      },
      {
        path: 'product/:id',
        name: 'ProductDetail',
        component: () => import('@/views/product/ProductDetail.vue')
      },
      {
        path: 'inventory',
        name: 'InventoryList',
        component: () => import('@/views/inventory/InventoryList.vue')
      },
      {
        path: 'order/inbound',
        name: 'InboundOrder',
        component: () => import('@/views/order/InboundOrder.vue')
      },
      {
        path: 'order/outbound',
        name: 'OutboundOrder',
        component: () => import('@/views/order/OutboundOrder.vue')
      },
      {
        path: 'report/inventory',
        name: 'InventoryReport',
        component: () => import('@/views/report/InventoryReport.vue')
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/auth/Profile.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters['auth/isAuthenticated']
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router