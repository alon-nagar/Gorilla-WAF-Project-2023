async function main(r)
{
	try
	{
		// Send the 'r' object to the Python Flask server on port 3333, with all the necessary data:
        let reply = await ngx.fetch("http://127.0.0.1:3333" + r.uri, {
        	method: r.method,
        	headers: r.headersIn,
        	body: r.requestText
        })

		// Write to the log file that the message was sent successfully:
		ngx.log(ngx.INFO, "Successfully sent the message");

		// Wait before closing the request:
		r.await();

		r.internalRedirect('@app-backend');
		
		// Trying to write to the 'njs_output.log' file, but it doesn't work:
		return JSON.stringify(reply);
	}
	catch (err)
	{
		// handle the error here
		ngx.log(ngx.ERR, "Failed to send the message: " + err);
		return err;
	}
}

export default { main };
