import React, { Component } from 'react';
import Grid from "@material-ui/core/Grid";
import WafAppBar from './WafAppBar';
import Devices from "./Devices";
import Hosts from "./Hosts";
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline'

class WafDashboard extends Component {

    constructor(props) {
        super(props);
        this.state = {
            show: "devices",
        };
    }

    render() {
        const { show } = this.state
        const darkTheme = createMuiTheme({ palette: { type: 'light', }, });

        let info;

        if (show === "devices") {
            info = <Devices dashboard={this} />;
        } else if (show === "hosts") {
            info = <Hosts dashboard={this} />;
        }

        return (
            <Grid container direction="column">
                <ThemeProvider theme={darkTheme}>
                    <CssBaseline />
                    <WafAppBar dashboard={this} />
                    <Grid container direction="row" style={{ paddingTop: "10px" }}>
                        <Grid item style={{ width: '100%' }}>
                            {info}
                        </Grid>
                    </Grid>
                </ThemeProvider>
            </Grid>
        );
    }
}

export default WafDashboard;
