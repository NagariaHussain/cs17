"""
Rung 2 — the loose (account, debit, credit) tuples become objects, and the
balancing rule moves INSIDE the transaction. A JournalEntry now knows whether
it balances; you ask IT, instead of remembering to run a check on the side.

This is encapsulation: the data (the postings) and the rule that governs it
(debits == credits) live together in one object. A bonus the tuples couldn't
give us — each entry can carry a narration describing *why* it happened. That
"why" is the seed of what ERPNext calls a voucher.

The trial balance at the bottom produces the SAME numbers as Rungs 0 and 1.
"""

from dataclasses import dataclass, field


@dataclass
class Posting:
    """One line of a transaction: an amount in the debit or the credit column."""
    account: str
    debit: int = 0   # paise
    credit: int = 0  # paise


@dataclass
class JournalEntry:
    """A transaction: a narration plus the postings that make it up.

    It knows the one rule that makes it a *valid* double-entry transaction, so
    you never have to remember to check from the outside.
    """
    narration: str
    postings: list = field(default_factory=list)

    def add(self, account, debit=0, credit=0):
        self.postings.append(Posting(account, debit, credit))
        return self  # return self so .add(...).add(...) chains read like a list

    def is_balanced(self):
        debits = sum(p.debit for p in self.postings)
        credits = sum(p.credit for p in self.postings)
        return debits == credits


class Ledger:
    """The append-only book of entries. It only accepts balanced ones."""

    def __init__(self):
        self.entries = []

    def post(self, entry):
        if not entry.is_balanced():
            raise ValueError(f"Refusing to post unbalanced entry: {entry.narration!r}")
        self.entries.append(entry)

    def postings(self):
        """Every posting across every entry — the flat ledger, for reporting."""
        for entry in self.entries:
            yield from entry.postings


ledger = Ledger()

# Transaction 1: the owner puts ₹1,000 of personal cash into the business.
ledger.post(
    JournalEntry("Owner invests cash")
        .add("Cash", debit=1000_00)
        .add("Capital", credit=1000_00)
)

# Transaction 2: the business buys ₹300 of supplies, paying cash.
ledger.post(
    JournalEntry("Buy supplies for cash")
        .add("Supplies", debit=300_00)
        .add("Cash", credit=300_00)
)

# Transaction 3: the fat-fingered rent payment. Now we can interrogate the
# entry BEFORE handing it to the ledger — ask the object about itself.
rent = (JournalEntry("Pay rent (typo)")
        .add("Rent", debit=300_00)
        .add("Cash", credit=30_00))   # <-- meant 300_00
print(f"Is {rent.narration!r} balanced? {rent.is_balanced()}\n")  # False


# ---------------------------------------------------------------------------
# Trial balance — same numbers as Rungs 0 & 1, now read off the objects.
# ---------------------------------------------------------------------------
def rupees(paise):
    sign = "-" if paise < 0 else " "
    paise = abs(paise)
    return f"{sign}₹{paise // 100}.{paise % 100:02d}"


balances = {}
for p in ledger.postings():
    balances[p.account] = balances.get(p.account, 0) + p.debit - p.credit

print("TRIAL BALANCE")
print("-" * 28)
for account, balance in balances.items():
    print(f"{account:<10} {rupees(balance):>14}")
print("-" * 28)
print(f"{'sum':<10} {rupees(sum(balances.values())):>14}")
print("\nThe books balance. ✓")
