#!/usr/bin/env python3
"""Builds the articles under /writing/. Run from the repo root: python3 writing/build.py"""
import json, html, os, datetime

GA = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-WWCZNNK7YW"></script>\n<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-WWCZNNK7YW");</script>\n<script src="/analytics.js" defer></script>'
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
CSS = '''.art{max-width:720px;margin:0 auto;padding:110px 24px 40px}
.art .k{margin-bottom:12px}.art h1{font-size:clamp(1.9rem,4vw,2.9rem);max-width:none}
.art .meta{font-family:var(--m);font-size:.74rem;color:var(--t3);margin:16px 0 34px;display:flex;gap:16px;flex-wrap:wrap}
.art p{max-width:none;font-size:1.05rem;line-height:1.7;margin:0 0 18px}
.art h2{font-size:1.35rem;margin:38px 0 12px;max-width:none}
.art ul,.art ol{margin:0 0 18px 22px;color:var(--t2);font-size:1.02rem;line-height:1.65}
.art li{margin-bottom:6px}
.art .num{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:26px 0}
.art .num div{border:1px solid var(--b1);border-radius:10px;padding:14px;background:var(--glass)}
.art .num b{display:block;font-size:1.5rem;font-weight:800;letter-spacing:-.04em;color:var(--ac2);line-height:1}
.art .num span{display:block;font-family:var(--m);font-size:.66rem;color:var(--t3);margin-top:7px;line-height:1.45}
@media(max-width:700px){.art .num{grid-template-columns:1fr 1fr}}
.art blockquote{border-left:3px solid var(--ac);padding:4px 0 4px 18px;margin:22px 0;color:var(--t1);font-size:1.1rem;font-weight:500}
.art .box{border:1px solid var(--acb);border-radius:12px;padding:20px 22px;background:var(--acg2);margin:26px 0}
.art .box p{margin:0;font-size:.98rem}
.art .box a{color:var(--ac2);border-bottom:1px solid var(--acb)}
.art a{color:var(--ac2)}
.art .cta{margin-top:40px}
.art .cta h2{margin:0 0 6px}
'''

