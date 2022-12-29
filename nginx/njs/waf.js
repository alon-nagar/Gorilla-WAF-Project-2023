// Use the njs request object to access request information
let request_method = njs.request.method;
let request_uri = njs.request.uri;

// Use the njs response object to set the response status and body
njs.response.status = 200;
njs.response.body = `The request method was ${request_method} and the request URI was ${request_uri}`;
