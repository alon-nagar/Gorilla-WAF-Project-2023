//const MongoDB = require("./waf_database.js");
//import MongoDB from './waf_database.js';

let count = 0;

function main(r)
{
//	try {
//	var db = new MongoDB("localhost", 27017);
//	}
//	catch (e)
//	{
//		return "Error: " + e;
//	}
//	db.add_to_IncomingPackets(r.remoteAddress, r.remotePort, r,requestText, true, "No Attack");
	//return "Request: " + r.requestText;
	// WORKING:
	//r.return(302, '/block.html?name=XSS Attack&count=2');
	count++;
	r.internalRedirect('@app-backend');
	return "Count: " + count;
	//return "Blocked Message: " + r.RequestText;
}

export default { main };
