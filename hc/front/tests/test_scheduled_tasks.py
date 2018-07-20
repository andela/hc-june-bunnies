from hc.api.models import Task
from hc.test import BaseTestCase
from datetime import timedelta as td
from django.utils import timezone


class ScheduledTaskTestCase(BaseTestCase):

    def setUp(self):
        super(ScheduledTaskTestCase, self).setUp()
        self.task = Task(task_scheduler=self.alice, subject="Alice task Here")
        self.task.schedule = "* * * * *"
        self.task.save()

    def test_it_works(self):
        self.client.login(username="alice@example.com", password="password")
        
        for email in ("alice@example.org", "bob@example.org"):
            self.client.login(username=email, password="password")
            response = self.client.get("/tasks/")
            self.assertEqual(response.status_code, 200)

    def test_it_creates_tasks(self):
      url = "/tasks/"
      form = {"email_subject": "email test", "email_body": "test", "schedule": "* * * * *"}
      tasks= Task.objects.all().count()
      self.client.login(username="alice@example.org", password="password")
      response = self.client.post(url, form)
      self.assertEqual(response.status_code, 200)
      self.assertEqual(tasks, 1)
