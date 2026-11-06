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
<div class="pt">
<p class="pt__tag">Lab</p>
<h1 class="pt__h pt__h--wide">Don&#8217;t take my word for it. Make the call.</h1>
<p class="pt__sub">Real decisions from my case studies, rebuilt so you make them first. <em>A few minutes each, and you see the judgment behind the result.</em></p>
</div>

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

<a class="lc" href="/lab/vacancy-clock/">
<div class="lc__art lc__art--vc" aria-hidden="true"><div class="mvc">
<div class="mvc__img"><span class="mvc__tier"></span><div class="mvc__chips"><span class="c1">Available from 27 Nov</span><span class="c2">3 viewing</span><span class="c3">ENSO Deal</span><span class="c4">Last room</span></div></div>
<div class="mvc__b"><span class="mvc__t">Double room, shared flat</span><span class="mvc__d">Valencia, 4 housemates</span>
<span class="mvc__p"><s>&#8364;640</s><span class="pn"><span class="pa">&#8364;640</span><span class="pb">&#8364;560</span></span><small>/ month</small></span></div>
</div></div>
<div class="lc__body">
<span class="lc__k">DESIGN / 3 MIN</span>
<span class="lc__h">The Vacancy Clock</span>
<span class="lc__p">Five rooms, five clocks. Decide what each listing card is allowed to show, then compare it with the risk engine that lifted bookings 34%.</span>
<div class="lc__shows"><b>WHAT IT SHOWS</b><span>Ethical urgency: signals calibrated to real risk, never invented.</span></div>
<div class="lc__foot"><span>ENSO Co-Living catalogue</span><span class="lc__go">Play &#8594;</span></div>
</div>
</a>

<div class="lc lc--soon" aria-disabled="true"><span class="lc__soon">Coming soon</span>
<div class="lc__art" aria-hidden="true"><div class="gates"><span>G1</span><i></i><span>G2</span><i></i><span>G3</span><i></i><span class="on">G4</span></div></div>
<div class="lc__body">
<span class="lc__k">REVIEW / COMING SOON</span>
<span class="lc__h">Gate 4</span>
<span class="lc__p">The fourth gate of a brief to content pipeline. You see what the system flagged and decide whether it moves on.</span>
<div class="lc__shows"><b>WHAT IT SHOWS</b><span>Workflow design: exception first review and human gates on AI output.</span></div>
<div class="lc__foot"><span>ShelfFlow</span><span class="lc__pill">Not available yet</span></div>
</div>
</div>

<div class="lc lc--soon" aria-disabled="true"><span class="lc__soon">Coming soon</span>
<div class="lc__art" aria-hidden="true"><div class="calc"><b>CONVERSIONS PER MONTH</b><i style="--w:62%"></i><b>EXPECTED LIFT</b><i style="--w:28%"></i><strong>? weeks</strong></div></div>
<div class="lc__body">
<span class="lc__k">CALCULATE / COMING SOON</span>
<span class="lc__h">Is your traffic enough to test?</span>
<span class="lc__p">Your monthly conversions and the lift you hope for. It tells you how long a test needs, or that it is not worth running.</span>
<div class="lc__shows"><b>WHAT IT SHOWS</b><span>When experimentation pays, and when it does not.</span></div>
<div class="lc__foot"><span>CRO toolkit</span><span class="lc__pill">Not available yet</span></div>
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
<div class="pt" style="margin-bottom:0">
<p class="pt__tag">Decide / 2 min / Growth and CRO</p>
<h1 class="pt__h">Would You Ship It?</h1>
<p class="pt__sub">Six checkout decisions. Real trade-offs. <em>No obvious answers.</em></p>
</div>
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


