import React from 'react';

export default class RegressionModel extends React.Component {

    constructor(props){
        super(props);
        this.state = {};
    }

    render(){
        return (
            <div className="col-sm-12">
                <span>Regression Model Template:</span>
                <hr/>
                <div className="form-group col-sm-push-2">
                    <label htmlFor="penalty">Penalty function: </label>
                    <select
                        name="penalty"
                        className="form-control"
                        onChange={(event) => {this.props.updateFunction('penalty', event.target.value)}}
                    >
                        <option value="undefined">Select Regression Penalty</option>
                        <option value="lasso">Lasso</option>
                        <option value="l1">L1</option>
                        <option value="l2">L2</option>
                        <option value="ridge">Ridge</option>
                    </select>
                </div>
            </div>
        )
    }
}