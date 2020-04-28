<template>
    <section class="question">
        <div class="row">
            <p><b>Wanna know your chances in this pandemic?</b></p>
        </div>
        <div class="row">
            <div class="col-md-2">
                <span style="">I am from </span>
            </div>
            <div class="col-md-7">
                <div class="autosuggest-container" style="">
                    <autosuggest-instance :key="1" auto-type="County"/>
                </div>
            </div>
            <div class="col-md-2">
                <span style="">aged </span>
                <b-form-input type="number" style="width:3em; display: inline-block"/>
            </div>
        </div>

        <div class="row" style="padding-top: 50px">
            <div class="col-md-2 offset-1">
                <span style=""> belonging to </span>
            </div>
            <div class="col-md-7">
                <div class="autosuggest-container" style="">
                    <autosuggest-instance :key="2" auto-type="Ethnicity"/>
                </div>
            </div>
        </div>

        <div class="row">
        </div>

        <div class="row" style="height: 400px">
            <span>Variables:</span>
            <div class="col-md-8 offset-1">
                <vue-word-cloud
                        style="position:absolute;"
                        :words="words"
                        :color="colors"
                        :spacing="spacing"
                        :snackbarText="''"
                        :progressVisible="true"
                        font-family="Roboto">
                    <template slot-scope="{text, weight}">
                        <div :title="text+' (W:'+ weight+')'" style="cursor: pointer;">
                            <div style="text-align: center;">{{text}}</div>
                        </div>
                    </template>
                </vue-word-cloud>
            </div>
        </div>

        <div class="row">
            <div class="col" style="color: black; font-size: 60px;">
                <div style="">
                    <font-awesome-icon icon="chevron-down"/>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
    import VueWordCloud from 'vuewordcloud';
    import AutosuggestInstance from "./AutosuggestInstance";
    // import Vue from 'vue';

    // Vue.component(VueWordCloud.name, VueWordCloud);


    export default {
        name: "Section1",
        components: {
            AutosuggestInstance,
            VueWordCloud
        },
        data: function () {
            return {
                // drawer: true,
                // fontSizeRatioValues: [0, 1 / 20, 1 / 5, 1 / 2, 1],
                // progress: undefined,
                // progressVisible: true,
                // rotationItemIndex: undefined,
                // snackbarText: '',
                // snackbarVisible: false,
                spacing: 2,
                // spacingValueIndex: 1,
                // spacingValues: [0, 1 / 4, 1 / 2, 1, 2],
                words: [['White', 0.6083505425400902], ['White', 0.873334764652425], ['Black', 0.9569713630340182], ['Black', 0.692588690952467], ['Ameri', 0.9232343696463737], ['Ameri', 0.2890185759097694], ['Asian', 0.10240036496155547], ['Asian', 0.20034511319586623], ['Nativ', 0.3544325155788284], ['Nativ', 0.3764106852907453], ['Not H', 0.9259030432889365], ['Not H', 0.12907901908498953], ['Not H', 0.5889146131102185], ['Not H', 0.1700541238783856], ['Not H', 0.5227741919367936], ['Not H', 0.38231429809007367], ['Not H', 0.35622667506597316], ['Not H', 0.05445444888944573], ['Not H', 0.3084309425580064], ['Not H', 0.19271706815968004], ['Not H', 0.3744384326588812], ['Not H', 0.2972297192053355], ['Hispa', 0.9242233028438677], ['Hispa', 0.9783904855518989], ['Hispa', 0.10486372234965613], ['Hispa', 0.2960361219630039], ['Hispa', 0.6243363487202025], ['Hispa', 0.30796248001651205], ['Hispa', 0.253007227205585], ['Hispa', 0.17970213881722807], ['Hispa', 0.9491128197493495], ['Hispa', 0.21508787147161834], ['Hispa', 0.6856650223772554], ['Hispa', 0.9269017784952683]],
                colors: ([, weight]) => weight > 0.9 ? '#F11712' : weight > 0.75 ? '#B3384D' : weight > 0.35 ? '#6C5F90' : '#0099F7'
            }
        },
        watch: {
            progress: function (currentProgress, previousProgress) {
                if (previousProgress) {
                    this.progressVisible = false;
                }
            },
        },
        methods: {
            onWordClick: function (word) {
                this.snackbarVisible = true;
                this.snackbarText = word[0];
            }
        }

    }


</script>

