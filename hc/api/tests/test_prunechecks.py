from datetime import timedelta

from django.utils import timezone
from hc.api.management.commands.prunechecks import Command
from hc.api.models import Check
from hc.test import BaseTestCase
from mock import patch


class PruneChecksTestCase(BaseTestCase):

    @patch("hc.api.management.commands.sendalerts.Command.handle_one")
    def test_it_reaches_prunes(self, mock):
        check = Check(user=None)
        check.created = timezone.now() - timedelta(days=1, minutes=30)
        check.save()

        # Expect no exceptions--

        result = Command().handle(check)
        self.assertEqual(result, "Done! Pruned 0 checks.")
    