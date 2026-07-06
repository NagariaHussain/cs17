"""A rough Scratch-stage sketch for the build-along game sheets.

The blocks on a build sheet show HOW to make the game; this shows WHAT it should
look like - the 480x360 stage with labelled sprite markers, little movement
arrows, and the score/timer readouts - so the student has a picture to aim at
before they start snapping blocks. Rendered inline as TikZ, like turtlegen and
boxgen (gens/gridframe). Deliberately rough: dots and labels, not real costumes.

Stage coordinates are Scratch's own: x runs -240..240, y runs -180..180, with
(0,0) in the middle. `SC` scales those units to cm.
"""

from __future__ import annotations

X, Y = 240, 180          # stage half-width / half-height, in Scratch units
SC = 0.011               # cm per stage unit -> a 5.3cm x 4.0cm sketch


def _c(x, y) -> tuple[float, float]:
    """A stage point (Scratch units) as (cm, cm), origin at the stage centre."""
    return (x * SC, y * SC)


def _marker(x, y, label, color, labelpos="below") -> list[str]:
    px, py = _c(x, y)
    # A fixed neutral edge: the fill may be a mix expression (e.g. yellow!85!orange)
    # which cannot take a further !black suffix, so the outline does not derive from it.
    return [
        r"\filldraw[%s,draw=black!55,line width=0.5pt] (%.3f,%.3f) circle (0.16);"
        % (color, px, py),
        r"\node[font=\scriptsize,%s=1.5pt] at (%.3f,%.3f) {%s};"
        % (labelpos, px, py, label),
    ]


def _motion(x, y, kind) -> list[str]:
    """A faint movement hint drawn behind a marker: `both` = a 4-way steer (the
    coin player), `leftright` = slide sideways (the dodge player), `down` = a
    falling arrow (the rock)."""
    px, py = _c(x, y)
    s = r"gray!70,line width=0.4pt,>=Stealth"
    out = []
    if kind in ("both", "leftright"):
        out.append(r"\draw[<->,%s] (%.3f,%.3f) -- (%.3f,%.3f);"
                   % (s, px - 0.42, py, px + 0.42, py))
    if kind == "both":
        out.append(r"\draw[<->,%s] (%.3f,%.3f) -- (%.3f,%.3f);"
                   % (s, px, py - 0.42, px, py + 0.42))
    if kind == "down":
        out.append(r"\draw[->,%s] (%.3f,%.3f) -- (%.3f,%.3f);"
                   % (s, px, py + 0.62, px, py + 0.22))
    return out


def _chip(name, value, cx, cy) -> str:
    """A Scratch variable monitor: a small orange rounded pill, `name value`."""
    return (r"\node[anchor=north west,rounded corners=1.5pt,fill=orange!85,"
            r"text=white,font=\scriptsize\bfseries,inner sep=2pt] at (%.3f,%.3f) "
            r"{%s\hspace{2pt}\colorbox{white}{\color{orange!85}%s}};"
            % (cx, cy, name, value))


def sketch(*, markers, readouts=(), motions=(), ground=None, caption="") -> str:
    """A centred stage sketch.

    markers  : list of (x, y, label, color[, labelpos]) sprite dots.
    readouts : list of (name, value) shown as monitors, stacked top-left.
    motions  : list of (x, y, kind) movement hints (see `_motion`).
    ground   : a y value to draw a ground line at (for the dodge game), or None.
    """
    x0, y0 = _c(-X, -Y)
    x1, y1 = _c(X, Y)
    L = [r"\begin{tikzpicture}[x=1cm,y=1cm,baseline=(current bounding box.center)]"]
    L.append(r"\fill[gray!6,rounded corners=2pt] (%.3f,%.3f) rectangle (%.3f,%.3f);"
             % (x0, y0, x1, y1))
    L.append(r"\draw[gray!55,rounded corners=2pt,line width=0.7pt] "
             r"(%.3f,%.3f) rectangle (%.3f,%.3f);" % (x0, y0, x1, y1))
    if ground is not None:
        gy = _c(0, ground)[1]
        L.append(r"\draw[brown!60,line width=1pt] (%.3f,%.3f) -- (%.3f,%.3f);"
                 % (x0, gy, x1, gy))
        L.append(r"\node[font=\tiny,text=brown!70,anchor=south east] at (%.3f,%.3f) "
                 r"{ground};" % (x1 - 0.05, gy))
    for m in motions:
        L += _motion(*m)
    for m in markers:
        L += _marker(*m)
    cy = y1 - 0.14
    for name, value in readouts:
        L.append(_chip(name, value, x0 + 0.12, cy))
        cy -= 0.46          # chip height plus a small gap so monitors do not touch
    L.append(r"\end{tikzpicture}")
    tikz = "\n".join(L)
    cap = (r"\par\vspace{3pt}{\footnotesize\itshape %s}" % caption) if caption else ""
    return (r"\par\vspace{8pt}\begin{center}\fbox{\begin{minipage}{0.7\linewidth}"
            r"\centering\vspace{4pt}\textbf{\footnotesize What you are building}"
            r"\par\vspace{5pt}%s%s\vspace{4pt}\end{minipage}}\end{center}"
            % (tikz, cap))
