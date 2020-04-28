<template>
    <div id="app">
        <NavBar/>
        <Header/>
        <Section1/>
        <Section10/>
    </div>
</template>

<script>

    import NavBar from './components/NavBar.vue'
    import Header from './components/Header.vue'
    import Section1 from './components/Section1.vue'
    import Section10 from './components/Section10.vue'
    import Vue from 'vue'

    import {BootstrapVue, IconsPlugin} from 'bootstrap-vue'
    import 'bootstrap/dist/css/bootstrap.css'
    import 'bootstrap-vue/dist/bootstrap-vue.css'
    // Install BootstrapVue
    Vue.use(BootstrapVue);
    // Optionally install the BootstrapVue icon components plugin
    Vue.use(IconsPlugin);


    // import VTooltip from 'v-tooltip'

    // Vue.use(VTooltip);


    // import ECharts from 'vue-echarts'
    // Vue.component('v-chart', ECharts);


    import Axios from "axios";
    Vue.prototype.$http = Axios;

    import config from "./config";
    Vue.prototype.$config = config;



    import {library} from '@fortawesome/fontawesome-svg-core'
    import {
        faVirus, faPeopleArrows, faHouseUser, faHandsWash, faHeadSideMask, faCheck, faVirusSlash, faAngleDoubleRight,
        faChevronCircleDown, faChevronDown
    } from '@fortawesome/free-solid-svg-icons'
    import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

    library.add(faVirus, faPeopleArrows, faHouseUser, faHandsWash, faHeadSideMask, faCheck, faVirusSlash,
        faAngleDoubleRight, faChevronCircleDown, faChevronDown);
    Vue.component('font-awesome-icon', FontAwesomeIcon);

    import {dom} from '@fortawesome/fontawesome-svg-core'

    dom.watch();// This will kick of the initial replacement of i to svg tags and configure a MutationObserver

    export default {
        name: 'App',
        components: {
            NavBar,
            Header,
            Section1,
            Section10
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

    section {
        padding: 100px;
        height: 100vh;
    }

    input {
        border: 0 !important;
        border-bottom: solid #42b983 5px !important;
        outline: 0 !important;
        font-size: 40px;
    }


</style>
