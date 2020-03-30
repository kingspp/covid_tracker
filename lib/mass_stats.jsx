import styles from "./styles.jsx";
import $ from './jquery.min';
import Tracker from "./tracker.jsx";

export const render = ({ data }) => {
    console.log(data);
    // data = data["statewise"];
    // for(var i=0; i<data.length;i++){
    //     console.log(data[i]['state']);
    //     if (data[i]['state']=='Karnataka') {
    //         data = data[i];
    //         return new Tracker(data.confirmed, data.critical, data.recovered, data.deaths, 'MASS').generate()
    //     }
    // }
    return <div>Fetching data . . .</div>

};

export default render;