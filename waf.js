function main(r)
{
	let funv = is_xss(r);
	if (funv[0])
	{
		r.return(302, '/block.html?name=XSS Attack&count=2&text=' + funv[1]);
	}
	else
	{
		r.internalRedirect('@app-backend');
	}

	return r.method + "     " + JSON.stringify(r.args);
}

export default { main };
