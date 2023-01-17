//const MongoDB = require("./waf_database.js");
//import MongoDB from './waf_database.js';

//let count = 0;
// const net = require('net');

// const client = new net.Socket();
//import $ from 'jquery';

// var XMLHttpRequest = require('xhr2');

function main(r)
{

//      try {
//      var db = new MongoDB("localhost", 27017);
//      }
//      catch (e)
//      {
//              return "Error: " + e;
//      }
//      db.add_to_IncomingPackets(r.remoteAddress, r.remotePort, r,requestText, true, "No Attack");
        //return "Request: " + r.requestText;
        // WORKING:
        //r.return(302, '/block.html?name=XSS Attack&count=2');
        //count++;



        //TRIES
        // var xhr = new XMLHttpRequest();
        // xhr.open("POST", "http://localhost:3333/", true);
        // xhr.setRequestHeader("Content-Type", "application/json");
        // xhr.send(JSON.stringify({ message: "hello world" }));


        // client.connect(3333, '127.0.0.1', function() {
        // console.log('Connected');
        // client.write('Hello, server! Love, Client.');
        // });
        
        // client.on('data', function(data) {
        // console.log('Received: ' + data);
        // client.destroy();
        // });
        
        // client.on('close', function() {
        // console.log('Connection closed');
        // });


        // fetch("http://localhost:3333/", {
        // method: "POST",
        // headers: {
        // "Content-Type": "text/plain"
        // },
        // body: "hello world"
        // });


        // $.ajax({
        // type: "POST",
        // url: "http://localhost:3333/",
        // data: "hello world",
        // success: function(response) {
        //         console.log(response);
        // }
        // });




        // var xhr = new XMLHttpRequest();
        // xhr.open("POST", "http://localhost:3333/", true);
        // xhr.setRequestHeader("Content-Type", "text/plain");
        // xhr.send("hello world");




        let options = {
        method: "POST",
        headers: {
                "Content-Type": "text/plain"
        },
        body: "hello world"
        };
        
        ngx.fetch("http://127.0.0.1:3333/", options)
        .then(response => {
                // handle the response here
                ngx.log(ngx.INFO, "Successfully sent the message");
        })
        .catch(error => {
                // handle the error here
                ngx.log(ngx.ERR, "Failed to send the message: " + error);
        });

        r.internalRedirect('@app-backend');
        // return "Request Text: " + r.requestText;


        
        //return "Blocked Message: " + r.RequestText;
}
//main("a");
export default { main };
