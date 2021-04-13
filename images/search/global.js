// Global exports
module.exports = Object.freeze({
    // dbhost: '127.0.0.1:5984', // Database URL
    dbhost: 'couchdb.server:5984', // Database URL
    dbuser: 'algorand', // Database user
    dbpass: 'algorand', // Database password
    // algodurl: 'http://127.0.0.1:4001', // Algod node endpoint
    algodurl: 'http://algod.server:4001', // Algod node endpoint
    algodapi: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', // Algod node API access header
    // algoIndexerUrl: 'http://127.0.0.1:8980', // Algo Indexer endpoint
    algoIndexerUrl: 'http://indexer.server:8980', // Algo Indexer endpoint
    algoIndexerToken: '',
});
