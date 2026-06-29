# CS 17 Accounting App Curriculum Review

This note reviews the current `q3` accounting app work and proposes a better teaching approach for using an accounting application to teach web development over three months.

The students are assumed to already know the accounting basics before this module starts:

- Golden rules of accounting
- Debit and credit
- Accounts and account types
- Vouchers
- Ledger entries by hand
- Trial balance basics

The goal of this module should not be “teach accounting again.” The goal should be:

> Teach web development by repeatedly converting a paper accounting action into a working web feature.

## Current Q3 Approach

The current work in `q3/accounting` is structured as rungs:

| Rung | Main idea |
| --- | --- |
| 0 | Raw rows |
| 1 | `post()` function |
| 2 | Objects |
| 3 | Polymorphic account types |
| 4 | Documents |
| 5 | Storage and dependency inversion |
| 6 | URL renders trial balance |
| 7 | Forms and validation create invoice |
| 8 | List/detail invoices |
| 9 | Cancel/amend |
| 10 | Users/login |
| 11 | Reports: P&L and Balance Sheet |

This is coherent from a software design perspective. It teaches abstraction, domain modeling, persistence boundaries, and eventually Flask.

However, it is not ideal if the primary course outcome is web development.

## Main Problem

The first six rungs happen before students build meaningful web interactions.

That means the early experience is mostly:

- Python data structures
- Object modeling
- Ledger abstractions
- Storage abstractions
- Domain design

These are valuable, but they delay the thing the students are supposed to learn: how a web app works.

For a web development course, students should encounter the web loop early:

> Browser → route → request → validation → database → redirect → rendered result

The accounting domain should be the teaching context, not a long pre-web detour.

## What Is Worth Keeping

The existing work has several strong ideas that should be retained:

- Every accounting action must produce a balanced journal entry.
- Documents such as invoices and payments should generate ledger postings.
- Reports should be computed from ledger entries, not manually stored.
- Cancellation should be handled through reversing entries, not deletion.
- Money should be represented carefully, preferably as integer paise.
- Students should reconcile the software output with hand-written accounting work.

These ideas are educationally strong because they connect accounting correctness with software correctness.

## Recommended Shift

Instead of using the current rungs as the student-facing path, use them as instructor reference material.

For students, build one evolving web app over 12 weeks.

The structure should be feature-first:

> Start with the smallest visible web app, then grow it one accounting feature at a time.

Each week should produce a working vertical slice. A vertical slice means the feature goes through the whole stack:

- HTML page
- Flask route
- Form handling, where relevant
- Validation
- SQLite persistence
- Report or listing
- Accounting reconciliation

This gives students repeated practice with the real shape of web development.

## Pedagogical Approach

Use a studio model with repeated accounting-to-web translation.

Every new concept should follow this rhythm:

1. Do the accounting on paper.
2. Predict what rows should exist in the database.
3. Build the smallest web feature that records the action.
4. Inspect the database rows.
5. Reconcile the trial balance or report.
6. Try invalid cases and observe validation.
7. Explain the full request/response flow.

The governing teaching line should be:

> Make an accounting prediction, build the smallest web feature that records it, inspect the stored data, and reconcile the result.

## Teaching Pattern

For each feature, use this sequence:

### 1. Instructor demo

The instructor builds a small version live.

Example:

> Create a manual journal entry form that accepts two lines and rejects unbalanced entries.

### 2. Class rebuild

The class rebuilds a similar example with guidance.

Example:

> Add a three-line journal entry where total debits must equal total credits.

### 3. Pair exercise

Students work in pairs on a near-transfer task.

Example:

> Add validation that prevents blank accounts and zero-value postings.

### 4. Individual variation

Each student handles a small unseen variation.

Example:

> Add narration to the voucher and display it on the journal detail page.

### 5. Reconciliation

Students prove the feature is correct by comparing:

- Paper voucher
- Journal rows
- Ledger rows
- Trial balance

This keeps the learning concrete.

## Suggested 12-Week Plan

