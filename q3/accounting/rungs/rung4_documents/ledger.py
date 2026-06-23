"""
Rung 4 — documents. The business stops speaking in debits and credits and
starts speaking in *documents*: "we invoiced Acme ₹500", "Acme paid ₹200". A
document knows its own posting rule, so it *emits* a balanced JournalEntry on
demand — you never hand-write `Dr Debtors / Cr Sales` again.

The pain this removes: by Rung 3 the ledger is solid, but every real transaction
still means remembering its accounting recipe — a sale is Dr Debtors / Cr Sales,
a receipt is Dr Cash / Cr Debtors, a purchase is the other way round... Get the
recipe wrong and the books are *balanced but meaningless*. The rule "which
accounts does THIS kind of transaction touch?" belongs to the document, not to
the person typing it.

The idea is an **interface**: every Document, whatever kind, promises one method
— `to_journal_entry()`. The Ledger asks only for that. It doesn't care whether
it's a SalesInvoice or a Payment; if it can express itself as a balanced entry,
it can be posted. This is the architecture the whole quarter is built on:

    Every business document, when posted, writes balanced debit/credit lines
    into one append-only ledger. Every report is just a query over that ledger.

And a document can't be fat-fingered into imbalance the way Rung 0 was: both
legs are computed from the *same* amount, so it's balanced by construction.

Same ledger machinery as Rung 3. The running story gains the business's first
sale, so the trial balance grows two accounts — Debtors and Sales.
"""

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Accounts — unchanged from Rung 3. balance() is still polymorphic by type.
# ---------------------------------------------------------------------------
class Account:
    def __init__(self, name):
        self.name = name

    def balance(self, debits, credits):
        raise NotImplementedError("each Account subclass defines its own balance")

    def __repr__(self):
        return self.name


class DebitNormalAccount(Account):    # assets, expenses — a debit grows them
    normal_side = "Dr"

    def balance(self, debits, credits):
        return debits - credits


class CreditNormalAccount(Account):   # liabilities, equity, income — a credit grows them
    normal_side = "Cr"

    def balance(self, debits, credits):
        return credits - debits


class Asset(DebitNormalAccount):      pass
class Expense(DebitNormalAccount):    pass
class Liability(CreditNormalAccount): pass
class Equity(CreditNormalAccount):    pass
class Income(CreditNormalAccount):    pass


# ---------------------------------------------------------------------------
# Postings, entries, ledger — unchanged from Rung 3, with one addition:
# the ledger can now post a *document*, not just a hand-built entry.
# ---------------------------------------------------------------------------
@dataclass
class Posting:
    account: Account
    debit: int = 0    # paise
    credit: int = 0   # paise


@dataclass
class JournalEntry:
    narration: str
    postings: list = field(default_factory=list)

    def add(self, account, debit=0, credit=0):
        self.postings.append(Posting(account, debit, credit))
        return self

    def is_balanced(self):
        debits = sum(p.debit for p in self.postings)
        credits = sum(p.credit for p in self.postings)
        return debits == credits


class Ledger:
    """The append-only book of entries. It only accepts balanced ones —
    whether you hand it an entry directly or a document that emits one."""

    def __init__(self):
        self.entries = []

    def post(self, entry):
        if not entry.is_balanced():
            raise ValueError(f"Refusing to post unbalanced entry: {entry.narration!r}")
        self.entries.append(entry)

    def post_document(self, document):
        """Post anything that satisfies the Document interface. The ledger asks
        only one thing of it: turn yourself into a balanced JournalEntry."""
        self.post(document.to_journal_entry())

    def postings(self):
        for entry in self.entries:
            yield from entry.postings


# ---------------------------------------------------------------------------
# Documents — the new layer. A Document is anything that can express itself as
# a balanced JournalEntry. That single promise is the *interface*; each kind of
# document keeps its own accounting recipe so nobody downstream has to know it.
# ---------------------------------------------------------------------------
class Document:
    def to_journal_entry(self):
        raise NotImplementedError("every Document must emit a balanced JournalEntry")


