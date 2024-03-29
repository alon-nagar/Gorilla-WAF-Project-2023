const ipInput = document.getElementById("ip_to_add");
const addIpButton = document.getElementById("add_ip_button");
const ipError = document.getElementById("ipError");


// Listener to check if IP input field is valid (not empty and in the right IPv4 format):
ipInput.addEventListener("input", function() 
{
    if (ipInput.value.length == 0) 
    {
        addIpButton.disabled = true;
        ipError.innerHTML = "Cannot be empty";
        ipError.style.display = "block";
    }
    else if (isIPv4(ipInput.value))
    {
        addIpButton.disabled = false;
        ipError.style.display = "none";
    }
    else 
    {
        addIpButton.disabled = true;
        ipError.innerHTML = "Format: X.X.X.X";
        ipError.style.display = "block";
    }
});


// Function to check if a string is in the right IPv4 format (using RegEx):
function isIPv4(text)
{
    const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    return ipRegex.test(text);
}


// Function to convert a boolean to a string (e.g. true -> "Yes"):
function boolToYesNo(boolVar)
{
    return boolVar ? "Yes" : "No";
}


// Function to generate the HTML code for the "Blacklist" table:
function generateBlacklistTableHTML(data) 
{
    let html = '';
    let moreStyle = '';

    data.forEach(item => 
    {
        if (item["Is Blocked"])
        {
            moreStyle = 'style="color: #ff3030;"';
        }
        else
        {
            moreStyle = '';
        }

        html += `<tr ${moreStyle}>
            <td><p>${item["IP Address"]}</p></td>
            <td><p>${item["Num of Attacks"]}</p></td>
            <td><p>${item["Attacks Performed"]}</p></td>
            <td><p>${boolToYesNo(item["Is Blocked"])}</p></td>
            <td><a onclick="deleteIP('${item["IP Address"]}')"><img src="Resources/trash-icon.png"></a></td>
        </tr>`;
    });
    
    return html;
}


// Function to get all blacklist from the MongoDB (Python Flask server) and display them in the "Blacklist" table:
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
            const tbody = document.querySelector("#blacklist_data");  // Select the table body.
            tbody.innerHTML = generateBlacklistTableHTML(data);
        }
    };

    xhr.send();
}


// Function to delete a given IP from the blacklist.
function deleteIP(ip)
{
    let xhr = new XMLHttpRequest();

    // Set the HTTP method and URL:
    xhr.open("GET", `http://localhost:4444/remove_ip_from_blacklist?ip_address=${ip}`, true);

    // Define what happens when the response is received:
    xhr.onreadystatechange = function() 
    {
        // If the request is done and the response is OK:
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) 
        {
            if (this.responseText != "Deleted from Blacklist")
            {
                ipError.innerHTML = this.responseText;
                ipError.style.display = "block";
            }
            else
            {
                ipInput.value = "";
                ipError.style.display = "none";
            }
        }
    };

    xhr.send();
    getBlacklist();  // Refresh "Blacklist" table.
}


// Function to add a IP to the blacklist. The IP is taken from the input field "#ip_to_add":
function addIp()
{
    let xhr = new XMLHttpRequest();

    // Set the HTTP method and URL:
    xhr.open("GET", `http://localhost:4444/add_ip_to_blacklist?ip_address=${document.querySelector("#ip_to_add").value}`, true);

    // Define what happens when the response is received:
    xhr.onreadystatechange = function() 
    {
        // If the request is done and the response is OK:
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) 
        {
            if (this.responseText != "Added to Blacklist")
            {
                ipError.innerHTML = this.responseText;
                ipError.style.display = "block";
            }
            else
            {
                ipInput.value = "";
                ipError.style.display = "none";
            }
        }
    };

    xhr.send();
    getBlacklist();  // Refresh "Blacklist" table.
}
