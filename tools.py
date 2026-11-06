#!/usr/bin/env python3
"""
Kalkulator numerik untuk materi Bab 10-11 (hanya butuh numpy).

Pemakaian (dari PHP atau terminal):
    python3 tools.py parametrik_panjang "cos(t)" "sin(t)" 0 6.283185307
    python3 tools.py parametrik_kemiringan "t**2" "t**3-3*t" 1
    python3 tools.py parametrik_luas "t-sin(t)" "1-cos(t)" 0 6.283185307
    python3 tools.py kutub_luas "1+sin(t)" 0 6.283185307
    python3 tools.py kutub_panjang "1+sin(t)" 0 6.283185307
    python3 tools.py barisan "n/(n+1)" 1 12

Ekspresi dievaluasi lewat AST berdaftar-putih (tidak memakai eval mentah),
sehingga aman dipanggil dari web.
"""
import ast
import json
import sys

import numpy as np

_FUNCS = {
    "sin": np.sin, "cos": np.cos, "tan": np.tan, "sec": lambda x: 1 / np.cos(x),
    "csc": lambda x: 1 / np.sin(x), "cot": lambda x: 1 / np.tan(x),
    "asin": np.arcsin, "acos": np.arccos, "atan": np.arctan,
    "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh,
    "exp": np.exp, "ln": np.log, "log": np.log, "sqrt": np.sqrt, "abs": np.abs,
}
_CONST = {"pi": np.pi, "e": np.e}
_BIN = {ast.Add: np.add, ast.Sub: np.subtract, ast.Mult: np.multiply,
        ast.Div: np.divide, ast.Pow: np.power, ast.Mod: np.mod}
_UN = {ast.USub: np.negative, ast.UAdd: np.positive}


def _eval(node, env):
    if isinstance(node, ast.Expression):
        return _eval(node.body, env)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in env:
            return env[node.id]
        if node.id in _CONST:
            return _CONST[node.id]
        raise ValueError(f"Nama tidak dikenal: {node.id}")
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN:
        return _BIN[type(node.op)](_eval(node.left, env), _eval(node.right, env))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UN:
        return _UN[type(node.op)](_eval(node.operand, env))
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id in _FUNCS and len(node.args) == 1 and not node.keywords):
        return _FUNCS[node.func.id](_eval(node.args[0], env))
    raise ValueError("Ekspresi tidak diizinkan")


def make_fn(expr, var="t"):
    expr = expr.replace("^", "**")
    if len(expr) > 200:
        raise ValueError("Ekspresi terlalu panjang")
    tree = ast.parse(expr, mode="eval")

    def f(x):
        x = np.asarray(x, dtype=float)
        with np.errstate(all="ignore"):
            r = _eval(tree, {var: x})
        return np.broadcast_to(np.asarray(r, dtype=float), x.shape).copy()

    return f


def num(text):
    """Baca angka atau ekspresi konstan seperti 2*pi."""
    return float(make_fn(str(text))(np.array([0.0]))[0])


def deriv(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)


def simpson(y, x):
    n = len(x) - 1
    if n % 2:
        raise ValueError("n harus genap")
    h = (x[-1] - x[0]) / n
    return h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum())


def grid(a, b, n=20000):
    return np.linspace(a, b, n + 1)


def main(argv):
    if len(argv) < 2:
        raise ValueError("Perintah tidak diberikan")
    cmd = argv[1]
    out = {"perintah": cmd}

    if cmd == "parametrik_panjang":
        fx, fy = make_fn(argv[2]), make_fn(argv[3])
        a, b = num(argv[4]), num(argv[5])
        t = grid(a, b)
        v = np.sqrt(deriv(fx, t) ** 2 + deriv(fy, t) ** 2)
        out["hasil"] = simpson(v, t)
        out["rumus"] = "L = ∫ √((dx/dt)² + (dy/dt)²) dt"

    elif cmd == "parametrik_kemiringan":
        fx, fy = make_fn(argv[2]), make_fn(argv[3])
        t0 = np.array([num(argv[4])])
        dx, dy = deriv(fx, t0)[0], deriv(fy, t0)[0]
        out.update(x=float(fx(t0)[0]), y=float(fy(t0)[0]), dx_dt=dx, dy_dt=dy)
        out["hasil"] = None if abs(dx) < 1e-9 else dy / dx
        out["catatan"] = "dx/dt ≈ 0 → tangen vertikal (atau titik singular)" if out["hasil"] is None else ""
        out["rumus"] = "dy/dx = (dy/dt)/(dx/dt)"

    elif cmd == "parametrik_luas":
        fx, fy = make_fn(argv[2]), make_fn(argv[3])
        a, b = num(argv[4]), num(argv[5])
        t = grid(a, b)
        out["hasil"] = simpson(fy(t) * deriv(fx, t), t)
        out["rumus"] = "A = ∫ y(t) x'(t) dt"

    elif cmd == "kutub_luas":
        r = make_fn(argv[2])
        a, b = num(argv[3]), num(argv[4])
        t = grid(a, b)
        out["hasil"] = simpson(0.5 * r(t) ** 2, t)
        out["rumus"] = "A = ½ ∫ r² dθ"

    elif cmd == "kutub_panjang":
        r = make_fn(argv[2])
        a, b = num(argv[3]), num(argv[4])
        t = grid(a, b)
        out["hasil"] = simpson(np.sqrt(r(t) ** 2 + deriv(r, t) ** 2), t)
        out["rumus"] = "L = ∫ √(r² + (dr/dθ)²) dθ"

    elif cmd == "barisan":
        f = make_fn(argv[2], var="n")
        n0, n1 = int(num(argv[3])), int(num(argv[4]))
        if n1 - n0 > 200:
            raise ValueError("Maksimum 200 suku")
        n = np.arange(n0, n1 + 1, dtype=float)
        out["suku"] = [{"n": int(i), "a_n": float(v)} for i, v in zip(n, f(n))]
        big = np.array([1e3, 1e5, 1e7])
        out["a_n_untuk_n_besar"] = {str(int(k)): float(v) for k, v in zip(big, f(big))}
        out["catatan"] = "Nilai untuk n besar memberi petunjuk limit; bukan bukti."

    else:
        raise ValueError(f"Perintah tidak dikenal: {cmd}")

    return out


if __name__ == "__main__":
    try:
        print(json.dumps(main(sys.argv), ensure_ascii=False, default=float))
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        sys.exit(1)
