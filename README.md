# Bookkeeping onboarding checklist

To start with a new bookkeeper, a business needs to agree the last month it trusts, list every bank, card, loan and payment processor account, and send statements for every month since, plus the old trial balance, unpaid invoice and bill lists and any payroll and sales tax reports. [ZeraBooks bookkeeping services](https://www.zerabooks.com/bookkeeping-services) start this way: a free call, then our team does the books on our own AI bookkeeping ledger, with a read-only login for you and an upload portal for the documents on this list.

These files make that list and find the gaps: a 14-item document request, an accounts inventory, a statement coverage check that lists every missing month and drafts the message asking for it, and eight fictional onboardings with the gaps that happen in real ones.

- Start here: [`onboarding-checklist.md`](onboarding-checklist.md) and [`document-request.csv`](document-request.csv)
- The check: [`check_statement_coverage.py`](check_statement_coverage.py) (Python 3.8+, standard library)
- Schemas: [`schema/`](schema/)
- Samples: [`samples/`](samples/), all fictional
- Release zip: [latest](https://github.com/ZeraBooks/bookkeeping-onboarding-checklist/releases/latest)

## Files

| File | What it is |
|---|---|
| `onboarding-checklist.md` | The decisions, account list and documents to settle before the first month, with U.S. and Canada items. |
| `document-request.csv` | 14 documents a bookkeeper asks for, why each is needed, the period, who it applies to and a Received column. |
| `accounts-inventory.csv` | Every account the business has had and the months a statement is needed for. Fictional sample rows. |
| `statements-received.csv` | One row per statement received, by account and month. Fictional sample rows. |
| `check_statement_coverage.py` | Compares the two: every missing month per account, statements for accounts not on the inventory, statements received twice, and statements outside the months needed. |
| `first-month.md` | What happens week by week in the first month of a remote bookkeeping engagement. |
| `schema/` | JSON Schemas for the inventory, the received list and the document request. |
| `samples/` | Eight fictional onboardings, each with an `expected.json` the tests check against. |

## How to use it

1. On the first call, agree the last month you trust and fill in
   `accounts-inventory.csv` with every account and the months needed.
   Include accounts that are closed now but were open in that period, and
   payment processors (Square, Stripe, Shopify, PayPal): their payouts are
   net of fees, and the monthly summary is how gross sales get booked.
2. Send the business owner `document-request.csv`. Delete rows that don't
   apply.
3. As statements arrive, add a row to `statements-received.csv`.
4. Find the gaps:

   ```
   python3 check_statement_coverage.py accounts-inventory.csv statements-received.csv
   ```

5. Ask for what's missing. `--request` writes the list for you, grouped by bank:

   ```
   $ python3 check_statement_coverage.py accounts-inventory.csv statements-received.csv --request
   Here's what we still need to start your books:

   First Example Bank (fictional)
   - Savings ending 5678: August 2026, September 2026

   Demo Lending (fictional)
   - Equipment loan ending 3456: July 2026, August 2026

   We also got a statement for "Old payroll account", which isn't on our list. What is this account, and is it still open?
   PDF statements from the bank's website are best. Send them however is easiest.
   ```

6. Start the bookkeeping once the script says 0 statements missing. `--json`
   prints the same result for a tracker or script. The exit code is 0 when
   nothing is missing, 1 when something is, and 2 when a file can't be read.

## The sample at the top level

The fictional business trusts its books through June 2026 and needs July to
October. The script finds savings missing August and September, the loan
missing July and August, and a statement for an "Old payroll account" that
nobody listed. That last one matters most: an account the owner forgot is the
usual reason a first month won't tie. All figures are fictional.

## Eight more onboardings

`scripts/generate_samples.py` builds them in `samples/`, each with the kind of gap that happens in real onboardings:

| Sample | Period | What the check finds |
|---|---|---|
| `juniper-lane-bakery` | Jan to Oct 2026 | Savings missing March and April; the Square summary missing September |
| `okafor-family-dental` | Jul 2025 to Sep 2026 | The equipment loan's first three months missing; a money market account nobody listed |
| `brightwater-landscaping` | Apr to Oct 2026 | A card closed in June needs statements only through June; one checking statement sent twice |
| `redline-freight` | Jan to Sep 2026 | No factoring reserve statements at all |
| `fernhill-goods` | Mar to Oct 2026 | Nothing missing: a card statement named "Summit card 1188" matches the inventory by its last 4 |
| `vega-cpa` | Jul to Oct 2026 | Nothing missing |
| `st-brendan-pantry` | Oct 2025 to Sep 2026 | The restricted grant account missing August and September; a September 2025 statement that isn't needed |
| `tan-ruiz-law` | Jan to Oct 2026 | The IOLTA trust account missing February; a line of credit nobody listed |

## FAQ

### How far back do the statements need to go?

To the last month the books can be trusted. If the old books were never
reconciled, that may be the start of the year or earlier, and the work is a
cleanup before ongoing bookkeeping.

### Why statements and not a bank export?

A statement prints the opening and closing balance for the month, which is
what each month is reconciled to. An export or app screen usually doesn't.

### Do I need to sort the documents before sending them?

No. Send everything you have. Sorting is part of the bookkeeper's job, and the
coverage check finds what's still missing.

### What about a statement period that doesn't end on the last day of the month?

Use the month the statement period ends in. A card statement that runs June 25
to July 24 counts as July.

## Working with ZeraBooks

[ZeraBooks bookkeeping services](https://www.zerabooks.com/bookkeeping-services):
our team does your books on ZeraBooks' own
[AI bookkeeping](https://www.zerabooks.com/ai-bookkeeping) ledger and delivers
your reports on the schedule you set. You get your own login with a read-only
view of your dashboard, and an upload portal to send statements, bills and
invoices. Plans start at $150 a month (USD), for businesses anywhere in the
world, and every engagement starts with a free call. When the books are
behind, see what a
[bookkeeping cleanup](https://www.zerabooks.com/bookkeeping-cleanup) involves.

## Tests

```
python3 scripts/generate_samples.py
python3 -m unittest discover -s tests -v
```

`MANIFEST.json` and `checksums.txt` list every data file with its SHA-256.

## License

The content and data in this repository are licensed under
[CC BY 4.0](LICENSE). The code (`check_statement_coverage.py` and `scripts/`)
is licensed under [MIT](LICENSE-CODE). Cite it with [`CITATION.cff`](CITATION.cff).

Related: [ZeraBooks/bookkeeping-handover-kit](https://github.com/ZeraBooks/bookkeeping-handover-kit) for the opening balances and access checklist when books move from another bookkeeper.

Maintained by [ZeraBooks](https://www.zerabooks.com).
