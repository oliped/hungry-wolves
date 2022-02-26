const process = require("process");
const fs = require('fs');
const pinataSDK = require('@pinata/sdk');
const PINATA_API_KEY = '8908337448b3ac2b29fb';
const PINATA_SECRET_API_KEY = '9ca76630743f7880b7bac9a48b7035f174f42e9f5fdc632e4ebcd6daef37b862';
const pinata = pinataSDK(PINATA_API_KEY, PINATA_SECRET_API_KEY);

var imgPath = process.argv[2]
const readableStreamForFile = fs.createReadStream(imgPath);
const options = {};

pinata.pinFileToIPFS(readableStreamForFile, options).then((result) => {
    console.log(result["IpfsHash"])
}).catch((err) => {
    console.log(err)
});
