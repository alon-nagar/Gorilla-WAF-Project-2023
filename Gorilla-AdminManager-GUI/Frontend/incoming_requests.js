function dateStringToReadableString(dateString)
{
    const date = new Date(dateString);
    return `${padZero(date.getUTCDate())}/${padZero(date.getUTCMonth() + 1)}/${date.getUTCFullYear()} ${padZero(date.getUTCHours())}:${padZero(date.getUTCMinutes())}:${padZero(date.getUTCSeconds())}`;
}

function padZero(num)
{
    return num.toString().padStart(2, '0');
}

// Function to generate the HTML code for the "Incoming Requests" table:
function generateIncomingRequestsTableHTML(data) 
{
    let html = '';
    data.reverse().forEach(item => {
    html += `<tr id=${item["_id"]["$oid"]}>
        <td><p>${dateStringToReadableString(item["Time"]["$date"])}</p></td>
        <td><p>${item["Client's IP"]}</p></td>
        <td><p>${item["HTTP Request"].split(" ")[0]}</p></td>
        <td><p>${item["HTTP Request"].split(" ")[1]}</p></td>
    </tr>`;
    });
    
    return html;
}

function getAllIncomingRequests() 
{

    // create a new XMLHttpRequest object
    let xhr = new XMLHttpRequest();

    // set the HTTP method and URL
    xhr.open("GET", "http://localhost:4444/get_all_incoming_requests", true);

    // define what happens when the response is received
    xhr.onreadystatechange = function() {

        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            // update the HTML with the response data
            data = JSON.parse(this.responseText);
            console.log(data)
            // Get a reference to the tbody element of the table:
            const tbody = document.querySelector("#incoming_requests_data");

            // Insert the initial rows into the table:
            tbody.innerHTML = generateIncomingRequestsTableHTML(data);
        }

    };

    // send the request
    xhr.send();

}
