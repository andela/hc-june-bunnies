import json
from datetime import timedelta as td
from django.utils.timezone import now
from hc import settings
from hc.api.models import Check
from hc.test import BaseTestCase


class ListChecksTestCase(BaseTestCase):

    def setUp(self):
        super(ListChecksTestCase, self).setUp()

        self.now = now().replace(microsecond=0)

        self.a1 = Check(user=self.alice, name="Alice 1")
        self.a1.timeout = td(seconds=3600)
        self.a1.grace = td(seconds=900)
        self.a1.last_ping = self.now
        self.a1.n_pings = 1
        self.a1.status = "new"
        self.a1.save()

        self.a2 = Check(user=self.alice, name="Alice 2")
        self.a2.timeout = td(seconds=86400)
        self.a2.grace = td(seconds=3600)
        self.a2.last_ping = self.now
        self.a2.status = "up"
        self.a2.save()

    def get(self):
        return self.client.get("/api/v1/checks/", HTTP_X_API_KEY="abc")

    def test_it_works(self):
        response = self.get()
        # asserting status code
        self.assertEqual(200,response.status_code)
        doc = response.json()
        # is "checks" a key in doc?
        self.assertTrue("checks" in doc)

        checks = {check["name"]: check for check in doc["checks"]}
        
        self.assertEqual(2, len(doc['checks']))
        pause_url1 = '{}/api/v1/checks/{}/pause'.format(settings.SITE_ROOT, self.a1.code)
        pause_url2 = '{}/api/v1/checks/{}/pause'.format(settings.SITE_ROOT, self.a2.code)
        alice1 = checks['Alice 1']
        alice2 = checks['Alice 2']

        # assert values for check 1 are ok
        self.assertEqual(alice1['timeout'], 3600)
        self.assertEqual(alice1['grace'], 900)
        self.assertEqual(alice1['ping_url'], self.a1.url())
        self.assertEqual(alice1['status'], "new")
        self.assertEqual(alice1['last_ping'], self.now.isoformat())
        self.assertEqual(alice1['n_pings'], 1)
        self.assertEqual(alice1['pause_url'], pause_url1)

        # assert values for check 2 are ok
        self.assertEqual(alice2['timeout'], 86400)
        self.assertEqual(alice2['grace'], 3600)
        self.assertEqual(alice2['ping_url'], self.a2.url())
        self.assertEqual(alice2['status'], "up")
        self.assertEqual(alice2['last_ping'], self.now.isoformat())
        self.assertEqual(alice2['n_pings'], 0)
        self.assertEqual(alice2['pause_url'], pause_url2)



    def test_it_shows_only_users_checks(self):
        bobs_check = Check(user=self.bob, name="Bob 1")
        bobs_check.save()

        response = self.get()
        data = response.json()
        self.assertEqual(len(data["checks"]), 2)
        for check in data["checks"]:
            self.assertNotEqual(check["name"], "Bob 1")


    def test_it_accepts_api_key_in_request(self):
        # test it rejects wrong api_key
        wrong_api_key = 'aajnsajs'
        response = self.client.get("/api/v1/checks/", HTTP_X_API_KEY=wrong_api_key)
        self.assertEqual(response.status_code, 400)

        # test it accepts the right api_key
        right_api_key = 'abc'
        response = self.client.get("/api/v1/checks/", HTTP_X_API_KEY=right_api_key)
        self.assertEqual(response.status_code, 200)



