/**
 * Created by milesg on 16.06.17.
 */

import React from 'react';
import RegressionModel from './model-templates/regression';
import RandomForestModel from './model-templates/random-forest';


class ModelBuilder extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            modelType: null,
            modelName: '',
        };
    }

    handleSubmit(event){
        console.log('Preventing default');
        event.preventDefault();
    }

    returnCurrentModel(){

        // Helper to return the model template form-control given current component's state
        // the case keys should match the select option values.
        switch (this.state.modelType) {
            case 'regression':
                return <RegressionModel/>;
                break;
            case 'random-forest':
                return <RandomForestModel/>;
                break;
            default:
                return null;
        }
    }

    render(){
        return (
            <form action="" onSubmit={this.handleSubmit}>

                {/*Model name*/}
                <div className="form-group">
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
                        <div className="form-group">
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
                        null
                }

                {/* Depending on the selection above, update the model template */}
                {this.returnCurrentModel()}

                <button type="submit" className="btn btn-primary">Submit</button>
            </form>
        )
    }
}

export default  ModelBuilder;