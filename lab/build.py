#!/usr/bin/env python3
"""Builds the Lab pages. Run from the repo root: python3 lab/build.py
Data for "Would you ship it?" lives in lab/gyg-calls.json: one source for the game and its static log."""
import json, html, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'services'))
from chrome import header, mobmenu, FOOTER
VER = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip() or "0"
esc = lambda s: html.escape(str(s), quote=True)

GA = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-WWCZNNK7YW"></script>\n<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-WWCZNNK7YW");</script>\n<script src="/analytics.js" defer></script>'
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
LABEL = {"ship": "Shipped", "iterate": "Iterated", "kill": "Killed"}


def head(title, desc, url, crumbs):
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]}
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<meta property="og:title" content="{esc(title.split(" / ")[0])}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="https://inigoangulo.com/img/og-home.png">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
<link rel="stylesheet" href="/services/services.css?v={VER}">
<link rel="stylesheet" href="/lab/lab.css?v={VER}">
{GA}
<script type="application/ld+json">{json.dumps(bc, ensure_ascii=False)}</script>
</head>
<body>
{header('lab', 'Lab')}{mobmenu('lab')}
<script src="/services/bar.js?v={VER}" defer></script>
<script src="/services/copy.js?v={VER}" defer></script>
'''


def index():
    url = "https://inigoangulo.com/lab/"
    out = head("Lab: real product decisions you make first / Inigo Angulo",
               "Interactive pieces rebuilt from real case studies. Make the call on real experiments and workflows, then see what the team decided and why.",
               url, [("Inigo Angulo", "https://inigoangulo.com/"), ("Lab", url)])
    out += '''<main class="lab"><div class="mx">
<span class="lab__k">Lab</span>
<h1 class="lab__h1">Don&#8217;t take my word for it. <em>Make the call.</em></h1>
<p class="lab__lead">Real decisions from my case studies, rebuilt so you make them first. A few minutes each, and you see the judgment behind the result, not only the result.</p>

<div class="lab__grid">

<a class="lc" href="/lab/would-you-ship-it/">
<div class="lc__art" aria-hidden="true"><div class="mini">
<span class="mini__stamp">KILLED</span>
<span class="mini__id">EXP-08</span><span class="mini__t">Single-page checkout</span>
<div class="mini__bars"><span class="mini__bar mini__bar--a"><i></i></span><span class="mini__bar mini__bar--b"><i></i></span></div>
<div class="mini__btns"><span>Ship</span><span>Iterate</span><span class="pk">Kill</span></div>
</div></div>
<div class="lc__body">
<span class="lc__k">DECIDE / 2 MIN</span>
<span class="lc__h">Would You Ship It?</span>
<span class="lc__p">Six checkout decisions. Real trade-offs. No obvious answers. Make each call, then see what the team actually decided, and why.</span>
<div class="lc__shows"><b>WHAT IT SHOWS</b><span>Experiment judgment: success criteria first, segments over averages.</span></div>
<div class="lc__foot"><span>GetYourGuide checkout</span><span class="lc__go">Play &#8594;</span></div>
</div>
</a>

<div class="lc lc--soon">
<div class="lc__art" aria-hidden="true"><div class="gates"><span>G1</span><i></i><span>G2</span><i></i><span>G3</span><i></i><span class="on">G4</span></div></div>
<div class="lc__body">
<span class="lc__k">REVIEW / NEXT</span>
<span class="lc__h">Gate 4</span>
<span class="lc__p">The fourth gate of a brief to content pipeline. You see what the system flagged and decide whether it moves on.</span>
<div class="lc__shows"><b>WHAT IT SHOWS</b><span>Workflow design: exception first review and human gates on AI output.</span></div>
<div class="lc__foot"><span>ShelfFlow</span><span class="lc__pill">Next</span></div>
</div>
</div>

<div class="lc lc--soon">
<div class="lc__art" aria-hidden="true"><div class="calc"><b>CONVERSIONS PER MONTH</b><i style="--w:62%"></i><b>EXPECTED LIFT</b><i style="--w:28%"></i><strong>? weeks</strong></div></div>
<div class="lc__body">
<span class="lc__k">CALCULATE / IN THE WORKSHOP</span>
<span class="lc__h">Is your traffic enough to test?</span>
<span class="lc__p">Your monthly conversions and the lift you hope for. It tells you how long a test needs, or that it is not worth running.</span>
<div class="lc__shows"><b>WHAT IT SHOWS</b><span>When experimentation pays, and when it does not.</span></div>
<div class="lc__foot"><span>CRO toolkit</span><span class="lc__pill">Later</span></div>
</div>
</div>

