from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from hc.api.management.commands.ensuretriggers import Command
from hc.api.models import Check


class EnsureTriggersTestCase(TestCase):

    def test_ensure_triggers(self):
        Command().handle()

        check = Check.objects.create()
        assert check.alert_after is None
        self.assertIsNone(check.alert_after, msg=None)

        check.last_ping = timezone.now()
        check.save()
        check.refresh_from_db()
        assert check.alert_after is not None
        self.assertIsNotNone(check.alert_after, msg=None)

        alert_after = check.alert_after

        check.last_ping += timedelta(days=1)
        check.save()
        check.refresh_from_db()
        alert_after_refresh = check.alert_after
        #Test that alert_after is lesser than the check's alert_after
        assert alert_after_refresh > alert_after 
