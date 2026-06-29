"""Render an Algorithm as Scratch 3 blocks (the scratch3 LaTeX package).

A third derived view of the single-source Algorithm, alongside the flowchart
(flowchart.py) and the pseudocode (algo.py). Because the Scratch script is
generated from the same statement tree the tracer executes, a "trace this
Scratch program" problem can never disagree with its trace table.

Statement -> Scratch mapping:

    read x      ->  ask [Enter x] and wait        (sensing)
                    set [x] to (answer)           (variables)
    x = expr    ->  set [x] to (expr)             (variables)
                    x = x + k  ->  change [x] by (k)   (the idiomatic form)
    print e     ->  say (e)                       (looks)
    if / else   ->  if <...> then  /  else        (control)
    while C     ->  repeat until <not C>          (control)

Two facts about Scratch shape the expression rendering:

  * Scratch has no `while`, only `repeat until`. A `while C` loop is therefore
    `repeat until <not C>`; we push the negation into the condition so it reads
    naturally (`while i <= n` -> `repeat until i > n`).
  * Scratch has only three comparison operators: `<`, `=`, `>`. Conditions must
    be authored with those (combined with and / or / not). An unsupported
    operator (`<=`, `>=`, `!=`, `//`, ...) raises, so a script Scratch could not
    express can't be authored by mistake.

The SAME expression string is parsed here (via `ast`) and evaluated by the
tracer, so the blocks and the trace stay in lock-step.
"""

from __future__ import annotations

import ast

from .algo import Assign, If, Input, Output, While


# ---- text escaping (block labels are typeset, not verbatim) ------------------

def _esc(s: str) -> str:
    s = str(s)
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
                 ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}"),
                 ("$", r"\$")]:
        s = s.replace(a, b)
    return s


def _num(v) -> str:
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v)


# ---- expression rendering (ast -> scratch3 reporters) ------------------------

_BINOP = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/", ast.Mod: "mod"}
_CMP = {ast.Eq: "=", ast.Lt: "<", ast.Gt: ">"}        # all Scratch offers
# negation of a comparison that lands on a Scratch-supported operator
_CMP_NEG = {ast.LtE: ">", ast.GtE: "<", ast.NotEq: "="}


def _parse(expr: str) -> ast.AST:
    return ast.parse(expr, mode="eval").body


def _value(node: ast.AST) -> str:
    """A value/number slot: a literal oval, a variable reporter, or a green
    arithmetic reporter (with its operands nested as further ovals)."""
    if isinstance(node, ast.Constant):
        return r"\ovalnum{%s}" % _esc(_num(node.value))
    if isinstance(node, ast.Name):
        return r"\ovalvariable{%s}" % _esc(node.id)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub) \
            and isinstance(node.operand, ast.Constant):
        return r"\ovalnum{-%s}" % _esc(_num(node.operand.value))
    if isinstance(node, ast.BinOp):
        op = _BINOP.get(type(node.op))
        if op is None:
            raise ValueError(f"Scratch has no operator for {ast.dump(node.op)} "
                             f"(use + - * / mod)")
        return r"\ovaloperator{%s %s %s}" % (_value(node.left), op,
                                             _value(node.right))
    raise ValueError(f"cannot render as a Scratch value: {ast.dump(node)}")


def _bool(node: ast.AST) -> str:
    """A boolean (hexagon) slot: a comparison, an and/or of booleans, or not."""
    if isinstance(node, ast.Compare):
        if len(node.ops) != 1:
            raise ValueError("chained comparison; write it as one comparison")
        sym = _CMP.get(type(node.ops[0]))
        if sym is None:
            raise ValueError("Scratch comparisons are only < = > ; rewrite "
                             f"{ast.dump(node.ops[0])} using those")
        return r"\booloperator{%s %s %s}" % (_value(node.left), sym,
                                             _value(node.comparators[0]))
    if isinstance(node, ast.BoolOp):
        word = "and" if isinstance(node.op, ast.And) else "or"
        out = _bool(node.values[0])
        for v in node.values[1:]:  # Scratch and/or are binary; nest left-to-right
            out = r"\booloperator{%s %s %s}" % (out, word, _bool(v))
        return out
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return r"\booloperator{not %s}" % _bool(node.operand)
    raise ValueError(f"cannot render as a Scratch boolean: {ast.dump(node)}")


def _until(node: ast.AST) -> str:
    """The condition for `repeat until`, i.e. the negation of a while-condition.
    Push the negation into a single comparison where that yields a supported
    operator (`i <= n` -> `i > n`); otherwise wrap the whole thing in `not`."""
    if isinstance(node, ast.Compare) and len(node.ops) == 1:
        sym = _CMP_NEG.get(type(node.ops[0]))
        if sym is not None:
            return r"\booloperator{%s %s %s}" % (_value(node.left), sym,
                                                 _value(node.comparators[0]))
    return r"\booloperator{not %s}" % _bool(node)


# ---- statement rendering -----------------------------------------------------

def _indent(lines: list[str]) -> list[str]:
    return ["  " + ln for ln in lines]


def _assign(s: Assign) -> str:
    node = _parse(s.expr)
    # x = x + k  /  x = x - k  is idiomatically the "change [x] by (k)" block
    if (isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub))
            and isinstance(node.left, ast.Name) and node.left.id == s.var
            and isinstance(node.right, ast.Constant)):
        k = node.right.value
        if isinstance(node.op, ast.Sub):
            k = -k
        return (r"\blockvariable{change \selectmenu{%s} by \ovalnum{%s}}"
                % (_esc(s.var), _esc(_num(k))))
    return (r"\blockvariable{set \selectmenu{%s} to %s}"
            % (_esc(s.var), _value(node)))


def _emit(stmts: list) -> list[str]:
    lines: list[str] = []
    for s in stmts:
        if isinstance(s, Input):
            lines.append(r"\blocksensing{ask \ovalnum{Enter %s} and wait}"
                         % _esc(s.var))
            lines.append(r"\blockvariable{set \selectmenu{%s} to \ovalsensing{answer}}"
                         % _esc(s.var))
        elif isinstance(s, Assign):
            lines.append(_assign(s))
        elif isinstance(s, Output):
            lines.append(r"\blocklook{say %s}" % _value(_parse(s.expr)))
        elif isinstance(s, If):
            cond = _bool(_parse(s.cond))
            if s.els:
                lines.append(r"\blockifelse{if %s then}{" % cond)
                lines += _indent(_emit(s.then))
                lines.append("}{")
                lines += _indent(_emit(s.els))
                lines.append("}")
            else:
                lines.append(r"\blockif{if %s then}{" % cond)
                lines += _indent(_emit(s.then))
                lines.append("}")
        elif isinstance(s, While):
            lines.append(r"\blockrepeatuntil{repeat until %s}{"
                         % _until(_parse(s.cond)))
            lines += _indent(_emit(s.body))
            lines.append("}")
        else:
            raise AssertionError(s)
    return lines


def scratch_blocks(algo, scale: float = 0.82) -> str:
    """The full `scratch` environment for `algo`, hatted with the green-flag
    block. `\\blockrepeatuntil` is defined in the worksheet preamble."""
    lines = [r"\begin{scratch}[%.2f]" % scale,
             r"\blockinit{when \greenflag\ clicked}"]
    lines += _emit(algo.body)
    lines.append(r"\end{scratch}")
    return "\n".join(lines)
