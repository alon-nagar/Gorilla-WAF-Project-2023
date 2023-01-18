function main(r)
{
	ngx.log(ngx.INFO, "Sending the message to the Python Flask server");

	ngx.fetch("http://127.0.0.1:3333" + r.uri, {
		method: r.method,
		headers: r.headersIn,
		body: r.requestText
	}).then(
		reply => {
			// Write to the log file that the message was sent successfully:
			ngx.log(ngx.INFO, "The message was sent successfully");
			r.internalRedirect('@app-backend');
			r.await();
		}
	).catch(
		error => {
			// handle the error here
			ngx.log(ngx.ERR, "Failed to send the message: " + error);
			r.internalRedirect('@app-backend');
			r.await();
		}
	);

	r.internalRedirect('@app-backend');
}

export default { main };
