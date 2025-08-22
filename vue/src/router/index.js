import Vue from 'vue'
import VueRouter from 'vue-router'
import homeView from '../views/homeView.vue'
import loginView from '../views/loginView.vue'
import registerView from '@/views/registerView.vue'
import userView from '../views/userView.vue'

import doctorlist from '../views/list/doctorlist.vue'
import druglist from'../views/list/druglist.vue'
import emrlist from '../views/list/emrlist'
import modellist from '../views/list/modellist'
import myselflist from '../views/list/myselflist'
import patientlist from '../views/list/patientlist'
import paylist from '../views/list/paylist'
import userlist from '../views/list/userlist'
import registrationlist from '../views/list/registrationlist.vue'
import maincount from '../views/count/maincount'
import doctor_userView from '@/views/doctor_userView.vue'
import EditEmr from '@/views/count/EditEmr.vue'
import AddEmr from '@/views/count/AddEmr.vue'
import DrugInventoryManagement from '../views/list/drug_inventory.vue'
import user_myself from '../components/user_myself.vue'
import user_registrations from '../components/user_registration.vue'
import user_emr from '../components/user_emr.vue'
import RegistrationCharts from '@/views/count/RegistrationCharts.vue'
import drugCharts from '@/views/count/drugCharts.vue'
import user_guahao from '../components/uer_guahao.vue'
import emr from '@/views/count/emr.vue'
import huajialist from '../views/list/huajialist.vue'
import user_huajia from '../components/user_huajia.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '',
    redirect: "/login",
  },
  {
    path:'/home',
    name:'home',
    component:homeView,
    children:[
      
      {path:'/list/doctorlist',component:doctorlist},
      {path:'/list/druglist',component:druglist},
      {path:'/list/emrlist',component:emrlist},
      {path:'/list/modellist',component:modellist},
      {path:'/list/patientlist',component:patientlist},
      {path:'/list/paylist',component:paylist},
      {path:'/list/userlist',component:userlist},
      {path:'/list/huajialist',component:huajialist},
      {path:'/list/registrationlist',component:registrationlist},
      {path:'/home',component:maincount},
      {path: '/edit-emr/:id', name: 'EditEmr',component: EditEmr },  // Add route for editing EMR
      {path: '/add-emr',name: 'AddEmr',component: AddEmr },  // Add route for adding EMR
      {path: '/drug-inventory', name: 'DrugInventoryManagement',component: DrugInventoryManagement},
      {path: '/RegistrationCharts',name: 'RegistrationCharts',component: RegistrationCharts },
      {path: '/drugCharts',name: 'drugCharts',component:drugCharts },
    ]

  },
  {
    path:'/login',
    name:'login',
    component:loginView
  },
  {
    path:'/register',
    name:'register',
    component:registerView
  },
  {
    path:'/patient',
    name:'patient',
    component:userView,
    children:[
      {path:'/components/user_emr',component:user_emr},
      {path:'/components/user_myself',component:user_myself},
      {path:'/components/user_registrations',component:user_registrations},
      {path:'/components/user_guahao',component:user_guahao},
      {path:'/components/user_huajia',component:user_huajia},
      {path:'/patient',component:maincount},
    ]
  },
  {
    path:'/doctor',
    name:'doctor',
    component:doctor_userView,
    children:[
      {path:'/list/myselflist',component:myselflist},
      {path:'/list/doctor_emrlist',component:emrlist},
      {path:'/list/doctor_modellist',component:modellist},
      {path:'/list/doctor_patientlist',component:patientlist},
      {path: '/emr',name: 'emr',component: emr },  //  route for adding EMR
      {path:'/doctor',component:maincount},
    ]
  },

]
const router = new VueRouter({
  routes
})
export default router
