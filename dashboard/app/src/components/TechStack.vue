<template>
    <section>
        <div class="container-fluid">
            <h1>Tech Stack</h1>
            <div class="row">
                <div class="col-4 card offset-1">
                    <h2>Data Analysis</h2>
                    <div class="row">
                        <div class="col">
                            <font-awesome-icon :icon="['fab', 'python']" style="font-size: 40px"/>
                        </div>
                        <div class="col">
                            <font-awesome-icon :icon="['fab', 'r-project']" style="font-size: 40px"/>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col" style="text-align: justify; font-size: 20px">
                            <li>Dplyr-R for EDA</li>
                            <li>Stats Models-Python for EDA</li>
                            <li>Mongo Charts</li>
                        </div>
                    </div>
                </div>

                <div class="col-4 card offset-2">
                    <h2>
                        <font-awesome-icon :icon="['fas', 'database']" style="font-size: 30px"/>
                        Database
                    </h2>
                    <div class="row">
                        <div class="col" style="text-align: justify; font-size: 20px">
                            <li>NoSQL Database - Mongodb</li>
                            <li>88 Different Sources</li>
                            <li>118 Attributes</li>
                            <li>Types - Demographics, Derived and Timeseries</li>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-4 card offset-1">
                    <h2><font-awesome-icon :icon="['fas', 'palette']" style="font-size: 30px"/> Frontend</h2>
                    <div class="row">
                        <div class="col">
                            <span style="font-size: 30px"> Vue JS</span>
                        </div>
                    </div>
                </div>

                <div class="col-4 card offset-2">
                    <h2><font-awesome-icon :icon="['fas', 'server']" style="font-size: 30px"/> Backend</h2>
                    <div class="row">
                        <div class="col">
                            <span style="font-size: 30px"> Python - Fast API</span>
                        </div>
                    </div>
                </div>


            </div>
        </div>

    </section>
</template>

<script>
    export default {
        name: "TechStack"
    }
</script>

<style scoped>
    .row {
        padding: 20px;
    }

    .col {
        padding: 10px;
    }
</style>