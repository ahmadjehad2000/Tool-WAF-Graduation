import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },
    title: {
        flexGrow: 1,
    },
}));

function renderHosts(dashboard) {
    dashboard.setState({ show: "hosts" })
}

function renderDevices(dashboard) {
    dashboard.setState({ show: "devices" })
}

function renderCaptures(dashboard) {
    dashboard.setState({ show: "captures" })
}

export default function WafAppBar(props) {
    const classes = useStyles();
    const dashboard = props.dashboard;

    return (
        <div className={classes.root}>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h4" className={classes.title} style={{ paddingLeft: '20px' }}>
                        <b>AAU Web Application Firewall</b><b style={{ fontSize: '15px', color: 'red', paddingLeft: '10px' }}>Dashboard</b>
                    </Typography>
                    <Button color="inherit" onClick={() => renderDevices(dashboard)}>Devices</Button>
                    <Button color="inherit" onClick={() => renderHosts(dashboard)}>Hosts</Button>
                    <Button color="inherit" onClick={() => renderCaptures(dashboard)}>Captures</Button>
                </Toolbar>
            </AppBar>
        </div>
    );
}