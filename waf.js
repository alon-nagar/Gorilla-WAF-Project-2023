async function main(r)
{
	var response = await ngx.fetch(`http://localhost:3333/${r.uri}`);
    var data = await response.json();
    //ngx.say(JSON.stringify(data));
	r.return(200, data);
	// let reply = await ngx.fetch("http://localhost:3333" + r.uri, {
	// 	method: r.method,
	// 	headers: r.headersIn,
	// 	body: r.requestText
	// })

	// let body = reply.text();
	// r.return(200, body);
}

export default { main };
