import $ from 'jquery';
import React from 'react';
import ReactDOM from 'react-dom';
import JumboTronComponent from './components/home/welcome-jumbotron';


class App extends React.Component {

    constructor (props){
        super(props);
        this.state = {authenticated: false};
    }

    render() {
        return (
            <JumboTronComponent/>
        )
    }
}




$(document).ready(function(){
    const contentNode = document.getElementById('app');
    ReactDOM.render(<App/>, contentNode);
});