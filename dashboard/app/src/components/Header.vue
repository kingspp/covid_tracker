<template>
    <header>
        <div class="container h-100">
            <div class="row" style="text-align: center;color: white; font-size: 60px">
                <div class="col-md-2">
                    <font-awesome-icon icon="people-arrows"/>
                </div>
                <div class="col-md-2">
                    <font-awesome-icon icon="house-user"/>
                </div>
                <div class="col-md-2">
                    <font-awesome-icon icon="hands-wash"/>
                </div>
                <div class="col-md-2">
                    <font-awesome-icon icon="head-side-mask"/>
                </div>
                <div class="col-md-2">
                    <font-awesome-icon icon="angle-double-right"/>
                </div>
                <div class="col-md-2">
                    <font-awesome-icon icon="virus-slash"/>
                </div>
            </div>
            <div class="row h-100" style="margin-top:-80px">
                <div class="col-lg-7 my-auto">
                    <div class="header-content mx-auto">
                        <!--                    <h1 class="mb-5" style="color: #FFF">COVID-19 has impacted over <b>119</b> countries, infecting-->
                        <!--                        <b>2m</b> people, of which  <b>38%</b> have recovered! <br><span style="font-size: 0.4em">- Source Github (May 02)</span>-->
                        <!--                    </h1>-->
                        <h1 style="color:white">COVID-19
                            <span
                                    class="txt-rotate"
                                    data-period="4000"
                                    data-rotate='[ "has impacted over 119 countries.", "has infected 2m people of which 38% have recovered!"]'></span>
                        </h1>

                    </div>
                </div>
                <div class="col-lg-5 my-auto">
                    <div class="device-container">
                        <div class="device-mockup iphone6_plus portrait white">
                            <div class="device">
                                <div class="screen">
                                    <font-awesome-icon icon="virus" class="brand-icon-1"
                                                       style="padding-bottom: 45px"/>
                                    <font-awesome-icon icon="virus" class="brand-icon-2"/>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col" style="color: white; font-size: 60px; margin-top: -20px">
                    <div style="">
                        <font-awesome-icon icon="chevron-circle-down"/>
                    </div>
                </div>
            </div>
        </div>
    </header>
</template>

<script>
    var TxtRotate = function (el, toRotate, period) {
        this.toRotate = toRotate;
        this.el = el;
        this.loopNum = 0;
        this.period = parseInt(period, 10) || 2000;
        this.txt = '';
        this.tick();
        this.isDeleting = false;
    };

    TxtRotate.prototype.tick = function () {
        var i = this.loopNum % this.toRotate.length;
        var fullTxt = this.toRotate[i];

        if (this.isDeleting) {
            this.txt = fullTxt.substring(0, this.txt.length - 1);
        } else {
            if (this.toRotate[this.txt.length] === "<")
                this.txt = fullTxt.substring(0, this.txt.length + 3);
            else
                this.txt = fullTxt.substring(0, this.txt.length + 1);
        }

        this.el.innerHTML = '<span class="wrap">' + this.txt + '</span>';

        var that = this;
        var delta = 100 - Math.random() * 100;

        if (this.isDeleting) {
            delta /= 2;
        }

        if (!this.isDeleting && this.txt === fullTxt) {
            delta = this.period;
            this.isDeleting = true;
        } else if (this.isDeleting && this.txt === '') {
            this.isDeleting = false;
            this.loopNum++;
            delta = 500;
        }

        setTimeout(function () {
            that.tick();
        }, delta);
    };

    window.onload = function () {
        var elements = document.getElementsByClassName('txt-rotate');
        for (var i = 0; i < elements.length; i++) {
            var toRotate = elements[i].getAttribute('data-rotate');
            var period = elements[i].getAttribute('data-period');
            if (toRotate) {
                new TxtRotate(elements[i], JSON.parse(toRotate), period);
            }
        }
        // INJECT CSS
        var css = document.createElement("style");
        css.type = "text/css";
        css.innerHTML = ".txt-rotate > .wrap { border-right: 0.08em solid #FFF;}";
        document.body.appendChild(css);
    };
    export default {
        name: "Header"
    }
</script>

<style scoped>
    header {
        position: relative;
        width: 100%;
        height: 100vh;
        padding-top: 150px;
        padding-bottom: 100px;
        /*color: #000;*/
        /*background: url("./assets/bg-pattern.png"), #7b4397;*/
        /* background: url("../img/bg-pattern.png"), -webkit-gradient(linear, right top, left top, from(#7b4397), to(#dc2430)); */
        /*background: url("../assets/bg-pattern.png"), linear-gradient(to left, #7b4397, #dc2430);*/
        background: url("../assets/bg-pattern.png"), linear-gradient(90deg, rgba(63, 94, 251, 1) 0%, rgba(252, 70, 107, 1) 100%);
        /*radial-gradient(circle, rgba(63,94,251,1) 0%, rgba(252,70,107,1) 100%);*/
        /*linear-gradient(120deg, #155799, #159957);*/
    }

    .header-content h1 {
        font-size: 55px;
    }

    .brand-icon-1 {
        color: white;
        font-size: 300px;
    }

    .brand-icon-2 {
        color: white;
        font-size: 100px;
    }

    .brand-icon-1 {
        -webkit-animation: breathing 7s ease-out infinite normal;
        animation: breathing 7s ease-out infinite normal;
        -webkit-font-smoothing: antialiased;
    }

    .brand-icon-2 {
        -webkit-animation: breathing 3s ease-out infinite normal;
        animation: breathing 3s ease-out infinite normal;
        -webkit-font-smoothing: antialiased;
    }

    @-webkit-keyframes breathing {
        0% {
            -webkit-transform: scale(0.9);
            transform: scale(0.9);
        }

        25% {
            -webkit-transform: scale(1);
            transform: scale(1);
        }

        60% {
            -webkit-transform: scale(0.9);
            transform: scale(0.9);
        }

        100% {
            -webkit-transform: scale(0.9);
            transform: scale(0.9);
        }
    }

    @keyframes breathing {
        0% {
            -webkit-transform: scale(0.9);
            -ms-transform: scale(0.9);
            transform: scale(0.9);
        }

        25% {
            -webkit-transform: scale(1);
            -ms-transform: scale(1);
            transform: scale(1);
        }

        60% {
            -webkit-transform: scale(0.9);
            -ms-transform: scale(0.9);
            transform: scale(0.9);
        }

        100% {
            -webkit-transform: scale(0.9);
            -ms-transform: scale(0.9);
            transform: scale(0.9);
        }
    }

</style>