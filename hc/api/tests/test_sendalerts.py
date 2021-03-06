from datetime import timedelta

from django.utils import timezone
from hc.api.management.commands.sendalerts import Command
from hc.api.models import Check
from hc.test import BaseTestCase
from mock import patch


class SendAlertsTestCase(BaseTestCase):

    @patch("hc.api.management.commands.sendalerts.Command.handle_one")
    def test_it_handles_few(self, mock):
        yesterday = timezone.now() - timedelta(days=1)
        names = ["Check %d" % d for d in range(0, 10)]

        for name in names:
            check = Check(user=self.alice, name=name)
            check.alert_after = yesterday
            check.status = "up"
            check.save()

        result = Command().handle_many()
        self.assertEqual(result, True, "handle_many should return True")

        handled_names = []
        for args, kwargs in mock.call_args_list:
            handled_names.append(args[0].name)

        self.assertEqual(set(names), set(handled_names))


    def test_it_handles_grace_period(self):
        check = Check(user=self.alice, status="up")
        # 1 day 30 minutes after ping the check is in grace period:
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        check.save()

        # Expect no exceptions--

        result = Command().handle_one(check)
        self.assertEqual(True, result, "handle_one should return True")


    @patch("hc.api.management.commands.sendalerts.Command.handle_one")
    def test_handle_many_true(self, mock):
        """Assert when Command's handle many that when handle_many should return True"""
        time = timezone.now() - timedelta(days=1)
        names = ["Name %d" % n for n in range(0, 1000)]

        for name in names:
            check = Check(user=self.bob, name=name)
            check.alert_after = time
            check.status = "up"
            check.nag_status=True
            check.save()
        result = Command().handle_many()
        self.assertEqual(result, True, "handle_many should return True")

    
        