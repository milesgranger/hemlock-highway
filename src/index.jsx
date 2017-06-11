import $ from 'jquery';
import React from 'react';
import ReactDOM from 'react-dom';
import socket from 'socket.io-client';
import JumboTronComponent from './components/home/welcome-jumbotron';
import FileUpload from './components/file-upload';
import NavBar from './components/nav-bar';
import MessageList from './components/user-messages';

class App extends React.Component {
    /*
    * Main app component for the homepage.
    * */
    constructor (props){
        super(props);
        this.state = {
            authenticatedStatus: (document.getElementById('authenticated-status').getAttribute('content').toLowerCase() === 'true'),
            authenticatedUser: document.getElementById('authenticated-user').getAttribute('content'),
            messages: []  // List of object w/ keys "alertType" and "message" where alertType is bootstrap alert type. ie. alert-success
        };
        // TODO (Miles) Find a way to change connection endpoint depending on debug or otherwise
        this.socket = socket.connect('//webapp-service.io:5555');
        //this.socket = socket.connect('//' + document.domain + ':' + location.port);
    }

    componentDidMount(){
        console.log('App mounted!');
        this.socket.on('connect', () => {
            this.socket.emit('new-connection', {
                authenticatedStatus: this.state.authenticatedStatus,
                authenticatedUser: this.state.authenticatedUser
            });
            console.log('Sent greeting to server!');
        });
        //this.socket.emit('submit-model', 'please-submit');
        this.socket.on('model-update', console.log);
        this.socket.on('server-message', (message) => this.handleServerMessage(message))
    }

    handleServerMessage(message){
        let messages = this.state.messages;
        messages.push(message);
        this.setState({messages: messages});
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
                <NavBar authenticated={this.state.authenticatedStatus}/>
                <div className="container">
                    <MessageList messages={this.state.messages}/>
                    <JumboTronComponent/>
                    <FileUpload/>
                </div>
            </div>
        );
    }
}

$(document).ready(function(){
    const contentNode = document.getElementById('app');
    ReactDOM.render(<App/>, contentNode);
});