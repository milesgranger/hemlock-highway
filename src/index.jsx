import $ from 'jquery';
import React from 'react';
import ReactDOM from 'react-dom';
import JumboTronComponent from './components/home/welcome-jumbotron';
import FileUpload from './components/file-upload';
import socket from 'socket.io-client';


class App extends React.Component {
    /*
    * Main app component for the homepage.
    * */
    constructor (props){
        super(props);
        this.state = {authenticated: false};
        this.socket = socket.connect('://' + document.domain + ':' + location.port);
    }
    componentDidMount(){
        console.log('App mounted!');
        this.socket.on('connect', (data) => this.greetServer(data));
    }
    componentWillUnmount(){
        console.log('App exiting');
        this.socket.emit('disconnect', 'disconnecting');
    }
    greetServer(data){
        this.socket.emit('connected', 'client connected')
    }
    render() {
        return (
            <div>

                <JumboTronComponent/>
                <FileUpload/>
            </div>
        );
    }
}

$(document).ready(function(){
    const contentNode = document.getElementById('app');
    ReactDOM.render(<App/>, contentNode);
});