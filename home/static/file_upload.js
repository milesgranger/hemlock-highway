/**
 * Created by miles on 5/6/2017.
 */

$(document).ready(function(){

    + function($) {
        'use strict';

        var dropZone = document.getElementById('drop-zone');
        var uploadForm = document.getElementById('js-upload-form');

        var updateProccessedFiles = function (file, url, success) {
            // Appends either a failure or success link to the file which was uploaded/failed
            $('#processed-files').append(
                success ?
                    '<a href="' + url + '" class="list-group-item list-group-item-success">' +
                        '<span class="badge alert-success pull-right">Success</span>' + file.name + '<br/>Size (GB): ' + parseFloat(file.size / 1000000000).toFixed(10) +
                    '</a>'
                    :
                    '<a href="#" class="list-group-item list-group-item-danger">' +
                        '<span class="badge alert-danger pull-right">Failed</span>' + file.name +
                    '</a>'
            )
        };

        var uploadFile = function(file, s3Data, url){
            // Given response from server, do the actual uploading of the file given the presigned dat
            $('#progress-bar').attr('aria-valuenow', "5").css('width', '5%');

            var xhr = new XMLHttpRequest();

            // Listener to update the progress bar.
            xhr.upload.addEventListener("progress", function(evt){
                if (evt.lengthComputable) {
                    var percentComplete = parseInt( (evt.loaded / evt.total) * 100 );
                    $('#progress-bar').attr('aria-valuenow', percentComplete).css('width', percentComplete + '%');
                }
            });

            // Setup the rest of xhr to send the file
            xhr.open('POST', s3Data.url, true);

            var postData = new FormData();
            for (var key in s3Data.fields){
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
        };

        var getSignedRequest = function (file) {
            // Fetch presigned data from the server for this file
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/sign_s3?file_name=" + file.name + "&file_type=" + file.type);
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        var response = JSON.parse(xhr.responseText);
                        uploadFile(file, response.data, response.url);
                    }
                    else {
                        console.log('Could not get signed URL from server, try again later?');
                    }
                }
            };
            xhr.send();
        };

        var startUpload = function(files) {
            // Send each file to the pipeline of uploading files
            for (var i = 0; i < files.length; i++) {
                getSignedRequest(files[i]);
            }
        };

        uploadForm.addEventListener('submit', function(e) {
            var uploadFiles = document.getElementById('js-upload-files').files;
            e.preventDefault();

            startUpload(uploadFiles)
        });

        dropZone.ondrop = function(e) {
            e.preventDefault();
            this.className = 'upload-drop-zone';
            startUpload(e.dataTransfer.files)
        };

        dropZone.ondragover = function() {
            this.className = 'upload-drop-zone drop';
            return false;
        };

        dropZone.ondragleave = function() {
            this.className = 'upload-drop-zone';
            return false;
        }
    }(jQuery);

});