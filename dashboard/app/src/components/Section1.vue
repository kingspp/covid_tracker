

<!--&lt;!&ndash;            <p>1. Stocks 2.Crypto 3.Currencies 4.Mobility 5. Other diseases</p>&ndash;&gt;-->




<template>
    <section>
        <div class="container-fluid">
            <div class="row"><h1>How the World is doing?</h1></div>
            <div class="row">
                <div class="col-md-6">
                    <v-chart :options="line"/>
                </div>
                <div class="col-md-6">
                    <ul>
                        <li>Global Percent Drop</li>
                    </ul>
                </div>
            </div>
        </div>

    </section>
</template>

<style>
    /**
     * The default size is 600px×400px, for responsive charts
     * you may need to set percentage values as follows (also
     * don't forget to provide a size for the container).
     */
    .echarts {
        width: 600px;
        height: 400px;
    }
</style>

<script>
    import ECharts from 'vue-echarts'
    import 'echarts/lib/chart/line'
    import 'echarts/lib/component/polar'
    import "echarts/lib/component/dataZoom";
    import "echarts/lib/component/tooltip";

    var data = [];
    var now = +new Date(1997, 9, 3);
    var oneDay = 24 * 3600 * 1000;
    var value = Math.random() * 1000;
    for (var i = 0; i < 1000; i++) {
        data.push(randomData());
    }

    function randomData() {
        now = new Date(+now + oneDay);
        value = value + Math.random() * 21 - 10;
        return {
            name: now.toString(),
            value: [
                [now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'),
                Math.round(value)
            ]
        };
    }

    export default {
        name: "Section1",
        components: {
            'v-chart': ECharts
        },
        data () {
            var indiaData=[];
            // usData,ukData,chinaData,japanData,italyData
            // var now = +new Date(1997, 9, 3);
            // var oneDay = 24 * 3600 * 1000;
            // var value = Math.random() * 1000;
            // for (var i = 0; i < 1000; i++) {
            //     data.push(randomData());
            // }

            // ;

            return {
                indiaData:[],
                line:{
                    title: {
                        text: '动态数据 + 时间坐标轴'
                    },
                    tooltip: {
                        trigger: 'axis',
                        formatter: function (params) {
                            params = params[0];
                            var date = new Date(params.name);
                            return date.getDate() + '/' + (date.getMonth() + 1) + '/' + date.getFullYear() + ' : ' + params.value[1];
                        },
                        axisPointer: {
                            animation: false
                        }
                    },
                    xAxis: {
                        type: 'time',
                        splitLine: {
                            show: false
                        }
                    },
                    yAxis: {
                        type: 'value',
                        boundaryGap: [0, '100%'],
                        splitLine: {
                            show: false
                        }
                    },
                    series: [{
                        name: 'India',
                        type: 'line',
                        showSymbol: false,
                        hoverAnimation: false,
                        data: this.indiaData
                    }]
                },
                fetchURL: this.$config.url + 'stocks',
            }
        },
        mounted() {
            this.timeout = setTimeout(() => {
                const dataPromise = this.$http.get(this.fetchURL);
                Promise.all([dataPromise]).then(values => {
                    this.indiaData = [];
                    console.log(values[0].data.data[0].stocks);
                    this.indiaData.push(values[0].data.data[0].stocks)

                    // const data = this.filterResults(values[0].data.data, query, "name");
                    // data.length &&
                    // this.suggestions.push({name: "destinations", data: data});
                });
            }, this.debounceMilliseconds);
        }
    }
</script>