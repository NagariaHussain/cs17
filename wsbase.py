"""Shared LaTeX setup for all cs17 worksheet generators.

Single place for the document class, page geometry, footer (cs17.org / author),
and the \\probrule separator. Each generator passes its own extra packages:

    from wsbase import preamble, compile_tex
    _PREAMBLE = preamble(r"\\usepackage{listings} ...")
"""

from __future__ import annotations

import subprocess
from pathlib import Path

FOOTER_LEFT = "cs17.org"
FOOTER_RIGHT = "Author: Hussain Nagaria"

_BASE = r"""\documentclass[11pt]{article}
\usepackage[margin=2cm]{geometry}
\usepackage{graphicx}
\usepackage[export]{adjustbox}
\usepackage{booktabs}
\usepackage[table]{xcolor}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyfoot[L]{\small\textcolor{gray}{%(left)s}}
\fancyfoot[C]{\thepage}
\fancyfoot[R]{\small\textcolor{gray}{%(right)s}}
\setlength{\parindent}{0pt}
\newcommand{\probrule}{\par\vspace{4pt}\textcolor{gray!50}{\hrulefill}\par\vspace{10pt}}
"""


def preamble(extra: str = "") -> str:
    """The shared preamble, plus a generator's extra packages/settings."""
    base = _BASE % {"left": FOOTER_LEFT, "right": FOOTER_RIGHT}
    return base + extra


def compile_tex(tex_path: Path):
    """Compile with Tectonic, cwd at the .tex dir so figure paths stay relative."""
    subprocess.run(["tectonic", tex_path.name], cwd=tex_path.parent, check=True)
