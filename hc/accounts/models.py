import base64
import os
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core import signing
from django.db import models
from django.urls import reverse
from django.utils import timezone
from hc.lib import emails
from hc.api.models import Check, Channel


class Profile(models.Model):
    # Owner:
    user = models.OneToOneField(User, blank=True, null=True)
    team_name = models.CharField(max_length=200, blank=True)
    team_access_allowed = models.BooleanField(default=False)
    next_report_date = models.DateTimeField(null=True, blank=True)
    reports_allowed = models.CharField(max_length=20, default="monthly")
    ping_log_limit = models.IntegerField(default=100)
    token = models.CharField(max_length=128, blank=True)
    api_key = models.CharField(max_length=128, blank=True)
    current_team = models.ForeignKey("self", null=True)
    

    def __str__(self):
        return self.team_name or self.user.email

    def send_instant_login_link(self, inviting_profile=None):
        token = str(uuid.uuid4())
        self.token = make_password(token)
        self.save()

        path = reverse("hc-check-token", args=[self.user.username, token])
        ctx = {
            "login_link": settings.SITE_ROOT + path,
            "inviting_profile": inviting_profile
        }
        emails.login(self.user.email, ctx)

    def send_set_password_link(self):
        token = str(uuid.uuid4())
        self.token = make_password(token)
        self.save()

        path = reverse("hc-set-password", args=[token])
        ctx = {"set_password_link": settings.SITE_ROOT + path}
        emails.set_password(self.user.email, ctx)

    def set_api_key(self):
        self.api_key = base64.urlsafe_b64encode(os.urandom(24))
        self.save()

    def send_report(self):
        # reset next report date first:
        
        frequency = { "daily":1, "weekly":7, "monthly":30}  # create a dictionary to store frequencies
        days = frequency[self.reports_allowed.lower()]
        now = timezone.now()
        self.next_report_date = now + timedelta(days=days)
        self.save()

        token = signing.Signer().sign(uuid.uuid4())
        path = reverse("hc-unsubscribe-reports", args=[self.user.username])
        unsub_link = "%s%s?token=%s" % (settings.SITE_ROOT, path, token)

        ctx = {
            "checks": self.user.check_set.order_by("created"),
            "now": now,
            "frequency": self.reports_allowed,
            "unsub_link": unsub_link
        }

        emails.report(self.user.email, ctx)

    def invite(self, user, check=None):
        # if member exists, add the new check
        if Member.objects.filter(user=user):
            for check in checks:
                Member.objects.get(user=user).check_assigned.add(check.id)
        else:
            member = Member(team=self, user=user)
            member.save()
            member.check_assigned.add(check.id)
        # assign check to user channels
        channels = Channel.objects.filter(user=user)
        for channel in channels:
            channel.checks.add(check.id)
        # Switch the invited user over to the new team so they
        # notice the new team on next visit:
        user.profile.current_team = self
        user.profile.save()

        user.profile.send_instant_login_link(self)


class Member(models.Model):
    team = models.ForeignKey(Profile)
    user = models.ForeignKey(User)
    check_assigned = models.ManyToManyField(Check)
