import React from 'react';

export default class RandomForestModel extends React.Component {

    constructor(props){
        super(props);
        this.state = {};
    }

    render(){
        return (
            <div>
                <span>Random Forest Template</span>
                <div className="form-group">

                    <label htmlFor="max-features">Max Features: </label>
                    <select name="max-features" className="form-control">
                        <option value="0-5">0 to 5</option>
                        <option value="5-10">5 to 10</option>
                    </select>
                </div>
            </div>

        )
    }
}