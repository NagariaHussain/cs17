"""
Rung 0 — the ledger is just a list of rows, written by hand.

A "GL entry" is one row: an account, an amount in the debit column, an amount
in the credit column. Posting a transaction means appending two (or more) rows
whose debits and credits are equal.

There is NOTHING here that stops you from getting it wrong. That is the point.
Run this file and read the last line of output.

Amounts are in PAISE (integers, never floats), so ₹1000.00 is written 1000_00.
"""

# The general ledger. Every row is one posting: (account, debit, credit).
gl = []

# Transaction 1: the owner puts ₹1,000 of personal cash into the business.
gl.append(("Cash",    1000_00, 0))
gl.append(("Capital", 0,       1000_00))

# Transaction 2: the business buys ₹300 of supplies, paying cash.
gl.append(("Supplies", 300_00, 0))
gl.append(("Cash",     0,      300_00))

# Transaction 3: pay ₹300 rent in cash... but a fat finger types 30 on the
# credit side. Nothing complains. The row goes straight into the ledger.
gl.append(("Rent", 300_00, 0))
gl.append(("Cash", 0,      30_00))   # <-- meant 300_00


# ---------------------------------------------------------------------------
# A trial balance: net each account (debit-positive), then sum every balance.
# If the books are sound, that grand sum is exactly ₹0.00.
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

grand_sum = sum(balances.values())
print(f"{'sum':<10} {rupees(grand_sum):>14}")
if grand_sum == 0:
    print("\nThe books balance. ✓")
else:
    print("\nThe books DO NOT balance. ✗")
    print("Somewhere above, a transaction is lopsided. Which one? Good luck —")
    print("nothing caught it when it was written, so the error surfaces here,")
    print("far from where you made it. (That is what Rung 1 fixes.)")
