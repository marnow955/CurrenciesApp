import '../main.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'


import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './components/App.vue'
import Home from './components/Home.vue'
import Signup from './components/Signup.vue'
import Login from './components/Login.vue'
import Currencies from './components/Currencies.vue'
import Predictions from './components/Predictions.vue'
import Offices from './components/Offices.vue'
import Favourities from './components/Favourities.vue'

import VueRouter from 'vue-router'
import VueResource from 'vue-resource'


Vue.use(BootstrapVue)
Vue.use(VueResource)
Vue.use(VueRouter)
import auth from './auth'

Vue.http.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('id_token');

// Check the user's auth status when the app starts
auth.checkAuth()

export var router = new VueRouter()

router.map({
  '/home': {
    component: Home
  },
  '/login': {
    component: Login
  },
  '/signup': {
    component: Signup
  },
  '/currencies': {
    component: Currencies
  },
  '/favourities': {
    component: Favourities
  },
  '/offices': {
    component: Offices
  },
  '/predictions': {
    component: Predictions
  }
})

router.redirect({
  '*': '/home'
})

router.start(App, '#app')

