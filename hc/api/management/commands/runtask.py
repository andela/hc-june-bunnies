from django.core.management.base import BaseCommand, CommandError
from hc.api.models import Task
from hc.lib import emails

class Command(BaseCommand):
    help = 'Executes a specific command based on a cron job'

    def add_arguments(self, parser):
        parser.add_argument('--code', type=str)

    def handle(self, *args, **options):
      task_code = options['code']
      try:
          task = Task.objects.get(code=task_code)
          print(task)
      except Task.DoesNotExist:
          raise CommandError('Task "%s" does not exist' % task_code)
      recipient = task.task_scheduler.email  
      ctx = {
            "subject":task.subject,
            "body":task.body,
            "recipient": recipient,
            "code":task_code
      }
      emails.send_task(recipient, ctx)

      self.stdout.write(self.style.SUCCESS('Task Successfully run"%s"' % task_code))