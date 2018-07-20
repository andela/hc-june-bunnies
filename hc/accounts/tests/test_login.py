from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from hc.api.models import Check


class LoginTestCase(TestCase):
    """Performs tests to ensure the login process works. By:

    * Checking that a login link is sent.
    * Checking that bad links are caught.
    """

    def test_it_sends_link(self):
        check = Check()
        check.save()

        session = self.client.session
        session["welcome_code"] = str(check.code)
        session.save()

        form = {"email": "alice@example.org"}

        r = self.client.post("/accounts/login/", form)
        assert r.status_code == 302
        # Assert that a user was created 
        self.assertTrue(User.is_active)

        # And email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Log in to healthchecks.io')
        # Assert contents of the email body
        self.assertIn('To log into healthchecks.io', mail.outbox[0].body)
        # Assert that check is associated with the new user

    def test_it_pops_bad_link_from_session(self):
        self.client.session["bad_link"] = True
        self.client.get("/accounts/login/")
        assert "bad_link" not in self.client.session

        ### Other tests to be added

