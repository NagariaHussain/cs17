# Rung 3 — accounts & polymorphism

> An account stops being a string and becomes an *object that knows its own
> type*. Ask any account for its balance and it does the right arithmetic for
> what it is — an asset one way, a liability the mirror image. The caller never
> asks "which kind is this?"

```sh
python ledger.py
```

## What changed

`"Cash"` (a bare string) became `Asset("Cash")` (an object), and the balance
arithmetic became a method each account type defines for itself:

```python
class DebitNormalAccount(Account):    # assets, expenses
    normal_side = "Dr"
    def balance(self, debits, credits):
        return debits - credits

class CreditNormalAccount(Account):   # liabilities, equity, income
    normal_side = "Cr"
    def balance(self, debits, credits):
        return credits - debits

class Asset(DebitNormalAccount):  pass
class Equity(CreditNormalAccount): pass
# ...
```

The reporting code then just says:

```python
bal = account.balance(debits, credits)   # the account picks the arithmetic
```

## The idea

**Polymorphism.** One message — `balance` — means different things depending on
the type of the object receiving it. The trial balance, the balance sheet, the
P&L: none of them contain `if account_type == "asset"`. They send `balance` and
let each account answer in its own way.

Compare the alternative this kills. Without polymorphism, *every* report needs
the same fork, copy-pasted and kept in sync by hand:

```python
if account_type in ("asset", "expense"):
    bal = debits - credits
else:
    bal = credits - debits
```

Five account types today, and that `if` in every report. Add a sixth type and
you hunt down every copy. Polymorphism moves the decision to one place — the
account classes — so adding `class ContraAsset(...)` teaches the *whole program*
at once.

## The output changed — and that's the point

This is the first rung whose trial balance is **not** byte-identical to the one
before it. The *data* is unchanged (the same postings, the same ledger), but the
*meaning* is richer, so the report gets better:

| | Rungs 0–2 | Rung 3 |
|---|---|---|
| Capital | −₹1000.00 (netted debit-positive — confusing) | **+₹1000.00 in the Cr column** (its natural balance) |
| The proof | everything sums to ₹0.00 | **total Dr == total Cr** (₹1000 = ₹1000) |

Rungs 0→2 reshaped code while holding behaviour fixed. Rung 3 is different: we
taught the program what accounts *are*, and a real two-column trial balance fell
out. Refactoring preserves behaviour; **modelling a new concept changes it on
purpose.**

A quiet bonus, like the narration in Rung 2: because accounts are objects with
identity, two postings to `cash` refer to the *same* account. A typo'd
`Asset("Cassh")` is a different object you have to create deliberately — strings
used to open a phantom account silently.

## The next pain

You still hand-write `Dr Debtors / Cr Sales` for every sale, holding each
transaction's accounting recipe in your head. That recipe belongs to the
*document* — a `SalesInvoice` should *emit* its own balanced entry.

➡️ [Rung 4 — documents](../rung4_documents/)

## Later (preview, not built yet)

- **Rung 5 — Storage.** Swap the in-memory list for SQLite, then an ORM, behind
  the same `Ledger` interface, with nothing above it changing.

⬅️ [Rung 2](../rung2_objects/)
