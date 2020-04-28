<template>
    <section>
        <div class="container-fluid">
            <div class="row">
                <div class="col">
                    <h1>How the World is doing?</h1>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <h2 class="text-center">Stock Markets</h2>
                    <line-chart
                            v-if="stockChartLoaded"
                            :chartdata="stockChartData"
                            :options="lineChartOptions"/>
                </div>
                <div class="col-md-6" style="font-size: 36px">
                    <li>On an average the global economy has suffered losses in excess of $36 Trillion (40% of $90
                        Trillion Global GDP)
                    </li>
                    <br/>
                    <li>Though the number of cases are increasing, the panic has stopped and the outlook is positive
                    </li>
                    [Source: Yahoo Finance]
                </div>
            </div>

            <div class="row" style="padding-top: 100px">
                <div class="col-md-4" style="font-size: 36px">
                    <h2 class="text-center">Currencies and Crypto</h2>
                    <li>Irrespective of increase in cases, USD remains world's reserve currency</li>
                    <li>Even crypto-currencies are not spared!</li>
                    <li>Hold on to your dollars $$!</li>
                    [Source: Investing]
                </div>
                <div class="col-md-4">
                    <line-chart
                            v-if="currencyChartLoaded"
                            :chartdata="currencyChartData"
                            :options="lineChartOptions"/>
                </div>
                <div class="col-md-4">
                    <line-chart
                            v-if="cryptoChartLoaded"
                            :chartdata="cryptoChartData"
                            :options="lineChartOptions"/>
                </div>
            </div>
        </div>

        <div class="container-fluid">
            <h2 class="text-center" style="padding-top: 60px">Impact of Social Distancing and Masks</h2>
            <div class="row" style="padding-top: 100px">
                <div class="col-md-6">
                    <div class="row">
                        <div class="col"><h2 class="text-center">Google Mobility Report</h2></div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <bar-chart
                                    v-if="currencyChartLoaded"
                                    :chartdata="currencyChartData"
                                    :options="lineChartOptions"/>
                        </div>
                    </div>
                    <div class="row">
                        <li>Irrespective of increase in cases, USD remains world's reserve currency</li>
                        -->
                        <li>Even crypto-currencies are not spared!</li>
                        <li>Hold on to your dollars $$!</li>
                        [Source: Investing]
                    </div>

                </div>
                <div class="col-md-6">
                    <div class="row">
                        <div class="col"><h2 class="text-center;">Confirmed Cases vs New Cases</h2></div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <bar-chart
                                    v-if="cryptoChartLoaded"
                                    :chartdata="cryptoChartData"
                                    :options="lineChartOptions"/>
                        </div>
                    </div>
                    <div class="row">
                        <li>Irrespective of increase in cases, USD remains world's reserve currency</li>
                        -->
                        <li>Even crypto-currencies are not spared!</li>
                        <li>Hold on to your dollars $$!</li>
                        [Source: Investing]
                    </div>

                </div>
            </div>

            <div class="row" style="padding-top: 100px">
                <div class="col-md-6">
                    <div class="row">
                        <div class="col"><h2 class="text-center">Recovery Factor</h2></div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <bar-chart
                                    v-if="currencyChartLoaded"
                                    :chartdata="currencyChartData"
                                    :options="lineChartOptions"/>
                        </div>
                    </div>
                    <div class="row">
                        <li>Irrespective of increase in cases, USD remains world's reserve currency</li>
                        <li>Even crypto-currencies are not spared!</li>
                        <li>Hold on to your dollars $$!</li>
                        [Source: Investing]
                    </div>

                </div>
                <div class="col-md-6">
                    <div class="row">
                        <div class="col"><h2 class="text-center;">Confirmed Deaths vs New Deaths</h2></div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <bar-chart
                                    v-if="cryptoChartLoaded"
                                    :chartdata="cryptoChartData"
                                    :options="lineChartOptions"/>
                        </div>
                    </div>
                    <div class="row">
                        <li>Irrespective of increase in cases, USD remains world's reserve currency</li>
                        -->
                        <li>Even crypto-currencies are not spared!</li>
                        <li>Hold on to your dollars $$!</li>
                        [Source: Investing]
                    </div>

                </div>
            </div>

        </div>
    </section>
</template>

