function is_xss(request)
{
    if (request.method == "GET")
    {
		// Iterate over the JSON object 'request.args', that contains the parameters of the GET request:
		for (let param_name in request.args)
		{
			let param_value = request.args[param_name];

			// If XSS is detected in the current parameter's name OR value -> return true:
			if (is_text_xss(param_name) || is_text_xss(param_value))
			{
				return true;
			}
		}
		
        // If the function hasn't returned true yet, then no XSS was detected:
        return false;
    }

    else if (request.method == "POST" || request.method == "PUT" || request.method == "DELETE")
    {
        return is_text_xss(request.requestText);
    }

    return false;
}


function is_text_xss(str)
{
    return str.toLowerCase().includes("<" || ">" || "\"" || "<script>" || "</script>"
                                        || "&lt;" || "&gt;" || "&quot;");
}
