const process = require("process");
const pinataSDK = require('@pinata/sdk');
const PINATA_API_KEY = '8908337448b3ac2b29fb';
const PINATA_SECRET_API_KEY = '9ca76630743f7880b7bac9a48b7035f174f42e9f5fdc632e4ebcd6daef37b862';
const pinata = pinataSDK(PINATA_API_KEY, PINATA_SECRET_API_KEY);

var metadata = process.argv[2]
var edition = process.argv[3]

var newMetadata = JSON.parse(metadata) 
// console.log(`newMetadata: ${newMetadata}`)

newMetadata["name"] = newMetadata["name"] + ` #${edition} of ${newMetadata["total_editions"]}`;

const options = {};
pinata.pinJSONToIPFS(newMetadata, options).then((result) => {
    console.log(result["IpfsHash"])
}).catch((err) => {
    console.log(err)
});    
