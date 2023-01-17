async function main(r)
{
	try
	{
        let reply = await ngx.fetch("http://127.0.0.1:3333" + r.uri, {
        	method: r.method,
        	headers: r.headersIn,
        	body: r.requestText
        })

		ngx.log(ngx.INFO, "Successfully sent the message");

		r.internalRedirect('@app-backend');
		//return reply;
	}
	catch (err)
	{
		return err;
		// handle the error here
		ngx.log(ngx.ERR, "Failed to send the message: " + err);
		return err;
	}
}

export default { main };
