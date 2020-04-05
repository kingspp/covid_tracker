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
        return <div>{this.type}:
            <span><i className="fa fa-check" style={{color:"red"}}/></span><span>{this.confirmed}</span>&nbsp;
            <span><i className="fa fa-circle" style={{color: 'orange'}}/></span>:<span>{this.active}</span>&nbsp;
            <span><i className="fa fa-circle" style={{color: 'green'}}/></span>:<span>{this.recovered}</span>&nbsp;
            <span><i className="fa fa-circle" style={{color: 'red'}}/></span>:<span>{this.deceased}</span>&nbsp;
        </div>
    }

}




export default  Tracker;