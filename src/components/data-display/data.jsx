import React from 'react';
import axios from 'axios';


const Row = ({record, header}) => {
    return (
        <tr>
            {header.map((column, i) => (<td key={i}>{record[column]}</td>))}
        </tr>
    )
};


export default class DataDisplay extends React.Component {

    constructor(props){
        super(props);
        this.state = {hasData: false};
        this.dataTable = null;
    }

    componentDidMount(){
        // When component mounts, get the test data
        // TODO: Fetch the user specific data.
        axios.get('/get-data')
            .then((data) => {this.buildFromJSON(data.data)})
            .catch((error) => {console.log(`error: ${error}`)});
    }

    buildFromJSON(data) {
        // Take a an array of objects and turn into a table
        // [{col1: val1, col2: val2, ...}, ...]
        let header = Object.keys(data[0]);

        this.dataTable = (
            <table className="table table-striped table-hover">
                <thead>
                    <tr>
                        {header.map((column, i) => (<th key={column}>{column}</th>))}
                    </tr>
                </thead>
                <tbody>
                {
                    data.map((record, i) => <Row key={i} record={record} header={header} />)
                }
                </tbody>
            </table>
        );
        this.setState({hasData: true});
    }

    render(){
        return (
            this.state.hasData ? this.dataTable : <h2>No data</h2>
        )
    }
}