POSTS = {
"one-person-ai-agent-team-445-prs": dict(
  title="445 PRs in seven weeks: what a one person team with AI agents actually looks like",
  desc="Real numbers from building Acervo with an AI engineering team: 484 pull requests, 1,456 CI runs, 15 gated releases, and what the human did all day.",
  date="2026-11-04", read="7 min",
  body="""
<p>Between September 16 and November 2, 2026, I built and shipped a production platform for car collections with no engineers on payroll. The GitHub API says 484 pull requests were opened, 445 merged, 38 closed without merging. 1,456 CI runs, 1,026 green. Fifteen numbered releases to production, each with a security report and one human approval. I want to describe what that looked like from the inside, because "I built it with AI" has started to mean anything, and the useful version is specific.</p>

<div class="num"><div><b>17 days</b><span>first commit to first production deploy</span></div><div><b>445</b><span>pull requests merged</span></div><div><b>1,456</b><span>CI runs, 147 red</span></div><div><b>15</b><span>gated releases</span></div></div>

<h2>The team, and why it is a team</h2>
<p>The work was done by eight AI agents with fixed roles: a lead that decomposes tickets and integrates, workers for frontend, backend and data, a reviewer, a security agent that runs a full penetration test before every promotion, a design agent with the only write access to Figma, and a verifier that only reads. Each one has a mandate written in a file, with what it may touch and what it must never touch. None of them has production credentials. That last sentence is the whole architecture.</p>
<p>Calling it a team is not marketing. The roles matter because the failure modes are the same as with people: a worker that starts from the wrong branch, a reviewer that approves its own work, a check that looks green because it did not run. Every rule in the repository exists because one of those happened and cost a day.</p>

<h2>What the human did all day</h2>
<p>Not code. I wrote tickets with acceptance criteria, answered decisions and approved releases. Every open question the agents hit became a numbered decision with lettered options and a recommendation; I answered with an id and a letter, "014-3 B", and the answer was written into the repository with the reasoning. Over seven weeks that produced more than 140 recorded decisions. That log is the product's memory, and it is why a new agent session can pick up where the last one stopped.</p>
<p>The other thing I did was say no. 38 pull requests were closed without merging. 147 CI runs went red. A red check on the exact commit blocks the merge, whoever asks, and the "whoever" includes me on a Friday evening wanting the feature out.</p>

<h2>The rhythm</h2>
<p>Week one was infrastructure: database, auth, row level security with tests that run as the role that must not pass, the CI pipeline. Day 17 was the first production release. From week four the rhythm settled at roughly forty tickets a week. A typical ticket, from a real day: written at 14:35, pull request opened by the lead at 16:56, fourteen checks green, pen test PASS at 17:20, merged, promoted at 19:50, served from the production domain at 19:54. Five hours, with a human at two of the gates.</p>

<h2>What was not fast</h2>
<p>Judgment. Deciding what the product should be took as long as it always has. The data model was argued over for days. The agents are very fast at building the wrong thing, which is why the first week was spent on invariants: which rules live in the database, which in the application, and the test that proves each one.</p>
<p>And verification. Reading a CI run instead of trusting its colour. Opening the deployment by its URL and looking for the content instead of asking the provider whether it was "READY". The gates where a human looks are the product; the agents are what make them affordable.</p>

<h2>What I would tell a team adopting this</h2>
<ul>
<li>Give agents roles and files, not prompts. A mandate that survives the session is worth ten clever instructions.</li>
<li>Isolation before speed. No agent holds production credentials. Promotion is a human act with a security report attached.</li>
<li>Write decisions down with ids. It is the only way to stop re-arguing them.</li>
<li>A check that did not run looks exactly like a check that passed. Read the run.</li>
<li>Count the closed pull requests. If none are closed, the review is not reviewing.</li>
</ul>

<div class="box"><p>The full case, with the evidence from the GitHub API, the data model, the promotion flow and the day the security gate said no: <a href="/work/acervo.html">Acervo, the case study</a>. If you want this for your company: <a href="/ai-product-builder/">AI build and deployment</a>.</p></div>
"""),
"green-check-is-not-proof": dict(
  title="Why a green check is not proof: the gates between an AI agent and production",
  desc="On October 6 a navigation redesign merged on 8 of 8 green checks. The e2e job had not run. What that taught me about verification when agents write the code.",
  date="2026-11-04", read="6 min",
  body="""
<p>On October 6, 2026, I merged a navigation redesign into main. The pull request showed eight checks, eight green. The next pull request touched a different directory, the browser tests ran for the first time against the new navigation, and twelve of them went red. One was a product failure: on desktop, there was no longer any way to add a car.</p>
<p>The e2e job had not run on the redesign. Its path filter only started it for four directories, and the redesign touched none of them. A skipped job reports as success. From the outside, a check that did nothing and a check that passed are identical. That is the sentence I keep coming back to, because it is the core problem of letting agents write code quickly: the volume of change goes up tenfold, and your ability to read it does not.</p>

<h2>The gates, as they stand now</h2>
<p>Every pull request on Acervo passes five required checks before main will accept it: lint with seven house rules, strict types, 4,300 unit and integration tests plus 5,900 database assertions, a check that the auth email templates are intact, and a secrets scan on every commit of the branch. A sixth, 590 browser tests, runs on every change that is not documentation. Since October 6 the filter is inverted: instead of a list of what triggers the browser tests, a list of what may skip them.</p>
<p>Then the release gate. Before any promotion to production, a security agent runs a full penetration test against local and staging, never production, and writes a report with a verdict. A FAIL blocks the promotion like a red check. On October 15 it said FAIL on a rule outside the feature being promoted; the feature shipped behind a flag and the rule was fixed first. Promotion itself is one human command, logged with who and when.</p>

<h2>Rules I had to write down</h2>
<ul>
<li><b>A skipped check does not count as green.</b> Before merging anything with a screen, open the e2e run and read it: which steps executed, how many tests passed.</li>
<li><b>Nothing is declared, everything is produced.</b> No agent writes "the deployment works". A script produces JSON with the deployment id and status, and the agent interprets it. "CI green" and "the preview" are not phrases; a run id and a URL are.</li>
<li><b>A test that documents a bug protects the bug.</b> If writing a test reveals something broken, it becomes a ticket and the test is marked pending, never green. A green test on a known failure makes the fix look like a regression.</li>
<li><b>Break a policy on purpose.</b> On any change to database security, the reviewer deliberately breaks one isolation rule and confirms the suite goes red. If it stays green, the tests do not test what they claim.</li>
<li><b>Read the annotations before the code.</b> Seven red checks in four seconds are not seven failures. One morning they were a billing limit on the CI account.</li>
</ul>

<h2>Why this matters more with agents</h2>
<p>None of these rules are new to engineering. What changed is that the agents are tireless and literal. They will produce a passing suite that proves nothing if that is what the rules permit, and they will do it 445 times. The only defence is to be precise about what counts as proof, and to make the human gates cheap enough that they are actually used. A gate nobody has time to open is not a gate.</p>

<blockquote>Nothing here required a better model. It required a rule about what counts as proof.</blockquote>

<div class="box"><p>The failure story, beat by beat, with the run ids, is in the <a href="/work/acervo.html#s10">Trust chapter of the Acervo case</a>. If your team is introducing agents and wants the guardrails with them: <a href="/ai-product-builder/">how I set that up</a>.</p></div>
"""),
"checkout-conversion-ten-experiments": dict(
  title="Checkout conversion: the ten experiments behind +11%",
  desc="At GetYourGuide, 38% of converters left checkout and came back with no re-entry experience. Ten experiments, four EU markets, +11% conversion, and the ones that lost.",
  date="2026-11-04", read="6 min",
  body="""
<p>The team was optimising the wrong step. Payment was instrumented to the pixel, and payment was fine. What nobody had measured was the gap: 38% of the people who eventually converted had left checkout at least once and come back, and when they came back the product treated them like strangers. No cart memory, no "you were here", a fresh start at step one.</p>
<p>That number came out of session recordings and a funnel rebuilt by user rather than by session. It changed the question from "how do we make payment faster" to "how do we make returning cheap". Ten experiments later, across four EU markets, checkout conversion was up 11%.</p>

<div class="num"><div><b>38%</b><span>of converters left checkout and came back</span></div><div><b>10</b><span>experiments, each with a written hypothesis</span></div><div><b>+11%</b><span>checkout conversion, four markets</span></div><div><b>4</b><span>experiments that lost or were flat</span></div></div>

<h2>How the programme was run</h2>
<p>Every experiment had a one page hypothesis before anything was built: what we believed, what would change, the metric, the sample size, the date we would read it. No peeking. No calling winners at 80% confidence because the quarter was ending. The losers were as useful as the winners, because each one closed a door the team had been arguing about for a year.</p>

<h2>What moved the number</h2>
<ul>
<li><b>Re-entry.</b> A returning visitor lands on the step they left, with their choices intact and one line acknowledging it. The single largest lift.</li>
<li><b>Trust at the moment of commitment.</b> Cancellation terms and what happens after booking, shown where the decision is made, not in a tab.</li>
<li><b>Fewer fields, asked later.</b> Everything that could be asked after payment was moved after payment.</li>
<li><b>Price without surprises.</b> The total the user saw on the product page is the total at the end. Any change is explained before the button, not on the receipt.</li>
</ul>

<h2>What did not</h2>
<ul>
<li>A redesigned payment method selector. Flat. Payment was never the problem.</li>
<li>Urgency messaging on the last step. Slight negative on returns, and it felt wrong; killed.</li>
<li>A progress bar. Flat. People knew where they were; they did not know where their cart was.</li>
</ul>

<h2>The lesson I reuse on every funnel</h2>
<p>Instrument the gaps, not the stages. Most analytics setups count people at each step and lose them between steps: the back button, the tab switch, the return visit three hours later. The leak is almost always there, and it is invisible until you rebuild the funnel per user. I have found the same shape since in a co-living booking flow (+34% after the redesign) and in a B2B onboarding. Different products, same blind spot.</p>

<div class="box"><p>The full case with all ten experiments is here: <a href="/work/checkout.html">GetYourGuide checkout redesign</a>. If your funnel has a leak you cannot find: <a href="/cro-ecommerce-consultant/">how a CRO engagement runs</a>.</p></div>
"""),
}

