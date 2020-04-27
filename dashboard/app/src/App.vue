<template>
  <div id="app">
    <NavBar/>
    <Header/>
<!--    <img alt="Vue logo" src="./assets/logo.png">-->
<!--    <HelloWorld msg="Welcome to Your Corona App"/>-->

  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import NavBar from './components/NavBar.vue'
import Header from './components/Header.vue'
// import { BModal, VBModal, BNavbar } from 'bootstrap-vue'
import Vue from 'vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)




import { library } from '@fortawesome/fontawesome-svg-core'
import { faVirus, faPeopleArrows, faHouseUser, faHandsWash, faHeadSideMask, faCheck, faVirusSlash, faAngleDoubleRight, faChevronCircleDown} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faVirus, faPeopleArrows, faHouseUser, faHandsWash, faHeadSideMask, faCheck, faVirusSlash, faAngleDoubleRight, faChevronCircleDown);
Vue.component('font-awesome-icon', FontAwesomeIcon);

import { dom } from '@fortawesome/fontawesome-svg-core'
dom.watch();// This will kick of the initial replacement of i to svg tags and configure a MutationObserver

export default {
  name: 'App',
  components: {
    NavBar,
    Header
    // HelloWorld
  }
}


</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
</style>
