# Bookkeeping onboarding checklist

Everything a bookkeeper needs before the first month can be done, in the order
it usually comes in. Work through it with the business owner on the first call.

## Decide first

- [ ] The last month you trust. Bookkeeping starts the month after it. If no
      month can be trusted, the work starts with a cleanup.
- [ ] Which months are behind and need catch-up work.
- [ ] How often you want the books closed and reports sent: monthly or
      quarterly.
- [ ] Who answers questions about transactions, and how they prefer to be
      asked.
- [ ] Who the business's accountant or tax preparer is, if it has one.

## List every account

- [ ] Fill in `accounts-inventory.csv`: every bank account, credit card, loan
      and line of credit the business has had since the last month you trust,
      including accounts that have since closed.
- [ ] Mark any personal account that was used for business. Those
      transactions need to be picked out by hand.

## Send the documents

- [ ] Work down `document-request.csv` and mark each item received.
- [ ] Send statements as PDFs from the bank, not screenshots of the app. A
      statement has the printed opening and closing balances; an app screen
      does not.
- [ ] Log each statement in `statements-received.csv`, then run
      `check_statement_coverage.py` until nothing is missing.

## If you are in the U.S.

- [ ] Sales tax returns filed, for each state you collect in.
- [ ] Contractor W-9 forms, so year-end contractor totals are ready for 1099s.

## If you are in Canada

- [ ] GST/HST registration number and the returns filed.
- [ ] Books kept in Canadian dollars. Note any U.S. dollar accounts on the
      inventory.

## Before work starts

- [ ] The scope is written down: accounts, months, catch-up work and the
      reporting schedule.
- [ ] Every account on the inventory has a statement for every month needed.
