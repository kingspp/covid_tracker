<template>
    <div class="container">
        <div class="row">
            <div class="col-md-6">
                <line-chart
                        v-if="loaded"
                        :chartdata="chartdata"
                        :options="options"/>
            </div>
        </div>
    </div>
</template>

<script>
    import LineChart from './LineChart'

    export default {
        name: 'LineChartContainer',
        components: {LineChart},
        data: () => ({
            loaded: false,
            chartdata: null
        }),
        async mounted() {
            this.loaded = false;
            try {
                // const { userlist } = await fetch('/api/userlist')
                const dataPromise = this.$http.get(this.$config.url + 'stocks');
                // {"red":"","orange":"","yellow":"","green":"","blue":"","purple":"","grey":""}"
                Promise.all([dataPromise]).then(values => {
                    let chartData = {labels: '', datasets: []};
                    let colors = ['rgb(255, 99, 132)', 'rgb(255, 159, 64)', 'rgb(255, 205, 86)', 'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)',' rgb(153, 102, 255)', 'rgb(201, 203, 207)'];
                    for (let coun = 0; coun < values[0].data.data.length; coun++) {
                        const data = values[0].data.data[coun].stocks;
                        let x = [];
                        let y = [];
                        for (let i = 0; i < data.length; i++) {
                            x.push(data[i][0]);
                            y.push(data[i][1]);
                        }
                        chartData['datasets'].push({
                            "label": values[0].data.data[coun].country,
                            fill:false,
                            backgroundColor:colors[coun],
                            borderColor:colors[coun],
                            "data": y
                        })
                    }

                    this.chartdata = chartData;
                    this.loaded = true
                });
            } catch (e) {
                console.error(e)
            }
        }
    }
</script>