monitoring
==========

In order to user the server to receive data from the plugin:


-------------------------------
Install mysql
Import the database schema provided in /server/database_construction.sql
-------------------------------
install node.js
sudo npm install express
sudo npm install body-parser
sudo npm install mysql
-------------------------------
Change in /server/server.js the config to the mysql server
-------------------------------
Change in /script/html5monitor.js the config to the node.js server
For example: http://0.0.0.0:3000/api/users
