<template>
    <section>
        <div class="container-fluid">
            <div class="row"><h1>How the World is doing?</h1></div>
            <div class="row" style="height: 200px;">
                <div class="col-md-6">
                    <line-chart
                            v-if="loaded"
                            :chartdata="chartdata"
                            :options="options"/>
                </div>
                <div class="col-md-6" style="font-size: 36px">
                    <li>On an average the global economy has suffered losses in exess of 36 T$ (40% of 90 T$ Global GDP)</li><br/>
                    <li>Though the number of cases are increasing, the panic has stopped and the outlook is positive</li>
                </div>
            </div>

        </div>
    </section>
</template>

<script>
    import LineChart from './LineChart'

    export default {
        name: 'LineChartContainer',
        components: {LineChart},
        data: () => ({
            loaded: false,
            chartdata: null,
            options:{
                responsive:true,
                maintainAspectRatio: false,
                elements: {
                    point:{
                        radius: 0
                    }
                }
            }
        }),
        async mounted() {
            this.loaded = false;
            try {
                // const { userlist } = await fetch('/api/userlist')
                const dataPromise = this.$http.get(this.$config.url + 'stocks');
                // {"red":"","orange":"","yellow":"","green":"","blue":"","purple":"","grey":""}"
                Promise.all([dataPromise]).then(values => {

                    let x = [];
                    let s = values[0].data.data[3].stocks;
                    for (let i = 0; i < s.length; i++) {
                        x.push(s[i][0])
                    }
                    let chartData = {labels: x, datasets: []};
                    let colors = ['rgb(255, 99, 132)', 'rgb(255, 159, 64)', 'rgb(255, 205, 86)', 'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)', 'rgb(153, 102, 255)', "#000000"];
                    for (let coun = 0; coun < values[0].data.data.length; coun++) {
                        const data = values[0].data.data[coun].stocks;
                        // let x = [];
                        let y = [];
                        for (let i = 0; i < data.length; i++) {
                            // x.push(data[i][0]);

                            if(x.indexOf(data[i][0]) > -1)
                                y.push(data[i][1]);
                        }
                        console.log(y);
                        chartData['datasets'].push({
                            "label": values[0].data.data[coun].country,
                            fill: false,
                            backgroundColor: colors[coun],
                            borderColor: colors[coun],
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