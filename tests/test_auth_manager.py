import unittest
from modules.Security_Access_Control.auth_manager import (
    verify_access,
    generate_token,
    USER_STORE,
)


class TestAuthManager(unittest.TestCase):

    def setUp(self):
        USER_STORE["user123"]["usage"] = 0

    def test_valid_access(self):
        result = verify_access("user123", "Prompt_Engine")
        self.assertEqual(result["status"], "granted")
        self.assertIn("timestamp", result)

    def test_user_not_found(self):
        result = verify_access("unknown_user", "Prompt_Engine")
        self.assertEqual(result["status"], "denied")
        self.assertEqual(result["reason"], "user_not_found")

    def test_unauthorized_module(self):
        result = verify_access("user123", "Unknown_Module")
        self.assertEqual(result["status"], "denied")
        self.assertEqual(result["reason"], "unauthorized_module")

    def test_quota_exceeded(self):
        USER_STORE["user123"]["usage"] = 100
        result = verify_access("user123", "Prompt_Engine")
        self.assertEqual(result["status"], "denied")
        self.assertEqual(result["reason"], "quota_exceeded")

    def test_generate_token(self):
        token = generate_token("user123")
        self.assertEqual(token["user_id"], "user123")
        self.assertTrue(token["valid"])
        self.assertIn("issued_at", token)


if __name__ == "__main__":
    unittest.main()
