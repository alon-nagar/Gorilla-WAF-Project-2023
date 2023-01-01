const { MongoClient } = require("mongodb");
const GORILLA_DB_NAME = "Gorilla_WAF_DB";
const BLACK_LIST_NAME = "BlackList";
const PACKET_LIST_NAME = "IncomingPackets";
const MAX_NUM_OF_ATTACKS = 3;

class MongoDB {
    constructor (db_ip, db_port) {
        
        //Create URI by the user IP and Port
        const URI = "mongodb://" + db_ip + ":" + db_port + "/" + GORILLA_DB_NAME;

        //Create new client by the URI
        this.client = new MongoClient(URI);
        this.start();
    }

    /*
        Function that create the database and collection if they don't exist.
        input: none
        output: none
    */
    async start (){

        try {
            //Conmect the client to the server.
            await this.client.connect();

            //Create both of the collections.
            await this.client.db().createCollection(BLACK_LIST_NAME);
            await this.client.db().createCollection(PACKET_LIST_NAME);
        } catch (e) {
            console.error();
        } finally {
            //Close the database.
            await this.client.close();
        }
    }

    /*
        Add new entry to the "Blacklist" collection, including all the information needed.
        input:
            ip_address (str): Attacker's IP Address.
            num_of_attacks (int): The number of attacks that the attacker did.
            is_blocked (bool): If the attacker is blocked or not (True if blocked, False if not) [3+ attacks = blocked].

        output: none.
    */
    async add_to_BlackList (ip_address, num_of_attacks, is_blocked) {
        await this.client.db(GORILLA_DB_NAME).collection(BLACK_LIST_NAME).insertOne(
            {
                "IP_Address" : ip_address,
                "Num_of_Attacks" : num_of_attacks,
                "Is_Blocked" : is_blocked
            }
        );
    }


    /*
        Add new entry to the "IncomingPacket" collection, including all the information needed.
        input:
            client_ip (str): Source IP, Client's IP.
            client_port (int): Source port, Client's Port.
            content (str): The HTTP message (Only application level).
            is_safe (bool): True if the packet is safe, False if not (in case of attack).
            name_of_attack (str): Attack's name (If packet is safe - leave empty).

        output: none.
    */
    async add_to_IncomingPackets (client_ip, client_port, content, is_safe, name_of_attack) {
        await this.client.db(GORILLA_DB_NAME).collection(PACKET_LIST_NAME).insertOne(
            {
                "Client's_IP" : client_ip,
                "Client's_Port" : client_port,
                "Num_of_Attacks" : content ,
                "Is_Safe" : is_safe, 
                "Name_of_Attack" : name_of_attack
            }
        );
    }


    /*
        Update the number of attacks that the attacker did, in the "Blacklist" collection, by the given IP.
        input:
            ip_address (string): Attacker's IP Address, the IP address in the entry we want to find and update.
            new_val (string): New value for the number of attacks.

        output: none.
    */
    async update_BlackList_num_of_attacks (ip_address, new_val) {

        await this.client.db(GORILLA_DB_NAME).collection(BLACK_LIST_NAME).findOneAndUpdate(
            //The identifier field
            {
                "IP_Address" : ip_address
            },
            
            //The field we want to update
            {$set: 
                {
                    "Num_of_Attacks" : new_val
                } 
            }
        );
    }


    /*
        Update the 'Is Blocked' field in the "Blacklist" collection, by the given IP.
        input:
            ip_address (string): Attacker's IP Address, the IP address in the entry we want to find and update.
            new_val (bool): New value for 'Is Blocked'.

        output: none.
    */
    async update_BlackList_is_blocked (ip_address, new_val) {

        await this.client.db(GORILLA_DB_NAME).collection(BLACK_LIST_NAME).findOneAndUpdate(
            //The identifier field
            {
                "IP_Address" : ip_address
            },
            
            //The field we want to update

            {$set: 
                {
                    "Is_Blocked" : new_val
                } 
            }
        );
    }

    
    /*
        Function that print list of the user's databases.
        input: the client
        output: none
    */
    async listDatabases (client) {
        //Create list of all the databases using admin (everyone has this database in MongoDB)
        const databaseList = await client.db().admin().listDatabases();

        console.log("Databases:");

        //Print them
        databaseList.databases.forEach(db => {
            console.log(`-${db.name}`);
        });
    }


    /*
        Function that change the user information according to the attack that he preformed.
        input:
            ip_address (str): Attacker's IP Address.

        output: none
    */
    async burn_attacker (ip_address) {

        //Create an array that contains the user information.
        const all_details =  await this.client.db(GORILLA_DB_NAME).collection(BLACK_LIST_NAME).find({"IP_Address" : ip_address}).toArray();


        try
        {
            //If the user doesn't exist in the database then this command will return error.
            var current_num_of_attacks = all_details[0].Num_of_Attacks;

            //Check if the user reached the maximum number of attacks, if he did, then we change his status
            if (current_num_of_attacks == MAX_NUM_OF_ATTACKS) {
                this.update_BlackList_is_blocked(ip_address, true);
            }

            //If the user hasn't reached the maximum number of attacks we add one.
            else
            {
                this.update_BlackList_num_of_attacks(ip_address, current_num_of_attacks + 1)
            }

        }
        catch
        {
            //If the user doesn't exist, then we add him to the database.
            this.add_to_BlackList(ip_address, 1, false);
        }
    }
}
// To connect to another file.
module.exports = MongoDB;


//const c = new MongoDB ("localhost", "27017");
//c.add_to_BlackList(1, 2, true);
//c.add_to_IncomingPackets(4444, 22, "Tttttt", false, "DDOS");
//c.update_BlackList_is_blocked(5555,"mememee");
//c.burn_attacker(2);
//console.log(c.is_in_BlackList(1));
//c.is_in_BlackList(1);
//console.log(c.is_in_BlackList(1));