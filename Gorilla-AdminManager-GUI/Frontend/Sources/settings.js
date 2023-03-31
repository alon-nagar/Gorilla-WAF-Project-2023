const urlInput = document.getElementById("url_to_add");
const addUrlButton = document.getElementById("add_url_button");
const urlError = document.getElementById("urlError");

// Listener to check if URL field is not empty.
urlInput.addEventListener("input", function() 
{
    if (urlInput.value.length == 0) 
    {
        addUrlButton.disabled = true;
        urlError.innerHTML = "Cannot be empty";
        urlError.style.display = "block";
    }
    else
    {
        addUrlButton.disabled = false;
        urlError.style.display = "none";
    }
});


// Function to generate the HTML code for the "Allowed URLs" table:
function generateAllowedURLsTableHTML(data)
{
    let html = '';

    data.forEach(item => 
    {
        url = item.replace("\n", "");
        html += `<tr>
            <td><p>${url}</p></td>
            <td><a onclick="deleteURL('${url}')"><img src="Resources/trash-icon.png"></a></td>
        </tr>`;
    });
    
    return html;
}


// Function to get all allowed urls from the Python Flask server and display them in the "Alloed redirect URLs" table:
function getAllowedURLs() 
{
    let xhr = new XMLHttpRequest();

    // Set the HTTP method and URL:
    xhr.open("GET", "http://localhost:4444/get_all_allowed_redirect_urls", true);

    // Define what happens when the response is received:
    xhr.onreadystatechange = function() 
    {
        // If the request is done and the response is OK:
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) 
        {
            data = JSON.parse(this.responseText);
            const tbody = document.querySelector("#allowed_urls_data");  // Select the table body.
            tbody.innerHTML = generateAllowedURLsTableHTML(data);
        }
    };

    xhr.send();
}


// Function to delete a given URL from the allowed urls.
function deleteURL(url)
{
    let xhr = new XMLHttpRequest();

    // Set the HTTP method and URL:
    xhr.open("GET", `http://localhost:4444/remove_url_from_allowed_redirect_urls?url=${url}`, true);

    // Define what happens when the response is received:
    xhr.onreadystatechange = function() 
    {
        // If the request is done and the response is OK:
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) 
        {
            if (this.responseText != "URL removed")
            {
                urlError.innerHTML = this.responseText;
                urlError.style.display = "block";
            }
            else
            {
                urlError.value = "";
                urlError.style.display = "none";
            }
        }
    };

    xhr.send();
    getAllowedURLs();  // Refresh "Allowed URLs" table.
}


// Function to add a URL to the allowed redirect urls. The URL is taken from the input field "#url_to_add":
function addURL()
{
    let xhr = new XMLHttpRequest();

    // Set the HTTP method and URL:
    xhr.open("GET", `http://localhost:4444/add_url_to_allowed_redirect_urls?url=${document.querySelector("#url_to_add").value}`, true);

    // Define what happens when the response is received:
    xhr.onreadystatechange = function() 
    {
        // If the request is done and the response is OK:
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) 
        {
            if (this.responseText != "URL added")
            {
                urlError.innerHTML = this.responseText;
                urlError.style.display = "block";
            }
            else
            {
                urlError.value = "";
                urlError.style.display = "none";
            }
        }
    };

    xhr.send();
    getAllowedURLs();  // Refresh "Allowed URLs" table.
}
