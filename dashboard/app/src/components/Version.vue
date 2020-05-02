<template>
    <span> {{version}}</span>
</template>

<script>
    import {getCommitVersion, getReleaseVersion} from 'autoversion';
    export default {
        name: "Version",
        data: function () {
            return {
                version: "v"+getCommitVersion('kingspp','covid19_research'),
                fontsize: "",
            }
        }
    }
</script>

<style scoped>

</style>