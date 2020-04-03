interval = 5 * 60 * 1000;

function fetchMysoreData() {
    $.ajax({
        url: "https://api.covid19india.org/state_district_wise.json",
        type: "GET",
        success: function (res) {
            $("#mysore").text(
                res["Karnataka"]["districtData"]["Mysuru"]["confirmed"]);
            $("#bangalore").text(
                res["Karnataka"]["districtData"]["Bengaluru"]["confirmed"]);
            $("#thane").text(
                res["Maharashtra"]["districtData"]["Thane"]["confirmed"]);
            $("#coimbatore").text(
                res["Tamil Nadu"]["districtData"]["Coimbatore"]["confirmed"]);
            $("#madurai").text(
                res["Tamil Nadu"]["districtData"]["Madurai"]["confirmed"]);
            $("#chennai").text(
                res["Tamil Nadu"]["districtData"]["Chennai"]["confirmed"]);
            $("#tirunelveli").text(
                res["Tamil Nadu"]["districtData"]["Tirunelveli"]["confirmed"]);
        }
    });
}

fetchMysoreData();

function fetchWorcesterData() {
    $.ajax({
        url:
            "https://coronavirus-tracker-api.herokuapp.com/v2/locations?source=csbs&country_code=US&timelines=false",
        type: "GET",
        // crossDomain: true,
        // headers: {  'Access-Control-Allow-Origin': 'https://codepen.io/prathyushsp/pen/GRJzeVO' },
        // dataType: "jsonp",
        success: function (res) {
            var data = res["locations"];
            for (let i = 0; i < data.length; i++) {
                if (
                    data[i]["county"] == "Worcester" &&
                    data[i]["province"] == "Massachusetts"
                ) {
                    console.log(data[i]);
                    $("#worcester").text(data[i]["latest"]["confirmed"]);
                    break;
                }
            }
        },
        error: function (err) {
            console.log(err);
        }
    });
}

fetchWorcesterData();

setInterval(fetchMysoreData, interval);
setInterval(fetchWorcesterData, interval);



var sc_project=12228730;
var sc_invisible=1;
var sc_security="bac17ab4";
var scJsHost = "https://";
document.write("<sc"+"ript type='text/javascript' src='" +
    scJsHost+
    "statcounter.com/counter/counter.js'></"+"script>");


<!-- End of Statcounter Code -->