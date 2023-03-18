const urlInput = document.getElementById("ip_to_add");
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


function getAllowedURLs() 
{
    // TODO: Initialize the table with the URLs from the text file.
}


function deleteURL(url)
{
    // TODO: go to the text file and remove the url.
    // Refresh the table.
}


function addURL()
{
    // TODO: go to the text file and add the url.
    // Refresh the table.
}
