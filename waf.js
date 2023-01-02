//const MongoDB = require("./waf_database.js");
//import MongoDB from './waf_database.js';

//let count = 0;

function main(r)
{
        let where = "";

        if (JSON.stringify(r).includes("GET"))
        {
                where = "GET";
                r.return(302, '/block.html?name=XSS Attack&count=2');
        }
        else if (JSON.stringify(r).includes("POST"))
        {
                where = "POST";
                r.internalRedirect('@app-backend');
        }
        where += " Unknown";
        return "Where: " + where;
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
        //r.internalRedirect('@app-backend');
        //return "Request Text: " + r.requestText;
        //return "Blocked Message: " + r.RequestText;
}

export default { main };
