"""List the statements still missing before bookkeeping can start.

Reads the accounts inventory (each account and the months it needs) and the
list of statements received, then prints every missing month per account and
any statement for an account that is not on the inventory.
Usage: python3 check_statement_coverage.py accounts-inventory.csv statements-received.csv
"""
import csv
import sys


def months(first: str, last: str):
    y, m = map(int, first.split("-"))
    ly, lm = map(int, last.split("-"))
    while (y, m) <= (ly, lm):
        yield f"{y:04d}-{m:02d}"
        m += 1
        if m == 13:
            y, m = y + 1, 1


def main(inventory: str, received: str) -> int:
    with open(inventory, newline="", encoding="utf-8") as f:
        accounts = list(csv.DictReader(f))
    with open(received, newline="", encoding="utf-8") as f:
        got = {(r["Account"].strip(), r["Month"].strip()) for r in csv.DictReader(f)}

    known = {a["Account"].strip() for a in accounts}
    missing_total = 0
    for a in accounts:
        name = a["Account"].strip()
        need = list(months(a["First month needed"], a["Last month needed"]))
        missing = [m for m in need if (name, m) not in got]
        missing_total += len(missing)
        status = "complete" if not missing else "missing " + ", ".join(missing)
        print(f"{name}: {len(need) - len(missing)} of {len(need)} months, {status}")

    extra = sorted({acct for acct, _ in got if acct not in known})
    for acct in extra:
        print(f"Not on the inventory: {acct}. Add it or ask what it is.")

    print(f"\n{missing_total} statement(s) missing.")
    return 1 if missing_total or extra else 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 check_statement_coverage.py accounts-inventory.csv statements-received.csv")
    sys.exit(main(*sys.argv[1:]))