@dataclass
class SalesInvoice(Document):
    """We sold something on credit. The recipe — Dr Debtors, Cr Sales — lives
    HERE, once, instead of in the head of whoever records the sale."""
    customer: str
    amount: int   # paise

    def to_journal_entry(self):
        return (JournalEntry(f"Sales Invoice — {self.customer}")
                .add(debtors, debit=self.amount)
                .add(sales, credit=self.amount))


@dataclass
class Payment(Document):
    """A customer paid down what they owe. Recipe: Dr Cash, Cr Debtors — the
    mirror of the invoice, and again the document is the only thing that knows."""
    customer: str
    amount: int   # paise

    def to_journal_entry(self):
        return (JournalEntry(f"Payment received — {self.customer}")
                .add(cash, debit=self.amount)
                .add(debtors, credit=self.amount))


# The chart of accounts. Documents above refer to these by name; in a real
# system (Rung 5 territory) they'd be looked up from the company's settings.
cash     = Asset("Cash")
supplies = Asset("Supplies")
debtors  = Asset("Debtors")     # money customers owe us — an asset
capital  = Equity("Capital")
sales    = Income("Sales")

ledger = Ledger()

# Transactions 1–2: still hand-written journal entries. Documents don't replace
# journals — opening capital and buying supplies are genuine manual entries even
# in ERPNext. Documents just *generate* entries for the repetitive business stuff.
ledger.post(
    JournalEntry("Owner invests cash")
        .add(cash, debit=1000_00)
        .add(capital, credit=1000_00)
)
ledger.post(
    JournalEntry("Buy supplies for cash")
        .add(supplies, debit=300_00)
        .add(cash, credit=300_00)
)

# Transaction 3: the business makes its first sale. We state it in BUSINESS
# terms; the document works out the ledger lines. Watch what we did NOT type.
invoice = SalesInvoice(customer="Acme Corp", amount=500_00)

emitted = invoice.to_journal_entry()
legs = "   ".join(f"Dr {p.account}" if p.debit else f"Cr {p.account}"
                  for p in emitted.postings)
print(f"SalesInvoice(Acme Corp, ₹500) emitted:  {legs}")
print(f"  balanced by construction? {emitted.is_balanced()}   "
      f"(we never typed a single Dr or Cr)\n")

ledger.post_document(invoice)

# Transaction 4: Acme pays ₹200 of the ₹500 — a different document, same
# interface. The ledger treats it identically: it just asks for the entry.
ledger.post_document(Payment(customer="Acme Corp", amount=200_00))


# ---------------------------------------------------------------------------
# Trial balance — identical reporting code to Rung 3. It reads postings off the
# ledger and never knows some of them were born from documents.
# ---------------------------------------------------------------------------
def rupees(paise):
    sign = "-" if paise < 0 else " "
    paise = abs(paise)
    return f"{sign}₹{paise // 100}.{paise % 100:02d}"


totals = {}
for p in ledger.postings():
    debits, credits = totals.get(p.account, (0, 0))
    totals[p.account] = (debits + p.debit, credits + p.credit)

print("TRIAL BALANCE")
print(f"{'':<10}{'Dr':>12}{'Cr':>12}")
print("-" * 34)
total_dr = total_cr = 0
for account, (debits, credits) in totals.items():
    bal = account.balance(debits, credits)
    if account.normal_side == "Dr":
        total_dr += bal
        print(f"{account.name:<10}{rupees(bal):>12}{'':>12}")
    else:
        total_cr += bal
        print(f"{account.name:<10}{'':>12}{rupees(bal):>12}")
print("-" * 34)
print(f"{'TOTAL':<10}{rupees(total_dr):>12}{rupees(total_cr):>12}")

if total_dr == total_cr:
    print("\nDebits equal credits. The books balance. ✓")
else:
    print("\nThe books DO NOT balance. ✗")
