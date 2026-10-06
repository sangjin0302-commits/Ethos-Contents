/* 손으로 그은 듯한 강조(Rough Notation, MIT, vendor/rough-notation).
   카드 HTML에서 강조할 글자를 <span data-annotate="underline|circle|box|bracket">…</span>로 감싸고
   이 파일과 vendor/rough-notation/rough-notation.iife.js를 <script>로 넣는다. 색은 브랜드 골드, 애니메이션 없음.
   렌더마다 모양이 같도록 난수를 고정한다(QA·시각 회귀용). 형광펜(highlight)은 글자 대비를 해쳐 쓰지 않는다. */
(function () {
  function run() {
    if (!window.RoughNotation) return;
    var seed = 20261006, original = Math.random;
    Math.random = function () { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
    var gold = getComputedStyle(document.documentElement).getPropertyValue('--ethos-gold').trim() || '#B8972A';
    document.querySelectorAll('[data-annotate]').forEach(function (el) {
      var type = el.getAttribute('data-annotate');
      if (['underline', 'circle', 'box', 'bracket'].indexOf(type) < 0) return;
      RoughNotation.annotate(el, {
        type: type, color: gold, animate: false, multiline: true,
        strokeWidth: type === 'underline' ? 3 : 2, iterations: type === 'underline' ? 2 : 1,
        padding: type === 'circle' ? [4, 8] : 2, brackets: ['left']
      }).show();
    });
    Math.random = original;
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(run); else run();
})();
