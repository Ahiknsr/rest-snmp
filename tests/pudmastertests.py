import sys
from nose.tools import assert_not_equal , assert_equals


#necessary as pdumaster is in parent directory
sys.path.append('../')


from pudmaster import Pdu


class TestPDU(Pdu):

    def nextCmd(self,oid):
        return [[(('some_oid'), (2))]]

    def getCmd(self,oid):
        return 1

    def setCmd(self,oid,value):
        return 1

#initilalize a object for testing
pdu_test = TestPDU('127.0.0.1',161,'access_string')


def test_get_num_towers():
    assert_equals(pdu_test.get_num_towers() , 2)


def test_change_state():
    assert_equals(pdu_test.change_state('A',6,'on') , 1)
    #case should fail as tower d doesn't exist
    assert_not_equal(pdu_test.change_state('d',6,'off') , 1)
    #case should fail as satate onoff doesn't exist
    assert_not_equal(pdu_test.change_state('A',6,'onoff') , 1)

