// Main function for XSS attack prevention:
function prevent_xss(request_str) 
{
    request_str = escape_html_entity(str);
}


function escape_malicious_characters(request_str) 
{
    // Replace all occurences of risky characters (<, >, ", &, ') with their HTML entity:
    request_str = request_str.replace(/</g, "&lt;")     // Escape < char.
                             .replace(/>/g, "&gt;")     // Escape > char.
                             .replace(/"/g, "&quot;")   // Escape " char.
                             .replace(/&/g, "&amp;")    // Escape & char.
                             .replace(/'/g, "&#x27;");  // Escape ' char.

    // Return the escaped, safe string:
    return request_str;
}
