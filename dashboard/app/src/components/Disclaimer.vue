<template>
    <section style="min-height: 400px">
        <h1>Disclaimer</h1>
        <p style="text-align: justify; font-size: 28px">{{disclaimer}}</p>
    </section>

</template>

<script>
    export default {
        name: "Disclaimer",
        data:function(){
            return {
                disclaimer:"Content from this presentation is STRICTLY ONLY for educational and research purposes and may contain errors. The model and data are inaccurate to the complex, evolving, and heterogeneous realities of different countries and are not directed towards any person, group, nationality or ethnicity. Predictions are uncertain by nature and are impressions of what the data reflects. Readers must take any predictions with caution. Overly optimism based on some predicted end dates is dangerous because it may loosen our disciplines and controls and cause the turnaround of the virus and must be avoided.​"
            }
        }
    }
</script>

<style scoped>

</style>