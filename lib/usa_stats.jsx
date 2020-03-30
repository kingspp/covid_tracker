import styles from "./styles.jsx";
import $ from './jquery.min';
import Tracker from "./tracker.jsx";

export const render = ({ data }) => {
    try {
        data = data[0];
        return new Tracker(data.confirmed, data.critical, data.recovered, data.deaths, 'USA').generate()
    }
    catch (e) {
        console.log(e)
        return <div>Fetching data . . . </div>
    }
};

export default render;