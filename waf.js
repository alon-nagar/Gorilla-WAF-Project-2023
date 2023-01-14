function main(r)
{
	if (is_xss(r))
	{
		r.return(302, '/block.html?name=XSS Attack&count=2');
	}
	else
	{
		r.internalRedirect('@app-backend');
	}

	return r.method + "     " + JSON.stringify(r.args);
}

export default { main };
