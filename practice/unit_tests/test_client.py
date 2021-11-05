import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, PORT, ACTION, PRESENCE
from client import create_message, check_ans


class TestClient(unittest.TestCase):   
    def test_create_message(self):
        test = create_message(server_port=7777)
        test[TIME] = 1635775000
        self.assertEqual(test, {ACTION: PRESENCE, PORT: 7777, TIME: 1635775000, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_check_ans_200(self):
        self.assertEqual(check_ans({RESPONSE: 200}), '200 : OK')

    def test_check_ans_400(self):
        self.assertEqual(check_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_check_ans_no_response(self):
        self.assertRaises(ValueError, check_ans, {ERROR: 'Bad Request'})

if __name__ == '__main__':
    unittest.main()
