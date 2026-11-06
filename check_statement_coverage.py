"""List the statements still missing before bookkeeping can start.

Reads the accounts inventory (each account and the months it needs) and the
list of statements received, then prints every missing month per account,
statements received twice, statements outside the months needed, and any
statement for an account that is not on the inventory.

Usage:
  python3 check_statement_coverage.py accounts-inventory.csv statements-received.csv
  python3 check_statement_coverage.py accounts-inventory.csv statements-received.csv --request
  python3 check_statement_coverage.py accounts-inventory.csv statements-received.csv --json

--request prints the missing statements as a plain list grouped by bank or
card company, ready to paste into a message to the client.
Exit code 0 when nothing is missing, 1 when something is, 2 on bad input.
Python 3.8+, standard library only.

Part of https://github.com/ZeraBooks/bookkeeping-onboarding-checklist
(ZeraBooks, https://www.zerabooks.com/bookkeeping-services).
"""
import argparse
import csv
import json
import re
import sys

MONTH = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
INVENTORY_COLUMNS = ["Account", "Type", "Institution", "Last 4", "First month needed", "Last month needed"]


def months(first: str, last: str):
    y, m = map(int, first.split("-"))
    ly, lm = map(int, last.split("-"))
    while (y, m) <= (ly, lm):
        yield f"{y:04d}-{m:02d}"
        m += 1
        if m == 13:
            y, m = y + 1, 1


def month_name(ym: str) -> str:
    names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    y, m = ym.split("-")
    return f"{names[int(m) - 1]} {y}"


def coverage(inventory: str, received: str) -> dict:
    with open(inventory, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing_cols = [c for c in INVENTORY_COLUMNS if c not in (reader.fieldnames or [])]
        if missing_cols:
            raise ValueError(f"{inventory} is missing columns: {', '.join(missing_cols)}")
        accounts = [{k: (v or "").strip() for k, v in r.items()} for r in reader]
    with open(received, newline="", encoding="utf-8-sig") as f:
        rows = [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]

    by_last4 = {a["Last 4"]: a["Account"] for a in accounts if a["Last 4"]}
    known = {a["Account"] for a in accounts}
    got, seen, twice = set(), set(), []
    for r in rows:
        name = r.get("Account", "")
        if name not in known and r.get("Last 4") in by_last4:
            name = by_last4[r["Last 4"]]
        month = r.get("Month", "")
        if not MONTH.match(month):
            raise ValueError(f"'{month}' for {name} is not a YYYY-MM month")
        key = (name, month)
        if key in seen:
            twice.append(key)
        seen.add(key)
        got.add(key)

    result = {"accounts": [], "missing_total": 0, "not_on_inventory": [], "received_twice": [], "not_needed": []}
    for a in accounts:
        name = a["Account"]
        for col in ("First month needed", "Last month needed"):
            if not MONTH.match(a[col]):
                raise ValueError(f"{name}: '{a[col]}' in {col} is not a YYYY-MM month")
        need = list(months(a["First month needed"], a["Last month needed"]))
        missing = [m for m in need if (name, m) not in got]
        extra = sorted(m for acct, m in got if acct == name and m not in need)
        result["missing_total"] += len(missing)
        result["accounts"].append({"account": name, "type": a["Type"], "institution": a["Institution"], "last4": a["Last 4"],
                                   "needed": len(need), "received": len(need) - len(missing), "missing": missing})
        result["not_needed"] += [{"account": name, "month": m} for m in extra]
    result["not_on_inventory"] = sorted({acct for acct, _ in got if acct not in known})
    result["received_twice"] = [{"account": a, "month": m} for a, m in twice]
    return result


def print_report(r: dict) -> None:
    for a in r["accounts"]:
        status = "complete" if not a["missing"] else "missing " + ", ".join(a["missing"])
        print(f"{a['account']}: {a['received']} of {a['needed']} months, {status}")
    for acct in r["not_on_inventory"]:
        print(f"Not on the inventory: {acct}. Add it or ask what it is.")
    for d in r["received_twice"]:
        print(f"Received twice: {d['account']} {d['month']}. Keep one and check they're the same statement.")
    for d in r["not_needed"]:
        print(f"Not needed: {d['account']} {d['month']} is outside the months on the inventory.")
    print(f"\n{r['missing_total']} statement(s) missing.")


def print_request(r: dict) -> None:
    by_inst = {}
    for a in r["accounts"]:
        if a["missing"]:
            by_inst.setdefault(a["institution"] or "Other", []).append(a)
    if not by_inst and not r["not_on_inventory"]:
        print("Thanks, we have every statement we need.")
        return
    print("Here's what we still need to start your books:\n")
    for inst, accts in by_inst.items():
        print(inst)
        for a in accts:
            ending = f" ending {a['last4']}" if a["last4"] else ""
            print(f"- {a['account']}{ending}: {', '.join(month_name(m) for m in a['missing'])}")
        print()
    for acct in r["not_on_inventory"]:
        print(f"We also got a statement for \"{acct}\", which isn't on our list. What is this account, and is it still open?")
    print("PDF statements from the bank's website are best. Send them however is easiest.")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="List the statements still missing before bookkeeping can start.")
    ap.add_argument("inventory")
    ap.add_argument("received")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--json", action="store_true")
    g.add_argument("--request", action="store_true", help="print a plain list to send the client")
    a = ap.parse_args(argv)
    try:
        r = coverage(a.inventory, a.received)
    except (OSError, ValueError, KeyError) as exc:
        print(f"could not check: {exc}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(r, indent=2))
    elif a.request:
        print_request(r)
    else:
        print_report(r)
    return 1 if r["missing_total"] or r["not_on_inventory"] else 0


if __name__ == "__main__":
    sys.exit(main())
