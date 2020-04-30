<template>
    <div>
        <b-navbar toggleable="lg" variant="faded" type="light" fixed="top">
            <b-navbar-brand href="#" class="navbar-brand">COVID 19<span style="font-size: 12px"> Beta v0.9.3</span></b-navbar-brand>

            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav class="navbar-nav">
<!--                    <b-nav-item href="#">Link</b-nav-item>-->
<!--                    <b-nav-item href="#" disabled>Disabled</b-nav-item>-->
                </b-navbar-nav>

                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto">
<!--                    <b-nav-form>-->
<!--                        <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>-->
<!--                        <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>-->
<!--                    </b-nav-form>-->

<!--                    <b-nav-item-dropdown text="Lang" right>-->
<!--                        <b-dropdown-item href="#">EN</b-dropdown-item>-->
<!--                        <b-dropdown-item href="#">ES</b-dropdown-item>-->
<!--                        <b-dropdown-item href="#">RU</b-dropdown-item>-->
<!--                        <b-dropdown-item href="#">FA</b-dropdown-item>-->
<!--                    </b-nav-item-dropdown>-->
                    <b-nav-item href="#"><span style="color:white;font-weight: bold; font-size: 20px">@teamcorona</span></b-nav-item>
<!--                    <b-nav-item-dropdown right>-->
                        <!-- Using 'button-content' slot -->
<!--                        <template v-slot:button-content>-->
<!--                            <em>User</em>-->
<!--                        </template>-->

<!--                        <b-dropdown-item href="#">Profile</b-dropdown-item>-->
<!--                        <b-dropdown-item href="#">Sign Out</b-dropdown-item>-->
<!--                    </b-nav-item-dropdown>-->
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </div>
</template>

<script>
    export default {
        name: "NavBar"
    }
</script>

<style scoped>
.navbar-brand{
    color:white!important;
    font-weight: bold;
    font-size: 28px;
}



.navbar-nav{
    color:white!important;
    /*display: none;*/
    /*font-weight: bold;*/

}

    .fixed-top{
        position: absolute!important;
    }
</style>