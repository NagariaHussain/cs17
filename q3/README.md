# q3 — web development (the accounting app)

Quarter-3 is a **follow-along build**: an accounting app, from first principles,
in Flask + SQLite. Some of it is built live in lecture; some is homework.

The pedagogical spine is **abstraction by subtraction of pain** — we never hand
students an abstraction. We write the raw, manual thing first, feel exactly what
hurts, and then introduce each abstraction (function → object → polymorphism →
documents → storage boundary) as the *refactor that relieves that specific pain.*

The one idea the whole quarter rests on, lifted from how ERPNext/QuickBooks/SAP
actually work behind the scenes:

> **Every business document, when posted, writes balanced debit/credit lines
> into one append-only ledger. Every report is just a query over that ledger.**

See [`accounting/`](accounting/) for the module.
