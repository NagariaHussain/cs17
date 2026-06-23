# Rung 2 — objects

> The rule moves *into* the data. A `JournalEntry` knows whether it balances.
> You ask the object about itself instead of remembering to check on the side.

```sh
python ledger.py
```

## What changed

Loose tuples became `Posting` and `JournalEntry` objects, and the balance check
became a method:

```python
entry = (JournalEntry("Owner invests cash")
            .add("Cash", debit=1000_00)
            .add("Capital", credit=1000_00))

entry.is_balanced()   # ask the entry itself
```

The thing you couldn't do in Rung 1 — interrogate a transaction *before*
posting it — is now natural: `rent.is_balanced()` returns `False` and you never
go near the ledger.

## The idea

**Encapsulation.** The data (the postings) and the invariant that governs it
(`debits == credits`) now live in the same object. In Rung 1 they had drifted
apart — rule in `post()`, data in tuples. Bringing them together means the rule
travels *with* every entry, wherever it goes.

A small but real bonus the tuples couldn't give us: each entry carries a
**narration** — the *why* of the transaction. That "why" is the seed of what
ERPNext stores as a **voucher** (which document caused these ledger lines), and
it's exactly the handle Rung 4 grabs when documents start *emitting* entries.

## Still the same behaviour

The trial balance prints the same numbers as Rungs 0 and 1 — Cash ₹700.00,
Capital −₹1000.00, Supplies ₹300.00, summing to ₹0.00. Three different shapes of
code, one unchanged result. That is what "refactoring" means, made visible.

## The next pain

Right now `Cash` is just a string and we net everything debit-positive — which
is why Capital prints as a confusing −₹1000.00. Real accounts have *types*: an
asset is debit-normal, a liability is credit-normal. Asking `account.balance()`
should mean different arithmetic per type — without `if`s scattered everywhere.

➡️ [Rung 3 — accounts & polymorphism](../rung3_accounts/)

## Later (previews, not built yet)

- **Rung 4 — Documents.** A `SalesInvoice` shouldn't make you hand-write
  `Dr Debtors / Cr Sales`. It should *emit* a balanced `JournalEntry` itself —
  the moment the whole "documents post to the ledger" architecture clicks.
- **Rung 5 — Storage.** Swap the in-memory list for SQLite, then an ORM, behind
  the same `Ledger` interface, with nothing above it changing.

⬅️ [Rung 1](../rung1_a_function/)
