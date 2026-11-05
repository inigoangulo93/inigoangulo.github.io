/* Lab: Would you ship it? Six real calls from the GetYourGuide checkout programme.
   Data comes from the JSON block in the page, built from /lab/gyg-calls.json. */
(function () {
  var root = document.getElementById('wys');
  var src = document.getElementById('wysData');
  if (!root || !src) return;
  var DATA = JSON.parse(src.textContent).calls;
  var N = DATA.length;
  var LABEL = { ship: 'Ship', iterate: 'Iterate', kill: 'Kill' };
  var DESC = { ship: 'Roll it out', iterate: 'Change it, test again', kill: 'Stop it here' };
  var STAMP = { ship: 'SHIPPED', iterate: 'ITERATED', kill: 'KILLED' };
  var KEYS = { s: 'ship', i: 'iterate', k: 'kill' };
  var st = { i: 0, picks: [], phase: 'ask' };

  var rail = root.querySelector('.wys__rail');
  var count = root.querySelector('.wys__count');
  var stage = root.querySelector('.wys__stage');
  var end = root.querySelector('.wys__end');

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function track(name, p) { if (typeof window.gtag === 'function') window.gtag('event', name, p || {}); }
  function fmt(r) {
    if (r.display) return r.display;
    var v = r.v, s = v > 0 ? '+' : v < 0 ? '−' : '';
    return s + Math.abs(v) + r.unit;
  }

  function drawRail() {
    rail.innerHTML = DATA.map(function (c, j) {
      var cls = 'wys__seg';
      if (st.picks[j]) cls += st.picks[j] === c.call ? ' is-hit' : ' is-miss';
      else if (j === st.i && st.phase !== 'end') cls += ' is-now';
      return '<span class="' + cls + '" data-n="' + (j + 1) + '">' + c.id + '</span>';
    }).join('');
    var done = st.picks.filter(Boolean).length;
    count.textContent = st.phase === 'end' ? 'All ' + N + ' calls made' : 'Call ' + (st.i + 1) + ' of ' + N;
    rail.setAttribute('aria-label', done + ' of ' + N + ' calls made');
  }

  function drawCard() {
    var c = DATA[st.i];
    var max = 0;
    c.rows.forEach(function (r) { if (r.type === 'bar') max = Math.max(max, Math.abs(r.v)); });
    if (!max) max = 1;
    var rows = c.rows.map(function (r) {
      if (r.type === 'sig') return '<div class="sig"><span>' + esc(r.label) + '</span><b class="' + r.tone + '">' + esc(r.text) + '</b></div>';
      var w = r.v === 0 ? 0 : Math.max(2, Math.abs(r.v) / max * 50);
      var dir = r.v < 0 ? 'neg' : 'pos';
      return '<div class="row"><span class="row__l">' + esc(r.label) + '</span>' +
        '<span class="row__track" aria-hidden="true"><i class="row__fill ' + dir + ' ' + r.tone + '" data-w="' + w + '"></i></span>' +
        '<span class="row__v ' + r.tone + '">' + esc(fmt(r)) + (r.ns ? '<small>n.s.</small>' : '') + '</span></div>';
    }).join('');
    var btns = ['ship', 'iterate', 'kill'].map(function (k) {
      return '<button type="button" class="wys__b" data-k="' + k + '"><b>' + LABEL[k] + ' <kbd>' + k.charAt(0).toUpperCase() + '</kbd></b><span>' + DESC[k] + '</span></button>';
    }).join('');
    stage.innerHTML =
      '<div class="wys__card is-in">' +
        '<div class="wys__head">' +
          '<span class="wys__id">' + c.id + '</span>' +
          '<h2 class="wys__h">' + esc(c.title) + '</h2>' +
          '<p class="wys__ctx">' + esc(c.ctx) + '</p>' +
        '</div>' +
        '<div class="wys__ask">' +
          '<span class="wys__q" id="wysQ">YOUR CALL</span>' +
          '<div class="wys__btns" role="group" aria-labelledby="wysQ">' + btns + '</div>' +
          '<div class="wys__rev" aria-live="polite"></div>' +
        '</div>' +
        '<div class="wys__res">' +
          '<div class="wys__res-k">THE RESULT<i><u class="u-good">better</u><u class="u-bad">worse</u><u class="u-flat">flat</u></i></div>' +
          rows +
        '</div>' +
      '</div>';
    var res = stage.querySelector('.wys__res');
    var items = res.querySelectorAll('.row,.sig');
    items.forEach(function (el, j) { el.style.transitionDelay = (0.12 + j * 0.12) + 's'; });
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        res.classList.add('is-shown');
        res.querySelectorAll('.row__fill').forEach(function (f, j) {
          f.style.transitionDelay = (0.3 + j * 0.15) + 's';
          f.style.width = f.getAttribute('data-w') + '%';
        });
      });
    });
    stage.querySelectorAll('.wys__b').forEach(function (b) {
      b.addEventListener('click', function () { pick(b.getAttribute('data-k')); });
    });
  }

  function pick(k) {
    if (st.phase !== 'ask') return;
    var c = DATA[st.i];
    st.picks[st.i] = k;
    st.phase = 'rev';
    var hit = k === c.call;
    stage.querySelectorAll('.wys__b').forEach(function (b) {
      var bk = b.getAttribute('data-k');
      b.disabled = true;
      if (bk === c.call) b.classList.add('is-team');
      else if (bk === k) b.classList.add('is-picked');
      else b.classList.add('is-dim');
    });
    var rev = stage.querySelector('.wys__rev');
    var last = st.i === N - 1;
    rev.className = 'wys__rev is-open ' + (hit ? 'hit' : 'miss');
    rev.innerHTML =
      '<span class="wys__stamp ' + c.call + '">' + STAMP[c.call] + '</span>' +
      '<p class="wys__lead">' + (hit ? esc(c.lead) : 'Different call. The team chose ' + LABEL[c.call] + '.') + '</p>' +
      '<p class="wys__why">' + esc(c.why) + '</p>' +
      '<button type="button" class="wys__next">' + (last ? 'See your score' : 'Next call') + ' <kbd>Enter</kbd></button>';
    rev.querySelector('.wys__next').addEventListener('click', next);
    rev.querySelector('.wys__next').focus({ preventScroll: true });
    var rb = rev.getBoundingClientRect();
    if (rb.bottom > window.innerHeight) window.scrollBy({ top: rb.bottom - window.innerHeight + 24, behavior: 'smooth' });
    drawRail();
    track('lab_answer', { lab: 'would_you_ship_it', exp: c.id, pick: k, hit: hit });
    if (st.i === 0) track('lab_start', { lab: 'would_you_ship_it' });
  }

  function next() {
    if (st.phase !== 'rev') return;
    if (st.i < N - 1) {
      st.i++; st.phase = 'ask'; drawRail(); drawCard();
      var top = root.getBoundingClientRect().top;
      if (top < 0) root.scrollIntoView({ behavior: 'smooth', block: 'start' });
      var first = stage.querySelector('.wys__b'); if (first) first.focus({ preventScroll: true });
    } else finish();
  }

  function finish() {
    st.phase = 'end';
    var hits = 0;
    DATA.forEach(function (c, j) { if (st.picks[j] === c.call) hits++; });
    drawRail();
    stage.innerHTML = '';
    stage.style.display = 'none';
    end.classList.add('is-open');
    var head = hits === N ? 'A perfect read.' : hits >= 5 ? 'You read it like the team did.' : hits >= 3 ? 'Where most product teams land.' : 'The tempting answer kept winning.';
    var note = hits >= 5 ? 'Including the wins that were not worth keeping. That is the hard part: a positive number is not a decision.'
      : hits >= 3 ? 'The misses are usually the wins that spend trust, or the averages that hide a losing segment.'
      : 'Most of these had a number that said ship. The call came from what the number was hiding.';
    end.querySelector('.end__h').textContent = head;
    end.querySelector('.end__p').textContent = note;
    end.querySelector('.recap').innerHTML = DATA.map(function (c, j) {
      var h = st.picks[j] === c.call;
      return '<div class="' + (h ? 'hit' : 'miss') + '"><b>' + c.id + '</b><span class="y">You: ' + LABEL[st.picks[j]] + '</span><span class="t">Team: ' + LABEL[c.call] + '</span></div>';
    }).join('');
    var fg = end.querySelector('.ring .fg');
    var C = 2 * Math.PI * 88;
    fg.style.strokeDasharray = C;
    fg.style.strokeDashoffset = C;
    var nEl = end.querySelector('.ring__n b');
    requestAnimationFrame(function () { requestAnimationFrame(function () { fg.style.strokeDashoffset = C * (1 - hits / N); }); });
    var t0 = null, dur = 1200;
    function tick(t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); nEl.textContent = Math.round(hits * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(tick); }
    nEl.textContent = '0'; requestAnimationFrame(tick);
    var share = 'I matched ' + hits + ' of ' + N + ' real checkout calls on "Would you ship it?" ' + location.origin + location.pathname;
    var copyBtn = end.querySelector('[data-act="copy"]');
    copyBtn.onclick = function () {
      var done = function () { copyBtn.textContent = 'Copied'; };
      try { navigator.clipboard.writeText(share).then(done, done); } catch (e) { done(); }
      track('lab_share', { lab: 'would_you_ship_it', via: 'copy' });
    };
    end.querySelector('[data-act="li"]').href = 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(location.origin + location.pathname);
    end.querySelector('[data-act="again"]').onclick = reset;
    track('lab_complete', { lab: 'would_you_ship_it', score: hits });
    root.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function reset() {
    st = { i: 0, picks: [], phase: 'ask' };
    end.classList.remove('is-open');
    end.querySelector('[data-act="copy"]').textContent = 'Copy your result';
    stage.style.display = '';
    drawRail(); drawCard();
    root.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var t = e.target; if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
    var r = root.getBoundingClientRect(); if (r.bottom < 0 || r.top > window.innerHeight) return;
    if (st.phase === 'ask' && KEYS[e.key.toLowerCase()]) { e.preventDefault(); pick(KEYS[e.key.toLowerCase()]); }
    else if (st.phase === 'rev' && (e.key === 'Enter' || e.key === 'ArrowRight')) { if (t && t.classList && t.classList.contains('wys__next') && e.key === 'Enter') return; e.preventDefault(); next(); }
  });

  root.classList.add('is-live');
  drawRail(); drawCard();
})();
