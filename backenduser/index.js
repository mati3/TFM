'use strict';

//==========MODULOS===============
var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var rest = require('request');

//==========VARIABLES===============
app.set('port', 3000);
app.set('rest',rest);

//==========INICIACION=============
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "https://localhost:4201");
    res.header("Access-Control-Allow-Credentials", "true");
    res.header("Access-Control-Allow-Methods", "POST, GET, DELETE, UPDATE, PUT");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, token");
    next();
});
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static('public'));

//==========CONNECT DB================
const mysql = require('mysql');
const AES = require('mysql-aes');
const fs = require('fs');
var con = mysql.createConnection({
    host: "database",
    user: "root",
    port: '3306',
    password: "mati",
    database: "mean",
    charset  : 'utf8'//,
//    ssl: {
//        ca: fs.readFileSync(__dirname + '/certs/ca.pem'),
//        key: fs.readFileSync(__dirname + '/certs/client-key.pem'),
//        cert: fs.readFileSync(__dirname + '/certs/client-cert.pem')
//    }
});
//==========RUTAS================

require("./funciones.js")(app, con, AES);

//===========RUN===============
const options= {
    key: fs.readFileSync('./certs/client-key.pem'),
    cert: fs.readFileSync('./certs/client-cert.pem')
}
const https = require("https");
// Lanza el servidor
app.listen(app.get('port'), function() {
    console.log("Servidor activo en el puerto: 3000");
});
https.createServer(options, app).listen(3001);
