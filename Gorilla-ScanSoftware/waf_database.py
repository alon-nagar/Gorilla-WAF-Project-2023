import pymongo

GORILLA_DB_NAME = "Gorilla_WAF_DB"
MAX_NUM_OF_ATTACKS = 3

class MongoDB:

    def __init__(self, db_ip, db_port):
        """
        Constructor that creates a connection to the database, and creates the collections if they don't exist.
        
        Args:
            db_ip (str): The IP address of the database.
            db_port (int): The port of the database.
        """
        
        # Open the connection with the MongoDB's IP&Port and init the '__db' field:
        self.__client = pymongo.MongoClient(db_ip, db_port)
        self.__db = self.__client[GORILLA_DB_NAME]
        
        # Try creating "Blacklist", "IncomingRequests", "AllowedRedirectURLs" collections (if not exist):
        try:
            self.__db.create_collection("Blacklist")
        except pymongo.errors.CollectionInvalid:
            pass
        
        try:
            self.__db.create_collection("IncomingRequests")
        except pymongo.errors.CollectionInvalid:
            pass
        
        try:
            self.__db.create_collection("AllowedRedirectURLs")
        except pymongo.errors.CollectionInvalid:
            pass

    
    def add_to_blacklist(self, ip_address, name_of_attack, num_of_attacks, is_blocked):
        """
        Add new entry to the "Blacklist" collection, including all the information needed.
        
        Args:
            ip_address (str): Attacker's IP Address.
            name_of_attack (str): Attack's name.
            num_of_attacks (int): The number of attacks that the attacker did.
            is_blocked (bool): If the attacker is blocked or not (True if blocked, False if not) [3+ attacks = blocked].
        """
        
        # Define the entry that we want to add to the collection, and add it:
        entry_to_add = {
            "IP Address": ip_address,
            "Attacks Performed": name_of_attack,
            "Num of Attacks": num_of_attacks,
            "Is Blocked": is_blocked
        }
        self.__db["Blacklist"].insert_one(entry_to_add)
        
        
    def add_to_incoming_requests(self, client_ip, content, is_safe, name_of_attack, time):
        """
        Add new entry to the "IncomingRequests" collection, including all the information needed.
        
        Args:
            client_ip (str): Source IP, Client's IP.
            content (str): The HTTP message (Only application level).
            is_safe (bool): True if the packet is safe, False if not (in case of attack).
            name_of_attack (str): Attack's name (If packet is safe - leave empty).
            time (str): The time that the packet was received.
        """
        
        # Define the entry that we want to add to the collection, and add it:
        entry_to_add = {
            "Client's IP": client_ip,
            "HTTP Request": content ,
            "Is Safe": is_safe, 
            "Name of Attack": name_of_attack,
            "Time" : time
        }
        self.__db["IncomingRequests"].insert_one(entry_to_add)
        
        
    def find_in_blacklist(self, ip_address):
        """
        Return entry from "Blacklist" collection, by the given IP.
        
        Args:
            ip_address (str): Attacker's IP Address, the IP address we want to find.
        Returns:
            dictionary: The entry that we found.
        """
        
        # Define the entry we want to find in "Blacklist" collection, and return the result:
        entry_to_find = {
            "IP Address": ip_address, 
        }
        return self.__db["Blacklist"].find_one(entry_to_find)
    

    def get_attacks_performed(self, ip_address):
        """
        Function that returns the attacks that the user preformed.
        
        Args:
            ip_address (str): Attacker's IP Address.
        """
        return self.find_in_blacklist(ip_address)["Attacks Performed"]
    
    
    def update_blacklist(self, ip_address, num_of_attacks, attack_name):
        """
        Update the number of attacks that the attacker did, in the "Blacklist" collection, by the given IP.
        
        Args:
            ip_address (str): Attacker's IP Address, the IP address in the entry we want to find and update.
            new_val (int): New value for the number of attacks.
        """
        
        # Define the entry we want to update in "Blacklist" collection, set the new value and update it:
        entry_to_update = { 
            "IP Address": ip_address,
        }
        
        #current_attacks = self.get_attack_preformed(ip_address) + "," + attack_name
        current_attacks = self.find_in_blacklist(ip_address)["Attacks Performed"] + ", " + attack_name
        
        new_value = {}
        #If the client is at the maximum number of attacks, block him:
        if num_of_attacks == MAX_NUM_OF_ATTACKS:
            new_value = { "$set": {"Attacks Performed": current_attacks, "Num of Attacks": num_of_attacks, "Is Blocked": True } }
        else:
            new_value = { "$set": {"Attacks Performed": current_attacks, "Num of Attacks": num_of_attacks } }
            
        self.__db["Blacklist"].update_one(entry_to_update, new_value)
        
    
    def update_blacklist_is_blocked(self, ip_address, new_val):
        """
        Update the 'Is Blocked' field in the "Blacklist" collection, by the given IP.
        
        Args:
            ip_address (str): Attacker's IP Address, the IP address in the entry we want to find and update.
            new_val (bool): New value for 'Is Blocked'.
        """
        
        # Define the entry we want to update in "Blacklist" collection, set the new value and update it:
        entry_to_update = { 
            "IP Address": ip_address,
        }
        new_value = { "$set": { "Is Blocked": new_val } } 
        self.__db["Blacklist"].update_one(entry_to_update, new_value)
        
        
    def delete_one_blacklist(self, ip_address):
        """
        Delete one entry from the "Blacklist" collection, by the given IP.
        Usually used when the attacker's 'Num of Attacks' = 0.

        Args:
            ip_address (str): Attacker's IP Address, the IP address in the entry we want to find and delete.
        """
        # Define the entry we want to delete in "Blacklist" collection and delete it:
        entry_to_delete = {
            "IP Address": ip_address, 
        }
        self.__db["Blacklist"].delete_one(entry_to_delete)
        

    def is_in_blacklist(self, ip_address):
        """
        Check if the given IP is in the "Blacklist" collection.
        
        Args:
            ip_address (str): Attacker's IP Address, the IP address we want to check.
        
        Returns:
            bool: True if the IP is in the collection, False if not.
        """
        
        return self.find_in_blacklist(ip_address) is not None
    
    
    def is_blocked(self, ip_address):
        """
        Function that checks if the user is blocked.
            
        Args:
            ip_address (str): Attacker's IP Address.
        """
        if (not self.is_in_blacklist(ip_address)):
            return False
        return self.find_in_blacklist(ip_address)["Is Blocked"]
        
    
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
    