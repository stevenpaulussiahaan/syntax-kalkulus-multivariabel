// Kalkulator numerik di peramban (tanpa server, tanpa eval). Setara dengan python/tools.py.
(function () {
  const FUNCS = {
    sin: Math.sin, cos: Math.cos, tan: Math.tan, sec: x => 1 / Math.cos(x), csc: x => 1 / Math.sin(x),
    cot: x => 1 / Math.tan(x), asin: Math.asin, acos: Math.acos, atan: Math.atan,
    sinh: Math.sinh, cosh: Math.cosh, tanh: Math.tanh, exp: Math.exp, ln: Math.log, log: Math.log,
    sqrt: Math.sqrt, abs: Math.abs
  };
  const CONST = { pi: Math.PI, e: Math.E };
  const has = (o, k) => Object.prototype.hasOwnProperty.call(o, k);

  // Parser recursive-descent: expr = term (+|- term)*; term = unary (*|/ unary)*; unary = -unary | pow; pow = atom (^ unary)?
  function compile(src, varName) {
    src = String(src).replace(/\*\*/g, '^');
    if (src.length > 200) throw new Error('Ekspresi terlalu panjang');
    const tok = src.match(/\s*(\d+\.?\d*(?:[eE][+-]?\d+)?|\.\d+|[A-Za-z_]\w*|[-+*/^(),])/g);
    if (!tok || tok.join('').replace(/\s/g, '') !== src.replace(/\s/g, '')) throw new Error('Ekspresi tidak valid');
    const T = tok.map(s => s.trim());
    let i = 0;
    const peek = () => T[i], next = () => T[i++];
    function expr() { let n = term(); while (peek() === '+' || peek() === '-') { const o = next(), r = term(), l = n; n = o === '+' ? v => l(v) + r(v) : v => l(v) - r(v); } return n; }
    function term() { let n = unary(); while (peek() === '*' || peek() === '/' || implicitStart()) { const o = (peek() === '*' || peek() === '/') ? next() : '*', r = unary(), l = n; n = o === '*' ? v => l(v) * r(v) : v => l(v) / r(v); } return n; }
    function implicitStart() { const t = peek(); return t !== undefined && (/^[A-Za-z_(]/.test(t) || /^\d|^\./.test(t)) && false; }
    function unary() { if (peek() === '-') { next(); const f = unary(); return v => -f(v); } if (peek() === '+') { next(); return unary(); } return pow(); }
    function pow() { const b = atom(); if (peek() === '^') { next(); const e = unary(); return v => Math.pow(b(v), e(v)); } return b; }
    function atom() {
      const t = next();
      if (t === undefined) throw new Error('Ekspresi tidak lengkap');
      if (/^(\d|\.)/.test(t)) { const c = parseFloat(t); return () => c; }
      if (t === '(') { const e = expr(); if (next() !== ')') throw new Error('Kurung tidak seimbang'); return e; }
      if (/^[A-Za-z_]/.test(t)) {
        if (peek() === '(') {
          if (!has(FUNCS, t)) throw new Error('Fungsi tidak dikenal: ' + t);
          next(); const a = expr(); if (next() !== ')') throw new Error('Kurung tidak seimbang');
          const f = FUNCS[t]; return v => f(a(v));
        }
        if (t === varName) return v => v;
        if (has(CONST, t)) { const c = CONST[t]; return () => c; }
        throw new Error('Nama tidak dikenal: ' + t);
      }
      throw new Error('Token tidak terduga: ' + t);
    }
    const f = expr();
    if (i !== T.length) throw new Error('Ekspresi tidak valid dekat "' + T[i] + '"');
    return f;
  }

  const num = s => compile(s, '_')(0);
  const deriv = (f, x, h = 1e-5) => (f(x + h) - f(x - h)) / (2 * h);
  function simpson(g, a, b, n = 20000) {
    const h = (b - a) / n; let s = g(a) + g(b);
    for (let k = 1; k < n; k++) s += g(a + k * h) * (k % 2 ? 4 : 2);
    return s * h / 3;
  }

  const MODES = {
    parametrik_panjang: { nama: 'Panjang kurva parametrik', f: ['x(t)', 'y(t)', 't awal', 't akhir'], def: ['cos(t)', 'sin(t)', '0', '2*pi'],
      run(a) { const fx = compile(a[0], 't'), fy = compile(a[1], 't'); return { hasil: simpson(t => Math.hypot(deriv(fx, t), deriv(fy, t)), num(a[2]), num(a[3])), rumus: "L = ∫ √((dx/dt)² + (dy/dt)²) dt" }; } },
    parametrik_kemiringan: { nama: 'Kemiringan garis singgung parametrik', f: ['x(t)', 'y(t)', 't₀'], def: ['t^2', 't^3-3*t', 'sqrt(3)'],
      run(a) { const fx = compile(a[0], 't'), fy = compile(a[1], 't'), t0 = num(a[2]); const dx = deriv(fx, t0), dy = deriv(fy, t0);
        return { x: fx(t0), y: fy(t0), 'dx/dt': dx, 'dy/dt': dy, hasil: Math.abs(dx) < 1e-9 ? 'tak hingga (tangen vertikal)' : dy / dx, rumus: 'dy/dx = (dy/dt)/(dx/dt)' }; } },
    parametrik_luas: { nama: 'Luas di bawah kurva parametrik', f: ['x(t)', 'y(t)', 't awal', 't akhir'], def: ['t-sin(t)', '1-cos(t)', '0', '2*pi'],
      run(a) { const fx = compile(a[0], 't'), fy = compile(a[1], 't'); return { hasil: simpson(t => fy(t) * deriv(fx, t), num(a[2]), num(a[3])), rumus: "A = ∫ y(t) x'(t) dt" }; } },
    kutub_luas: { nama: 'Luas daerah kutub', f: ['r(t) (t = θ)', 'θ awal', 'θ akhir'], def: ['cos(2*t)', '-pi/4', 'pi/4'],
      run(a) { const r = compile(a[0], 't'); return { hasil: simpson(t => 0.5 * r(t) ** 2, num(a[1]), num(a[2])), rumus: 'A = ½ ∫ r² dθ' }; } },
    kutub_panjang: { nama: 'Panjang kurva kutub', f: ['r(t) (t = θ)', 'θ awal', 'θ akhir'], def: ['1+sin(t)', '0', '2*pi'],
      run(a) { const r = compile(a[0], 't'); return { hasil: simpson(t => Math.hypot(r(t), deriv(r, t)), num(a[1]), num(a[2])), rumus: 'L = ∫ √(r² + (dr/dθ)²) dθ' }; } },
    barisan: { nama: 'Suku-suku barisan', f: ['a(n)', 'n awal', 'n akhir'], def: ['n/(n+1)', '1', '12'],
      run(a) { const f = compile(a[0], 'n'), n0 = Math.round(num(a[1])), n1 = Math.round(num(a[2]));
        if (n1 - n0 > 200) throw new Error('Maksimum 200 suku');
        const suku = []; for (let n = n0; n <= n1; n++) suku.push({ n, a_n: f(n) });
        return { suku, a_n_untuk_n_besar: { 1000: f(1e3), 100000: f(1e5), 10000000: f(1e7) }, catatan: 'Nilai untuk n besar memberi petunjuk limit; bukan bukti.' }; } }
  };

  const sel = document.getElementById('mode'), box = document.getElementById('fields'),
        out = document.getElementById('out'), err = document.getElementById('err'), form = document.getElementById('calc');
  Object.entries(MODES).forEach(([k, m]) => sel.add(new Option(m.nama, k)));
  function render() {
    const m = MODES[sel.value]; box.innerHTML = '';
    m.f.forEach((lab, i) => { const l = document.createElement('label'); l.textContent = lab + ' ';
      const inp = document.createElement('input'); inp.name = 'a' + i; inp.value = m.def[i]; inp.required = true; l.appendChild(inp); box.appendChild(l); });
    out.textContent = ''; err.textContent = '';
  }
  sel.addEventListener('change', render);
  form.addEventListener('submit', ev => {
    ev.preventDefault(); err.textContent = ''; out.textContent = '';
    try {
      const vals = [...box.querySelectorAll('input')].map(i => i.value.trim());
      const res = MODES[sel.value].run(vals);
      out.textContent = JSON.stringify(res, null, 2);
    } catch (e) { err.textContent = e.message; }
  });
  render();
})();
