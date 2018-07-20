from django.core import mail
from hc.api.models import Task
from hc.test import BaseTestCase
from django.utils import timezone
from datetime import timedelta
from mock import patch
from django.core.management import call_command
from hc.api.management.commands.runtask import Command

class SendTaskTestCase(BaseTestCase):

    def test_can_run_task(self):   
        task = Task(subject="Test task", task_scheduler=self.alice)
        task.schedule = "* * * * *"
        task.save()

        result = call_command('runtask', '--code', task.code)
        self.assertEqual(result, 'Run 1 task') 
        # Assert that the email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Scheduled Task: %s' %task.subject)
    