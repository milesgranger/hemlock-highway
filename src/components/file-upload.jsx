import React from 'react';

class FileDropZone extends React.Component {
    /*
    * The file dropzone
    * */
    constructor(props){
        super(props);
        this.state = {hovering: false};
    }
    render(){
        return (
            <div>
                <h4>Or drag and drop files below</h4>
                <div className="upload-drop-zone" id="drop-zone">
                    Just drag and drop files here
                </div>
            </div>

        )
    }
}

class FileUploadProgress extends React.Component {
    /*
    * Show a progress bar given 'progress' between 0 and 100
    * */
    constructor(props){
        super(props);
        this.state = {progress: 0};
    }

    render(){
        return (
            <div className="progress">
                <div className="progress-bar" id="progress-bar" role="progressbar" aria-valuenow={this.state.progress}
                     aria-valuemin="0" aria-valuemax="100" style={{width: this.state.progress + "%"}}>
                    <span className="sr-only">{this.state.progress}% Complete</span>
                </div>
            </div>
        )
    }
}

class FinishedUploads extends React.Component {
    /*
    * Show a list of the completed uploads
    * */
    constructor(props){
        super(props);
        this.state = {};
    }

    render(){
        return (
            <div className="js-upload-finished">
                <h3>Processed files</h3>
                <div className="list-group" id="processed-files">
                    <a href="#" className="list-group-item list-group-item-success"><span
                        className="badge alert-success pull-right">Success</span>image-01.jpg</a>
                    <a href="#" className="list-group-item list-group-item-success"><span
                        className="badge alert-success pull-right">Success</span>image-02.jpg</a>
                </div>
            </div>
        )
    }
}

class FileUpload extends React.Component {

    constructor(props) {
        super(props);
        this.state = {};
    }

    render(){
        return (
            <div id="file-upload">
                <div className="panel panel-default">
                    <div className="panel-heading"><strong>Upload Files</strong></div>
                    <div className="panel-body">

                        <h4>Select files from your computer</h4>
                        <form action="" method="post" encType="multipart/form-data" id="js-upload-form">
                            <div className="form-inline">
                                <div className="form-group">
                                    <input type="file" name="files[]" id="js-upload-files" multiple/>
                                </div>
                                <button type="submit" className="btn btn-sm btn-primary" id="js-upload-submit">Upload
                                    files
                                </button>
                            </div>
                        </form>


                        <FileDropZone/>

                        <FileUploadProgress/>

                        <FinishedUploads/>
                    </div>
                </div>
            </div>
        )
    }
}

export default FileUpload;
