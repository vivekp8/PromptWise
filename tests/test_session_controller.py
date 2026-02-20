# tests/test_session_controller.py

import unittest
from modules.Chat_Session_Management import session_controller


class TestSessionController(unittest.TestCase):

    def test_create_session(self):
        session_id = session_controller.create_session("vivek")
        self.assertIsNotNone(session_id)
        session = session_controller.get_session(session_id)
        self.assertTrue(session["active"])

    def test_get_existing_session(self):
        session_id = session_controller.create_session("vivek")
        session = session_controller.get_session(session_id)
        self.assertEqual(session["user_id"], "vivek")

    def test_get_invalid_session(self):
        session = session_controller.get_session("invalid_id")
        self.assertIsNone(session)


if __name__ == "__main__":
    unittest.main()
