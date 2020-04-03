import styles from "./styles.jsx";
import $ from './jquery.min';
import Tracker from "./tracker.jsx";

export const render = ({ data }) => {
    try {
        data = data["statewise"];
        for (var i = 0; i < data.length; i++) {
            if (data[i]['state'] == 'Karnataka') {
                data = data[i];
                return new Tracker(data.confirmed, data.active, data.recovered, data.deaths, 'KAR').generate()
            }
        }
        return <div>Fetching data . . .</div>
    }
    catch (e) {
        console.log(e);
        return <div>Fetching data . . . </div>
    }

};

export default render;