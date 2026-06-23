# Rung 4 — documents

> You stop speaking in debits and credits and start speaking in *documents*:
> "we invoiced Acme ₹500", "Acme paid ₹200". Each document knows its own
> accounting recipe, so it *emits* a balanced journal entry on demand. The
> ledger asks every document the same one question — "what entry do you make?" —
> and doesn't care what kind it is.

```sh
python ledger.py
```

## What changed

A `Document` layer sits on top of the ledger. Each document type carries its own
posting rule and hands back a ready-made, balanced entry:

```python
class Document:
    def to_journal_entry(self):
        raise NotImplementedError          # the one promise every document makes

@dataclass
class SalesInvoice(Document):
    customer: str
    amount: int
    def to_journal_entry(self):
        return (JournalEntry(f"Sales Invoice — {self.customer}")
                    .add(debtors, debit=self.amount)     # the recipe lives
                    .add(sales,   credit=self.amount))   # HERE, written once
```

And the ledger gains one method that works for *any* document:

```python
def post_document(self, document):
    self.post(document.to_journal_entry())   # ask for the entry, then post it
```

So recording the sale reads like the business, not like bookkeeping:

```python
ledger.post_document(SalesInvoice("Acme Corp", 500_00))
ledger.post_document(Payment("Acme Corp", 200_00))
```

## The idea

**Interfaces (programming to a promise, not a type).** `post_document` never
checks *what kind* of document it got. It relies on a single shared promise —
`to_journal_entry()` — that every document keeps in its own way. A `SalesInvoice`
keeps it one way, a `Payment` the mirror way, and the ledger is blind to the
difference. Add `PurchaseInvoice` tomorrow and `post_document` already handles
it, untouched.

This is the keystone the whole quarter rests on:

> Every business document, when posted, writes balanced debit/credit lines into
> one append-only ledger. Every report is just a query over that ledger.

Two pains vanish at once:

- **You no longer hand-write Dr/Cr.** The recipe ("a sale is Dr Debtors / Cr
  Sales") lives in `SalesInvoice`, written once, not in the memory of whoever
  records the sale. Get it wrong in one place and you fix it in one place.
- **A document can't be fat-fingered into imbalance.** Both legs are computed
  from the *same* `amount`, so the entry is balanced *by construction* — the
  Rung 0 typo is now structurally impossible, not merely caught.

## Documents generate entries — they don't replace them

Notice transactions 1–2 (owner's capital, buying supplies) are still hand-written
`JournalEntry`s. Documents don't abolish journal entries; they *manufacture* them
for the repetitive business cases. Everything — manual or document-born — still
flows through the same `post()` and lands as balanced lines in the one ledger.
The trial balance code is byte-for-byte Rung 3's and never knows the difference.

## What the story gained

The business made its first sale, so two accounts join the trial balance:
**Debtors** (an asset — money Acme owes us) and **Sales** (income). After the
₹500 invoice and a ₹200 payment, Debtors correctly shows ₹300 still outstanding,
and the books balance at ₹1500 on each side.

## The next pain

The ledger is still an in-memory Python list — close the program and the books
evaporate. The list needs to become a file on disk, but *without* welding the
database to every report and document. The app should depend on "a ledger", not
on "a list".

➡️ [Rung 5 — storage](../rung5_storage/)

⬅️ [Rung 3](../rung3_accounts/)
