/* Lab: Would you ship it? Six real decisions from the GetYourGuide checkout programme.
   Data: the JSON block in the page, built from /lab/gyg-calls.json. No backend, nothing stored. */
(function () {
  var root = document.getElementById('wys');
  var src = document.getElementById('wysData');
  if (!root || !src) return;
  var D = JSON.parse(src.textContent);
  var DATA = D.calls;
  var N = DATA.length;
  var BY = {}; DATA.forEach(function (c, j) { BY[c.id] = j; });
  var LABEL = { ship: 'Ship', iterate: 'Iterate', kill: 'Kill' };
  var DESC = { ship: 'Roll it out', iterate: 'Improve or investigate first', kill: 'Stop the experiment' };
  var KEYS = { s: 'ship', i: 'iterate', k: 'kill' };
  var ORDER = ['EXP-06', 'EXP-08', 'EXP-09', 'EXP-10', 'EXP-07', 'EXP-01']; // most instructive first, for highlights
  var st = { i: 0, picks: [], phase: 'ask' };

  var rail = root.querySelector('.wys__rail');
  var count = root.querySelector('.wys__count');
  var stage = root.querySelector('.wys__stage');
  var end = root.querySelector('.wys__end');
  var log = document.getElementById('wysLog');

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function track(name, p) { if (typeof window.gtag === 'function') window.gtag('event', name, p || {}); }
  function fmt(r) { if (r.display) return r.display; var v = r.v; return (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(v) + r.unit; }
  function pickOf(id) { return st.picks[BY[id]]; }
  function scrollTo(el) { var t = el.getBoundingClientRect().top; if (t < 60 || t > window.innerHeight * 0.6) el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }

  /* ---------- tendencies: transparent rules on the actual answers ---------- */
  var TEND = [
    { key: 'evidence', name: 'Evidence-driven', desc: 'You look for sufficient evidence before scaling.',
      rule: 'Held back where the evidence was flat, not significant or partial (EXP-08, EXP-09, EXP-10): one point each time you did not ship.',
      max: 3, score: function () { return ['EXP-08', 'EXP-09', 'EXP-10'].filter(function (id) { return pickOf(id) !== 'ship'; }).length; } },
    { key: 'trust', name: 'Trust-conscious', desc: 'You protect the customer experience and long term value.',
      rule: 'Held back where trust or experience paid the price: EXP-06 (two points for kill, one for iterate) and EXP-08 (one point if not shipped).',
      max: 3, score: function () { var p = pickOf('EXP-06'); return (p === 'kill' ? 2 : p === 'iterate' ? 1 : 0) + (pickOf('EXP-08') !== 'ship' ? 1 : 0); } },
    { key: 'adaptive', name: 'Adaptive', desc: 'You separate improving an idea from abandoning it.',
      rule: 'Chose iterate where a signal survived the headline result (EXP-08, EXP-09, EXP-10): one point each.',
      max: 3, score: function () { return ['EXP-08', 'EXP-09', 'EXP-10'].filter(function (id) { return pickOf(id) === 'iterate'; }).length; } },
    { key: 'growth', name: 'Growth-driven', desc: 'You prioritise immediate, measurable impact.',
      rule: 'Shipped where a headline number was up but a cost or doubt sat next to it (EXP-06, EXP-08, EXP-10): one point each.',
      max: 3, score: function () { return ['EXP-06', 'EXP-08', 'EXP-10'].filter(function (id) { return pickOf(id) === 'ship'; }).length; } }
  ];
  function readTendencies() {
    var t = TEND.map(function (x) { var s = x.score(); return { key: x.key, name: x.name, desc: x.desc, rule: x.rule, s: s, max: x.max, r: s / x.max }; });
    var sorted = t.slice().sort(function (a, b) { return b.r - a.r; });
    var top = sorted[0];
    var tied = sorted.filter(function (x) { return x.r === top.r; });
    var second = tied.length === 1 ? sorted.filter(function (x) { return x !== top && x.r >= 0.66; })[0] : null;
    return { all: t, top: top, tied: tied.length > 1 ? tied.slice(0, 2) : null, second: second };
  }

  /* ---------- rail ---------- */
  function drawRail() {
    rail.innerHTML = DATA.map(function (c, j) {
      var cls = 'wys__seg', p = st.picks[j];
      if (p) cls += p === c.call ? ' is-hit' : ' is-diff';
      else if (j === st.i && st.phase !== 'end') cls += ' is-now';
      return '<span class="' + cls + '" data-n="' + (j + 1) + '">' + c.id + '</span>';
    }).join('');
    var done = st.picks.filter(Boolean).length;
    count.textContent = st.phase === 'end' ? 'Six decisions made' : 'Decision ' + (st.i + 1) + ' of ' + N;
    rail.setAttribute('aria-label', done + ' of ' + N + ' decisions made');
  }

  /* ---------- one decision ---------- */
  function evidence(c) {
    var max = 0;
    c.rows.forEach(function (r) { if (r.type === 'bar') max = Math.max(max, Math.abs(r.v)); });
    if (!max) max = 1;
    return c.rows.map(function (r) {
      if (r.type === 'sig') return '<div class="sig"><span>' + esc(r.label) + '</span><b class="' + r.tone + '">' + esc(r.text) + '</b></div>';
      var w = r.v === 0 ? 0 : Math.max(2, Math.abs(r.v) / max * 50);
      return '<div class="row"><span class="row__l">' + esc(r.label) + '</span>' +
        '<span class="row__track" aria-hidden="true"><i class="row__fill ' + (r.v < 0 ? 'neg' : 'pos') + ' ' + r.tone + '" data-w="' + w + '"></i></span>' +
        '<span class="row__v ' + r.tone + '">' + esc(fmt(r)) + (r.ns ? '<small>n.s.</small>' : '') + '</span></div>';
    }).join('');
  }

  function drawCard() {
    var c = DATA[st.i];
    var more = c.more.map(function (m) { return '<li>' + esc(m) + '</li>'; }).join('') + '<li class="prog">' + esc(D.programme) + '</li>';
    var btns = ['ship', 'iterate', 'kill'].map(function (k) {
      return '<button type="button" class="wys__b" data-k="' + k + '"><b>' + LABEL[k] + ' <kbd>' + k.charAt(0).toUpperCase() + '</kbd></b><span>' + DESC[k] + '</span></button>';
    }).join('');
    stage.innerHTML =
      '<div class="wys__card is-in">' +
        '<div class="wys__head">' +
          '<span class="wys__id">' + c.id + '</span>' +
          '<h2 class="wys__h">' + esc(c.title) + '</h2>' +
          '<dl class="brief"><dt>Context</dt><dd>' + esc(c.context) + '</dd><dt>We expected</dt><dd>' + esc(c.hypothesis) + '</dd></dl>' +
        '</div>' +
        '<div class="wys__res">' +
          '<div class="wys__res-k">EVIDENCE<i><u class="u-good">better</u><u class="u-bad">worse</u><u class="u-flat">flat</u></i></div>' +
          evidence(c) +
          '<div class="to"><div class="to__i to__i--g"><b>Gain</b><span>' + esc(c.gain) + '</span></div><div class="to__i to__i--r"><b>Risk</b><span>' + esc(c.risk) + '</span></div></div>' +
          '<details class="more"><summary>More context</summary><ul>' + more + '</ul></details>' +
        '</div>' +
        '<div class="wys__ask">' +
          '<span class="wys__q" id="wysQ">YOUR CALL: WHAT SHOULD WE DO NEXT?</span>' +
          '<div class="wys__btns" role="group" aria-labelledby="wysQ">' + btns + '</div>' +
          '<div class="wys__rev" aria-live="polite"></div>' +
        '</div>' +
      '</div>';
    var res = stage.querySelector('.wys__res');
    res.querySelectorAll('.row,.sig,.to').forEach(function (el, j) { el.style.transitionDelay = (0.1 + j * 0.1) + 's'; });
    requestAnimationFrame(function () { requestAnimationFrame(function () {
      res.classList.add('is-shown');
      res.querySelectorAll('.row__fill').forEach(function (f, j) { f.style.transitionDelay = (0.25 + j * 0.15) + 's'; f.style.width = f.getAttribute('data-w') + '%'; });
    }); });
    stage.querySelectorAll('.wys__b').forEach(function (b) { b.addEventListener('click', function () { pick(b.getAttribute('data-k')); }); });
  }

  function pick(k) {
    if (st.phase !== 'ask') return;
    var c = DATA[st.i];
    var same = k === c.call;
    st.picks[st.i] = k; st.phase = 'rev';
    stage.querySelectorAll('.wys__b').forEach(function (b) {
      var bk = b.getAttribute('data-k');
      b.disabled = true;
      if (bk === k) b.classList.add('is-picked');
      if (bk === c.call) b.classList.add('is-team');
      if (bk !== k && bk !== c.call) b.classList.add('is-dim');
    });
    var rev = stage.querySelector('.wys__rev');
    var last = st.i === N - 1;
    rev.className = 'wys__rev is-open ' + (same ? 'same' : 'diff');
    rev.innerHTML =
      '<div class="fb__calls">' +
        '<div><span>YOUR CALL</span><b>' + LABEL[k] + '</b></div>' +
        '<div><span>THE TEAM’S DECISION</span><b class="t">' + LABEL[c.call] + '</b></div>' +
      '</div>' +
      '<p class="fb__state">' + (same ? 'Aligned with the original team.' : 'A different call from the original team.') + '</p>' +
      '<span class="fb__k">WHY</span><p class="fb__why">' + esc(c.why) + '</p>' +
      (same ? '' : '<p class="fb__alt"><b>The case for your call.</b> ' + esc(c.alt[k]) + '</p>') +
      '<div class="fb__lesson"><span>PRODUCT LESSON</span><p>' + esc(c.lesson) + '</p></div>' +
      '<button type="button" class="wys__next">' + (last ? 'See how you decided' : 'Next decision') + ' <kbd>Enter</kbd></button>';
    rev.querySelector('.wys__next').addEventListener('click', next);
    rev.querySelector('.wys__next').focus({ preventScroll: true });
    setTimeout(function () { var rb = rev.getBoundingClientRect(); if (rb.top > window.innerHeight * 0.75) window.scrollBy({ top: rb.top - window.innerHeight * 0.35, behavior: 'smooth' }); }, 60);
    drawRail();
    if (st.i === 0) track('lab_start', { lab: 'would_you_ship_it' });
    track('lab_answer', { lab: 'would_you_ship_it', exp: c.id, pick: k, aligned: same });
  }

  function next() {
    if (st.phase !== 'rev') return;
    if (st.i < N - 1) {
      st.i++; st.phase = 'ask'; drawRail(); drawCard(); scrollTo(root);
      var first = stage.querySelector('.wys__b'); if (first) first.focus({ preventScroll: true });
    } else finish();
  }

  /* ---------- results ---------- */
  function finish() {
    st.phase = 'end';
    var aligned = 0;
    DATA.forEach(function (c, j) { if (st.picks[j] === c.call) aligned++; });
    drawRail();
    stage.innerHTML = ''; stage.hidden = true;
    end.hidden = false; end.classList.remove('is-open'); void end.offsetWidth; end.classList.add('is-open');

    // A. alignment
    end.querySelector('.ra__n').innerHTML = '<b>' + aligned + ' of ' + N + '</b> decisions aligned with the original team.';
    end.querySelector('.ra__dots').innerHTML = DATA.map(function (c, j) {
      var s = st.picks[j] === c.call;
      return '<span class="' + (s ? 'is-hit' : 'is-diff') + '" title="' + c.id + '"><i>' + c.id + '</i><b>' + LABEL[st.picks[j]] + (s ? '' : ' / team: ' + LABEL[c.call]) + '</b></span>';
    }).join('');

    // B. tendencies
    var T = readTendencies();
    var head = T.tied ? T.tied[0].name + ' and ' + T.tied[1].name.toLowerCase() + ', evenly' : T.top.name + (T.second ? ', with a ' + T.second.name.toLowerCase() + ' streak' : '');
    end.querySelector('.tb__h').textContent = head;
    end.querySelector('.tb__p').textContent = T.tied ? T.tied[0].desc + ' ' + T.tied[1].desc : T.top.desc;
    end.querySelector('.tb__bars').innerHTML = T.all.map(function (x) {
      var on = T.tied ? T.tied.indexOf(x) >= 0 : x === T.top;
      return '<div class="tb__row' + (on ? ' is-top' : '') + '"><span>' + x.name + '</span><i><u data-w="' + Math.round(x.r * 100) + '"></u></i><b>' + x.s + ' of ' + x.max + '</b></div>';
    }).join('');
    end.querySelector('.tb__rules').innerHTML = T.all.map(function (x) { return '<li><b>' + x.name + ', ' + x.s + ' of ' + x.max + '.</b> ' + esc(x.rule) + '</li>'; }).join('');
    requestAnimationFrame(function () { requestAnimationFrame(function () {
      end.querySelectorAll('.tb__row u').forEach(function (u, j) { u.style.transitionDelay = (0.2 + j * 0.12) + 's'; u.style.width = u.getAttribute('data-w') + '%'; });
    }); });

    // C. highlights
    var a = ORDER.filter(function (id) { return pickOf(id) === DATA[BY[id]].call; })[0];
    var d = ORDER.filter(function (id) { return pickOf(id) !== DATA[BY[id]].call; })[0];
    var hA = a ? (function (c) { return '<span class="hl__k">WHERE YOU ALIGNED</span><span class="hl__id">' + c.id + '</span><p class="hl__t">' + esc(c.title) + '</p><p class="hl__calls">You and the team: ' + LABEL[c.call] + '</p><p class="hl__p">' + esc(c.lesson) + '</p>'; })(DATA[BY[a]])
      : '<span class="hl__k">WHERE YOU ALIGNED</span><p class="hl__p">No alignment in these six. Every call you made has a defensible case; this only measures distance from what the team decided at the time.</p>';
    var hD = d ? (function (c) { var p = pickOf(c.id); return '<span class="hl__k">WHERE YOU DIVERGED</span><span class="hl__id">' + c.id + '</span><p class="hl__t">' + esc(c.title) + '</p><p class="hl__calls">You: ' + LABEL[p] + '. The team: ' + LABEL[c.call] + '.</p><p class="hl__p">' + esc(c.alt[p]) + ' ' + esc(c.lesson) + '</p>'; })(DATA[BY[d]])
      : '<span class="hl__k">WHERE YOU DIVERGED</span><p class="hl__p">Nowhere in these six. The closest call in the programme was EXP-08: a simpler flow that held on desktop and lost on mobile.</p>';
    end.querySelector('.hl__a').innerHTML = hA;
    end.querySelector('.hl__d').innerHTML = hD;

    // share
    var url = location.origin + location.pathname;
    var strongest = T.tied ? T.tied[0].name + ' and ' + T.tied[1].name : T.top.name;
    var share = 'Would you ship it?\nI made 6 product decisions based on real checkout experiments.\n' + aligned + '/6 aligned with the original team decisions.\nMy strongest tendency: ' + strongest + '.\n' + url;
    end.querySelector('.share__txt').textContent = share;
    var copyBtn = end.querySelector('[data-act="copy"]');
    copyBtn.textContent = 'Copy result';
    copyBtn.onclick = function () {
      var ok = function () { copyBtn.textContent = 'Copied'; }, fail = function () { selectShare(); copyBtn.textContent = 'Selected, press Ctrl+C'; };
      try { navigator.clipboard.writeText(share).then(ok, fail); } catch (e) { fail(); }
      track('lab_share', { lab: 'would_you_ship_it', via: 'copy' });
    };
    var li = end.querySelector('[data-act="li"]');
    li.href = 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(url);
    li.onclick = function () { track('lab_share', { lab: 'would_you_ship_it', via: 'linkedin' }); };
    end.querySelectorAll('[data-act="again"]').forEach(function (b) { b.onclick = reset; });
    end.querySelector('[data-act="explore"]').onclick = function () { openLog(true); };
    openLog(false);
    track('lab_complete', { lab: 'would_you_ship_it', aligned: aligned, tendency: T.top.key });
    scrollTo(root);
    var h = end.querySelector('.ra__n'); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
  }
  function selectShare() { var r = document.createRange(); r.selectNodeContents(end.querySelector('.share__txt')); var s = getSelection(); s.removeAllRanges(); s.addRange(r); }

  function openLog(go) {
    if (!log) return;
    log.hidden = false; log.classList.add('is-open');
    if (go) { log.scrollIntoView({ behavior: 'smooth', block: 'start' }); var h = log.querySelector('h2'); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); } }
  }

  function reset() {
    st = { i: 0, picks: [], phase: 'ask' };
    end.hidden = true; end.classList.remove('is-open');
    if (log) { log.hidden = true; log.classList.remove('is-open'); }
    stage.hidden = false;
    drawRail(); drawCard(); scrollTo(root);
    var first = stage.querySelector('.wys__b'); if (first) first.focus({ preventScroll: true });
    track('lab_retake', { lab: 'would_you_ship_it' });
  }

  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var t = e.target; if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SUMMARY' || t.isContentEditable)) return;
    var r = root.getBoundingClientRect(); if (r.bottom < 0 || r.top > window.innerHeight) return;
    var key = (e.key || '').toLowerCase();
    if (st.phase === 'ask' && KEYS[key]) { e.preventDefault(); pick(KEYS[key]); }
    else if (st.phase === 'rev' && (e.key === 'Enter' || e.key === 'ArrowRight')) {
      if (e.key === 'Enter' && t && t.classList && t.classList.contains('wys__next')) return; // native button handles Enter
      e.preventDefault(); next();
    }
  });

  if (log) { log.hidden = true; log.classList.remove('is-open'); }
  end.hidden = true;
  drawRail(); drawCard();
})();
