<template>
    <div id="app" class="hide-native-scrollbar">
        <NavBar/>
        <Header/>
        <Disclaimer/>
        <Section1/>
        <Section10/>
        <TechStack/>
        <Footer/>
    </div>
</template>

<script>

    import NavBar from './components/NavBar.vue'
    import Header from './components/Header.vue'
    import Section1 from './components/Section1.vue'
    import Section10 from './components/Section10.vue'
    import Disclaimer from './components/Disclaimer.vue'
    import TechStack from './components/TechStack.vue'
    import Footer from './components/Footer.vue'
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
        faChevronCircleDown, faChevronDown, faChevronRight, faDatabase,faPalette, faServer, faMale, faHeart
    } from '@fortawesome/free-solid-svg-icons'
    import { faRProject, faPython } from '@fortawesome/free-brands-svg-icons'
    import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

    library.add(faVirus, faPeopleArrows, faHouseUser, faHandsWash, faHeadSideMask, faCheck, faVirusSlash,
        faAngleDoubleRight, faChevronCircleDown, faChevronDown, faChevronRight, faPython, faRProject, faDatabase,
        faPalette, faServer, faMale, faHeart);
    Vue.component('font-awesome-icon', FontAwesomeIcon);

    import {dom} from '@fortawesome/fontawesome-svg-core'

    dom.watch();// This will kick of the initial replacement of i to svg tags and configure a MutationObserver

    export default {
        name: 'App',
        components: {
            NavBar,
            Header,
            Section1,
            Section10,
            Disclaimer,
            TechStack,
            Footer
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
        min-height: 100vh;
    }

    input {
        border: 0 !important;
        border-bottom: solid #42b983 5px !important;
        outline: 0 !important;
        font-size: 40px;
    }

    ::-webkit-scrollbar {display:none;}


    .section-dark{
        background: #F8F8F8
    }

    .card{
        border-radius: 5px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2),0 6px 20px 0 rgba(0,0,0,0.19)!important;
        padding: 50px;
    }


</style>