| Week | Accounting feature | Web development concepts | Accounting concept reinforced |
| --- | --- | --- | --- |
| 1 | Static ledger and trial balance page | HTML, CSS, tables, semantic markup | Ledger format, debit/credit columns |
| 2 | Flask renders ledger data | Routes, templates, request/response | Accounts and normal balances |
| 3 | Manual journal entry form | GET/POST, forms, validation, PRG pattern | Balanced journal entries |
| 4 | Persist journal entries | SQLite, schema design, insert/select, foreign keys | Journal and posting tables |
| 5 | Journal list and detail pages | Dynamic URLs, joins, 404 handling | Voucher to journal-entry mapping |
| 6 | Trial balance from database | Aggregation, grouping, helper functions, tests | Trial balance reconciliation |
| 7 | Sales invoice | Multi-table writes, transactions | Dr Debtors / Cr Sales |
| 8 | Customer receipt | Reusing forms and handlers, refactoring | Dr Cash / Cr Debtors |
| 9 | Expense or purchase voucher | Reusable validation, account filtering | Expense, cash, creditors |
| 10 | P&L and Balance Sheet | Report queries, date filters, query params | Income statement and accounting equation |
| 11 | Cancel/amend and users | Reversals, audit trail, sessions, password hashing | Correction without erasing history |
| 12 | Capstone feature | Integration, debugging, peer review | End-to-end accounting workflow |

Good capstone feature options:

- Cash book
- Receivables report
- Ageing report
- Purchase voucher
- General journal import
- Customer statement

## Recommended App Progression

### Phase 1: Read-only web app

Start with hard-coded data.

Students should first learn how data becomes HTML.

Build:

- Home page
- Chart of accounts page
- Ledger page
- Trial balance page

Do not start with login, object-oriented abstractions, or complex database design.

### Phase 2: Manual journal entries

Introduce forms only after students can render accounting data.

Build:

- New journal entry form
- Multiple debit/credit lines
- Validation for balanced entries
- Error messages
- Journal list page
- Journal detail page

This is the first major web milestone.

### Phase 3: Database-backed accounting

Move from in-memory or hard-coded rows to SQLite.

Build tables such as:

- `accounts`
- `journal_entries`
- `postings`

Students should inspect the database directly after each feature.

The key lesson:

> A voucher is not just a form submission. It becomes durable rows that reports can query.

### Phase 4: Business documents

Once manual journals work, introduce documents that generate journal entries.

Build:

- Sales invoice
- Customer receipt
- Expense voucher

Each document should generate balanced postings.

Example sales invoice:

| Account | Debit | Credit |
| --- | ---: | ---: |
| Accounts Receivable | 1,000 |  |
| Sales Revenue |  | 1,000 |

Example receipt:

| Account | Debit | Credit |
| --- | ---: | ---: |
| Cash | 1,000 |  |
| Accounts Receivable |  | 1,000 |

### Phase 5: Reports

Reports should come after students understand stored journal rows.

Build:

- Trial balance
- Profit and loss
- Balance sheet
- Customer outstanding

Reports should be treated as queries over source transactions.

Do not store report totals manually.

### Phase 6: Audit and correction

Introduce cancellation and amendment late.

Students should learn that accounting software usually does not delete history. It records corrections.

Build:

- Cancel invoice
- Reversal journal entry
- Amendment flow
- Audit fields such as created by, cancelled by, amended from, timestamps

## Practical Web Concepts to Introduce

### HTML and CSS

Use accounting tables to teach:

- Table structure
- Right-aligned numeric columns
- Form layout
- Error display
- Print-friendly pages
- Basic accessibility

### HTTP and Flask

Use accounting actions to teach:

- GET for viewing
- POST for creating
- Redirect after POST
- URL parameters
- Query parameters for date filters
- 404 pages for missing vouchers

### Forms and validation

Accounting gives natural validation cases:

- Debit total must equal credit total.
- Amount must be positive.
- Account must exist.
- Voucher date is required.
- Invoice cannot be cancelled twice.
- Cancelled invoice cannot be amended.

### SQLite

Use the accounting domain to teach:

- Primary keys
- Foreign keys
- One journal entry with many postings
- Transactions
- Joins
- Aggregates
- Constraints

### Transactions

Transactions are especially important.

When creating an invoice, the app may need to create:

- A journal entry
- Posting rows
- An invoice row

