async function main(r)
{
	try
	{
		// Send the client's request for vulnerability scanning (to the Python Flask server on port 3333):
        let reply = await ngx.fetch("http://127.0.0.1:3333" + r.uri, {
        	method: r.method,
        	headers: r.headersIn,
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
			let block_page = `/block.html?name=${attack_name}&text=${blocked_text}count=${count}`;
			r.return(302, block_page);
		}

		else if (vulnerability_status.includes("BLACKLIST"))
		{
			// TODO: BLACKLIST blocking...
		}

		// If the response is something else, throw an error:
		else
		{
			throw "Something went wrong with Gorilla's system..."
		}
	}
	catch (error_msg)
	{
		// If an error occurred, return it to the client:
		r.return(302, error_msg);
	}
}


export default { main };
