"""Rung 6 — a URL for the books.

The web layer sits on TOP of the kernel: a request comes in, a handler reads the
books through the kernel's Ledger interface, and a response goes out. The kernel
itself (kernel.py) is imported untouched — it has no idea it lives inside a web
server.
"""
import os
import sqlite3

from flask import Flask, g, render_template

import kernel

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books.db")

app = Flask(__name__)


def get_db():
    """One SQLite connection per request, stashed on flask.g."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def get_ledger():
    """The kernel's SQLiteLedger, wrapped around this request's connection."""
    return kernel.SQLiteLedger(get_db())


def init_db():
    """Seed the four opening transactions if the GL is empty."""
    ledger = get_ledger()
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM gl_entry").fetchone()[0]
    if count:
        return
    ledger.post(kernel.JournalEntry("Owner invests cash")
                .add(kernel.cash, debit=1000_00)
                .add(kernel.capital, credit=1000_00))
    ledger.post(kernel.JournalEntry("Buy supplies for cash")
                .add(kernel.supplies, debit=300_00)
                .add(kernel.cash, credit=300_00))
    ledger.post_document(kernel.SalesInvoice("Acme Corp", 500_00))
    ledger.post_document(kernel.Payment("Acme Corp", 200_00))


@app.route("/")
def trial_balance():
    rows, total_dr, total_cr = kernel.trial_balance(get_ledger())
    return render_template(
        "trial_balance.html",
        rows=rows,
        total_dr=total_dr,
        total_cr=total_cr,
        rupees=kernel.rupees,
    )


with app.app_context():
    init_db()
