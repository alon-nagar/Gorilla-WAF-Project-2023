//const MongoDB = require("./waf_database.js");
//import MongoDB from './waf_database.js';

//let count = 0;

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
        //r.args = prevent_xss(r.args);
        //r.internalRedirect('@app-backend');
        //var p = JSON.stringify(r.args);
        /*      for (var key in Object.keys(r.args))
        {
                if (r.args[key] != undefined)
                {
                        r.args[key] = escape_malicious_characters(r.args[key]);
                }
        }*/
        //r.internalRedirect('@app-backend');
        //r.args = escape_malicious_characters(r.args);
        if (JSON.stringify(r.args).toLowerCase().includes("<script>"))
        {
                r.return(302, '/block.html?name=XSS Attack&count=2');
        }
        else
        {
                r.internalRedirect('@app-backend');
        }

        return JSON.stringify(r.args);
        //return "Request Text: " + r.requestText;
        //return "Blocked Message: " + r.RequestText;
}


// Main function for XSS attack prevention:
function prevent_xss(request_str) 
{
    request_str = escape_malicious_characters(request_str);
    return request_str;
}


function escape_malicious_characters(request_str) 
{
  // Replace all occurences of risky characters (<, >, ", &, ') with their HTML entity:
  request_str = request_str.replace(/</g, "&lt;")     // Escape < char.
                           .replace(/>/g, "&gt;")     // Escape > char.
                           .replace(/&/g, "&amp;")    // Escape & char.
                           .replace(/'/g, "&#x27;")  // Escape ' char.
                           .replace(/;/g, "&#59;");  // Escape ; char.
  // Return the escaped, safe string:
  return request_str;
}



export default { main };
