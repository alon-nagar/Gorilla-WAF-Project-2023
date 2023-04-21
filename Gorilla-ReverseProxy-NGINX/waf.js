async function main(r)
{
	try
	{
		// Parse the GET parameters if they exist, to a url string, that will be fetch:
		let url = "http://flask-waf:3333" + r.uri;
		if (r.args) 
		{
			url += "?" + dict_to_uri_parameters_string(r.args);
		}

		// Assign the real client's IP to the headers sent to the Python Flask server:
		let headers = Object.assign({}, r.headersIn, {
			"X-Forwarded-For": r.remoteAddress,
		});
		
		// Send the client's request for vulnerability scanning (to the Python Flask server on port 3333):
		let reply = await ngx.fetch(url, {
			method: r.method,
			headers: headers,
			body: r.requestText
		});

		// Get the response from the Python Flask server (which is either "ALLOW", "BLOCK", or "BLACKLIST"):
		let vulnerability_status = await reply.text();
		
		// If the response is "ALLOW", pass the client's request to the backend server:
		if (vulnerability_status == "ALLOW")
		{
			// Pass the client's request to the backend server:
			r.internalRedirect("@app-backend");
		}

		// If the response is "BLOCK", parse the JSON string from the Python Flask server, and return the block page to the client:
		else if (vulnerability_status.includes("BLOCK"))
		{
			// Example for the JSON string from the Python Flask server:
			// BLOCK { 
			// 	"attack_name": "SQL Injection Attack",   --> The name of the attack that was detected.
			// 	"blocked_text": "' OR 1=1; --",          --> The text where the attack has been detected.
			// 	"count": 2                               --> The number of times the user performed attacks.
			// }

			// Parse the JSON string from the Python Flask server:
			let json_str = vulnerability_status.split("BLOCK")[1];
			let json_obj = JSON.parse(json_str);
			
			// Parse the necessary data from the JSON string, to pass to the 'block' page:
			let attack_name = json_obj.attack_name;
			let blocked_text = json_obj.blocked_text;
			let count = json_obj.count;

			// Parse the data to a block page, and return it to the client:
			let block_page = `/block.html?name=${attack_name}&count=${count}&text=${encodeURIComponent(blocked_text)}`;

			r.return(302, block_page);
		}

		else if (vulnerability_status.includes("BLACKLIST"))
		{
			// Example for the JSON string from the Python Flask server:
			// BLACKLIST { 
			// 	"attacks_performed": "XSS Attack, SQL Injection, LFI/RFI"  --> The attacks that the current client pefromed.
			// }
			
			// Parse the JSON string from the Python Flask server:
			let json_str = vulnerability_status.split("BLACKLIST")[1];
			let json_obj = JSON.parse(json_str);
			
			// Parse the necessary data from the JSON string, to pass to the 'block_blacklisted' page:
			let attacks_performed = json_obj.attacks_performed;

			// Parse the data to a block_blacklisted page, and return it to the client:
			let block_blacklisted_page = `/block_blacklisted.html?attacks_performed=${attacks_performed}`;

			r.return(302, block_blacklisted_page);
		}

		// If the response is something else, throw an error:
		else
		{
			throw "It's not you, it us. Something went wrong with Gorilla's system..." + "\n" + vulnerability_status;
		}
	}
	catch (error_msg)
	{
		// If an error occurred, return it to the client:
		r.return(200, error_msg);
	}
}


/*
 * Convert a dictionary to a URI parameters string.
 * For example: { "param1": "value1", "param2": "value2" } --> "param1=value1&param2=value2"
 * Source: https://stackoverflow.com/questions/1714786/query-string-encoding-of-a-javascript-object
 */
function dict_to_uri_parameters_string(obj) 
{
	var str = [];
	
	for (var p in obj) 
	{
		if (Array.isArray(obj[p])) 
		{
			for (var i = 0; i < obj[p].length; i++) 
			{
				str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p][i]));
			}
		} 
		else 
		{
			str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
		}
	}

	return str.join("&");
}
  

export default { main };
