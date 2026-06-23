"""
Rung 1 — the same ledger, but every transaction now goes through ONE function
that refuses to write unless debits equal credits.

The typo from Rung 0 can no longer get in. The error is caught at the moment of
posting — right where you made it — instead of surfacing 3,000 rows later as a
trial balance that won't sum to zero.

This is the first abstraction: a name (`post`) that hides a few steps AND
guards an invariant. Nothing about the ledger's *data* changed — it's still a
list of (account, debit, credit) rows. Notice the trial balance code below is
byte-for-byte the same as Rung 0. Same behaviour, safer shape.
"""

# The general ledger: still just a list of (account, debit, credit) rows.
gl = []


def post(*lines):
    """Append a transaction's lines to the ledger — only if it balances.

    Each line is (account, debit_paise, credit_paise). The invariant of
    double-entry bookkeeping is simply: total debits == total credits.
    """
    debits = sum(debit for _, debit, _ in lines)
    credits = sum(credit for _, _, credit in lines)
    if debits != credits:
        raise ValueError(
            f"Unbalanced: debits {debits} != credits {credits}. Refusing to post."
        )
    gl.extend(lines)


# Transaction 1: the owner puts ₹1,000 of personal cash into the business.
post(("Cash",    1000_00, 0),
     ("Capital", 0,       1000_00))

# Transaction 2: the business buys ₹300 of supplies, paying cash.
post(("Supplies", 300_00, 0),
     ("Cash",     0,      300_00))

# Transaction 3: the SAME fat-fingered rent payment as Rung 0 — but now it is
# caught here, at the source, the instant we try to post it.
try:
    post(("Rent", 300_00, 0),
         ("Cash", 0,      30_00))   # <-- meant 300_00
except ValueError as e:
    print(f"Caught at posting time: {e}\n")


# ---------------------------------------------------------------------------
# Trial balance — IDENTICAL to Rung 0. The data model didn't change.
# ---------------------------------------------------------------------------
def rupees(paise):
    sign = "-" if paise < 0 else " "
    paise = abs(paise)
    return f"{sign}₹{paise // 100}.{paise % 100:02d}"


balances = {}
for account, debit, credit in gl:
    balances[account] = balances.get(account, 0) + debit - credit

print("TRIAL BALANCE")
print("-" * 28)
for account, balance in balances.items():
    print(f"{account:<10} {rupees(balance):>14}")
print("-" * 28)
print(f"{'sum':<10} {rupees(sum(balances.values())):>14}")
print("\nThe books balance. ✓  (the bad transaction never made it in)")
