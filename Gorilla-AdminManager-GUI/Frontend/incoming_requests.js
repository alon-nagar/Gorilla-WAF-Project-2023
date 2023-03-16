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

// Get a reference to the tbody element of the table:
const tbody = document.querySelector("#incoming_requests_data");


// Example of how to modify the rows dynamically
const newData = [
    { time: '16/03/2023 18:00', ipAddress: '192.168.2.2', httpMethod: 'POST', uri: '/logout.php' },
    { time: '16/03/2023 17:58', ipAddress: '10.0.0.5', httpMethod: 'GET', uri: '/dashboard.php' }
];

// Insert the initial rows into the table:
tbody.innerHTML = generateIncomingRequestsTableHTML(newData);
