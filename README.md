# rest-snmp
This repo provides a REST Api to manage sentry model PDU's.

# initial setup

Install dependencies
pip2 install -r requirements.txt

Setup database
sqlite3 /tmp/data.db < schema.sql

# usage
start the server using
python2 rest_server.py

To add pdu send a json post request containing pdus ip address and it's access string
curl -H "Content-Type: application/json" -X POST -d '{"ip":"10.0.1.13","acc_str":"access_string_here"}' http://localhost:5000/pdu/
it will return the a response containing id , the returned id will be used to control pdu

To view all the added pdu's and their id's , you have to send a get request
curl  http://localhost:5000/pdu/

To get status of Tower A , outlet 4 and pdu id 1 
curl  http://localhost:5000/status/1/A/4

To change status of Tower B , outlet 2 and pdu id 2
curl -H "Content-Type: application/json" -X POST -d '{"id":2,"tower":"B","outlet":2,"state":"off"}' http://localhost:5000/changestate/
vaild states are on , off , reboot

To remove pdu , you have to send a delete request containing pdu ip
curl -H "Content-Type: application/json" -X DELETE -d '{"ip":"10.0.1.13"}' http://localhost:5000/pdu/
