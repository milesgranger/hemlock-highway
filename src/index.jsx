import React from 'react';
import ReactDOM from 'react-dom';
import socket from 'socket.io-client';
import JumboTronComponent from './components/home-page-components/welcome-jumbotron';
import FileUpload from './components/file-upload';
import ModelBuilder from './components/model-builder';
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
    }

    componentDidMount(){
        console.log('App mounted!');
    }

    handleServerMessage(message){
        let messages = this.state.messages;
        messages.push(message);
        this.setState({messages: messages});
    }

    componentWillUnmount(){
        console.log('App exiting');
    }

    render() {
        return (
            <div>
                <NavBar authenticated={this.state.authenticatedStatus}/>
                <div className="container">
                    <MessageList messages={this.state.messages}/>
                    <JumboTronComponent/>
                    <ModelBuilder/>
                </div>
            </div>
        );
    }
}

document.addEventListener("DOMContentLoaded", function(event){
    const contentNode = document.getElementById('app');
    ReactDOM.render(<App/>, contentNode);
});