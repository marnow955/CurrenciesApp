<template>
  <nav class="navbar navbar-default">
    <div class="container">
      <ul class="nav navbar-nav">
        <li><a v-link="'home'">Home</a></li>
        <li v-if="!user.authenticated"><a v-link="'login'">Login</a></li>
        <li v-if="!user.authenticated"><a v-link="'signup'">Sign Up</a></li>
        <li><a v-link="'currencies'">Currencies</a></li>
        <li v-if="user.authenticated"><a v-link="'predictions'">Predictions</a></li>
        <li v-if="user,authenticated"><a v-link="'favourities'">Favourities</a></li>
        <li v-if="user.authenticated"><a v-link="'login'" @click="logout()">Logout</a></li>
      </ul>
    </div>
  </nav>
  <div class="container">
    <router-view></router-view>
  </div>
</template>

<script>
import auth from '../auth'

export default {
  data() {
    return {
      user: auth.user
    }
  },

  methods: {

    logout() {
      auth.logout()
    }
  }
}
</script>
