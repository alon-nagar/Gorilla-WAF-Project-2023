// Function to generate the HTML code for the "Incoming Requests" table:
function generateBlacklistTableHTML(data) 
{
    let html = '';
    data.forEach(item => {
    html += `<tr>
        <td><p>${item.ipAddress}</p></td>
        <td><p>${item.numOfAttacks}</p></td>
        <td><p>${item.attacksPeformed}</p></td>
        <td><p>${item.isBlocked}</p></td>
    </tr>`;
    });
    
    return html;
}

// Get a reference to the tbody element of the table:
const tbody = document.querySelector("#blacklist_data");


// Example of how to modify the rows dynamically
const newData = [
    { ipAddress: '192.168.2.2', numOfAttacks: 2, attacksPeformed: 'SQL Injection, XSS', isBlocked: 'Yes' }
];

// Insert the initial rows into the table:
tbody.innerHTML = generateBlacklistTableHTML(newData);
