"""Generate fictional onboarding samples in samples/.

    python3 scripts/generate_samples.py

Eight fictional businesses starting with a new bookkeeper. Each folder has
accounts-inventory.csv, statements-received.csv and expected.json (what the
coverage check must report). The gaps are the ones that happen in real
onboardings: a savings account nobody remembered, a card closed mid-year, a
processor account, a statement sent twice, a statement named differently
from the inventory. Seeded, so the files are the same every run.
"""
import csv
import json
import os
import random
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from check_statement_coverage import months  # noqa: E402

OUT = os.path.join(ROOT, "samples")
INV = ["Account", "Type", "Institution", "Last 4", "First month needed", "Last month needed", "Notes"]
REC = ["Account", "Month", "Last 4", "File"]

BIZ = [
    ("juniper-lane-bakery", "2026-01", "2026-10", [
        ("Operating checking", "Bank", "Harbor Point Savings Bank", "4471", None, ""),
        ("Savings", "Bank", "Harbor Point Savings Bank", "0932", None, ""),
        ("Business card", "Credit card", "Summit Card Services", "9014", None, ""),
        ("Square", "Payment processor", "Square", "", None, "Monthly sales and fees summary")],
     {"drop": [("Savings", "2026-03"), ("Savings", "2026-04"), ("Square", "2026-09")]}),
    ("okafor-family-dental", "2025-07", "2026-09", [
        ("Operating checking", "Bank", "Cedar Valley Credit Union", "5249", None, ""),
        ("Payroll checking", "Bank", "Cedar Valley Credit Union", "5250", None, ""),
        ("Practice card", "Credit card", "Granite Bank Card", "3380", None, ""),
        ("Equipment loan", "Loan", "Prairie Trust Bank", "7781", None, "Chair and imaging equipment")],
     {"drop": [("Equipment loan", "2025-07"), ("Equipment loan", "2025-08"), ("Equipment loan", "2025-09")], "extra": [("Old money market", "2025-12")]}),
    ("brightwater-landscaping", "2026-04", "2026-10", [
        ("Operating checking", "Bank", "Northfield National Bank", "1428", None, ""),
        ("Fuel card", "Credit card", "Fleet Fuel Card Co", "0071", None, ""),
        ("Old business card", "Credit card", "Summit Card Services", "2210", "2026-06", "Closed in June")],
     {"twice": [("Operating checking", "2026-05")]}),
    ("redline-freight", "2026-01", "2026-09", [
        ("Operating checking", "Bank", "Prairie Trust Bank", "5416", None, ""),
        ("Factoring reserve", "Other", "Northline Factoring", "", None, "Monthly reserve statement"),
        ("Truck loan 1", "Loan", "Highway Equipment Finance", "6610", None, ""),
        ("Truck loan 2", "Loan", "Highway Equipment Finance", "6611", None, "")],
     {"drop": [("Factoring reserve", m) for m in ("2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09")]}),
    ("fernhill-goods", "2026-03", "2026-10", [
        ("Checking", "Bank", "Lakeshore Community Bank", "7983", None, ""),
        ("Shopify Payments", "Payment processor", "Shopify", "", None, ""),
        ("PayPal", "Payment processor", "PayPal", "", None, ""),
        ("Business card", "Credit card", "Summit Card Services", "1188", None, "")],
     {"renamed": [("Business card", "Summit card 1188")]}),
    ("vega-cpa", "2026-07", "2026-10", [
        ("Checking", "Bank", "Lakeshore Community Bank", "1628", None, ""),
        ("Card", "Credit card", "Granite Bank Card", "2004", None, "")],
     {}),
    ("st-brendan-pantry", "2025-10", "2026-09", [
        ("Checking", "Bank", "Harbor Point Savings Bank", "2431", None, ""),
        ("Savings", "Bank", "Harbor Point Savings Bank", "2432", None, ""),
        ("Grant account", "Bank", "Harbor Point Savings Bank", "2433", None, "Restricted county grant")],
     {"drop": [("Grant account", "2026-08"), ("Grant account", "2026-09")], "outside": [("Checking", "2025-09")]}),
    ("tan-ruiz-law", "2026-01", "2026-10", [
        ("Operating", "Bank", "Northfield National Bank", "9014", None, ""),
        ("IOLTA trust", "Bank", "Northfield National Bank", "9015", None, "Client trust account"),
        ("Firm card", "Credit card", "Summit Card Services", "3301", None, "")],
     {"drop": [("IOLTA trust", "2026-02")], "extra": [("Line of credit", "2026-05"), ("Line of credit", "2026-06")]}),
]


def write(path, cols, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\r\n")
        w.writeheader()
        w.writerows(rows)


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    index = []
    for slug, first, last, accts, gaps in BIZ:
        f = os.path.join(OUT, slug)
        os.makedirs(f)
        inv, rec = [], []
        expected = {"missing": {}, "not_on_inventory": sorted({a for a, _ in gaps.get("extra", [])}), "received_twice": [], "not_needed": []}
        drop = set(gaps.get("drop", []))
        renamed = dict(gaps.get("renamed", []))
        for name, typ, inst, last4, closed, notes in accts:
            end = closed or last
            inv.append({"Account": name, "Type": typ, "Institution": inst, "Last 4": last4, "First month needed": first, "Last month needed": end, "Notes": notes})
            miss = []
            for m in months(first, end):
                if (name, m) in drop:
                    miss.append(m)
                    continue
                shown = renamed.get(name, name)
                rec.append({"Account": shown, "Month": m, "Last 4": last4, "File": f"{(shown).lower().replace(' ', '-')}-{m}.pdf"})
            expected["missing"][name] = miss
        for name, m in gaps.get("twice", []):
            rec.append({"Account": name, "Month": m, "Last 4": "", "File": f"{name.lower().replace(' ', '-')}-{m}-copy.pdf"})
            expected["received_twice"].append({"account": name, "month": m})
        for name, m in gaps.get("extra", []):
            rec.append({"Account": name, "Month": m, "Last 4": "", "File": f"{name.lower().replace(' ', '-')}-{m}.pdf"})
        for name, m in gaps.get("outside", []):
            rec.append({"Account": name, "Month": m, "Last 4": "", "File": f"{name.lower().replace(' ', '-')}-{m}.pdf"})
            expected["not_needed"].append({"account": name, "month": m})
        rec.sort(key=lambda r: (r["Account"], r["Month"]))
        write(os.path.join(f, "accounts-inventory.csv"), INV, inv)
        write(os.path.join(f, "statements-received.csv"), REC, rec)
        expected["missing_total"] = sum(len(v) for v in expected["missing"].values())
        json.dump(expected, open(os.path.join(f, "expected.json"), "w", encoding="utf-8"), indent=2)
        index.append([slug, first, last, len(inv), len(rec), expected["missing_total"], len(expected["not_on_inventory"])])
    with open(os.path.join(OUT, "index.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["sample", "first_month", "last_month", "accounts", "statements_received", "statements_missing", "accounts_not_on_inventory"])
        w.writerows(index)
    print(f"{len(index)} samples")


if __name__ == "__main__":
    main()
