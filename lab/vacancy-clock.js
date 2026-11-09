/* Lab: The Vacancy Clock. Rebuilt from the ENSO Co-Living risk tier system.
   Tiers and the signal matrix are the shipped system. Rooms, prices and viewer counts are illustrative.
   No backend, nothing stored. */
(function () {
  var root = document.getElementById('vc');
  if (!root) return;

  var SIG = [
    { k: 'date', l: 'Availability date', chip: 1 },
    { k: 'viewers', l: 'Viewer count', chip: 1 },
    { k: 'deal', l: 'ENSO Deal tag', chip: 1 },
    { k: 'strike', l: 'Strikethrough price' },
    { k: 'last', l: 'Last room in flat', chip: 1 },
    { k: 'clean', l: 'Free cleaning' },
    { k: 'exit', l: 'No exit fee' },
    { k: 'member', l: 'Free membership' },
    { k: 'flex', l: 'Flexible entry date' }
  ];
  var LBL = {}; SIG.forEach(function (s) { LBL[s.k] = s.l; });

  var TIERS = [
    { n: 'L1', name: 'Calm', c: '#5eead4', min: 31, on: ['date'],
      why: 'More than 30 days out. Nothing is at risk yet, so the card stays clean: just the date. Pushing now spends trust you will need later.' },
    { n: 'L2', name: 'Watch', c: '#a3e635', min: 15, on: ['date', 'viewers'],
      why: 'Two to four weeks out, a viewer count appears. It is the one signal I would rebuild today, with something that stays true when nobody is watching, like how many people saved the room this month.' },
    { n: 'L3', name: 'Deals', c: '#f59e0b', min: 7, on: ['date', 'viewers', 'deal', 'strike', 'last', 'clean'],
      why: 'One to two weeks out. A real ENSO Deal unlocks: strikethrough price and free cleaning, plus last room context when it is true.' },
    { n: 'L4', name: 'High', c: '#fb923c', min: 0, on: ['date', 'viewers', 'deal', 'strike', 'last', 'clean', 'exit', 'member'],
      why: 'Under a week. The full stack: deal, no exit fee and free membership. In the experiment this tier drove the biggest uplift, +86%.' },
    { n: 'L5', name: 'Overdue', c: '#ef4444', min: -9999, on: ['date', 'viewers', 'deal', 'strike', 'clean', 'flex'],
      why: 'Past the target date, every day costs money. Commitment perks stop helping. What moves someone now is a flexible entry date.' }
  ];
  function tierOf(d) { for (var i = 0; i < TIERS.length; i++) if (d >= TIERS[i].min) return TIERS[i]; }

  // Illustrative rooms, mixed order so every round is a real call.
  var ROOMS = [
    { city: 'Madrid', name: 'Double room, Malasaña', mates: 3, d: 21, last: false, price: 690, px: '30%' },
    { city: 'Barcelona', name: 'Single room, Gràcia', mates: 4, d: 4, last: true, price: 720, px: '85%' },
    { city: 'Lisbon', name: 'Double room, Arroios', mates: 3, d: 38, last: false, price: 640, px: '55%' },
    { city: 'Valencia', name: 'Single room, Ruzafa', mates: 4, d: -6, last: false, price: 560, px: '10%' },
    { city: 'Valencia', name: 'Double room, Benimaclet', mates: 2, d: 10, last: true, price: 610, px: '70%' }
  ];
  var DAY = 140; // ~4.2K EUR a month per empty room

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function track(n, p) { if (typeof window.gtag === 'function') window.gtag('event', n, p || {}); }
  function eur(n) { return '€' + Math.round(n).toLocaleString('en-US'); }
  function dayLabel(d) { return d < 0 ? (-d) + (d === -1 ? ' day overdue' : ' days overdue') : d === 0 ? 'Today' : d + (d === 1 ? ' day' : ' days'); }
  // What the tenant sees: a calendar move-in date, never the internal days-to-target clock.
  var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function availLabel(d) {
    if (d <= 0) return 'Available now';
    var t = new Date(); t.setDate(t.getDate() + d);
    return 'Available from ' + t.getDate() + ' ' + MON[t.getMonth()];
  }
  function deal(p) { return Math.round(p * 0.875 / 10) * 10; }

  // The card is rendered once with every element present. Updates only toggle .on, so each
  // chip, perk and price fades and resizes in place instead of the whole card re-rendering.
  function card(room, on, opts) {
    var chips = [
      ['date', '', availLabel(room.d)],
      ['viewers', '', '3 people viewing'],
      ['deal', ' vcr__chip--deal', 'ENSO Deal'],
      ['last', ' vcr__chip--hot' + (room.last ? '' : ' is-false'), 'Last room in this flat']
    ].map(function (c) { return '<span class="vcr__chip' + c[1] + '" data-k="' + c[0] + '"><span>' + c[2] + '</span></span>'; }).join('');
    var perks = ['clean', 'exit', 'member', 'flex'].map(function (k) { return '<span data-k="' + k + '"><span>+ ' + LBL[k] + '</span></span>'; }).join('');
    var html = '<div class="vcr" data-c="' + (opts && opts.tint ? 1 : 0) + '">' +
      '<div class="vcr__img" role="img" aria-label="Illustrative photo of the room" style="--px:' + (room.px || '50%') + '"><div class="vcr__chips">' + chips + '</div></div>' +
      '<div class="vcr__b"><span class="vcr__t">' + esc(room.name) + '</span>' +
      '<span class="vcr__d">' + esc(room.city) + ', ' + room.mates + ' housemates</span>' +
      '<div class="vcr__p"><s data-k="strike"><span>' + eur(room.price) + '</span></s><span class="vcr__now"><span class="a">' + eur(room.price) + '</span><span class="b">' + eur(deal(room.price)) + '</span></span> <small>/ month</small></div>' +
      '<div class="vcr__perks">' + perks + '</div></div></div>';
    var w = document.createElement('div'); w.innerHTML = html;
    var el = w.firstChild; setCard(el, room, on, opts);
    return el;
  }
  function setCard(el, room, on, opts) {
    el.querySelectorAll('[data-k]').forEach(function (e) { e.classList.toggle('on', on.indexOf(e.dataset.k) > -1); });
    el.classList.toggle('is-deal', on.indexOf('strike') > -1);
    var d = el.querySelector('[data-k="date"] > span');
    if (d) d.textContent = availLabel(room.d);
    if (opts && opts.tint) el.style.borderColor = tierOf(room.d).c + '66';
  }
  function mount(host, el) { host.innerHTML = ''; host.appendChild(el); return el; }

  /* ---------------- Game ---------------- */
  var game = root.querySelector('.vc__game');
  var st = { i: 0, picks: [], res: [] };

  function verdict(room, pick) {
    var t = tierOf(room.d), out = [], over = 0, under = 0, fals = 0;
    SIG.forEach(function (s) {
      var you = pick.indexOf(s.k) > -1, sys = t.on.indexOf(s.k) > -1;
      if (you === sys) { out.push({ k: s.k, m: 'ok', you: you }); return; }
      if (you && s.k === 'last' && !room.last) { fals++; out.push({ k: s.k, m: 'false', txt: 'Not true for this room. The system never shows a claim it cannot prove.' }); return; }
      if (you) {
        over++;
        var txt = room.d < 0 && (s.k === 'exit' || s.k === 'member') ? 'Wrong lever this late. Past the date, flexibility moves people, not commitment perks.' :
          s.k === 'last' ? 'True, but not yet a reason to push at this distance.' : 'Too early. Pressure the risk does not justify yet.';
        out.push({ k: s.k, m: 'over', txt: txt });
      } else { under++; out.push({ k: s.k, m: 'under', txt: 'Missed. A real lever the risk justified.' }); }
    });
    return { t: t, rows: out, over: over, under: under, fals: fals, hits: out.filter(function (r) { return r.m === 'ok'; }).length };
  }

  function rail() {
    return '<div class="vc__rail">' + ROOMS.map(function (r, j) {
      var c = j < st.i ? 'is-done' : j === st.i ? 'is-now' : '';
      return '<span class="' + c + '"></span>';
    }).join('') + '</div>';
  }

  function ask() {
    var room = ROOMS[st.i], pick = ['date'];
    var cost = room.d < 0 ? '<span class="vc__cost">Already lost: ' + eur(-room.d * DAY) + ', and ' + eur(DAY) + ' more every day</span>' : '<span class="vc__cost vc__cost--calm">No money lost yet. The clock is running.</span>';
    game.innerHTML =
      '<div class="vc__top"><span class="vc__count">Room ' + (st.i + 1) + ' of ' + ROOMS.length + '</span>' + rail() + '</div>' +
      '<div class="vc__round is-in">' +
        '<div class="vc__ask">' +
          '<span class="vc__k">' + esc(room.city) + ' / internal clock, only ENSO sees this</span>' +
          '<p class="vc__clock">' + dayLabel(room.d) + '<small>' + (room.d < 0 ? 'past its target move-in date' : 'until its target move-in date') + '</small></p>' +
          cost +
          '<p class="vc__fact">' + (room.last ? 'It is the last free room in its flat.' : 'Other rooms in the flat are also free.') + ' 3 people are viewing it right now.</p>' +
          '<p class="vc__q">What is this card allowed to show? Tap the signals you would turn on.</p>' +
          '<div class="vc__sigs">' + SIG.map(function (s) {
            return '<button type="button" class="vc__sig" data-k="' + s.k + '" aria-pressed="' + (pick.indexOf(s.k) > -1) + '">' + s.l + '</button>';
          }).join('') + '</div>' +
          '<button type="button" class="vc__go">Lock it in</button>' +
        '</div>' +
        '<div class="vc__prev"><span class="vc__k">Your card, as the tenant sees it</span><div class="vc__card"></div></div>' +
      '</div>';
    var cel = mount(game.querySelector('.vc__card'), card(room, pick));
    var go = game.querySelector('.vc__go');
    game.querySelectorAll('.vc__sig').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.dataset.k, i = pick.indexOf(k);
        if (i > -1) pick.splice(i, 1); else pick.push(k);
        b.setAttribute('aria-pressed', i < 0);
        setCard(cel, room, pick);
      });
    });
    go.addEventListener('click', function () { reveal(room, pick.slice()); });
  }

  function reveal(room, pick) {
    var v = verdict(room, pick);
    st.picks[st.i] = pick; st.res[st.i] = v;
    track('vc_round', { room: st.i + 1, hits: v.hits, over: v.over, under: v.under });
    var head = v.hits === 9 ? 'Calibrated. Exactly what the system shows.' :
      v.fals ? 'You showed something that is not true.' :
      v.over > v.under ? 'You pushed harder than the risk justified.' :
      v.under > v.over ? 'You held back where the risk was real.' : 'Close, with a few signals off.';
    var diffs = v.rows.filter(function (r) { return r.m !== 'ok'; }).map(function (r) {
      return '<li class="vc__d vc__d--' + r.m + '"><b>' + (r.m === 'under' ? '− ' : '+ ') + LBL[r.k] + '</b><span>' + r.txt + '</span></li>';
    }).join('');
    var last = st.i === ROOMS.length - 1;
    game.querySelector('.vc__round').outerHTML =
      '<div class="vc__round vc__round--rev is-in">' +
        '<div class="vc__ask">' +
          '<span class="vc__k">' + esc(room.city) + ', ' + dayLabel(room.d) + '</span>' +
          '<p class="vc__tier" style="color:' + v.t.c + ';border-color:' + v.t.c + '">' + v.t.n + ' ' + v.t.name + '</p>' +
          '<p class="vc__vh">' + head + '</p>' +
          '<p class="vc__why">' + v.t.why + '</p>' +
          (diffs ? '<ul class="vc__diffs">' + diffs + '</ul>' : '') +
          '<p class="vc__score">' + v.hits + ' of 9 signal calls match the system</p>' +
          '<button type="button" class="vc__go">' + (last ? 'See your result' : 'Next room') + ' &#8594;</button>' +
        '</div>' +
        '<div class="vc__prev vc__prev--two">' +
          '<div><span class="vc__k">Your card</span><div class="vc__c1"></div></div>' +
          '<div><span class="vc__k" style="color:' + v.t.c + '">What ENSO showed</span><div class="vc__c2"></div></div>' +
        '</div>' +
      '</div>';
    mount(game.querySelector('.vc__c1'), card(room, pick));
    mount(game.querySelector('.vc__c2'), card(room, v.t.on, { tint: 1 }));
    game.querySelector('.vc__go').addEventListener('click', function () {
      if (last) return end();
      st.i++; ask(); scroll();
    });
    scroll();
  }

  function end() {
    var hits = 0, over = 0, under = 0, fals = 0, early = 0, late = 0;
    st.res.forEach(function (v, j) {
      hits += v.hits; over += v.over; under += v.under; fals += v.fals;
      if (ROOMS[j].d >= 15) early += v.over; else late += v.under;
    });
    var type = fals ? { h: 'The persuader', p: 'You showed at least one claim that was not true for that room. That is the line the whole system was built to hold: every chip on the card has to be provable from live data.' } :
      hits >= 42 ? { h: 'Calibrated', p: 'You matched the risk engine almost call for call. Urgency only where the clock justified it, and the right lever once the date had passed.' } :
      early > late ? { h: 'Pushes early', p: 'You turned on pressure while rooms were still safe. In testing, countdown style urgency made four out of five people say it felt like a pushy booking site. Calm rooms stay calm.' } :
      late > early ? { h: 'Holds back late', p: 'You protected trust, but left real levers off when rooms were about to cost money. Truthful urgency is not the enemy of trust: the guardrails held while bookings rose.' } :
      { h: 'Almost calibrated', p: 'A few signals off in both directions. The pattern that matters: urgency grows with real risk, and the lever changes once the date has passed.' };
    track('vc_end', { hits: hits, over: over, under: under, falsehoods: fals });
    var txt = 'The Vacancy Clock: ' + hits + '/45 signal calls matched the risk engine. ' + type.h + '. ' + location.origin + '/lab/vacancy-clock/';
    game.innerHTML =
      '<div class="vc__top"><span class="vc__count">Result</span>' + rail().replace(/is-now/g, 'is-done') + '</div>' +
      '<div class="vc__end is-in">' +
        '<p class="vc__big"><b>' + hits + '</b>/45</p><p class="vc__bigl">signal calls matched the shipped risk engine</p>' +
        '<div class="vc__type"><span class="vc__k">How you calibrated</span><p class="vc__th">' + type.h + '</p><p class="vc__tp">' + type.p + '</p>' +
        '<div class="vc__bars"><div><span>Pushed too early</span><i style="--w:' + Math.min(100, over * 8) + '%"></i><b>' + over + '</b></div>' +
        '<div><span>Held back</span><i style="--w:' + Math.min(100, under * 8) + '%"></i><b>' + under + '</b></div>' +
        '<div><span>Untrue claims</span><i class="r" style="--w:' + Math.min(100, fals * 25) + '%"></i><b>' + fals + '</b></div></div></div>' +
        '<div class="vc__acts">' +
          '<a class="vc__btn vc__btn--p" href="/work/enso.html#s11">See the system in the case study &#8594;</a>' +
          '<button type="button" class="vc__btn" data-act="copy">Copy your result</button>' +
          '<a class="vc__btn" target="_blank" rel="noopener" href="https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(location.origin + '/lab/vacancy-clock/') + '">Share on LinkedIn</a>' +
          '<button type="button" class="vc__btn" data-act="again">Play again</button>' +
        '</div>' +
      '</div>';
    game.querySelector('[data-act="again"]').addEventListener('click', function () { st = { i: 0, picks: [], res: [] }; ask(); scroll(); });
    game.querySelector('[data-act="copy"]').addEventListener('click', function (e) {
      var b = e.currentTarget;
      try { navigator.clipboard.writeText(txt).then(function () { b.textContent = 'Copied'; }, function () { b.textContent = txt; }); } catch (x) { b.textContent = txt; }
    });
    scroll();
  }

  function scroll() { var t = game.getBoundingClientRect().top; if (t < 60 || t > window.innerHeight * 0.5) game.scrollIntoView({ behavior: 'smooth', block: 'start' }); }

  /* ---------------- Free mode ---------------- */
  var fr = root.querySelector('.vc__free');
  var free = { name: 'Double room, shared flat', city: 'Valencia', mates: 4, d: 40, last: true, price: 640 };
  fr.innerHTML =
    '<div class="vcf">' +
      '<div class="vcf__l">' +
        '<div class="vcf__row"><label class="vc__k" for="vcRange">Internal clock: days until the target move-in date</label>' +
        '<button type="button" class="vc__btn vcf__play" aria-pressed="false">&#9654; Run the clock</button></div>' +
        '<input type="range" id="vcRange" min="-14" max="45" step="1" value="40">' +
        '<div class="vcf__scale"><span>overdue</span><span>0</span><span>15</span><span>30</span><span>45 days</span></div>' +
        '<div class="vcf__now"><span class="vcf__days"></span><span class="vc__tier vcf__tier"></span></div>' +
        '<div class="vcf__cost"><span class="vc__k">Cost of the empty room</span><b></b><small></small></div>' +
        '<p class="vcf__why"></p>' +
        '<div class="vcf__els">' + SIG.map(function (s) { return '<span data-k="' + s.k + '">' + s.l + '</span>'; }).join('') + '</div>' +
      '</div>' +
      '<div class="vcf__card"></div>' +
    '</div>';
  var r = fr.querySelector('#vcRange'), play = fr.querySelector('.vcf__play'), timer = null, fcard = null;
  function upd() {
    free.d = +r.value; var t = tierOf(free.d);
    fr.querySelector('.vcf__days').textContent = dayLabel(free.d);
    var tb = fr.querySelector('.vcf__tier'); tb.textContent = t.n + ' ' + t.name; tb.style.color = t.c; tb.style.borderColor = t.c;
    var lost = free.d < 0 ? -free.d * DAY : 0;
    fr.querySelector('.vcf__cost b').textContent = eur(lost);
    fr.querySelector('.vcf__cost b').style.color = lost ? '#f87171' : 'var(--t1)';
    fr.querySelector('.vcf__cost small').textContent = lost ? 'and ' + eur(DAY) + ' more every day it stays empty' : 'Nothing lost yet. Losses start at the target date, about ' + eur(DAY) + ' a day.';
    fr.querySelector('.vcf__why').textContent = t.why;
    fr.querySelectorAll('.vcf__els span').forEach(function (e) { e.classList.toggle('on', t.on.indexOf(e.dataset.k) > -1); });
    if (!fcard) fcard = mount(fr.querySelector('.vcf__card'), card(free, t.on, { tint: 1 }));
    else setCard(fcard, free, t.on, { tint: 1 });
  }
  function stop() { clearInterval(timer); timer = null; play.innerHTML = '&#9654; Run the clock'; play.setAttribute('aria-pressed', 'false'); }
  play.addEventListener('click', function () {
    if (timer) return stop();
    if (+r.value <= +r.min) r.value = r.max;
    play.innerHTML = '&#10074;&#10074; Pause'; play.setAttribute('aria-pressed', 'true'); track('vc_play');
    timer = setInterval(function () { if (+r.value <= +r.min) return stop(); r.value = +r.value - 1; upd(); }, 260);
  });
  r.addEventListener('input', function () { stop(); upd(); });
  upd();

  root.classList.add('is-live');
  ask();
})();
