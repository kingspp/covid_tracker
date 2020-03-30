import $ from "./jquery.min";
// import  "./fontawesome.js";
// import "./fa.css";



function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

class Tracker{
    constructor(confirmed, active, recovered, deceased, type) {
        this.type=type
        this.confirmed = confirmed;
        this.active = active;
        this.recovered = recovered;
        this.deceased = deceased;

    }

    generate(){
        console.log('in gen hello');
        return <div>{this.type}:
            <span><i className="fa fa-check" style={{color:"red"}}/></span><span>{this.confirmed}</span>&nbsp;
            <span><i className="fa fa-circle" style={{color: 'orange'}}/></span>:<span>{this.active}</span>&nbsp;
            <span><i className="fa fa-circle" style={{color: 'green'}}/></span>:<span>{this.recovered}</span>&nbsp;
            <span><i className="fa fa-circle" style={{color: 'red'}}/></span>:<span>{this.deceased}</span>&nbsp;
        </div>
    }

    track(){
        fetch('https://corona.lmao.ninja/all')
            .then(response => response.json())
            .then(data => {
                return new Tracker(data.cases, data.active, data.recovered, data.deaths, "Global: ").generate()
            });
    }

    // track(initialState){
    //     $.getJSON("https://corona.lmao.ninja/all", function(result){
    //         console.log(result);
    //         this.confirmed = result.cases;
    //         this.active = result.active;
    //         this.recovered = result.recovered;
    //         this.deceased = result.deaths;
    //         initialState.state  = {global: "<span>Casasdasdas</span>as"};
    //     })
    //     // await sleep(this.delay);
    //     // this.track(initialState);
    // }

}




export default  Tracker;