These must succeed or fail together.

This is a strong practical lesson:

> If the invoice row is saved but the ledger entry fails, the accounting system is corrupt.

### Testing

Tests should be introduced early and kept small.

Good tests:

- Unbalanced journal entry is rejected.
- Balanced journal entry is accepted.
- Trial balance totals match.
- Sales invoice creates correct postings.
- Cancelling an invoice creates reversing postings.
- Report totals match known fixtures.

### Authentication

Authentication should come late.

Students should first understand the accounting workflow. Then add:

- Login
- Logout
- Password hashing
- Current user
- Created-by fields
- Basic authorization rules

## JavaScript Recommendation

Do not introduce JavaScript early unless the course specifically requires it.

The core web-development lessons can be taught well with:

- Flask
- Server-rendered HTML
- CSS
- SQLite

JavaScript can be added late for focused enhancements:

- Live invoice totals
- Adding/removing invoice lines
- Client-side validation hints

Even then, the server must remain the source of truth.

## Issues in the Current Implementation to Fix Before Teaching

The current final app demonstrates useful ideas, but some implementation choices should not be copied directly into teaching material.

### Money parsing

The code claims to use integer money, but parsing currently goes through floating point.

That is a bad habit to teach.

Use a strict parser based on integer paise or `Decimal`.

### Split commits

Some flows create ledger entries and business documents in separate commits.

For teaching, this should be changed to use a single database transaction.

Students should learn atomicity:

> Either the full voucher is recorded, or none of it is.

### Incomplete audit trail

The app has some `created_by` behavior, but cancellation and amendment should also record:

- Who cancelled
- When it was cancelled
- Why it was cancelled
- Which document it amends
- Which document amended it

### Classroom-only shortcuts

Hard-coded secrets and demo credentials are acceptable only as temporary classroom scaffolding.

They should be clearly labeled and removed from production-style examples.

### Missing tests

The current app should have tests before being used as the main teaching artifact.

At minimum, tests should cover:

- Balanced posting
- Invalid unbalanced posting
- Invoice creation
- Payment creation
- Trial balance
- Cancellation
- P&L
- Balance sheet

### Limited accounting surface

The current app mainly focuses on sales invoices.

To make better use of students’ accounting preparation, add:

- Manual journal entries
- Customer receipts
- Expense vouchers
- Purchases or creditors
- Cash book

## Better Structure for the Repository

Instead of many fully separate student rungs, keep one main evolving app and optional checkpoints.

Suggested structure:

```text
q3/accounting_app/
  app.py
  schema.sql
  accounting.py
  reports.py
  templates/
  static/
  tests/
  lessons/
    week01_static_pages.md
    week02_flask_templates.md
    week03_journal_form.md
    ...
  checkpoints/
    week01/
    week02/
    week03/
```

The `checkpoints` folder can preserve working states for reference, but students should experience the app as one growing system.

## Assessment Ideas

Avoid assessing only whether the UI works.

Assess whether the student can explain the full accounting and web flow.

Good assessment prompts:

- Show the journal rows created by this voucher.
- Explain why this entry is balanced.
- Explain which Flask route handled this form.
- Explain why redirect-after-POST is used.
- Show the SQL query behind the trial balance.
- Break this voucher intentionally and explain the validation error.
- Cancel this invoice and show the reversing entry.
- Reconcile the app’s trial balance with a hand-written trial balance.

## Recommended Weekly Student Deliverables

Each week, students should submit:

- A working app feature
- One screenshot or short demo
- The relevant database rows
- A short reconciliation note
- One test or manual test case

Example weekly reconciliation note:

> I created invoice INV-001 for ₹1,000. The app debited Accounts Receivable and credited Sales Revenue. The trial balance still balances because total debit and total credit both increased by ₹1,000.

## Final Recommendation

Keep the current `q3/accounting` rungs as instructor reference material, but do not use them as the primary student path.

For a web development course, use a single evolving accounting app built through weekly vertical slices.

The best teaching loop is:

> Paper accounting entry → web form/page → database rows → report → reconciliation.

This approach teaches web development, database design, validation, testing, and software correctness while continuously reinforcing the accounting concepts students already know.
