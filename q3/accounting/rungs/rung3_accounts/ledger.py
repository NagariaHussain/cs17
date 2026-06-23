"""
Rung 3 — accounts grow up. `Cash` stops being a bare string and becomes an
Account *object* that knows its own type — and, crucially, knows how to turn a
pile of debits and credits into a balance the right way round.

The pain this removes: in Rungs 0–2 we netted every account debit-positive, so
Capital — money the business OWES back to its owner — came out as a confusing
−₹1000.00. To print a *real* trial balance you'd have to write the same fork in
every report you ever wrote:

    if account_type in ("asset", "expense"):
        balance = debits - credits        # debit-normal
    else:
        balance = credits - debits        # credit-normal

That `if` would reappear in the balance sheet, the P&L, everywhere. Polymorphism
deletes it: you ask `account.balance(debits, credits)` and the account computes
itself. An Asset subtracts one way, an Equity the other, and the caller never
asks which — it doesn't need to know.

Same postings as every rung before. The trial balance changes — for the first
time — and THAT is the lesson: now that the program knows what each account
*means*, Capital reports its natural +₹1000.00 credit balance, and the books
prove themselves the way real books do — total debits == total credits.
"""

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Accounts — a tiny class hierarchy. For our purposes the ONLY thing that
# differs between an asset and a liability is which way `balance` subtracts.
# So that one method is all the subclasses override. That is polymorphism:
# one message (`balance`), many behaviours, chosen by the object's type.
# ---------------------------------------------------------------------------
class Account:
    """An account has a name and a rule for reading its balance off the ledger.
    The rule is abstract here; each kind of account supplies its own."""

    def __init__(self, name):
        self.name = name

    def balance(self, debits, credits):
        raise NotImplementedError("each Account subclass defines its own balance")

    def __repr__(self):
        return self.name


class DebitNormalAccount(Account):
    """Assets and expenses — what you HAVE or SPEND. A debit grows them, so the
    balance is debits minus credits."""
    normal_side = "Dr"

    def balance(self, debits, credits):
        return debits - credits


class CreditNormalAccount(Account):
    """Liabilities, equity, income — what you OWE or EARN. A credit grows them,
    so the balance is credits minus debits — the mirror image."""
    normal_side = "Cr"

    def balance(self, debits, credits):
        return credits - debits


# The five account types every accounting system has, expressed as the two
# normal-side behaviours above. Naming them is worth it: a reader who sees
# `Equity("Capital")` knows instantly how it behaves, with no lookup table.
class Asset(DebitNormalAccount):      pass
class Expense(DebitNormalAccount):    pass
class Liability(CreditNormalAccount): pass
class Equity(CreditNormalAccount):    pass
class Income(CreditNormalAccount):    pass


# ---------------------------------------------------------------------------
# Postings, entries, and the ledger — carried over from Rung 2 unchanged, with
# ONE difference: a Posting now points at an Account object, not a bare string.
# ---------------------------------------------------------------------------
@dataclass
class Posting:
    """One line of a transaction. `account` is an Account object now, so a
    typo'd name can't silently open a brand-new account behind your back."""
    account: Account
    debit: int = 0    # paise
    credit: int = 0   # paise


@dataclass
class JournalEntry:
    """A transaction: a narration plus the postings that make it up. It still
    knows the one rule that makes it valid — total debits == total credits."""
    narration: str
    postings: list = field(default_factory=list)

    def add(self, account, debit=0, credit=0):
        self.postings.append(Posting(account, debit, credit))
        return self  # chain .add(...).add(...) so an entry reads like a list

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


# Accounts are objects now: created once, then referenced by identity. Two
# postings to `cash` mean the SAME account, not two strings that happen to match.
cash     = Asset("Cash")
supplies = Asset("Supplies")
capital  = Equity("Capital")
rent     = Expense("Rent")

ledger = Ledger()

# Transaction 1: the owner puts ₹1,000 of personal cash into the business.
ledger.post(
    JournalEntry("Owner invests cash")
        .add(cash, debit=1000_00)
        .add(capital, credit=1000_00)
)

# Transaction 2: the business buys ₹300 of supplies, paying cash.
ledger.post(
    JournalEntry("Buy supplies for cash")
        .add(supplies, debit=300_00)
        .add(cash, credit=300_00)
)

# Transaction 3: the same fat-fingered rent payment — still caught, because the
# ledger still refuses anything that doesn't balance. We just ask the entry.
bad_rent = (JournalEntry("Pay rent (typo)")
            .add(rent, debit=300_00)
            .add(cash, credit=30_00))   # <-- meant 300_00
print(f"Is {bad_rent.narration!r} balanced? {bad_rent.is_balanced()}\n")  # False


# ---------------------------------------------------------------------------
# Trial balance — now in its REAL two-column shape. We net each account's
# debits and credits, then let EACH ACCOUNT report its own balance on its own
# natural side. There is no `if asset / else liability` here: that knowledge
# moved into the account classes, where it belongs.
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
    bal = account.balance(debits, credits)   # <-- the polymorphic call
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
