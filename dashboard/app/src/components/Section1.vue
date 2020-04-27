<template>
    <section class="question">
        <div class="autosuggest__results-container" style="display: none"></div>
        <div class="autosuggest__input--open" style="display: none"></div>
        <div><span style="margin-left: -6em;">I am from </span>
            <div class="autosuggest-container" style="display: inline-block">
                <autosuggest-instance :key="1" auto-type="County" />
            </div>
            <span style="margin-left: 11em;">aged </span>
            <b-form-input type="number" style="width:3em; display: inline-block"/>
            <span> belonging to</span> <div class="autosuggest-container" style="display: inline-block">
                <autosuggest-instance :key="2" auto-type="Ethnicity"/>
            </div>
        </div>
    </section>
</template>

<script>
    import AutosuggestInstance from "./AutosuggestInstance";
    // Vue.use(VueAutosuggest);
    export default {
        name: "Section1",
        components:{
            AutosuggestInstance
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

    ul {
        width: 100%;
        color: rgba(30, 39, 46, 1.0);
        list-style: none;
        margin: 0;
        padding: 0.5rem 0 .5rem 0;
    }

    li {
        margin: 0 0 0 0;
        border-radius: 5px;
        padding: 0.75rem 0 0.75rem 0.75rem;
        display: flex;
        align-items: center;
    }

    li:hover {
        cursor: pointer;
    }

    .autosuggest-container {
        display: inline-block;
        position: absolute;
        justify-content: center;
        border:0;
        /*width: 280px;*/
    }

    input {
        border:0!important;
        border-bottom: solid #42b983 5px!important;
        outline: 0!important;
        font-size: 40px;
    }

    input:focus {
        outline: none !important;
    }

    /*#autosuggest { width: 100%; display: block;}*/
    .autosuggest__results-item--highlighted {
        background-color: rgba(51, 217, 178, 0.2);
    }

    #autosuggest input{
        border:0!important;
    }
</style>