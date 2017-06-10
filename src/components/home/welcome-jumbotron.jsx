/**
 * Created by milesg on 09.06.17.
 */
import React from 'react';

class JumboTronComponent extends React.Component {

    render() {
        return (
            <div className="jumbotron">
                <div className="container">
                    <h1>Opplett.io</h1>
                    <p>
                        An easy interface to modern Machine Learning algorithms and visualizations.<br/>
                        No membership tiers or contracts.
                        Pay for what you use, it's that simple.
                    </p>
                    <p>
                        <a className="btn btn-primary btn-lg" href="#" role="button">Learn more &raquo;</a>
                    </p>
                </div>
            </div>
        )
    }
}

export default JumboTronComponent;