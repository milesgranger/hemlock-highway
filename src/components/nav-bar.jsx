/**
 * Created by milesg on 11.06.17.
 */
import React from 'react';


const NavBar = ({authenticated}) => {
    /*
    * Main Nav bar
    * */
    return (
        <nav className="navbar navbar-inverse">
            <div className="container-fluid">
                <div className="navbar-header">
                    <button type="button" className="navbar-toggle collapsed" data-toggle="collapse"
                            data-target="#navbar"
                            aria-expanded="false" aria-controls="navbar">
                        <span className="sr-only">Toggle navigation</span>
                        <span className="icon-bar"></span>
                    </button>
                    <a className="navbar-brand" href="/">Opplett.io</a>
                </div>
                <div id="navbar" className="navbar-collapse collapse">
                    {
                        authenticated ?
                            <a href="/login" role="button" className="btn btn-success navbar-right">Profile</a>
                            :
                            <a href="/login" role="button" className="btn btn-success navbar-right">Log in</a>
                    }
                </div>
            </div>
        </nav>
    )
};

export default NavBar