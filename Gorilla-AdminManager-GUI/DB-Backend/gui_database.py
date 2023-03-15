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
        
    
    def add_ip_to_blacklist(self, ip_address):
        """
        Add new IP to the "Blacklist" collection.
        
        Args:
            ip_address (str): Attacker's IP Address.
            
        Returns:
            str: Indication if the IP was added to the "Blacklist" collection or not for some reason.
        """
        
        # Check that the IP is not already in the "Blacklist" collection:
        if (self.is_in_blacklist(ip_address)):
            return "Already in Blacklist"
        
        # Define the entry that we want to add to the collection, and add it:
        entry_to_add = {
            "IP Address": ip_address,
            "Attacks Performed": "",
            "Num of Attacks": 0,
            "Is Blocked": False,
        }
        self.__db["Blacklist"].insert_one(entry_to_add)
        return "Added to Blacklist"
        
        
    def delete_ip_from_blacklist(self, ip_address):
        """
        Delete entry from the "Blacklist" collection, by the given IP.
        
        Args:
            ip_address (str): The IP address we want to delete.
            
        Returns:
            str: Indication if the IP was deleted from the "Blacklist" collection or not for some reason.
        """
        
        if (not self.is_in_blacklist(ip_address)):
            return "Not in Blacklist"
        
        entry_to_delete = {
            "IP Address": ip_address, 
        }
        self.__db["Blacklist"].delete_one(entry_to_delete)
        return "Deleted from Blacklist"
        
    
    def is_in_blacklist(self, ip_address):
        """
        Check if the given IP is in the "Blacklist" collection.
        
        Args:
            ip_address (str): Attacker's IP Address, the IP address we want to check.
        
        Returns:
            bool: True if the IP is in the collection, False if not.
        """
        entry_to_find = {
            "IP Address": ip_address, 
        }
        
        return self.__db["Blacklist"].find_one(entry_to_find) is not None
    
    
    def is_in_incoming_request(self, id):
        entry_to_find = {
            "_id": ObjectId(id),
        }
        
        return self.__db["IncomingRequests"].find_one(entry_to_find) is not None
    
    
    def get_http_request(self, id):
        entry_to_find = {
            "_id": ObjectId(id),
        }
        return json.dumps(list(self.__db["IncomingRequests"].find_one(entry_to_find)), default=json_util.default)
    
    
    def get_blacklisted_ip(self, ip_address):
        entry_to_find = {
            "IP Address": ip_address,
        }
        return json.dumps(list(self.__db["Blacklist"].find_one(entry_to_find)), default=json_util.default)
    
    
    def get_incoming_requests_collection(self):
        return json.dumps(list(self.__db["IncomingRequests"].find()), default=json_util.default)
    
    
    def get_blacklist_collection(self):
        return json.dumps(list(self.__db["Blacklist"].find()), default=json_util.default)
    