import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, PORT, ACTION, PRESENCE
from server import check_client_message


class TestServer(unittest.TestCase):
    err_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    ok_dict = {RESPONSE: 200}

    def test_ok_check(self):
        self.assertEqual(check_client_message(
            {ACTION: PRESENCE, PORT: 7777, TIME: 1635775000, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_dict)

    def test_no_action(self):
        self.assertEqual(check_client_message(
            {PORT: 7777, TIME: 1635775000, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_wrong_action(self):
        self.assertEqual(check_client_message(
            {ACTION: 'Wrong', PORT: 7777, TIME: 1635775000, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_time(self):
        self.assertEqual(check_client_message(
            {ACTION: PRESENCE, PORT: 7777, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_user(self):
        self.assertEqual(check_client_message(
            {ACTION: PRESENCE, PORT: 7777, TIME: 1635775000}), self.err_dict)

    def test_unknown_user(self):
        self.assertEqual(check_client_message(
            {ACTION: PRESENCE, PORT: 7777, TIME: 1635775000, USER: {ACCOUNT_NAME: 'User'}}), self.err_dict)

if __name__ == '__main__':
    unittest.main()
