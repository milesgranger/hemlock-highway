import React from 'react';


const FileUploadProgress = ({uploadProgress}) => {
    /*
    * Show a progress bar given 'progress' between 0 and 100
    * */
    return (
        <div className="progress">
            <div className="progress-bar" id="progress-bar" role="progressbar" aria-valuenow={uploadProgress}
                 aria-valuemin="0" aria-valuemax="100" style={{width: uploadProgress + "%"}}>
                <span className="sr-only">{uploadProgress}% Complete</span>
            </div>
        </div>
    )
};

const FinishedUploads = ({processedUploads}) => {
    /*
    * Show a list of the completed uploads
    * */
    return (
        <div className="js-upload-finished">
            <h3>Processed files</h3>
            <div className="list-group" id="processed-files">
                {processedUploads}
            </div>
        </div>
    )
};

const ProcessedUpload = ({file, successful, url}) => {
    // Processed Upload element
    return(
        successful ?
            <a href={url} className="list-group-item list-group-item-success">
                <span className="badge alert-success pull-right">Success</span>
                {file.name}<br/>Size (GB): {parseFloat(file.size / 1000000000).toFixed(10)}
            </a>
            :
            <a href="#" className="list-group-item list-group-item-danger">
                <span className="badge alert-danger pull-right">Failed</span>{file.name}
            </a>
    )
};

class FileDropZone extends React.Component {
    /*
    * The file dropzone
    * */
    constructor(props){
        super(props);
        this.state = {className: 'upload-drop-zone'};
    }

    handleDrop(e){
        // Prevent the default submit action, and handle uploading through
        // the parent component (FileUpload) process.
        e.preventDefault();
        this.setState({className: 'upload-drop-zone'});
        this.props.startUpload(e.dataTransfer.files);
    }

    handleDragOver(e){
        e.preventDefault();
        this.setState({className: 'upload-drop-zone drop'});
        return false;
    }

    handleDragLeave(e){
        e.preventDefault();
        this.setState({className: 'upload-drop-zone'});
        return false;
    }

    render(){
        return (
            <div>
                <h4>Or drag and drop files below</h4>
                <div
                    onDragOver={(e) => this.handleDragOver(e)}
                    onDragLeave={(e) => this.handleDragLeave(e)}
                    onDrop={(e) => this.handleDrop(e)}
                    className={this.state.className}
                >
                    Just drag and drop files here!
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
        this.state = {
            uploadProgress: 0,
            processedUploads: []
        };
    }

    updateProccessedFiles(file, url, successful){
        // Appends either a failure or success link to the file which was uploaded/failed
        let currentUploads = this.state.processedUploads;
        currentUploads.push(<ProcessedUpload key={file.name} file={file} successful={successful} url={url}/>);
        this.setState({processedUploads: currentUploads});
    }

    uploadFile(file, s3Data, url){

        // Given response from server, do the actual uploading of the file given the presigned dat
        this.setState({uploadProgress: 5});

        // Define the new request object
        const xhr = new XMLHttpRequest();

        // Listener to update the progress bar.
        xhr.upload.addEventListener("progress", (evt) => {
            if (evt.lengthComputable) {
                let percentComplete = parseInt( (evt.loaded / evt.total) * 100 );
                this.setState({uploadProgress: percentComplete});
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
        xhr.onreadystatechange = () => {
            if(xhr.readyState === 4) {
                if (xhr.status === 200 || xhr.status === 204) {
                    this.updateProccessedFiles(file, url, true);
                }
                else {
                    console.log('Could not upload the file! XHR Status: ' + xhr.status);
                    this.updateProccessedFiles(file, url, false);
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
        for (let i = 0; i < files.length; i++) {
            this.getSignedRequest(files[i]);
        }
    }

    handleSubmit(e){
        e.preventDefault();
        let files = document.getElementById('js-upload-files').files;
        this.startUpload(files);
    }

    render(){
        return (
            <div id="file-upload">
                <div className="panel panel-default">
                    <div className="panel-heading"><strong>Upload Files</strong></div>
                    <div className="panel-body">

                        <h4>Select files from your computer</h4>
                        <form action="" method="post" encType="multipart/form-data" id="js-upload-form" onSubmit={(e) => this.handleSubmit(e)}>
                            <div className="form-inline">
                                <div className="form-group">
                                    <input type="file" name="files[]" id="js-upload-files" multiple/>
                                </div>
                                <button type="submit" className="btn btn-sm btn-primary" id="js-upload-submit">
                                    Upload files
                                </button>
                            </div>
                        </form>

                        <FileDropZone startUpload={(files) => this.startUpload(files)}/>

                        <FileUploadProgress uploadProgress={this.state.uploadProgress}/>

                        <FinishedUploads processedUploads={this.state.processedUploads}/>
                    </div>
                </div>
            </div>
        )
    }
}

export default FileUpload;
