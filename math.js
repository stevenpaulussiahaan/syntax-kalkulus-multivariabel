// Render semua rumus \( \) dan \[ \] dengan KaTeX (lokal, tanpa internet).
document.addEventListener('DOMContentLoaded', function () {
  renderMathInElement(document.body, {
    delimiters: [{ left: '\\[', right: '\\]', display: true }, { left: '\\(', right: '\\)', display: false }],
    throwOnError: false, strict: 'ignore'
  });
  document.documentElement.setAttribute('data-math-ready', '1');
});
