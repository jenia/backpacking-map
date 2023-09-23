import unittest
from socket import getaddrinfo
from unittest.mock import patch

from app.example import resolve_postgres


class TestStringMethods(unittest.TestCase):
    @patch("app.example.getaddrinfo")
    def given_stateful_service_when_one_service_exists_then_return_service_ip(
        self, test_patch
    ):
        service = "google.com"
        port = 80
        address_google = getaddrinfo(service, port)
        ip_wanted = address_google[0][4][0]
        test_patch.return_value = address_google
        ret = resolve_postgres(service, port)
        self.assertEqual(ret, ip_wanted)
