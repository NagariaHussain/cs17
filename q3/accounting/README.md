# accounting — building the ledger, one abstraction at a time

A follow-along accounting app built from first principles. We start where the
hand-written paper ledger left off — **raw rows you type by hand** — and climb a
ladder of abstractions, one rung per concept, each motivated by a pain the
previous rung made you feel.

## Why accounting (the history hook)

- **Double-entry bookkeeping is the oldest information system still in daily
  use.** Luca Pacioli printed it in 1494; the debit/credit/ledger structure has
  survived ~530 years unchanged. The data model you're about to build predates
  the computer by five centuries.
- **The first business computer ran accounting.** LEO (1951) did inventory
  valuation and payroll — cutting one employee's payroll calc from ~8 minutes by
  hand to seconds.
- **The app that made the PC serious was accounting too** — VisiCalc (1979), the
  first spreadsheet.

Accounting is the oldest information system, the first business-computing
workload, *and* the killer app of the personal computer.

## The abstraction ladder

Each rung is a runnable program. Every rung posts the **same** running example
— *"I put ₹1,000 of my own cash into the business, then bought ₹300 of supplies"*
— so you can watch the code change character against a fixed task. Rungs 0→2
print the **same** trial balance throughout: that's the proof that *refactoring*
changes the shape of the code, not its behavior. Rung 3 is the first to change
the output on purpose — because there we don't refactor, we teach the program a
new concept (what an account *is*), and a real trial balance falls out.

| Rung | Folder | New idea | The pain it removes |
|------|--------|----------|---------------------|
| 0 | [`rungs/rung0_raw_rows`](rungs/rung0_raw_rows/) | the ledger is just a list of rows | — (this *is* the pain) |
| 1 | [`rungs/rung1_a_function`](rungs/rung1_a_function/) | **procedural abstraction** — `post()` enforces the balance rule | unbalanced entries slip in silently |
| 2 | [`rungs/rung2_objects`](rungs/rung2_objects/) | **encapsulation** — the rule lives *inside* the entry object | you had to *remember* to check |
| 3 | [`rungs/rung3_accounts`](rungs/rung3_accounts/) | **polymorphism** — `account.balance()` by account type | `if asset: ... else: ...` everywhere |
| 4 | [`rungs/rung4_documents`](rungs/rung4_documents/) | **interfaces** — documents *emit* balanced entries | hand-writing Dr/Cr for every invoice |
| 5 | _(later)_ `rung5_storage` | **dependency inversion** — swap list → SQLite → ORM | the DB is welded to the app |

Storage (SQLite) is deliberately **not** rung 0. We stay in plain Python until
the coupling to "where the data lives" actually hurts (rung 5) — same principle
as everything else: don't introduce the abstraction before the pain.

## How to run

Each rung is self-contained, no dependencies:

```sh
python q3/accounting/rungs/rung0_raw_rows/ledger.py
python q3/accounting/rungs/rung1_a_function/ledger.py
python q3/accounting/rungs/rung2_objects/ledger.py
python q3/accounting/rungs/rung3_accounts/ledger.py
python q3/accounting/rungs/rung4_documents/ledger.py
```

Run them in order. The trial balance stays identical through Rungs 0→2 while the
code underneath changes character — then Rung 3 upgrades it to a real two-column
report once the program understands what each account means.

## Teaching notes

- **Resist refactoring early.** The value is in living at a rung long enough to
  *want* the next one. Let the annoyance land before you climb.
- **Money is integer paise, never floats.** `1000_00` means ₹1000.00. (A
  standalone CS lesson: why `0.1 + 0.2 != 0.3`.)
- **Corrections are new facts, not edits.** Later rungs make the ledger truly
  append-only; mistakes are fixed with reversing entries, never `UPDATE`/`DELETE`
  — the same idea as a write-ahead log or git history.
