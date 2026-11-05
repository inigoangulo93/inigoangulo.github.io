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
<meta property="og:image" content="https://inigoangulo.com/img/og.png">
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
<span class="lc__h">Would you ship it?</span>
<span class="lc__p">Six real calls from a checkout programme. Read the result, choose ship, iterate or kill, then see what the team did and why.</span>
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
<p class="lab__note"><span>Same numbers as the case studies</span><span>No sign up</span><span>Works on a phone</span></p>
</div></main>
'''
    out += FOOTER + '\n</body>\n</html>\n'
    return out


def game():
    d = json.load(open(os.path.join(HERE, 'gyg-calls.json')))
    calls = d["calls"]
    url = "https://inigoangulo.com/lab/would-you-ship-it/"
    out = head("Would you ship it? Six real checkout A/B test calls / Lab, Inigo Angulo",
               "Six real experiments from the GetYourGuide checkout programme. Read the result, decide ship, iterate or kill, and compare your call with the team's.",
               url, [("Inigo Angulo", "https://inigoangulo.com/"), ("Lab", "https://inigoangulo.com/lab/"), ("Would you ship it?", url)])
    log = "".join(
        f'<li><b>{esc(c["id"])}</b><span style="color:var(--t1)">{esc(c["title"])}</span>'
        f'<span>{esc("; ".join((r.get("display") or ((("+" if r["v"] > 0 else "−" if r["v"] < 0 else "") + str(abs(r["v"])) + r["unit"]))) + (" (n.s.)" if r.get("ns") else "") + " " + r["label"].lower() if r["type"] == "bar" else r["label"] + ": " + r["text"] for r in c["rows"]))}</span>'
        f'<span><em>{LABEL[c["call"]].upper()}</em> {esc(c["why"])}</span></li>' for c in calls)
    out += f'''<main class="lab"><div class="mx">
<a class="lab__back" href="/lab/">&#8592; Lab</a>
<span class="lab__k">Decide / 2 min / Growth and CRO</span>
<h1 class="lab__h1">Would you ship it? <em>Six real calls</em> from a checkout programme.</h1>
<p class="lab__lead">GetYourGuide checkout: ten experiments, +11% conversion across four markets. Read each result, make your call, then see what the team decided and why.</p>
<div class="lab__meta"><span>6 calls</span><span>About 2 minutes</span><span>Keys: S, I, K, Enter</span></div>

<section class="wys" id="wys" aria-label="Would you ship it?">
<div class="wys__top"><span class="wys__count">Call 1 of {len(calls)}</span><div class="wys__rail" role="img"></div></div>
<div class="wys__stage"><noscript><p>This piece needs JavaScript. The full log with every call is below.</p></noscript></div>
<div class="wys__end" aria-live="polite"><div class="end">
<div class="ring"><svg viewBox="0 0 200 200" aria-hidden="true"><circle class="bg" cx="100" cy="100" r="88"/><circle class="fg" cx="100" cy="100" r="88"/></svg><div class="ring__n"><b>0</b><span>of {len(calls)} calls</span></div></div>
<div>
<p class="end__h"></p><p class="end__p"></p>
<div class="recap"></div>
<div class="end__acts">
<button type="button" class="wys__btn wys__btn--p" data-act="copy">Copy your result</button>
<a class="wys__btn" data-act="li" href="#" target="_blank" rel="noopener">Share on LinkedIn</a>
<a class="wys__btn" href="/work/checkout.html">Read the full case &#8594;</a>
<button type="button" class="wys__btn" data-act="again">Play again</button>
</div>
</div>
</div></div>
</section>

<section class="shows">
<span class="lab__k" style="color:var(--t3)">What this shows</span>
<div class="shows__g">
<div><b>Success criteria first</b><p>Every test had its winning rule written before launch. That is why a +4.2% could still be killed.</p></div>
<div><b>The segment, not the average</b><p>72% of the uplift lived on mobile. A neutral desktop result never paid for a mobile loss.</p></div>
<div><b>Kill the test, keep the principle</b><p>The single page lost. Unbroken context survived and shipped as two named steps.</p></div>
</div>
<div class="links"><a href="/work/checkout.html">Read the full case &#8594;</a><a href="/cro-ecommerce-consultant/">CRO and commerce &#8594;</a><a href="/writing/checkout-conversion-ten-experiments/">Ten checkout experiments, written up &#8594;</a></div>
</section>

<details class="log"><summary>The full log: all six calls, results and reasons</summary><ol>{log}</ol></details>
</div></main>
'''
    out += FOOTER + '\n'
    out += '<script type="application/json" id="wysData">' + json.dumps(d, ensure_ascii=False).replace('</', '<\\/') + '</script>\n'
    out += f'<script src="/lab/wys.js?v={VER}" defer></script>\n</body>\n</html>\n'
    return out


os.makedirs(os.path.join(HERE, 'would-you-ship-it'), exist_ok=True)
open(os.path.join(HERE, 'index.html'), 'w').write(index())
open(os.path.join(HERE, 'would-you-ship-it', 'index.html'), 'w').write(game())
print('built lab/index.html and lab/would-you-ship-it/index.html')
