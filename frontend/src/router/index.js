import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
// import App from '../App.vue'
import Home from '../components/Home.vue'
import Signup from '@/components/Signup.vue'
import Dashboard from '@/components/Dashboard.vue'
import Admin from '@/components/Admin.vue'
import Admin_login from '@/components/Admin_login.vue'
import Bookings_user from '@/components/Bookings_user.vue'
import Slots_user from '@/components/Slots_user.vue'
import UserInfo from '@/components/UserInfo.vue'
import Manage_slots from '@/components/Manage_slots.vue'
import App_bookings from '@/components/App_bookings.vue'
import User_details from '@/components/User_details.vue'
import Chart from '@/components/Chart.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      
    },
    {
      path:'/signup',
      name:'signup',
      component: Signup,
    },
    {
      path:'/user-dashboard',
      name:'user-dashboard',
      component: Dashboard,
    },
    {
      path:'/admin-dashboard',
      name:'admin-dashboard',
      component: Admin,
    },
    {
      path:'/admin-login',
      name:'admin-login',
      component:Admin_login,
    },
    {
      path:'/slots_user',
      name:'slots_user',
      component:Slots_user,
    },
    {
      path:'/bookings_user',
      name:'bookings_user',
      component: Bookings_user,
    },
    {
      path:'/user_info',
      name:'user_info',
      component:UserInfo,
    },
    {
      path:'/manage_slots',
      name:'manage_slots',
      component:Manage_slots,
    },
    {
      path:'/app_bookings',
      name:'app_bookings',
      component:App_bookings,
    },
    {
      path:'/user_details',
      name:'user_details',
      component:User_details,
    },
    {
      path:'/chart',
      name:'chart',
      component:Chart,
    },

  ],
})

export default router
