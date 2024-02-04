const { MongoClient, ServerApiVersion } = require('mongodb');
const fs = require('fs');

// Read the content of the secret .pem file
const credentials = fs.readFileSync('/etc/secrets/mongodb/X509capstone.pem', 'utf8');

const client = new MongoClient(process.env.MONGO_CONNECTION_STRING, {
  tlsCertificateKeyFile: credentials,
  serverApi: ServerApiVersion.v1
});

async function run() {
  try {
    await client.connect();
    const database = client.db(process.env.MONGO_DB); // Replace with your actual MongoDB database name
    const collection = database.collection(process.env.MONGO_COLLECTION); // Replace with your actual MongoDB collection name
    const docCount = await collection.countDocuments({});
    console.log(docCount);
    // perform actions using client
  } finally {
    // Ensures that the client will close when you finish/error
    await client.close();
  }
}

run().catch(console.dir);
