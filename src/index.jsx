import $ from 'jquery';
import React from 'react';
import ReactDOM from 'react-dom';
import JumboTronComponent from './components/home/welcome-jumbotron';
import FileUpload from './components/file-upload';

class App extends React.Component {

    constructor (props){
        super(props);
        this.state = {authenticated: false};
    }

    componentDidMount(){

    }


    render() {
        return (
            <div>
                <JumboTronComponent/>
                <FileUpload/>
            </div>

        )
    }
}




$(document).ready(function(){
    const contentNode = document.getElementById('app');
    ReactDOM.render(<App/>, contentNode);
});