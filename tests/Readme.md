How to run tests :

Separate tests are written for pudmaster and rest-server 

To run tests for pudmaster , change to tests directory 
```
nosetests-2.7 -s -v pudmastertests.py
```

to run tests for rest-api provided ,first run the tests server in parent directory
```
python2  test_server.py
```

and then run the tests using
```
nosetests-2.7 -s -v viewstests.py
```
