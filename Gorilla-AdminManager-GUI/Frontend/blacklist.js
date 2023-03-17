// Function to convert a boolean to a string (e.g. true -> "Yes"):
function boolToYesNo(boolVar)
{
    return boolVar ? "Yes" : "No";
}


// Function to generate the HTML code for the "Incoming Requests" table:
function generateBlacklistTableHTML(data) 
{
    let html = '';
    data.forEach(item => {
    html += `<tr>
        <td><p>${item["IP Address"]}</p></td>
        <td><p>${item["Num of Attacks"]}</p></td>
        <td><p>${item["Attacks Performed"]}</p></td>
        <td><p>${boolToYesNo(item["Is Blocked"])}</p></td>
        <td><a onclick="deleteIP('${item["IP Address"]}')"><img src="Resources/trash-icon.png"></a></td>
    </tr>`;
    });
    
    return html;
}


function getBlacklist() 
{
    let xhr = new XMLHttpRequest();

    // Set the HTTP method and URL:
    xhr.open("GET", "http://localhost:4444/get_all_blacklist", true);

    // Define what happens when the response is received:
    xhr.onreadystatechange = function() 
    {
        // If the request is done and the response is OK:
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) 
        {
            data = JSON.parse(this.responseText);
            console.log(data);
            const tbody = document.querySelector("#blacklist_data");  // Select the table body.
            tbody.innerHTML = generateBlacklistTableHTML(data);
        }
    };

    xhr.send();
}

function deleteIP(ip)
{
    alert(ip);
}