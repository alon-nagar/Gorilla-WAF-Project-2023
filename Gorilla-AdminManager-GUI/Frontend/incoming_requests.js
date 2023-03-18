// Function to convert date string to raedable string (e.g. 2021-01-01T00:00:00.000Z -> 01/01/2021 00:00:00)):
function dateStringToReadableString(dateString)
{
    const date = new Date(dateString);
    return `${padZero(date.getUTCDate())}/${padZero(date.getUTCMonth() + 1)}/${date.getUTCFullYear()} ${padZero(date.getUTCHours())}:${padZero(date.getUTCMinutes())}:${padZero(date.getUTCSeconds())}`;
}


// Function to pad a number with a zero (e.g. 1 -> 01):
function padZero(num)
{
    return num.toString().padStart(2, '0');
}


// Function to convert a boolean to a string (e.g. true -> "Yes"):
function boolToYesNo(boolVar)
{
    return boolVar ? "Yes" : "No";
}


// Function to generate the HTML code for the "Incoming Requests" table:
function generateIncomingRequestsTableHTML(data) 
{
    let html = '';
    let moreStyle = '';
    
    data.reverse().forEach(item => 
    {
        if (item["Is Safe"])
        {
            moreStyle = '';
        }
        else
        {
            moreStyle = 'style="color: #ff3030;"';
        }

        html += `<tr ${moreStyle} id=${item["_id"]["$oid"]} onclick=expandRequest('${item["_id"]["$oid"]}')>
            <td><p>${dateStringToReadableString(item["Time"]["$date"])}</p></td>
            <td><p>${item["Client's IP"]}</p></td>
            <td><p>${item["HTTP Request"].split(" ")[0]}</p></td>
            <td><p>${item["HTTP Request"].split(" ")[1]}</p></td>
        </tr>`;
    });
    
    return html;
}


// Function to generate the HTML code for the "Expand Request" div:
function generateExpandRequestHTML(data)
{
    let html = `<p><b>Time: </b>${dateStringToReadableString(data["Time"]["$date"])}</p>
        <p><b>IP Address: </b>${data["Client's IP"]}</p>
        <p><b>Is Safe? </b>${boolToYesNo(data["Is Safe"])}</p>
        <p><b>Attack Name: </b>${data["Name of Attack"]}</p>
        <p style="white-space: pre-wrap;"><b>Content: </b><br>${data["HTTP Request"]}</p>`;
    
    return html;
}


// Function to get all incoming requests from the MongoDB (Python Flask server) and display them in the "Incoming Requests" table:
function getAllIncomingRequests() 
{
    let xhr = new XMLHttpRequest();

    // Set the HTTP method and URL:
    xhr.open("GET", "http://localhost:4444/get_all_incoming_requests", true);

    // Define what happens when the response is received:
    xhr.onreadystatechange = function() 
    {
        // If the request is done and the response is OK:
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) 
        {
            data = JSON.parse(this.responseText);
            const tbody = document.querySelector("#incoming_requests_data");  // Select the table body.
            tbody.innerHTML = generateIncomingRequestsTableHTML(data);
        }
    };

    xhr.send();
}


// Function to get a specific incoming request by its '_id' from the MongoDB (Python Flask server) and display it in the "Expand Request" div:
function expandRequest(id)
{
    let xhr = new XMLHttpRequest();

    // Set the HTTP method and URL:
    xhr.open("GET", `http://localhost:4444/get_request_by_id?id=${id}`, true);

    // Define what happens when the response is received:
    xhr.onreadystatechange = function() 
    {
        // If the request is done and the response is OK:
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) 
        {
            data = JSON.parse(this.responseText);
            const divFill = document.querySelector("#expand_reqeust_table");  // Select the div.
            divFill.innerHTML = generateExpandRequestHTML(data);
            divFill.style = "";  // Show DIV.
        }
    };

    

    xhr.send();
}
