# Test custom Django management commands

# Mocks behavior of db
from unittest.mock import patch

# Imports one of possible errors when connecting to db
from psycopg2 import OperationalError as Psycopg2Error

# lets us call command by name
from django.core.management import call_command

# another exception that may be called when connecting to db
from django.db.utils import OperationalError

# type of test we will be running
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTest(SimpleTestCase):
    # Test commands

    def test_wait_for_db_ready(self, patched_check):
        # Test waiting for db if db ready
        patched_check.return_value = True

        call_command("wait_for_db")

        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        # Test waiting for db when getting Op Error

        patched_check.side_effect = (
            [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        )

        call_command("wait_for_db")

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])
