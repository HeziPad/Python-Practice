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
