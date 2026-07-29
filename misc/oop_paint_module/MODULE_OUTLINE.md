# OOP Module — the Paint App (JavaScript + p5.js)

Planning doc for a future object-oriented-programming module, built around the
**drawing/paint app** case study from the University of London (Goldsmiths)
*Introduction to Programming II* course. Teaching language: **JavaScript with
p5.js**, in the browser.

> Why the paint app: every abstract OOP idea produces something you can see and
> click. The whole design hangs on one polymorphism trick — the main loop calls
> `selectedTool.draw()` without knowing which tool it is — so students *feel*
> the open/closed principle instead of just reading about it.

---

## 1. Learning outcomes

By the end of the module a student can:

1. Explain and use **objects, constructors, and `this`** — bundling state +
   behaviour.
2. Explain **encapsulation** — an object owns its own data and the methods that
   touch it.
3. Design to a **shared interface** — agree a contract (`name`, `icon`,
   `draw()`) that many different objects satisfy.
4. Use **polymorphism / dynamic dispatch** — one call site, many behaviours
   (`selectedTool.draw()`).
5. Prefer **composition** — a `Toolbox` *has* tools; a tool *uses* the shared
   canvas and `ColourPalette`.
6. Apply the **open/closed principle** — add a whole new tool without editing
   any existing tool.
7. Read an unfamiliar codebase (the starter template) and **extend it
   cleanly**.

---

## 2. The one big idea (teach this explicitly)

Every tool is an object satisfying the **same informal interface**:

| Member              | Required | Purpose                                        |
|---------------------|----------|------------------------------------------------|
| `name`              | ✅       | id used for selection + UI linking             |
| `icon`              | ✅       | toolbar button image                           |
| `draw()`            | ✅       | per-frame behaviour, called by the main loop   |
| `populateOptions()` | optional | render this tool's own settings (e.g. slider)  |
| `unselectTool()`    | optional | cleanup when switching away                    |

The `Toolbox` keeps a `tools` array and a `selectedTool`. `addTool()` validates
`name`+`icon`, stores the tool, builds its sidebar button. The main `draw()`
loop just calls `selectedTool.draw()`. **Adding a tool = writing a new
constructor that honours the contract. No existing code changes.** That single
sentence is the spine of the module.

---

## 3. Session-by-session outline (8 sessions)

Each session = concept + a concrete change to the running paint app. Sessions
pair a **build-along** (live, guided) with an **on-your-own extension**.

### Session 1 — Objects & state
- **Concept:** object literals, properties, methods, `this`.
- **Build:** a `ColourPalette` object holding the current colour + swatches;
  wire a couple of swatches to `fill()`/`stroke()`.
- **Outcome:** "an object bundles data with the functions that use it."

### Session 2 — Constructors & the first tool
- **Concept:** constructor functions, `new`, instances vs. the blueprint.
- **Build:** `FreehandTool` — `{name, icon, draw()}`; `draw()` connects
  `previousMouseX/Y` to `mouseX/Y` with `line()`.
- **Outcome:** first object that satisfies the tool contract.

### Session 3 — The Toolbox & polymorphism ★ (keystone session)
- **Concept:** shared interface + dynamic dispatch. **This is the payoff
  session.**
- **Build:** `Toolbox` with `addTool()` / `selectTool()`; main loop calls
  `selectedTool.draw()`. Add a second tool (`LineTool`) and watch the *same*
  call site behave differently.
- **Outcome:** students can articulate polymorphism in their own words.

### Session 4 — Encapsulation & per-tool options
- **Concept:** private-ish state, each object minding its own business.
- **Build:** `populateOptions()` — `FreehandTool` gets its own `lineWidth`
  slider; `unselectTool()` clears the panel. Tools no longer leak state into
  each other.
- **Outcome:** two tools with independent settings, no shared globals.

### Session 5 — Composition over globals
- **Concept:** objects holding references to other objects; passing
  collaborators in.
- **Build:** tools use the shared `ColourPalette` (`colourP.resetColors()`) and
  the canvas explicitly rather than reaching for globals.
- **Outcome:** clear "has-a"/"uses-a" relationships.

### Session 6 — Open/closed: add tools without fear
- **Concept:** extending by adding, not editing.
- **Build (choose 1–2):** `SprayTool` (density/size sliders), `MirrorTool`
  (draws a reflected stroke), `RectTool`/`EllipseTool`.
- **Outcome:** each new tool is a new file; `sketch.js` and the other tools stay
  untouched.

### Session 7 — State that persists: pixels
- **Concept:** committing vs. previewing; why a naive redraw erases everything.
- **Build:** `loadPixels()`/`updatePixels()` and `get()` so a shape can be
  *previewed* live and *committed* on release. Covers the classic `get()`
  rectangle-only gotcha.
- **Tools:** `StampTool` (place an image at the cursor), `EraserTool`,
  rectangular `CutTool` (select → move → drop).
- **Outcome:** understands canvas state as a resource the objects share.

### Session 8 — Design review & your own tool
- **Concept:** reading + critiquing an OOP design; the contract as documentation.
- **Build:** each student ships **one original tool** of their own design that
  honours the contract, plus a short written rationale (which concept it
  exercises).
- **Outcome:** transfer — apply the pattern unprompted.

---

## 4. The running artifact

One project, growing every session (mirrors the real course's starter →
extended arc):

```
index.html          toolbar + canvas; one <script> per class
sketch.js           setup()/draw() loop; owns the shared canvas
toolbox.js          Toolbox: tool registry + current selection
colourPalette.js    ColourPalette: swatches, resetColors()
helperFunctions.js  shared utilities (save, pixel helpers)
tools/*.js          ONE constructor per tool
assets/             icon images
lib/                p5.js
```

Ship a **starter template** (toolbar + canvas + one seeded tool) so students
extend rather than start from a blank file — reading existing code is a stated
outcome (§1.7).

---

## 5. Assessment

- **Formative:** the per-session on-your-own extension.
- **Summative:** extend the app with N new tools (suggest 3–4), each honouring
  the contract, plus a written design rationale mapping features → OOP concepts.
- **Rubric axes:** contract adherence (does `addTool()` accept it untouched?),
  encapsulation (no leaked globals), originality of the student's own tool,
  code readability, correct pixel/commit handling.

---

## 6. Fit with the cs17 toolchain — open questions

This module teaches **JavaScript/p5.js**, whereas the repo's generators emit
**LaTeX worksheets from Python**. Decisions to make before building:

- **Worksheet format:** do the guided build-along sessions become printed
  worksheets (like the `scratchgen` build-alongs), an interactive web page, or
  both? A `p5gen`-style generator could render annotated JS listings the way
  `scratchgen` renders Scratch blocks.
- **Code display:** need syntax-highlighted JS in LaTeX (e.g. `minted`) if
  printed — decide early.
- **Runnable target:** where do students actually run p5.js — the p5 web editor,
  a bundled local template, or an embedded editor on cs17.org?
- **Placement:** this sits well after the Scratch build-alongs (WS12–19) as the
  first *text-code* OOP module.

---

## 7. Sources

- felipe-balbi ITP2 notes (the linked syllabus PDF) — world-class/notes,
  level-4/introduction-to-programming-ii.
- Reference extended implementation: `mrizwan47/uol-itp2-project` ("Paint 1985")
  — toolbox/tool architecture, `ColourPalette`, pixel handling.
- University of London — *Object Oriented Programming* specialisation (MOOC).
