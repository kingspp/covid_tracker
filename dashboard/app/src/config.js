var SERVER_CONFIG =  {
    hostname: 'localhost',
        port: 1345,
        version:'v1'
}

export default {
    url:'http://'+SERVER_CONFIG.hostname+':'+SERVER_CONFIG.port+'/'+SERVER_CONFIG.version+"/"

}