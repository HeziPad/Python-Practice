# Python-Practice
Server-client, sockets, threading, sql - OOD

Project objective:

  Creating a "Water station" clients, and a server which communicates with the clients, while using SQL database for gathered info.
  Water-stations have water sensor, and can trigger an alarm upon detection of misfunctioning.

Details:

  1. The server shall allow new Water-stations to connect to it.
  2. The server will send to all clients a "keep-alive" request every minute.
  3. Upon receiving "keep-alive" message, each Water-station will send back to the server the following data:
    a. ID of the Water-station.
    b. Current date and time.
    c. Alarm status (0 or 1).
    d. Sensor status (0 or 1).
  4. The mentioned data shall be stored in a 'client_status.txt' file in each Water-station.
  5. The database of the server ('data.db') shall be implemented using sqlite3.

In this implementation:

  1. "client.py" - Run this on a Water-station client. Make sure arguments are valid (representing an active server).
  2. "client_status.txt" - Contains Water-station client status. Make sure not to change format of data (i.e. '3 chars,char,char')
  3. "server.py" - Run this on (to be) a server. Make sure arguments are valid (unused port, path to database is valid).
  4. "wateralarm_client.py" - Class used by client. 
  5. "wateralarm_server.py" - Class used by server. Inherits from 'wateralarm_sql.py'
  6. "wateralarm_sql.py" - Class used by server.
  
  - Files to be on server: "server.py", "wateralarm_server.py", "wateralarm_sql.py".
  - Files to be on client: "client.py", "client_status.txt", "wateralarm_client.py".
  
Notes:

  - This implementation is rather simple. There is NOT enough checks of data integrity and NOT all "corners" are covered, since it was written for the purpose of learning only.