def esc(s): return html.escape(s, quote=True)

def page(slug, d):
    url = f"https://inigoangulo.com/writing/{slug}/"
    ld = {"@context":"https://schema.org","@type":"Article","headline":d["title"],"description":d["desc"],"datePublished":d["date"],"dateModified":d["date"],"author":{"@type":"Person","@id":"https://inigoangulo.com/#person","name":"Inigo Angulo","url":"https://inigoangulo.com/"},"publisher":{"@type":"Person","name":"Inigo Angulo"},"mainEntityOfPage":url,"image":"https://inigoangulo.com/img/og.png"}
    bc = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inigo Angulo","item":"https://inigoangulo.com/"},{"@type":"ListItem","position":2,"name":"Writing","item":"https://inigoangulo.com/writing/"},{"@type":"ListItem","position":3,"name":d["title"],"item":url}]}
    nice = datetime.date.fromisoformat(d["date"]).strftime("%B %-d, %Y")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(d["title"])} / Inigo Angulo</title>
<meta name="description" content="{esc(d["desc"])}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<meta property="og:title" content="{esc(d["title"])}">
<meta property="og:description" content="{esc(d["desc"])}">
<meta property="og:image" content="https://inigoangulo.com/img/og.png">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
<link rel="stylesheet" href="/services/services.css">
<style>{CSS}</style>
{GA}
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(bc,ensure_ascii=False)}</script>
</head>
<body>
<header class="bar"><div class="bar__inner"><a class="bar__name" href="/">Inigo Angulo</a><nav class="bar__nav"><a class="bar__btn" href="/#work">Work</a><a class="bar__btn" href="/writing/">Writing</a><a class="bar__btn" href="/#about">About</a></nav><a class="bar__cta" href="https://cal.com/inigoangulo/30min">Book a call</a></div></header>
<main><article class="art">
<span class="k">Writing</span>
<h1>{esc(d["title"])}</h1>
<div class="meta"><span>Inigo Angulo</span><span>{nice}</span><span>{d["read"]} read</span></div>
{d["body"]}
<div class="cta"><h2>Working on something like this?</h2><p>Thirty minutes, no deck. <a href="https://cal.com/inigoangulo/30min">Book a call</a> or <a href="mailto:inigoangulo@gmail.com">email me</a>.</p></div>
</article></main>
<footer><div class="mx"><span>2026 Inigo Angulo, Zurich</span><span><a href="/writing/">All writing</a> &nbsp; <a href="https://www.linkedin.com/in/i%C3%B1igo-angulo-1ab25a134/" rel="noopener" target="_blank">LinkedIn</a> &nbsp; <a href="https://github.com/inigoangulo93" rel="noopener" target="_blank">GitHub</a></span></div></footer>
</body>
</html>
'''

def index():
    items = "".join(f'<a class="post" href="/writing/{s}/"><span class="k" style="margin-bottom:6px">{datetime.date.fromisoformat(d["date"]).strftime("%B %-d, %Y")} / {d["read"]}</span><h2>{esc(d["title"])}</h2><p>{esc(d["desc"])}</p></a>' for s,d in POSTS.items())
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Writing: product, AI agent teams, conversion / Inigo Angulo</title>
<meta name="description" content="Notes from building products with AI agent teams, running experiments on checkout funnels, and deciding what is worth building.">
<link rel="canonical" href="https://inigoangulo.com/writing/">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
{FONTS}
<link rel="stylesheet" href="/services/services.css">
<style>.list{{max-width:760px;margin:0 auto;padding:110px 24px 40px}}.post{{display:block;border:1px solid var(--b1);border-radius:12px;padding:22px 24px;margin-bottom:14px;background:var(--glass);transition:border-color .2s,transform .2s}}.post:hover{{border-color:var(--acb);transform:translateY(-2px)}}.post h2{{font-size:1.25rem;margin:0 0 8px}}.post p{{font-size:.95rem}}.post .k::before{{content:""}}</style>
{GA}
</head>
<body>
<header class="bar"><div class="bar__inner"><a class="bar__name" href="/">Inigo Angulo</a><nav class="bar__nav"><a class="bar__btn" href="/#work">Work</a><a class="bar__btn" href="/writing/">Writing</a><a class="bar__btn" href="/#about">About</a></nav><a class="bar__cta" href="https://cal.com/inigoangulo/30min">Book a call</a></div></header>
<main><div class="list"><span class="k">Writing</span><h1 style="font-size:2rem;margin-bottom:28px">What I learned shipping, written down.</h1>{items}</div></main>
<footer><div class="mx"><span>2026 Inigo Angulo, Zurich</span><span><a href="/">Home</a></span></div></footer>
</body>
</html>
'''

if __name__ == "__main__":
    os.makedirs("writing", exist_ok=True)
    open("writing/index.html","w").write(index())
    for s,d in POSTS.items():
        os.makedirs(f"writing/{s}", exist_ok=True)
        open(f"writing/{s}/index.html","w").write(page(s,d))
        print("built", s)
