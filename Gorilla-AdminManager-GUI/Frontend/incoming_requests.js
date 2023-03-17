// Function to generate the HTML code for the "Incoming Requests" table:
function generateIncomingRequestsTableHTML(data) 
{
    let html = '';
    data.forEach(item => {
    html += `<tr>
        <td><p>${item.time}</p></td>
        <td><p>${item.ipAddress}</p></td>
        <td><p>${item.httpMethod}</p></td>
        <td><p>${item.uri}</p></td>
    </tr>`;
    });
    
    return html;
}

function getData() 
{

    // create a new XMLHttpRequest object
    let xhr = new XMLHttpRequest();

    // set the HTTP method and URL
    xhr.open("GET", "http://localhost:4444/get_all_incoming_requests", true);

    // define what happens when the response is received
    xhr.onreadystatechange = function() {

        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            // update the HTML with the response data
            document.getElementById("xyz").innerHTML = this.responseText;
        }

    };

    // send the request
    xhr.send();

}
