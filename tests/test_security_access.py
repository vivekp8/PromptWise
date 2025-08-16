import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from core import security_access
from unittest.mock import patch

class TestSecurityAccess(unittest.TestCase):
    def test_real_access(self):
        self.assertEqual(security_access.get_user_role(1), "admin")
        self.assertEqual(security_access.get_user_role(3), "viewer")
        self.assertEqual(security_access.get_user_role(99), "guest")

    @patch("core.security_access.get_user_role")
    def test_mocked_access(self, mock_get_role):
        mock_get_role.return_value = "editor"
        role = security_access.get_user_role(42)
        self.assertEqual(role, "editor")