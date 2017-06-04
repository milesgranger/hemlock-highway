/**
 * Created by milesg on 04.06.17.
 */

$(document).ready(function(){

    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function () {
        console.log('Sending connection message to server..');
        socket.emit('new-connection', {data: 'hello from client'});
    });

    socket.on('model-update', function(data){
        console.log(data['progress']);
    });


   $('#runmodel').click(function(){
       socket.emit('submit-model', {datalocation: 'path/to/foo.csv'});
   }); // End of click func

});
