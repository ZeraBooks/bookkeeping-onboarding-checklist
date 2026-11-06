import contextlib
import glob
import io
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import check_statement_coverage as cov  # noqa: E402


class Samples(unittest.TestCase):
    def test_each_sample_reports_what_expected_says(self):
        folders = sorted(glob.glob(os.path.join(ROOT, "samples", "*", "")))
        self.assertEqual(len(folders), 8)
        for f in folders:
            exp = json.load(open(os.path.join(f, "expected.json")))
            r = cov.coverage(os.path.join(f, "accounts-inventory.csv"), os.path.join(f, "statements-received.csv"))
            self.assertEqual({a["account"]: a["missing"] for a in r["accounts"]}, exp["missing"], f)
            self.assertEqual(r["missing_total"], exp["missing_total"], f)
            self.assertEqual(r["not_on_inventory"], exp["not_on_inventory"], f)
            self.assertEqual(r["received_twice"], exp["received_twice"], f)
            self.assertEqual(r["not_needed"], exp["not_needed"], f)

    def test_root_example_still_works_the_same(self):
        r = cov.coverage(os.path.join(ROOT, "accounts-inventory.csv"), os.path.join(ROOT, "statements-received.csv"))
        self.assertEqual(r["missing_total"], 4)
        self.assertEqual(r["not_on_inventory"], ["Old payroll account"])

    def test_renamed_account_matches_by_last4(self):
        f = os.path.join(ROOT, "samples", "fernhill-goods")
        r = cov.coverage(os.path.join(f, "accounts-inventory.csv"), os.path.join(f, "statements-received.csv"))
        self.assertEqual(r["not_on_inventory"], [])

    def test_request_message(self):
        f = os.path.join(ROOT, "samples", "redline-freight")
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = cov.main([os.path.join(f, "accounts-inventory.csv"), os.path.join(f, "statements-received.csv"), "--request"])
        self.assertEqual(code, 1)
        self.assertIn("Northline Factoring", out.getvalue())
        self.assertIn("January 2026", out.getvalue())

    def test_months(self):
        self.assertEqual(list(cov.months("2025-11", "2026-02")), ["2025-11", "2025-12", "2026-01", "2026-02"])

    def test_bad_month_is_rejected(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            inv = os.path.join(d, "i.csv")
            open(inv, "w").write("Account,Type,Institution,Last 4,First month needed,Last month needed\nChecking,Bank,X,1234,2026-13,2026-10\n")
            rec = os.path.join(d, "r.csv")
            open(rec, "w").write("Account,Month\n")
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(cov.main([inv, rec]), 2)


if __name__ == "__main__":
    unittest.main()
