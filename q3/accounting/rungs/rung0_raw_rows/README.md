# Rung 0 — raw rows, by hand

> **No magic.** The general ledger is a list. Each row is one posting. Posting a
> transaction is appending two rows that should add up. The "computer" is doing
> nothing you couldn't do on paper.

```sh
python ledger.py
```

## What you write

Two literal rows per transaction:

```python
gl.append(("Cash",    1000_00, 0))        # debit Cash  ₹1000
gl.append(("Capital", 0,       1000_00))  # credit Capital ₹1000
```

## The pain (this is the whole reason Rung 1 exists)

Transaction 3 has a typo — `30_00` where it should be `300_00`. **Nothing
objects.** The program runs happily. The mistake only shows up at the very end,
as a trial balance that doesn't sum to zero — with no hint of *which* of the
(here 3, in real life 3,000) transactions is the lopsided one.

The error is detected **far in time and space from where it was made.** That gap
is the pain. The fix is obvious once you feel it: *check the moment you post.*

➡️ [Rung 1 — a function](../rung1_a_function/)
