# Rung 11 — the reports owners actually want

> Rung 10 handed a bookkeeper everything: a trial balance, invoices to create,
> list, open, cancel and amend, all behind a login. But an owner never reads a
> trial balance. They ask two questions — *did we make money?* and *what do we
> own and owe?* This rung answers both with a Profit & Loss and a Balance Sheet,
> and the punchline of the whole quarter falls out for free: a report is just
> another **query** over the one append-only ledger.

```sh
pip install -r requirements.txt
flask --app app run
```

Then visit http://localhost:5000/ (log in as **admin** / **admin**).

This is the capstone, so it supersets every feature from rungs 6–10: read the
trial balance, create/list/open invoices via a `sales_invoice` document table,
cancel and amend them, users + login — plus the two new reports and the full
navigation bar.

## What changed

Two new routes, and neither stores a single new row:

```python
@app.route("/reports/pnl")              # Income − Expense  → Net Profit
@app.route("/reports/balance-sheet")    # Assets  vs  Liabilities + Equity + Net Profit
```

Both lean on the kernel's **polymorphic account types** to sort accounts into
buckets — the report doesn't know account names, only kinds:

```python
for account, balance in kernel.trial_balance(get_ledger())[0]:
    if   isinstance(account, kernel.Income):    buckets["income"].append(...)
    elif isinstance(account, kernel.Expense):   buckets["expense"].append(...)
    elif isinstance(account, kernel.Asset):     buckets["asset"].append(...)
    elif isinstance(account, kernel.Liability): buckets["liability"].append(...)
    elif isinstance(account, kernel.Equity):    buckets["equity"].append(...)
```

- **P&L** lists Income and Expense and shows **Net Profit = Income − Expense**
  (prominent, class `ok` when positive). With the seed: Sales ₹500.00, no
  expenses → Net Profit ₹500.00.
- **Balance Sheet** sums Assets (Cash ₹900 + Supplies ₹300 + Debtors ₹300 =
  ₹1500.00) on one side, and Liabilities + Equity + Net Profit
  (Capital ₹1000 + Net Profit ₹500 = ₹1500.00) on the other, with an
  **in balance ✓** indicator.

The **full nav** lights up once you're logged in: Trial Balance · Invoices ·
New Invoice · P&L · Balance Sheet, with *logged in as &lt;user&gt;* and a Logout
button on the right.

## The idea

**Every report is a query over one ledger.** There is no reporting data — only
the same postings, regrouped. The trial balance nets every account; the P&L
keeps just the Income and Expense ones; the Balance Sheet keeps the Asset,
Liability and Equity ones. Same source, three lenses.

This cashes in **Rung 3**: because each account *is* its type — `Asset`,
`Income`, `Equity` — a report can categorize accounts with `isinstance` instead
of hard-coded name lists, and the kernel's polymorphic `balance()` already
returns each account on its natural side. It also closes the quarter's thesis:
*every business document posts balanced lines to one ledger; every report is a
query over that ledger.*

Watch how the two sides of the Balance Sheet tie out. Assets total ₹1500. Equity
alone (Capital ₹1000) is only ₹1000 — short by exactly the ₹500 the business
earned. That ₹500 is the **Net Profit** carried straight from the P&L. Profit
flows into equity, so adding it makes Equity + Liabilities ₹1500 too. The same
balanced double entry that kept debits equal to credits in the GL is what keeps
the Balance Sheet in balance — it was true all along; the report just shows it.

## The ladder is complete

```
0  raw rows      a list of tuples, nothing guards it
1  a function     post() guards debits == credits
2  objects        the rule lives inside the entry
3  accounts       account.balance() is polymorphic by type
4  documents      documents emit their own balanced entries
5  storage        the ledger is an interface; storage is swappable
6  a url          the kernel speaks HTTP — a trial balance in the browser
7  create         a form posts a real invoice into the GL
8  list / detail  invoices persist as documents you can list and open
9  cancel / amend  corrections are reversing entries, never edits
10 users          a login gates the books; every post is stamped with who
11 reports        the P&L and Balance Sheet — every report a query    ← you are here
```

What you've built is a small but real accounting application: typed accounts,
balanced-by-construction documents posting into one append-only ledger on disk,
behind a login, with the reports an owner actually reads — the shape ERPNext,
QuickBooks and SAP all take, in miniature.

Where to go next, now that the rungs are done:

- **More doctypes.** Add a Purchase Invoice (Expense up, Creditors up) or an
  Expense voucher. Each is just another `Document` that emits a balanced entry —
  and it shows up in the P&L and Balance Sheet for free, no report changes.
- **Multi-company.** Tag every GL row with a company and scope each query by it;
  the reports stay the same shape.
- **Swap the backend.** The app is written against the `Ledger` interface, so
  you can replace `SQLiteLedger` with an ORM-backed (or Postgres) ledger behind
  the *same* interface and nothing above it has to change — exactly the
  dependency inversion Rung 5 set up.

⬅️ [Rung 10](../rung10_users/)
