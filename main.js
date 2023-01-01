const MongoDB = require('./waf_database.js');


function main () 
{
    const client = new MongoDB ("localhost", "27017");
}

main();