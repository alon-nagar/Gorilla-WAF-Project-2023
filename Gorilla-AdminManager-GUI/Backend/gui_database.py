import pymongo
from bson.objectid import ObjectId
from bson import json_util
import json

GORILLA_DB_NAME = "Gorilla_WAF_DB"

class MongoDB:

    def __init__(self, db_ip, db_port):
        """
        Constructor that creates a connection to the database.
        
        Args:
            db_ip (str): The DB's IP.
            db_port (int): The DB's Port.
        """
        
        self.__client = pymongo.MongoClient(db_ip, db_port)
        self.__db = self.__client[GORILLA_DB_NAME]
        
    
    # ------------------------------------[ INCOMING REQUESTS ]------------------------------------
    def get_all_incoming_requests(self):
        """Function to return all the entries in the "IncomingRequests" collection.

        Returns:
            str: JSON string includes all the entries in the "IncomingRequests" collection.
        """
        return json.dumps(list(self.__db["IncomingRequests"].find()), default=json_util.default)
    
    
    def get_request_by_id(self, id):
        """Function to return a specific entry in the "IncomingRequests" collection, by the given ID.

        Args:
            id (str): The entry's ID.

        Returns:
            str: JSON string includes the entry in "IncomingRequests" (or "Not in Incoming Requests" if ID not found).
        """
        
        if not self.is_in_incoming_request(id):
            return "Not in Incoming Requests"
        
        entry_to_find = {
            "_id": ObjectId(id),
        }
        return json.dumps(self.__db["IncomingRequests"].find_one(entry_to_find), default=json_util.default)
    
    
    # Helper function:
    def is_in_incoming_request(self, id):
        """Function to check if the given ID is in the "IncomingRequests" collection.

        Args:
            id (str): The entry's ID to check.

        Returns:
            bool: True if the ID is in the collection, False if not.
        """
        
        entry_to_find = {
            "_id": ObjectId(id),
        }
        return self.__db["IncomingRequests"].find_one(entry_to_find) is not None
        
    
    # ----------------------------------------[ BLACKLIST ]----------------------------------------
    def get_all_blacklist(self):
        """Function to return all the entries in the "Blacklist" collection.

        Returns:
            str: JSON string includes all the entries in the "Blacklist" collection.
        """
        results = []
        for document in self.__db["Blacklist"].find():
            results.append(document)
        return json.dumps(results, default=json_util.default)
    
    
    def get_blacklist_entry_by_ip(self, ip_address):
        """Function to return a specific entry in the "Blacklist" collection, by the given IP.

        Args:
            ip_address (str): The entry's IP Address.

        Returns:
            str: JSON string includes the entry in "Blacklist" (or "Not in Blacklist" if IP not found).
        """
        
        if not self.is_in_blacklist(ip_address):
            return "Not in Blacklist"
        
        entry_to_find = {
            "IP Address": ip_address,
        }
        return json.dumps(self.__db["Blacklist"].find_one(entry_to_find), default=json_util.default)
    
    
    def add_ip_to_blacklist(self, ip_address):
        """Function to add IP to the "Blacklist" collection.

        Args:
            ip_address (str): The IP address to add.

        Returns:
            str: "Added to Blacklist" if added, "Already in Blacklist" if IP is already the blacklist.
        """
        
        if self.is_in_blacklist(ip_address):
            return "Already in Blacklist"
        
        entry_to_add = {
            "IP Address": ip_address,
            "Attacks Performed": "",
            "Num of Attacks": 0,
            "Is Blocked": True,
        }
        self.__db["Blacklist"].insert_one(entry_to_add)
        return "Added to Blacklist"
        
    
    def remove_ip_from_blacklist(self, ip_address):
        """Functino to remove IP from the "Blacklist" collection.

        Args:
            ip_address (str): The IP address to remove.

        Returns:
            str: "Deleted from Blacklist" if deleted, "Not in Blacklist" if IP is not in the blacklist.
        """
        
        if not self.is_in_blacklist(ip_address):
            return "Not in Blacklist"
        
        entry_to_remove = {
            "IP Address": ip_address, 
        }
        self.__db["Blacklist"].delete_one(entry_to_remove)
        return "Deleted from Blacklist"
            
        
    # Helper function:
    def is_in_blacklist(self, ip_address):
        """Function to check if the given IP is in the "Blacklist" collection.

        Args:
            ip_address (str): The entry's IP Address to check.

        Returns:
            bool: True if the IP is in the collection, False if not.
        """
        
        entry_to_find = {
            "IP Address": ip_address, 
        }
        return self.__db["Blacklist"].find_one(entry_to_find) is not None
    
    
    # ----------------------------------------[ ALLOWED REDIRECT URLs ]----------------------------------------
    def get_all_allowed_urls(self):
        """
        Return all the allowed redirect URLs from the "AllowedRedirectURLs" collection.
        It parses the collection and returns a list of all the URLs (only).
        
        Returns:
            list of str: List of all the allowed redirect URLs in strings.
        """
        all_collection_data = list(self.__db["AllowedRedirectURLs"].find())
        all_urls = [entry["URL"] for entry in all_collection_data]
        return all_urls
        
    
    def add_allowed_url(self, url):
        """
        Add new entry to the "AllowedRedirectURLs" collection, including all the information needed.
        
        Args:
            url (str): The allowed redirect URL.
        """
        
        # Define the entry that we want to add to the collection, and add it:
        entry_to_add = {
            "URL": url
        }
        self.__db["AllowedRedirectURLs"].insert_one(entry_to_add)
    
    
    def delete_allowed_url(self, url):
        """
        Delete one entry from the "AllowedRedirectURLs" collection, by the given URL.

        Args:
            url (str): The allowed redirect URL to delete.
        """
        # Define the entry we want to delete in "AllowedRedirectURLs" collection and delete it:
        entry_to_delete = {
            "URL": url, 
        }
        self.__db["AllowedRedirectURLs"].delete_one(entry_to_delete)
    