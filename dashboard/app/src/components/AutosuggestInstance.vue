<template>
  <div class="container">
    <vue-autosuggest
      class="hello"
      ref="autosuggest"
      v-model="query"
      :suggestions="suggestions"
      :input-props="inputProps"
      :section-configs="sectionConfigs"
      :get-suggestion-value="getSuggestionValue"
      @input="fetchResults"
    >
      <template slot-scope="{ suggestion }">
        <div>
          {{ suggestion.item }}
        </div>
      </template>
    </vue-autosuggest>
  </div>
</template>

<script>
    import {VueAutosuggest} from "vue-autosuggest";
    import axios from "axios";
    import config from "../config";

    export default {
        name: "App",
        components: {
            VueAutosuggest
        },
        props:{
            autoType:String
        },
        data() {
            return {
                query: "",
                results: [],
                timeout: null,
                selected: null,
                searchText: "",
                debounceMilliseconds: 50,
                fetchURL: config.url + this.autoType.toLowerCase(),

                inputProps: {
                    id: "autosuggest__input",
                    style: {width: "100%"},
                    placeholder: this.autoType,
                },
                suggestions: [],
                sectionConfigs: {
                    destinations: {
                        limit: 6,
                        label: "Destination",
                        onSelected: selected => {
                            this.selected = selected.item;
                        }
                    },
                    default: {
                        onSelected: () => {
                            this.doSearch(this);
                        }
                    }
                }
            };
        },
        methods: {
            doSearch() {
                console.log("Searching...");
            },
            fetchResults() {
                const query = this.query;

                clearTimeout(this.timeout);
                this.timeout = setTimeout(() => {
                    const dataPromise = axios.get(this.fetchURL);
                    Promise.all([dataPromise]).then(values => {
                        this.suggestions = [];
                        this.selected = null;
                        const data = this.filterResults(values[0].data.data, query, "name");
                        data.length &&
                        this.suggestions.push({name: "destinations", data: data});
                    });
                }, this.debounceMilliseconds);
            },
            filterResults(data, text, field) {
                return data
                    .filter(item => {
                        if (item.toLowerCase().indexOf(text.toLowerCase()) > -1) {
                            return item;
                        }
                    })
                    .sort();
            },
            getSuggestionValue(suggestion) {
                let {name, item} = suggestion;
                // return name === "hotels" ? item.title : item.name;
                console.log(item)
                return item;
            }
        },
        watch: {
            suggestions(n, o) {
                // console.log({ n, o });
            }
        }
    };
</script>

<style>
    #app {
        font-family: "Avenir", Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        color: #2c3e50;
        margin-top: 60px;
    }

    .avatar {
        height: 25px;
        width: 25px;
        border-radius: 20px;
        margin-right: 10px;
    }

    #autosuggest__input {
        outline: none;
        position: relative;
        display: block;
        border: 1px solid #616161;
        padding: 10px;
        width: 100%;
        box-sizing: border-box;
        -webkit-box-sizing: border-box;
        -moz-box-sizing: border-box;
    }

    #autosuggest__input.autosuggest__input-open {
        border-bottom-left-radius: 0;
        border-bottom-right-radius: 0;
    }

    .autosuggest__results-container {
        position: inline;

        width: 100%;
    }

    .autosuggest__results {
        font-weight: 300;
        margin: 0;
        position: absolute;
        z-index: 10000001;
        width: 100%;
        border: 1px solid #e0e0e0;
        border-bottom-left-radius: 4px;
        border-bottom-right-radius: 4px;
        background: white;
        padding: 0px;
        max-height: 400px;
        overflow-y: scroll;
    }

    .autosuggest__results ul {
        list-style: none;
        padding-left: 0;
        margin: 0;
    }

    .autosuggest__results .autosuggest__results-item {
        cursor: pointer;
        padding: 15px;
    }

    #autosuggest ul:nth-child(1) > .autosuggest__results-before {
        border-top: none;
    }

    .autosuggest__results .autosuggest__results-before {
        color: gray;
        font-size: 11px;
        margin-left: 0;
        padding: 15px 13px 5px;
        border-top: 1px solid lightgray;
    }

    .autosuggest__results .autosuggest__results-item:active,
    .autosuggest__results .autosuggest__results-item:hover,
    .autosuggest__results .autosuggest__results-item:focus,
    .autosuggest__results
    .autosuggest__results-item.autosuggest__results-item--highlighted {
        background-color: #f6f6f6;
    }
</style>
