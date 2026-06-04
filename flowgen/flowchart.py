"""Render an Algorithm to a flowchart via Graphviz.

Graphviz auto-lays-out the control flow, including loop back-edges, which is the
whole reason for using it over hand-placed boxes. Shapes follow flowchart
convention:
    Start / End   ellipse (terminator)
    read / print  parallelogram (I/O)
    assignment    rectangle (process)
    if / while    diamond (decision), branches labelled Yes / No
"""

from __future__ import annotations

import itertools

import graphviz

from .algo import Algorithm, Assign, If, Input, Output, While


def _build_dot(algo: Algorithm) -> graphviz.Digraph:
    dot = graphviz.Digraph()
    dot.attr(rankdir="TB", nodesep="0.35", ranksep="0.4")
    dot.attr("node", fontname="Helvetica", fontsize="11", margin="0.08,0.05")
    dot.attr("edge", fontname="Helvetica", fontsize="9", arrowsize="0.7")
    ids = itertools.count()

    def node(shape, label, **kw):
        nid = f"n{next(ids)}"
        dot.node(nid, label, shape=shape, **kw)
        return nid

    def link(prev_exits, dst):
        for src, lbl in prev_exits:
            dot.edge(src, dst, label=lbl or "")

    def seq(stmts, prev_exits):
        for s in stmts:
            prev_exits = stmt(s, prev_exits)
        return prev_exits

    def stmt(s, prev_exits):
        if isinstance(s, Input):
            n = node("parallelogram", f"read {s.var}")
            link(prev_exits, n)
            return [(n, None)]
        if isinstance(s, Assign):
            n = node("box", f"{s.var} = {s.expr}")
            link(prev_exits, n)
            return [(n, None)]
        if isinstance(s, Output):
            n = node("parallelogram", f"print {s.expr}")
            link(prev_exits, n)
            return [(n, None)]
        if isinstance(s, If):
            d = node("diamond", s.cond)
            link(prev_exits, d)
            then_exits = seq(s.then, [(d, "Yes")])
            else_exits = seq(s.els, [(d, "No")]) if s.els else [(d, "No")]
            return then_exits + else_exits
        if isinstance(s, While):
            d = node("diamond", s.cond)
            link(prev_exits, d)
            body_exits = seq(s.body, [(d, "Yes")])
            link(body_exits, d)  # loop back to the test
            return [(d, "No")]
        raise AssertionError(s)

    start = node("ellipse", "Start")
    exits = seq(algo.body, [(start, None)])
    end = node("ellipse", "End")
    link(exits, end)
    return dot


def render(algo: Algorithm, path_stem: str, formats=("pdf", "png", "svg")):
    """Render the flowchart and save `path_stem.<fmt>` for each format."""
    dot = _build_dot(algo)
    for fmt in formats:
        data = dot.pipe(format=fmt)
        with open(f"{path_stem}.{fmt}", "wb") as f:
            f.write(data)
    return dot