def clock():
    url = "https://inigoangulo.com/lab/vacancy-clock/"
    out = head("The Vacancy Clock: design ethical urgency for real listings / Lab, Inigo Angulo",
               "Five co-living rooms, five vacancy clocks. Decide what each listing card may show, then compare with the risk tier system that lifted ENSO bookings 34% without hurting trust.",
               url, [("Inigo Angulo", "https://inigoangulo.com/"), ("Lab", "https://inigoangulo.com/lab/"), ("The Vacancy Clock", url)])
    tiers = [("L1 Calm", "30+ days", "date"), ("L2 Watch", "15 to 30", "date viewers"),
             ("L3 Deals", "7 to 14", "date viewers deal strike last clean"),
             ("L4 High", "0 to 6", "date viewers deal strike last clean exit member"),
             ("L5 Overdue", "past date", "date viewers deal strike clean flex")]
    sigs = [("date", "Availability date"), ("viewers", "Live viewer count"), ("deal", "ENSO Deal tag"), ("strike", "Strikethrough price"),
            ("last", "Last room in flat"), ("clean", "Free cleaning"), ("exit", "No exit fee"), ("member", "Free membership"), ("flex", "Flexible entry date")]
    mx = '<table class="vc__mx"><thead><tr><th>Signal</th>' + "".join(f"<th>{n}<br><small>{d}</small></th>" for n, d, _ in tiers) + "</tr></thead><tbody>"
    mx += "".join("<tr><td>" + l + "</td>" + "".join("<td>" + ("&#10003;" if k in on.split() else "&#8211;") + "</td>" for _, _, on in tiers) + "</tr>" for k, l in sigs)
    mx += "</tbody></table>"
    out += f'''<main class="lab"><div class="mx">
<a class="lab__back" href="/lab/">&#8592; Lab</a>
<div class="pt" style="margin-bottom:0">
<p class="pt__tag">Design / 3 min / Conversion and trust</p>
<h1 class="pt__h">The Vacancy Clock</h1>
<p class="pt__sub">Every empty room costs about &#8364;4.2K a month. <em>How much urgency is honest?</em></p>
</div>
<p class="lab__lead">From the ENSO Co-Living catalogue. Five rooms, each with its own clock. Decide what each listing card is allowed to show, then compare it with the risk tier system that shipped and lifted booking conversion 34% in a 14,208 user A/B test.</p>
<div class="lab__meta"><span>5 rooms</span><span>About 3 minutes</span><span>Real tier system</span><span>Illustrative rooms and prices</span></div>
<details class="more lab__data"><summary>About the data</summary><p>The five tiers and which signals each one activates are the system that shipped at ENSO Co-Living across Lisbon, Valencia, Madrid and Barcelona. Rooms, prices and viewer counts here are illustrative. The daily cost is the average of about &#8364;4.2K a month per empty room, spread over 30 days.</p></details>

<section class="vc" id="vc" aria-label="The Vacancy Clock">
<p class="vc__sec">Your call: five rooms</p>
<div class="vc__game" aria-live="polite"><p class="vc__count">Loading the first room</p></div>
<p class="vc__sec">Free mode: run the clock</p>
<div class="vc__free"></div>
<div class="vc__fail">
<p class="wys__fail-h">The interactive version did not start.</p>
<p class="wys__fail-p">It needs JavaScript. <button type="button" class="wys__retry" onclick="location.reload()">Try again</button> or read the system below. The full story is in the <a href="/work/enso.html#s11">ENSO case study</a>.</p>
{mx}
</div>
</section>
<noscript><style>#vc .vc__fail{{display:block}}#vc .vc__game,#vc .vc__free,#vc .vc__sec{{display:none}}</style></noscript>
</div></main>
'''
    out += FOOTER + '\n'
    out += f'<script src="/lab/vacancy-clock.js?v={VER}" defer onerror="var v=document.getElementById(\'vc\');if(v)v.classList.add(\'is-failed\')"></script>\n'
    out += '<script>setTimeout(function(){var v=document.getElementById("vc");if(v&&!v.classList.contains("is-live"))v.classList.add("is-failed")},9000)</script>\n'
    out += '</body>\n</html>\n'
    return out


os.makedirs(os.path.join(HERE, 'would-you-ship-it'), exist_ok=True)
open(os.path.join(HERE, 'index.html'), 'w').write(index())
open(os.path.join(HERE, 'would-you-ship-it', 'index.html'), 'w').write(game())
os.makedirs(os.path.join(HERE, 'vacancy-clock'), exist_ok=True)
open(os.path.join(HERE, 'vacancy-clock', 'index.html'), 'w').write(clock())
print('built lab/index.html, lab/would-you-ship-it/index.html and lab/vacancy-clock/index.html')
