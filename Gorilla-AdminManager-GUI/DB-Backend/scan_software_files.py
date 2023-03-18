class AllowedRedirectURLs:
    """Class that handles the allowed redirect URLs file."""
    
    def __init__(self, allowed_url_file_location):
        """Constructor that creates a "connection" to the file for reading and writing.

        Args:
            allowed_url_file_location (str): file's location.
        """
        self.__txt_path = allowed_url_file_location
        self.__file_object = open(self.__txt_path, "r+")
        
    
    def __del__(self):
        """
        Destructor that closes the file.
        """
        self.__file_object.close()
    
    
    def get_allowed_urls(self):
        """Function to return all the allowed URLs.
        
        Returns:
            list: List of all the allowed URLs.
        """
        self.__file_object.seek(0)  # Reset the file pointer to the beginning of the file.
        return self.__file_object.readlines()
    
    
    def add_url(self, url):
        """Function to add a new URL to the file.

        Args:
            url (str): The URL to add.

        Returns:
            str: "URL added" if the URL was added successfully, otherwise an error message.
        """
        try:
            self.__file_object.seek(0)  # Reset the file pointer to the beginning of the file.
            file_content = self.__file_object.read()
            if url + "\n" in file_content:
                return "URL already exists"
            else:
                self.__file_object.seek(0, 2)  # Move the file pointer to the end of the file.
                self.__file_object.write(url + "\n")
                return "URL added"
        except Exception as e:
            return "Error: " + str(e)
    
    
    def remove_url(self, url):
        """Function to remove a URL from the file.

        Args:
            url (str): The URL to remove.
        
        Returns:
            str: "URL removed" if the URL was removed successfully, otherwise an error message indicates "URL not found".
        """
        self.__file_object.seek(0)  # Reset the file pointer to the beginning of the file.
        file_content_before_delete = self.__file_object.read()
        file_content_after_delete = file_content_before_delete.replace(url + "\n", "")
        
        if file_content_after_delete == file_content_before_delete:
            return "URL not found"
        else:
            self.__file_object.seek(0)  # Reset the file pointer to the beginning of the file.
            self.__file_object.truncate()  # Clear the file contents.
            self.__file_object.write(file_content_after_delete)  # Write the new contents.
            return "URL removed"