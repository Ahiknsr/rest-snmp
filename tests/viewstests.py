import requests


#test adding a pdu is working or not
def test_adding_pdu():
    r = requests.post('http://localhost:5000/pdu/', json={"ip": "127.4.0.1","acc_str":"test_str"})
    assert 'id' in r.json().keys()
    r = requests.post('http://localhost:5000/pdu/', json={"ip": "127.4.0.1","acc_str":"test_str"})
    #adding the same ip should throw an error
    assert 'Error' in r.json().keys()
    r = requests.post('http://localhost:5000/pdu/', json={"ip": "127.4.0.a","acc_str":"test_str"})
    #adding the invalid ip should throw an error
    assert 'Error' in r.json().keys()
    r = requests.post('http://localhost:5000/pdu/', json={"ip": "127.4.0.a"})
    #adding pdu without access string should throw a error
    assert 'Error' in r.json().keys()


#testing api endpoint 
def test_view_pdu():
    r = requests.get('http://localhost:5000/pdu/')
    #we have added '127.4.0.1' in above step , so it should be present
    assert '127.4.0.1' in r.json().viewvalues()


#testing status end point
def test_status_endpoint():
    #we need a vaild pdu id
    r = requests.get('http://localhost:5000/pdu/')
    pdu_id = r.json().keys()[0]
    url = 'http://localhost:5000/status/' + pdu_id + '/A/1'
    r = requests.get(url)
    assert 'Status' in r.json().keys()


#testing changing status endpoint
def test_change_status():
    #we need a vaild pdu id
    r = requests.get('http://localhost:5000/pdu/')
    pdu_id = r.json().keys()[0]
    r = requests.post('http://localhost:5000/changestate/' , json={'id':pdu_id ,'tower':'A','state':'off'})
    assert 'done' in r.json()

#testing deleting pdu from database
def test_delete_pdu():
    r = requests.delete('http://localhost:5000/pdu/' , json={'ip':'127.4.0.1'})
    assert 'Sucess' in r.json()
    