<script>
    import LineChart from './LineChart'
    import BarChart from './BarChart'

    import * as changeCase from "change-case";

    export default {
        name: 'Section1',
        components: {LineChart, BarChart},
        data: () => ({
            currencyChartLoaded: false,
            stockChartLoaded: false,
            cryptoChartLoaded: false,
            stockChartData: {},
            currencyChartData: {},
            cryptoChartData: {},
            lineChartOptions: {
                responsive: true,
                maintainAspectRatio: false,
                elements: {
                    point: {
                        radius: 0
                    }
                }
            }
        }),
        async mounted() {
            this.loaded = false;
            try {
                // const { userlist } = await fetch('/api/userlist')
                const stockDataPromise = this.$http.get(this.$config.url + 'stocks');
                const currencyDataPromise = this.$http.get(this.$config.url + 'currencies');
                const cryptoDataPromise = this.$http.get(this.$config.url + 'crypto');
                // {"red":"","orange":"","yellow":"","green":"","blue":"","purple":"","grey":""}"
                Promise.all([stockDataPromise]).then(values => {

                    let x = [];
                    let s = values[0].data.data[3].stocks;
                    for (let i = 0; i < s.length; i++) {
                        x.push(s[i][0])
                    }
                    let stockChartData = {labels: x, datasets: []};
                    let colors = ['rgb(255, 99, 132)', 'rgb(255, 159, 64)', 'rgb(255, 205, 86)', 'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)', 'rgb(153, 102, 255)', "#000000"];
                    for (let coun = 0; coun < values[0].data.data.length; coun++) {
                        const data = values[0].data.data[coun].stocks;
                        // let x = [];
                        let y = [];
                        for (let i = 0; i < data.length; i++) {
                            // x.push(data[i][0]);

                            if (x.indexOf(data[i][0]) > -1)
                                y.push(data[i][1]);
                        }
                        stockChartData['datasets'].push({
                            "label": values[0].data.data[coun].country,
                            fill: false,
                            backgroundColor: colors[coun],
                            borderColor: colors[coun],
                            "data": y
                        })
                    }

                    this.stockChartData = stockChartData;
                    this.stockChartLoaded = true
                });

                Promise.all([currencyDataPromise]).then(values => {

                    let x = [];
                    let s = values[0].data.data[3].currencies;
                    for (let i = 0; i < s.length; i++) {
                        x.push(s[i][0])
                    }
                    let currencyChartData = {labels: x, datasets: []};
                    let colors = ['rgb(255, 99, 132)', 'rgb(255, 159, 64)', 'rgb(255, 205, 86)', 'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)', 'rgb(153, 102, 255)', "#000000"];
                    for (let coun = 0; coun < values[0].data.data.length; coun++) {
                        const data = values[0].data.data[coun].currencies;
                        // let x = [];
                        let y = [];
                        for (let i = 0; i < data.length; i++) {
                            // x.push(data[i][0]);

                            if (x.indexOf(data[i][0]) > -1)
                                y.push(data[i][1]);
                        }
                        currencyChartData['datasets'].push({
                            "label": values[0].data.data[coun].country,
                            fill: false,
                            backgroundColor: colors[coun],
                            borderColor: colors[coun],
                            "data": y
                        })
                    }
                    this.currencyChartData = currencyChartData;
                    this.currencyChartLoaded = true
                });

                Promise.all([cryptoDataPromise]).then(values => {

                    let x = [];
                    let s = values[0].data.data[2].crypto;
                    for (let i = 0; i < s.length; i++) {
                        x.push(s[i][0])
                    }
                    let cryptoChartData = {labels: x, datasets: []};
                    let colors = ['rgb(255, 99, 132)', 'rgb(255, 159, 64)', 'rgb(255, 205, 86)', 'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)', 'rgb(153, 102, 255)', "#000000"];
                    for (let coun = 0; coun < values[0].data.data.length; coun++) {
                        const data = values[0].data.data[coun].crypto;
                        // let x = [];
                        let y = [];
                        for (let i = 0; i < data.length; i++) {
                            // x.push(data[i][0]);

                            if (x.indexOf(data[i][0]) > -1)
                                y.push(data[i][1]);
                        }
                        cryptoChartData['datasets'].push({
                            "label": values[0].data.data[coun].country,
                            fill: false,
                            backgroundColor: values[0].data.data[coun].country === 'COVID-19' ? "#000000" : colors[coun],
                            borderColor: values[0].data.data[coun].country === 'COVID-19' ? "#000000" : colors[coun],
                            "data": y
                        })
                    }
                    this.cryptoChartData = cryptoChartData;
                    this.cryptoChartLoaded = true
                });

            } catch (e) {
                console.error(e)
            }
        }
    }
</script>