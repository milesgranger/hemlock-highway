/**
 * Created by milesg on 16.06.17.
 */
import axios from 'axios';
import React from 'react';
import RegressionModel from './model-templates/regression';
import RandomForestModel from './model-templates/random-forest';


export default class ModelBuilder extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            modelType: null,
            modelName: '',
            canSubmit: true,
            modelData: {}
        };
        this.handleChildComponentUpdate = this.handleChildComponentUpdate.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event){
        console.log('Preventing default');
        event.preventDefault();
        console.log('Submitting this data: ' + this.state.modelData);
        axios.post('/model-submission', this.state.modelData)
            .then((response) => {
                console.log(response)
            })
            .catch((error) => {
                console.log(error)
            })
    }

    handleChildComponentUpdate(key, value){
        /* Update the data which is sent to the server
        * key    = specific piece of the model architecture according to current modelType. ie. 'regression-penalty': <value>
        * value  = the actual value of the piece. This can be anything which matches what the backend model expects given the key
        */
        let currentModelData = this.state.modelData;
        currentModelData['model-name'] = this.state.modelName;
        currentModelData['model-type'] = this.state.modelType;
        currentModelData[key] = value;
        this.setState({modelData: currentModelData});
    }

    returnCurrentModel(){

        // Helper to return the model template form-control given current component's state
        // the case keys should match the select option values.
        switch (this.state.modelType) {
            case 'regression':
                return <RegressionModel updateFunction={this.handleChildComponentUpdate}/>;
                break;
            case 'random-forest':
                return <RandomForestModel updateFunction={this.handleChildComponentUpdate}/>;
                break;
            default:
                return null;
        }
    }

    render(){
        return (
            <div className="row">
                <form action="" onSubmit={this.handleSubmit} className="col-sm-8 col-sm-offset-2">

                    <div className="row">
                        {/*Model name*/}
                        <div className="form-group col-sm-6">
                            <label htmlFor="model-name" className="form-check-label">
                                Model Name:
                            </label>
                            <input name="model-name"
                                   type="text"
                                   placeholder="Name for your model"
                                   className="form-control"
                                   onChange={(event) => this.setState({modelName: event.target.value})}
                                   value={this.state.modelName}
                            />
                        </div>

                        {/* Select type of model - Each one of these should have a corresponding Component
                            show when user has entered a name for the model
                        */}
                        {
                            this.state.modelName ?
                                <div className="form-group col-sm-6">
                                    <label htmlFor="model-type">Model type:</label>
                                    <select name="model-type"
                                            id="model-type"
                                            className="form-control"
                                            value={this.state.modelType}
                                            onChange={(event) => this.setState({modelType: event.target.value})}
                                    >
                                        <option value="">Select Model Type</option>
                                        <option value="regression">Regression</option>
                                        <option value="random-forest">Random Forest</option>
                                    </select>
                                </div>
                                :
                                <div className=""></div>
                        }
                    </div>

                    <div className="row">
                        {/* Depending on the selection above, update the model template */}
                        {this.returnCurrentModel()}
                    </div>

                    <div className="form-group col-sm-12">
                        <button type="submit" className="btn btn-primary form-control" disabled={!this.state.canSubmit}>Submit</button>
                    </div>

                </form>
            </div>
        )
    }
}