import React , {Component}from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import MaterialTable from "material-table";

class Captures extends Component {
    constructor(props) {
        super(props);
        this.state = {
            captures: [],
            countdownValue: process.env.REACT_APP_REFRESH_RATE,
        };

}

countdown() {   
    this.setState({countdownValue: this.state.countdownValue-1})
    if (this.state.countdownValue === 0) {
        this.fetchCaptures()
    }
}

fetchCaptures() {   
    let requestUrl = "http://localhost:5000/capture"
    fetch(requestUrl)
        .then(res => res.json())
        .then((data) => {
            console.log(data)
            this.setState({captures: data})
            this.setState({countdownValue: 1})
        })
        .catch((e) => {
            console.log(e)
            this.setState({countdownValue: 1})
        });
    }
  componentDidMount() {
        this.fetchCaptures(false)
        this.interval = setInterval(() => this.countdown(), 1000)
    }

    componentWillUnmount() {
        clearInterval(this.interval)
    }

    render() {
            
            const {captures} = this.state;
            return(
                <div className="container" style={{maxWidth: "100%"}}>
                    <link
                        rel="stylesheet"
                        href="https://fonts.googleapis.com/icon?family=Material+Icons"
                    />
                    <Grid container direction="row" justify="center" alignItems="center">
                        <h2>Captures Table</h2>
                      
                      {/* <h6>Time until refresh: {this.state.countdownValue} seconds</h6> */}
                         <Button variant="contained" onClick={() => {
                        this.fetchCaptures()
                    }}>Refresh Captures</Button>
                    </Grid>
                    <MaterialTable
                        title="Captures information"
                        columns={[
                            { title: "Capture ID", field: "id" },
                             { title: "Capture source IP", field: "srcip" },
                                { title: "Capture destination IP", field: "dstip" },
                                    { title: "Capture url", field: "url" },
                                     { title: "Time", field: "timestamp" },
                                     { title: "Http Version", field: "httpver" },
                                     { title: "Http method", field: "method" },
                                    //  { title: "Packet info", field: "full-packet-info" },
                                
                        
            //              "id": id,
            // "srcip": ip,
            // "dstip": destip,
            // "method": method,
            // "httpver": httpver,
            // "url": url,
            // "timestamp": [currentdate, currenttime],
            // "full-packet-info": str(packetinfo)
                                    ]}
                        data={Object.values(captures)}
                        options={{
                            sorting:true,
                            padding:"dense",
                            pageSize: 10
                        }}
                    />
                </div>
            )
        }
    }
export default Captures;



