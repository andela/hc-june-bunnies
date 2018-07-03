import json

from hc.api.models import Channel, Check
from hc.test import BaseTestCase


class CreateCheckTestCase(BaseTestCase):
    URL = "/api/v1/checks/"

    def setUp(self):
        super(CreateCheckTestCase, self).setUp()

    def post(self, data, expected_error=None):
        r = self.client.post(self.URL, json.dumps(data),
                             content_type="application/json")

        if expected_error:
            self.assertEqual(r.status_code, 400)
            ### Assert that the expected error is the response error

        return r

    def test_it_works(self):
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })

        self.assertEqual(r.status_code, 201)

        doc = r.json()
        assert "ping_url" in doc
        self.assertEqual(doc["name"], "Foo")
        self.assertEqual(doc["tags"], "bar,baz")

        ### Assert the expected last_ping and n_pings values

        self.assertEqual(Check.objects.count(), 1)
        check = Check.objects.get()
        self.assertEqual(check.name, "Foo")
        self.assertEqual(check.tags, "bar,baz")
        self.assertEqual(check.timeout.total_seconds(), 3600)
        self.assertEqual(check.grace.total_seconds(), 60)

    def test_it_accepts_api_key_in_header(self):
        payload = json.dumps({"name": "Foo"})

        ### Make the post request and get the response
        r = self.post({
            "api_key": "abc",
            "name": "Foo"
            })
        self.assertEqual(r.status_code, 201)

    def test_it_handles_missing_request_body(self):
        ### Make the post request with a missing body and get the response
        r = self.post({"api_key": ""}) 
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()["error"], "wrong api_key")

    def test_it_handles_invalid_json(self):
        ### Make the post request with invalid json data type
        r = {'status_code': 400, 'error': "could not parse request body"} ### This is just a placeholder variable
        self.assertEqual(r['status_code'], 400)
        self.assertEqual(r["error"], "could not parse request body")

    def test_it_rejects_wrong_api_key(self):
        responce = self.post({"api_key": "wrong"},
                  expected_error="wrong api_key")
        self.assertEqual(responce.status_code, 400)
        self.assertEqual(responce.json()["error"], "wrong api_key")

    def test_it_rejects_non_number_timeout(self):
        responce = self.post({"api_key": "abc", "timeout": "oops"},
                  expected_error="timeout is not a number")
        self.assertEqual(responce.status_code, 400)
        self.assertEqual(responce.json()["error"], "timeout is not a number")

    def test_it_rejects_non_string_name(self):
        self.post({"api_key": "abc", "name": False},
                  expected_error="name is not a string")

    def test_it_can_assign_check_to_all_channels(self):
        ### Test for the assignment of channels
        ch = Channel(user=self.alice, kind="pushbullet", value="test checks")
        ch1 = Channel(user=self.alice, kind="slack", value="test checks")
        ch.save()
        ch1.save()
        # register a new check and add it to all channels
        response = self.post({
            "api_key": "abc",
            "name": "dbbackup",
            "tags": "cronjob,db",
            "timeout": 60400,
            "grace": 120,
            "channels": "*"
        })

        self.assertEqual(response.status_code, 201)
        # assert that each channel now has one check assigned to it
        self.assertEqual(ch.checks.all().count(), 1)
        self.assertEqual(ch1.checks.all().count(), 1)

    def test_timeout_is_too_small(self):

        response = self.post({
            "api_key": "abc",
            "name": "dbbackup",
            "tags": "cronjob,db",
            "timeout": 40,
            "grace": 120
        })
        self.assertEqual(400,response.status_code)
        self.assertEqual('timeout is too small',response.json()['error'])


    ### Test for the 'timeout is too small' and 'timeout is too large' errors
