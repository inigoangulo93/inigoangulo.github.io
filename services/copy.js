/* Copy button on code and prompt blocks, plus a light success snackbar shared by the site (window.siteSnack). */
(function () {
  var CSS = ''
    + '.cb{position:relative;margin:22px 0}'
    + '.cb>pre{margin:0!important;padding-top:20px}'
    + '.cb__btn{position:absolute;top:10px;right:10px;z-index:2;display:inline-flex;align-items:center;gap:7px;height:32px;padding:0 11px;border-radius:8px;border:1px solid var(--b1,rgba(255,255,255,.08));background:rgba(11,11,16,.92);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);color:var(--t2,#9a9aae);font:500 .7rem/1 var(--m,monospace);letter-spacing:.04em;cursor:pointer;opacity:.75;transition:opacity .2s,color .2s,border-color .2s,background .2s}'
    + '.cb:hover .cb__btn,.cb__btn:focus-visible{opacity:1}'
    + '.cb__btn:hover{color:var(--t1,#f4f4f6);border-color:var(--b2,rgba(255,255,255,.14))}'
    + '.cb__btn:focus-visible{outline:2px solid var(--ac,#2dd4bf);outline-offset:2px}'
    + '.cb__btn svg{width:14px;height:14px;flex:none}'
    + '.cb__btn .cb__ok{display:none}'
    + '.cb__btn.is-ok{color:var(--ac,#2dd4bf);border-color:var(--acb,rgba(45,212,191,.2));opacity:1}'
    + '.cb__btn.is-ok .cb__ic{display:none}.cb__btn.is-ok .cb__ok{display:block}'
    + '@media (hover:none){.cb__btn{opacity:1}}'
    + '@media (max-width:480px){.cb__btn{padding:0 9px}.cb__btn span{display:none}}'
    + '.snack{position:fixed;left:50%;bottom:calc(24px + env(safe-area-inset-bottom,0px));z-index:9999;display:flex;align-items:center;gap:10px;padding:11px 18px 11px 12px;border-radius:999px;background:rgba(10,10,14,.94);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border:1px solid var(--acb,rgba(45,212,191,.2));box-shadow:0 10px 40px rgba(0,0,0,.55),0 0 24px var(--acg,rgba(45,212,191,.12));color:var(--t1,#f4f4f6);font:500 .82rem/1.2 var(--s,sans-serif);letter-spacing:.005em;pointer-events:none;opacity:0;transform:translate(-50%,14px);transition:opacity .25s var(--e,ease),transform .35s var(--e,ease)}'
    + '.snack.is-on{opacity:1;transform:translate(-50%,0)}'
    + '.snack__i{display:grid;place-items:center;width:22px;height:22px;border-radius:50%;background:var(--acg,rgba(45,212,191,.12));color:var(--ac,#2dd4bf)}'
    + '.snack__i svg{width:13px;height:13px}'
    + '@media (prefers-reduced-motion:reduce){.snack{transition:opacity .2s;transform:translate(-50%,0)}}';

  var ICON_COPY = '<svg class="cb__ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="2.5"/><path d="M5 15H4.5A1.5 1.5 0 0 1 3 13.5v-9A1.5 1.5 0 0 1 4.5 3h9A1.5 1.5 0 0 1 15 4.5V5"/></svg>';
  var ICON_OK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';

  function inject() {
    if (document.getElementById('cb-css')) return;
    var s = document.createElement('style'); s.id = 'cb-css'; s.textContent = CSS; document.head.appendChild(s);
  }

  var snackEl, snackT;
  window.siteSnack = function (msg) {
    inject();
    if (!snackEl) {
      snackEl = document.createElement('div'); snackEl.className = 'snack';
      snackEl.setAttribute('role', 'status'); snackEl.setAttribute('aria-live', 'polite');
      snackEl.innerHTML = '<span class="snack__i">' + ICON_OK + '</span><span class="snack__t"></span>';
      document.body.appendChild(snackEl);
    }
    snackEl.querySelector('.snack__t').textContent = msg || 'Copied to clipboard';
    snackEl.classList.remove('is-on'); void snackEl.offsetWidth; snackEl.classList.add('is-on');
    clearTimeout(snackT); snackT = setTimeout(function () { snackEl.classList.remove('is-on'); }, 2000);
  };

  function legacyCopy(text) {
    var ta = document.createElement('textarea'); ta.value = text; ta.setAttribute('readonly', '');
    ta.style.cssText = 'position:fixed;top:-1000px;opacity:0'; document.body.appendChild(ta); ta.select();
    var ok = false; try { ok = document.execCommand('copy'); } catch (e) {} document.body.removeChild(ta); return ok;
  }
  window.siteCopy = function (text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text).catch(function () { if (!legacyCopy(text)) throw new Error('copy'); });
    return legacyCopy(text) ? Promise.resolve() : Promise.reject(new Error('copy'));
  };

  function init() {
    var blocks = document.querySelectorAll('pre:not(.share__txt):not([data-nocopy])');
    if (!blocks.length) return;
    inject();
    blocks.forEach(function (pre) {
      if (pre.parentNode.classList && pre.parentNode.classList.contains('cb')) return;
      var wrap = document.createElement('div'); wrap.className = 'cb';
      pre.parentNode.insertBefore(wrap, pre); wrap.appendChild(pre);
      var btn = document.createElement('button'); btn.type = 'button'; btn.className = 'cb__btn';
      btn.setAttribute('aria-label', 'Copy to clipboard');
      btn.innerHTML = ICON_COPY + '<svg class="cb__ok" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg><span>Copy</span>';
      var label = btn.querySelector('span'), t;
      btn.addEventListener('click', function () {
        var code = pre.querySelector('code') || pre;
        window.siteCopy(code.innerText.replace(/\n$/, '')).then(function () {
          btn.classList.add('is-ok'); label.textContent = 'Copied';
          window.siteSnack('Copied to clipboard');
          clearTimeout(t); t = setTimeout(function () { btn.classList.remove('is-ok'); label.textContent = 'Copy'; }, 1800);
          if (window.gtag) try { gtag('event', 'copy_block', { page: location.pathname }); } catch (e) {}
        }, function () { window.siteSnack('Could not copy, select the text instead'); });
      });
      wrap.appendChild(btn);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
