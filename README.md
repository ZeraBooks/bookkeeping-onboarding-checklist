# Bookkeeping onboarding checklist

To start with a new bookkeeper, a business needs to agree the last month it
trusts, list every bank, card and loan account, and send statements for every
month since, plus the old trial balance, unpaid invoice and bill lists and any
payroll and sales tax reports. These files make that list and find the gaps.

## Files

| File | What it is |
|---|---|
| `onboarding-checklist.md` | The decisions, account list and documents to settle before the first month, with U.S. and Canada items. |
| `document-request.csv` | 14 documents a bookkeeper asks for, why each is needed, the period, who it applies to and a Received column. |
| `accounts-inventory.csv` | Every account the business has had and the months a statement is needed for. Fictional sample rows. |
| `statements-received.csv` | One row per statement received, by account and month. Fictional sample rows. |
| `check_statement_coverage.py` | Compares the two and lists every missing month per account, plus statements for accounts not on the inventory. Python 3, standard library only. |
| `first-month.md` | What happens week by week in the first month of a remote bookkeeping engagement. |

## How to use it

1. On the first call, agree the last month you trust and fill in
   `accounts-inventory.csv` with every account and the months needed.
2. Send the business owner `document-request.csv`. Delete rows that don't
   apply.
3. As statements arrive, add a row to `statements-received.csv`.
4. Find the gaps:

   ```
   python3 check_statement_coverage.py accounts-inventory.csv statements-received.csv
   ```

5. Ask for what's missing. Start the bookkeeping once the script says 0
   statements missing.

## The sample

The fictional business trusts its books through June 2026 and needs July to
October. The script finds savings missing August and September, the loan
missing July and August, and a statement for an "Old payroll account" that
nobody listed. That last one matters most: an account the owner forgot is the
usual reason a first month won't tie. All figures are fictional.

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

## Learn more

[Bookkeeping services](https://www.zerabooks.com/bookkeeping-services) on
ZeraBooks, and what a
[bookkeeping cleanup](https://www.zerabooks.com/bookkeeping-cleanup) involves
when the books are behind.

## License

The content and data in this repository are licensed under
[CC BY 4.0](LICENSE). The code (`check_statement_coverage.py`) is licensed
under [MIT](LICENSE-CODE).

Maintained by [ZeraBooks](https://www.zerabooks.com).
