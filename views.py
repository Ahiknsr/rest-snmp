import sqlite3 
from flask.ext.restful import Resource
from flask import Flask, request, g, jsonify


from dbfunctions import query_db
from pudmaster import Pdu
from utils import validate_ip


PORT = 161
tower_dict = { 'A':'1' , 'a':'1' , 'B':'2' , 'b':'2' }
state_dict = {'0':'off' , '1':'on' ,'2':'offwait' , '3':'onwait' , '4':'offerror' , '5':'onerror'}


class PDU(Resource):

    def get(self):
        data = query_db('select id , ip from entries ')
        return  jsonify(data) 


    def post(self):
        json = request.json
        try:
            if validate_ip(json['ip']):
                g.db.execute('insert into entries ( ip , acc_str ) values ( ? , ? ) ', [ json['ip'] , json['acc_str'] ])
                g.db.commit()
                pdu_data = query_db('select * from entries where ip = ? ' ,[ json['ip'] ] , one = True  )
                return { 'id' : pdu_data[0] }
            else:
                return { 'Error' : 'invalid address' }
        except sqlite3.IntegrityError as e:
            return { 'Error' : 'ip address already exists' }
        except:
            print 'unhandled exception has occurred '
            return { 'Error' : 'Bad request' }


    def delete(self):
        try:
            json = request.json
            print 'delete request'
            g.db.execute('delete from entries where ip = ? ' , [ json['ip'] ] )
            g.db.commit()
            return { 'Sucess' : json['ip'] }
        except Exception as e:
            print e
            return {'Error' }

class Status(Resource):

    def get(self,id,tower,outlet):
        pdu_data = query_db('select ip , acc_str from entries where id = ? ' , [ id ] , one = True )
        if pdu_data is None:
            return { 'Error' : 'id doesn"t exist'}
        pdu = Pdu(pdu_data[0],PORT,pdu_data[1])
        oid = '1.3.6.1.4.1.1718.3.2.3.1.3.' + tower_dict[tower] + '.1.' + str(outlet)
        state = str(pdu.state_from_oid(oid))
        print state
        try:
            return { 'Sataus' : state_dict[state] }
        except KeyError:
            if 'No SNMP response' in state:
                return { 'Error' : 'unable to connect to Pdu' }
        except Exception as e:
            print e
            return {'Error'}


class ChangeState(Resource):

    def post(self):
        json = request.json
        pdu_data = query_db('select ip , acc_str from entries where id = ? ' , [ json['id']] , one = True )
        if pdu_data is None:
            return { 'Error' : 'id doesn"t exist'}
        pdu = Pdu(pdu_data[0],PORT,pdu_data[1])
        ret_value = pdu.change_state(json['tower'],json['outlet'],json['state'])
        if 'No SNMP response received' in str(ret_value):
            return { 'Error' : 'unable to connect to pdu' }
        else:
            return 'done'