</div>
</div></main>
'''
    out += FOOTER + '\n</body>\n</html>\n'
    return out


SCENARIO_KEYS = ["id", "title", "context", "hypothesis", "rows", "gain", "risk", "more"]
DECISION_KEYS = ["id", "call", "why", "lesson", "alt"]


def game():
    d = json.load(open(os.path.join(HERE, 'gyg-calls.json')))
    calls = d["calls"]
    url = "https://inigoangulo.com/lab/would-you-ship-it/"
    out = head("Would You Ship It? Six real checkout A/B test decisions / Lab, Inigo Angulo",
               "Six checkout decisions from the GetYourGuide experiment programme. Real trade-offs, no obvious answers. Make each call, then see what the team decided and why.",
               url, [("Inigo Angulo", "https://inigoangulo.com/"), ("Lab", "https://inigoangulo.com/lab/"), ("Would You Ship It?", url)])

    def ev(r):
        if r["type"] == "sig":
            return f'{r["label"]}: {r["text"]}'
        v = r.get("display") or (("+" if r["v"] > 0 else "\u2212" if r["v"] < 0 else "") + str(abs(r["v"])) + r["unit"])
        return f'{r["label"]} {v}' + (" (not significant)" if r.get("ns") else "")
    # Scenarios only: context and evidence, never the team's decision. Shown if the interactive version cannot start.
    scen = "".join(
        f'<li><span class="lg__id">{esc(c["id"])}</span><div><p class="lg__t">{esc(c["title"])}</p>'
        f'<p><b>Context.</b> {esc(c["context"])} <b>We expected:</b> {esc(c["hypothesis"])}</p>'
        f'<p><b>Evidence.</b> {esc("; ".join(ev(r) for r in c["rows"]))}.</p></div></li>' for c in calls)
    page_data = {"programme": d["programme"], "calls": [{k: c[k] for k in SCENARIO_KEYS} for c in calls]}

    out += f'''<main class="lab"><div class="mx">
<a class="lab__back" href="/lab/">&#8592; Lab</a>
<span class="lab__k">Decide / 2 min / Growth and CRO</span>
<h1 class="lab__h1">Would You Ship It?</h1>
<p class="lab__sub">Six checkout decisions. Real trade-offs. No obvious answers.</p>
<p class="lab__lead">From the GetYourGuide checkout experiment programme. Make each call, then see what the team actually decided, and why.</p>
<div class="lab__meta"><span>6 decisions</span><span>About 2 minutes</span><span>Real A/B tests</span><span class="lab__keys">Keys: S, I, K, Enter</span></div>
<details class="more lab__data"><summary>About the data</summary><p>{esc(d["programme"])}</p></details>

<section class="wys" id="wys" aria-label="Would You Ship It?" aria-busy="true">
<div class="wys__top"><span class="wys__count">Decision 1 of {len(calls)}</span><div class="wys__rail" role="img" aria-label="Progress"></div></div>
<div class="wys__stage">
<div class="wys__load" role="status"><span class="wys__spin" aria-hidden="true"></span><span>Loading the first decision</span></div>
</div>
<div class="wys__end" hidden>
<div class="ra"><p class="ra__n"></p><div class="ra__dots"></div><p class="ra__note">Alignment with what the team decided at the time, not a measure of product skill.</p></div>
<div class="end__grid">
<div class="tb">
<span class="end__k">HOW YOU DECIDED</span>
<p class="tb__h"></p><p class="tb__p"></p>
<div class="tb__bars"></div>
<details class="more tb__how"><summary>How this is read</summary><ul class="tb__rules"></ul><p class="tb__cav">Four lenses applied to six decisions with fixed rules. Read it as a pattern in these calls, not a profile of how you work.</p></details>
</div>
<div class="hl"><div class="hl__i hl__a"></div><div class="hl__i hl__d"></div></div>
</div>
<div class="share">
<span class="end__k">SHARE</span>
<pre class="share__txt"></pre>
<div class="end__acts">
<button type="button" class="wys__btn" data-act="copy">Copy your result</button>
<a class="wys__btn" data-act="li" href="#" target="_blank" rel="noopener">Share on LinkedIn</a>
</div>
</div>
<div class="end__cta">
<a class="wys__btn wys__btn--p" href="/work/checkout.html#s06">See how I think about product decisions &#8594;</a>
<button type="button" class="wys__btn" data-act="explore">Explore all six decisions</button>
<button type="button" class="wys__btn" data-act="again">Play again</button>
</div>
</div>
<div class="wys__fail" id="wysFail">
<p class="wys__fail-h">The interactive version did not start.</p>
<p class="wys__fail-p">It needs JavaScript, and it may have been blocked or failed to load. <button type="button" class="wys__retry" onclick="location.reload()">Try again</button> or read the six scenarios below. The decisions the team made are in the <a href="/work/checkout.html#s05">checkout case study</a>.</p>
<ol class="wys__scen">{scen}</ol>
</div>
</section>

<details class="lg" id="wysLog" hidden><summary><h2 class="lg__h">Explore all six decisions</h2></summary><div class="lg__body"></div></details>
<noscript><style>#wys .wys__load{{display:none}}#wys .wys__fail{{display:block}}</style></noscript>
</div></main>
'''
    out += FOOTER + '\n'
    out += '<script type="application/json" id="wysData">' + json.dumps(page_data, ensure_ascii=False).replace('</', '<\\/') + '</script>\n'
    out += f'<script src="/lab/wys.js?v={VER}" defer onerror="var w=document.getElementById(\'wys\');if(w)w.classList.add(\'is-failed\')"></script>\n'
    out += '<script>setTimeout(function(){var w=document.getElementById("wys");if(w&&!w.classList.contains("is-live"))w.classList.add("is-failed")},9000)</script>\n'
    out += '</body>\n</html>\n'
    dec = {"calls": [{k: c[k] for k in DECISION_KEYS} for c in calls]}
    open(os.path.join(HERE, 'would-you-ship-it', 'decisions.json'), 'w').write(json.dumps(dec, ensure_ascii=False))
    return out


os.makedirs(os.path.join(HERE, 'would-you-ship-it'), exist_ok=True)
open(os.path.join(HERE, 'index.html'), 'w').write(index())
open(os.path.join(HERE, 'would-you-ship-it', 'index.html'), 'w').write(game())
print('built lab/index.html and lab/would-you-ship-it/index.html')
