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
                // CR: What's the [ , ] for? What does each element in the array represent?
				return [true, param_name + "=" + param_value];
			}
		}
		
        // If the function hasn't returned true yet, then no XSS was detected:
        return [false, ""];
    }

    else if (request.method == "POST" || request.method == "PUT" || request.method == "DELETE")
    {
        // CR: What's the [ , ] for? What does each element in the array represent?
        return [ is_text_xss(request.requestText), request.requestText ];
    }

    return [false, ""];
}


// CR: 'str' is not a good name for a parameter. It's not clear what it is.
function is_text_xss(str)
{
    return str.toLowerCase().includes("<" || ">" || "\"" || "<script>" || "</script>"
                                        || "&lt;" || "&gt;" || "&quot;");
}
