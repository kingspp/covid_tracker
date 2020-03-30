import styles from "./styles.jsx";
import $ from './jquery.min';
import Tracker from "./tracker.jsx";

export const render = ({ data }) => {
    try {
        data = data['Karnataka']['districtData']['Mysuru'];
        return new Tracker(data.confirmed, data.critical, data.recovered, data.deaths, 'MYS').generate()
    }
    catch (e) {
        console.log(e)
        return <div>Fetching data . . . </div>
    }
};

export default render;