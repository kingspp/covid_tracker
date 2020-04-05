import styles from "./styles.jsx";
import $ from './jquery.min';
import Tracker from "./tracker.jsx";

export const render = ({ data }) => {
    try {
        data = data.statewise[0];
        return new Tracker(data.confirmed, data.active, data.recovered, data.deaths, 'IND').generate()
    }
    catch (e) {
        console.log(e)
        return <div>Fetching data . . . </div>
    }
};

export default render;