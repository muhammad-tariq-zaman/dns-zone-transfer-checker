import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import check

def row(server, zone, status, records):
    return {"server": server, "zone": zone, "axfr_status": status,
            "records_transferred": str(records)}

class TestZoneTransferChecker(unittest.TestCase):
    def test_allowed_with_records_is_exposed(self):
        self.assertEqual(check([row("ns1", "example.com", "ALLOWED", 42)])[0][4], "EXPOSED")
    def test_allowed_empty_records(self):
        self.assertEqual(check([row("ns1", "example.com", "ALLOWED", 0)])[0][4], "ALLOWED (EMPTY)")
    def test_denied_is_blocked(self):
        self.assertEqual(check([row("ns1", "example.com", "DENIED", 0)])[0][4], "BLOCKED")
    def test_refused_is_blocked(self):
        self.assertEqual(check([row("ns1", "example.com", "REFUSED", 0)])[0][4], "BLOCKED")
    def test_timeout_is_inconclusive(self):
        self.assertEqual(check([row("ns1", "example.com", "TIMEOUT", 0)])[0][4], "INCONCLUSIVE")
    def test_status_case_insensitive(self):
        self.assertEqual(check([row("ns1", "example.com", "denied", 0)])[0][4], "BLOCKED")
    def test_exposed_first(self):
        r = check([row("ns2", "b.example", "DENIED", 0),
                   row("ns1", "a.example", "ALLOWED", 10)])
        self.assertEqual(r[0][1], "a.example")
    def test_empty_input(self):
        self.assertEqual(check([]), [])