<style scoped>
    .question {
        font-size: 40px;
    }

    /*.autosuggest__results-container {*/
    /*    position: absolute !important;*/
    /*    background: #2c3e50;*/
    /*    opacity: 0.45;*/
    /*}*/
    /*.demo {*/
    /*    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;*/
    /*}*/

    /*input {*/
    /*    width: 260px;*/
    /*    padding: 0.5rem;*/
    /*}*/

    /*ul {*/
    /*    width: 100%;*/
    /*    color: rgba(30, 39, 46, 1.0);*/
    /*    list-style: none;*/
    /*    margin: 0;*/
    /*    padding: 0.5rem 0 .5rem 0;*/
    /*}*/

    /*li {*/
    /*    margin: 0 0 0 0;*/
    /*    border-radius: 5px;*/
    /*    padding: 0.75rem 0 0.75rem 0.75rem;*/
    /*    display: flex;*/
    /*    align-items: center;*/
    /*}*/

    /*li:hover {*/
    /*    cursor: pointer;*/
    /*}*/

    /*.autosuggest-container {*/
    /*display: inline-block;*/
    /*position: absolute;*/
    /*justify-content: center;*/
    /*border: 0;*/
    /*width: 280px;*/
    /*}*/

    input {
        border: 0 !important;
        border-bottom: solid #42b983 5px !important;
        outline: 0 !important;
        font-size: 40px;
    }

    /*input:focus {*/
    /*    outline: none !important;*/
    /*}*/

    /*#autosuggest { width: 100%; display: block;}*/
    /*.autosuggest__results-item--highlighted {*/
    /*    background-color: rgba(51, 217, 178, 0.2);*/
    /*}*/

    /*#autosuggest input {*/
    /*    border: 0 !important;*/
    /*}*/


    .tooltip {
        display: block !important;
        z-index: 10000;
    }

    .tooltip .tooltip-inner {
        background: black;
        color: white;
        border-radius: 16px;
        padding: 5px 10px 4px;
    }

    .tooltip .tooltip-arrow {
        width: 0;
        height: 0;
        border-style: solid;
        position: absolute;
        margin: 5px;
        border-color: black;
        z-index: 1;
    }

    .tooltip[x-placement^="top"] {
        margin-bottom: 5px;
    }

    .tooltip[x-placement^="top"] .tooltip-arrow {
        border-width: 5px 5px 0 5px;
        border-left-color: transparent !important;
        border-right-color: transparent !important;
        border-bottom-color: transparent !important;
        bottom: -5px;
        left: calc(50% - 5px);
        margin-top: 0;
        margin-bottom: 0;
    }

    .tooltip[x-placement^="bottom"] {
        margin-top: 5px;
    }

    .tooltip[x-placement^="bottom"] .tooltip-arrow {
        border-width: 0 5px 5px 5px;
        border-left-color: transparent !important;
        border-right-color: transparent !important;
        border-top-color: transparent !important;
        top: -5px;
        left: calc(50% - 5px);
        margin-top: 0;
        margin-bottom: 0;
    }

    .tooltip[x-placement^="right"] {
        margin-left: 5px;
    }

    .tooltip[x-placement^="right"] .tooltip-arrow {
        border-width: 5px 5px 5px 0;
        border-left-color: transparent !important;
        border-top-color: transparent !important;
        border-bottom-color: transparent !important;
        left: -5px;
        top: calc(50% - 5px);
        margin-left: 0;
        margin-right: 0;
    }

    .tooltip[x-placement^="left"] {
        margin-right: 5px;
    }

    .tooltip[x-placement^="left"] .tooltip-arrow {
        border-width: 5px 0 5px 5px;
        border-top-color: transparent !important;
        border-right-color: transparent !important;
        border-bottom-color: transparent !important;
        right: -5px;
        top: calc(50% - 5px);
        margin-left: 0;
        margin-right: 0;
    }

    .tooltip.popover .popover-inner {
        background: #f9f9f9;
        color: black;
        padding: 24px;
        border-radius: 5px;
        box-shadow: 0 5px 30px rgba(black, .1);
    }

    .tooltip.popover .popover-arrow {
        border-color: #f9f9f9;
    }

    .tooltip[aria-hidden='true'] {
        visibility: hidden;
        opacity: 0;
        transition: opacity .15s, visibility .15s;
    }

    .tooltip[aria-hidden='false'] {
        visibility: visible;
        opacity: 1;
        transition: opacity .15s;
    }
</style>