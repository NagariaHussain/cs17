# Rung 10 — who posted this?

> In Rung 9 anyone with the URL could post, cancel or amend an invoice — and the
> books never recorded *who* did it. No accountability, no multi-user. A ledger
> demands an audit trail: not just *what* happened but *who* made it happen. So
> we add user accounts, lock every page behind a login, and stamp each invoice
> with its author.

```sh
pip install -r requirements.txt
flask --app app run
```

Then visit http://localhost:5000/ (log in as admin / admin).

## What changed

- **A `user` table.** `id`, a `UNIQUE` `username`, and a `password_hash` — never
  the password itself. Passwords go through `werkzeug.security.generate_password_hash`
  on the way in and `check_password_hash` on the way out, so the database never
  holds a plaintext secret.
- **A `login_required` gate.** A small `functools.wraps` decorator: if there's no
  `user` in `flask.session`, redirect to `/login`. It's applied to *every* app
  route except `login` and `register` — even reading the trial balance now
  requires logging in. The door is locked.
- **A `created_by` stamp.** `create_invoice` now takes a `created_by` and writes
  it onto the `sales_invoice` row. The invoice list and detail pages show
  "Posted by &lt;user&gt;". `init_db` seeds a default `admin` / `admin` user so a
  fresh database is reachable, and the opening Acme invoice is stamped to admin.

The accounting kernel (`kernel.py`) is still imported untouched — users,
sessions and the document store all live in `app.py`, above the ledger boundary.

## The idea

**Authentication is the audit trail accounting requires.** A general ledger has
recorded *what* happened for 530 years; a real system also has to record *who*.
Sessions plus password hashing give us identity, the `login_required` gate makes
identity mandatory, and `created_by` writes that identity onto every document. A
posting is no longer an anonymous fact floating in the database — it carries the
name of the person who stands behind it. That's the difference between a toy and
a system people can actually be held to.

## The next pain

You have exactly **one** report — the trial balance — and it's really just a raw
list of account balances. But the owner doesn't ask "are the books balanced?";
they ask "did we make money?" and "what are we worth?". Those are the **Profit &
Loss** and the **Balance Sheet** — the reports owners actually read, each just a
different query over the same append-only ledger.

➡️ [Rung 11 — the reports owners actually want](../rung11_reports/)

⬅️ [Rung 9](../rung9_cancel_amend/)
