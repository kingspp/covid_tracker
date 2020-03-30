import GlobalStats from "./lib/global_tracker.jsx";
import Tracker from "./lib/tracker.jsx";
import INDStats from "./lib/india_stats.jsx";
import KARStats from "./lib/kar_stats.jsx";
import MYSStats from "./lib/mys_stats.jsx";
import BaseLoader from "./lib/base_loader.jsx";
import styles from "./lib/styles.jsx";
import  "./lib/fontawesome.js";
import { css } from "uebersicht"


export const command = "./covid_tracker/script.sh";
export const refreshFrequency = 30*1000*60; // widget will run command once a second

console.log(command);

const parse = data => {
    try {
        return JSON.parse(data);
    } catch (e) {
        return undefined;
    }
};


var global_data = {};


function dataParser(data){
    data = data['all'];
    global_data['global']=new Tracker(data['totalConfirmed'], data['totalConfirmed'] - data['totalDeaths'] - data['totalRecovered'], data['totalRecovered'],  data['totalDeaths'],'GLB').generate();
    try {
        data = data['areas'];
        for (var i = 0; i < data.length; i++) {
            if (data[i]['id'] == 'unitedstates') {
                global_data['usa'] = new Tracker(data[i]['totalConfirmed'], data[i]['totalConfirmed'] - data[i]['totalDeaths'] - data[i]['totalRecovered'], data[i]['totalDeaths'], data[i]['totalRecovered'], 'USA').generate();
                let usData = data[i]['areas'];
                for (var j = 0; j < usData.length; j++) {
                    if (usData[j]['id'] == 'massachusetts_unitedstates') {
                        global_data['mass'] = new Tracker(usData[j]['totalConfirmed'], usData[j]['totalConfirmed'] - usData[j]['totalDeaths'] - usData[j]['totalRecovered'], usData[j]['totalDeaths'], usData[j]['totalRecovered'], 'MAS').generate();
                        let massData = usData[j]['areas'];
                        for (var k = 0; k < massData.length; k++) {
                            if (massData[k]['id'] == 'worcester_massachusetts_unitedstates') {
                                global_data['worcester'] = new Tracker(massData[k]['totalConfirmed'], massData[k]['totalConfirmed'] - massData[k]['totalDeaths'] - massData[k]['totalRecovered'], massData[k]['totalDeaths'], massData[k]['totalRecovered'], 'WOR').generate();
                                break;
                            }
                        }
                        break;
                    }
                }
                break;
            }
        }
    }
    catch (e) {
    }
}


export const render = ({ output, error }) => {
    try {
        var data = parse(output);
        dataParser(data);
        return (
            <div style={styles}>
                <BaseLoader/>
                {/*{global_data['global']}*/}
                <GlobalStats data={data.global}/>
                {global_data['usa']}
                {global_data['mass']}
                {global_data['worcester']}
                <INDStats data={data.ind}/>
                <KARStats data={data.ind}/>
                <MYSStats data={data.mys}/>
            </div>
        )
    }
    catch (e) {
        console.log(e);
        return <div>Fetching data . . . </div>
    }
};
