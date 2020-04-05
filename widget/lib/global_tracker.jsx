import styles from "./styles.jsx";
import $ from './jquery.min';
import Tracker from "./tracker.jsx";

export const render = ({ data }) => {
    try {
        return new Tracker(data.cases, data.active, data.recovered, data.deaths, 'GLB').generate()
    }
    catch (e) {
        console.log(e)
        return <div>Fetching data . . . </div>
    }
};


export default render;