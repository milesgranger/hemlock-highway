import React from 'react';
import $ from 'jquery';


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
    /*
    * Main FileUpload Widget
    * Complete with upload form, drop area, progress bar and list of loaded files
    * */
    constructor(props) {
        super(props);
        this.state = {};
    }
    uploadFile(file, s3Data, url){

        // Given response from server, do the actual uploading of the file given the presigned dat
        $('#progress-bar').attr('aria-valuenow', "5").css('width', '5%');

        // Define the new request object
        const xhr = new XMLHttpRequest();

        // Listener to update the progress bar.
        xhr.upload.addEventListener("progress", function(evt){
            if (evt.lengthComputable) {
                let percentComplete = parseInt( (evt.loaded / evt.total) * 100 );
                $('#progress-bar').attr('aria-valuenow', percentComplete).css('width', percentComplete + '%');
            }
        });

        // Setup the rest of xhr to send the file
        xhr.open('POST', s3Data.url, true);

        // Prepare the file and meta data for sending
        let postData = new FormData();
        for (let key in s3Data.fields){
            if (s3Data.fields.hasOwnProperty(key)){
                postData.append(key, s3Data.fields[key]);
            }
        }
        postData.append('file', file);

        // Update the list with success or failure of files.
        xhr.onreadystatechange = function(){
            if(xhr.readyState === 4) {
                if (xhr.status === 200 || xhr.status === 204) {
                    updateProccessedFiles(file, url, true);
                }
                else {
                    console.log('Could not upload the file! XHR Status: ' + xhr.status);
                    updateProccessedFiles(file, url, false);
                }
            }
        };
        xhr.send(postData);
    }
    getSignedRequest(file){

        // Fetch presigned data from the server for this file
        let xhr = new XMLHttpRequest();
        xhr.open(
            "GET",
            "/sign-s3?file-name=" + file.name + "&file-type=" + file.type + "&file-size=" + file.size
        );
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    let response = JSON.parse(xhr.responseText);
                    this.uploadFile(file, response.data, response.url);
                }
                else {
                    // TODO(Miles) notify the user explicitly that upload failed.
                    console.log('Could not get signed URL from server, try again later?');
                }
            }
        }.bind(this);
        xhr.send();
    }
    startUpload(files){
        // Send each file to the pipeline of uploading files
        for (var i = 0; i < files.length; i++) {
            this.getSignedRequest(files[i]);
        }
    }
    render(){
        return (
            <div id="file-upload">
                <div className="panel panel-default">
                    <div className="panel-heading"><strong>Upload Files</strong></div>
                    <div className="panel-body">

                        /*Form to manually select files from computer*/
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

                        /*File drop zone*/
                        <FileDropZone/>

                        /*File upload progress bar*/
                        <FileUploadProgress/>

                        /*List of finished files*/
                        <FinishedUploads/>
                    </div>
                </div>
            </div>
        )
    }
}

export default FileUpload;
