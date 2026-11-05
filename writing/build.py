#!/usr/bin/env python3
"""Builds the articles under /writing/. Run from the repo root: python3 writing/build.py"""
import json, html, os, subprocess, datetime, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_posts import BUILD_POSTS
from kit import KIT, ORDER as KIT_ORDER, CAPS as KIT_CAPS, ARTICLE_TO_KIT
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'services'))
from chrome import header, mobmenu, FOOTER
VER = subprocess.run(["git","rev-parse","--short","HEAD"],capture_output=True,text=True).stdout.strip() or "0"

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
.art .fig{margin:26px 0;border:1px solid var(--b1);border-radius:12px;padding:16px;background:var(--glass)}.art .fig svg{width:100%;height:auto;display:block}.art figcaption{font-family:var(--m);font-size:.72rem;color:var(--t3);margin-top:10px}
.art .series{border:1px solid var(--b1);border-radius:12px;padding:16px 20px;margin:0 0 30px;background:var(--glass)}.art .series__k{font-family:var(--m);font-size:.66rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ac);display:block;margin-bottom:8px}.art .series ul{list-style:none;margin:0;display:grid;gap:6px}.art .series li{font-size:.92rem;margin:0}.art .series em{font-style:normal;font-family:var(--m);font-size:.68rem;color:var(--t3)}
.art .tag{font-family:var(--m);font-size:.7rem;color:var(--ac2);border:1px solid var(--acb);border-radius:999px;padding:3px 10px}
.art table{width:100%;border-collapse:collapse;margin:22px 0;font-size:.92rem;line-height:1.5}.art th,.art td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--b1)}.art th{font-family:var(--m);font-size:.68rem;letter-spacing:.08em;text-transform:uppercase;color:var(--t3);font-weight:500}.art td{color:var(--t2)}.art td:first-child{color:var(--t1)}
.art pre{background:#0b0b10;border:1px solid var(--b1);border-radius:12px;padding:18px 20px;margin:22px 0;overflow-x:auto;font-family:var(--m);font-size:.8rem;line-height:1.6;color:var(--t2)}.art pre code{font-family:inherit}
.art .faq{margin:40px 0 0}.art .faq h2{margin-bottom:6px}.art .faq details{border-bottom:1px solid var(--b1);padding:14px 0}.art .faq summary{cursor:pointer;font-weight:600;color:var(--t1);font-size:1.02rem;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:16px}.art .faq summary::-webkit-details-marker{display:none}.art .faq summary::after{content:'';flex:none;width:10px;height:10px;border-right:2px solid var(--ac2);border-bottom:2px solid var(--ac2);transform:rotate(45deg) translate(-2px,-2px);transition:transform .3s cubic-bezier(.16,1,.3,1)}.art .faq details[open] summary::after{transform:rotate(225deg) translate(-2px,-2px)}.art .faq p{margin:10px 0 0;font-size:.98rem;color:var(--t2)}.art .faq details[open] p{animation:faqIn .32s cubic-bezier(.16,1,.3,1) both}@keyframes faqIn{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}
@media(max-width:700px){.art table{display:block;overflow-x:auto;white-space:normal}}
.art .cta{margin-top:40px}
.art .cta h2{margin:0 0 6px}
'''

POSTS = {
"ai-agent-teams-software-development": dict(
  tag="agents", hub=True, title="AI agent teams for software development: what actually works in 2026",
  desc="How to run a team of AI coding agents that ships to production: roles with mandates, isolation, gates, a decision log, and the numbers from seven weeks of doing it.",
  meta='How to run a team of AI coding agents that ships to production: roles with mandates, isolation, gates, a decision log, and seven weeks of numbers.',
  date="2026-11-04", read="9 min",
  body="""
<p>Most of what is written about AI coding agents is either a demo or a warning. This is neither. It is the operating model I used to build and run a production platform with eight agents and no engineers on payroll: 445 merged pull requests, 1,456 CI runs and 15 gated releases in seven weeks. The model is not clever. It is a set of boring decisions about who may do what, and it is the reason the numbers are real instead of a story.</p>
<p>This is the hub of a series. Each section links to a deeper piece. If you want the method as steps to follow rather than the operating model, start with <a href="/writing/how-to-build-an-mvp-with-ai-agents/">how to build an MVP with AI agents</a>.</p>

<figure class="fig"><svg viewBox="0 0 720 300" role="img" aria-label="Diagram: a human writes tickets and takes decisions; a lead agent decomposes work to worker agents; a reviewer and a security agent gate the output; a human approves promotion to production">
<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#6b6b80"/></marker></defs>
<g font-family="JetBrains Mono,monospace" font-size="11" fill="#9a9aae">
<rect x="20" y="110" width="120" height="80" rx="8" fill="rgba(34,197,94,.08)" stroke="rgba(34,197,94,.55)"/><text x="80" y="140" text-anchor="middle" fill="#bbf7d0" font-weight="600">HUMAN</text><text x="80" y="158" text-anchor="middle">tickets</text><text x="80" y="173" text-anchor="middle">decisions</text>
<rect x="190" y="110" width="110" height="80" rx="8" fill="#101018" stroke="rgba(255,255,255,.2)"/><text x="245" y="140" text-anchor="middle" fill="#f4f4f6" font-weight="600">LEAD</text><text x="245" y="158" text-anchor="middle">decompose</text><text x="245" y="173" text-anchor="middle">integrate</text>
<rect x="350" y="30" width="110" height="46" rx="8" fill="#101018" stroke="rgba(255,255,255,.2)"/><text x="405" y="58" text-anchor="middle">frontend</text>
<rect x="350" y="92" width="110" height="46" rx="8" fill="#101018" stroke="rgba(255,255,255,.2)"/><text x="405" y="120" text-anchor="middle">backend</text>
<rect x="350" y="154" width="110" height="46" rx="8" fill="#101018" stroke="rgba(255,255,255,.2)"/><text x="405" y="182" text-anchor="middle">data</text>
<rect x="350" y="216" width="110" height="46" rx="8" fill="#101018" stroke="rgba(255,255,255,.2)"/><text x="405" y="244" text-anchor="middle">design</text>
<rect x="510" y="70" width="110" height="46" rx="8" fill="rgba(245,158,11,.06)" stroke="rgba(245,158,11,.5)"/><text x="565" y="98" text-anchor="middle" fill="#fcd34d">review</text>
<rect x="510" y="140" width="110" height="46" rx="8" fill="rgba(245,158,11,.06)" stroke="rgba(245,158,11,.5)"/><text x="565" y="168" text-anchor="middle" fill="#fcd34d">security</text>
<rect x="510" y="210" width="110" height="46" rx="8" fill="rgba(34,197,94,.08)" stroke="rgba(34,197,94,.55)"/><text x="565" y="232" text-anchor="middle" fill="#bbf7d0">approve</text><text x="565" y="247" text-anchor="middle">human</text>
<rect x="650" y="210" width="60" height="46" rx="8" fill="#101018" stroke="#2dd4bf"/><text x="680" y="238" text-anchor="middle" fill="#5eead4">PROD</text>
<g fill="none" stroke="#6b6b80" stroke-width="1.2" marker-end="url(#a)">
<path d="M140 150 L190 150"/><path d="M300 150 L325 150 L325 53 L350 53"/><path d="M300 150 L325 150 L325 115 L350 115"/><path d="M300 150 L325 150 L325 177 L350 177"/><path d="M300 150 L325 150 L325 239 L350 239"/>
<path d="M460 53 L485 53 L485 93 L510 93"/><path d="M460 115 L485 115 L485 93"/><path d="M460 177 L485 177 L485 93"/><path d="M460 239 L485 239 L485 93"/>
<path d="M565 116 L565 140"/><path d="M565 186 L565 210"/><path d="M620 233 L650 233"/>
</g>
<text x="20" y="285" font-size="10" fill="#6b6b80">green: a human decides / amber: an agent gates / nobody right of the lead holds production credentials</text>
</g></svg><figcaption>The shape of the team. The volume comes from the middle; the trust comes from the edges.</figcaption></figure>

<h2>1. Roles with mandates, not prompts</h2>
<p>Each agent has a file that says what it does, which files it may touch, and what it must never do. A lead that decomposes tickets and integrates. Workers for frontend, backend and data. A reviewer that returns a list of concrete faults, not opinions. A security agent that runs a full penetration test before every release. A design agent with the only write access to the design tool. A verifier that only reads and can only answer PASS, FAIL or UNVERIFIABLE from a script's output.</p>
<p>The mandate outlives the session. That is the difference between a team and a chat: a worker that receives an instruction mid task from anyone but the lead does not apply it, it returns it. That rule alone removed a class of failures where a stray instruction in a file or a log was treated as a command.</p>

<h2>2. Isolation before speed</h2>
<p>Every ticket gets a branch from an up to date main, never from another ticket's branch. Every worker gets its own worktree and, when it needs a database, its own local stack with its own ports. Two agents sharing one database reset each other and measure the neighbour's schema; I learned that on a day five of them did it at once.</p>
<p>No agent holds production credentials. Not read only, not "just for checking". Agents deploy to production through a workflow that holds the secrets; they never see them. The reasoning is simple: an agent with a production token can route around every other gate, so the token is the gate.</p>

<h2>3. Gates that mean something</h2>
<p>Five required checks before main accepts a merge: lint with house rules, strict types, the test suites, a check that auth templates are intact, and a secrets scan on every commit of the branch. Browser tests on every change that is not documentation. A penetration test with a written verdict before every promotion. Then one human approval.</p>
<p>The subtle part is what counts as proof. A skipped check reports as green. A test that documents a bug protects the bug. A deployment that says READY can serve a 404. I wrote the rules for that in <a href="/writing/green-check-is-not-proof/">Why a green check is not proof</a>, and the two human gates in <a href="/writing/human-in-the-loop-coding-agents/">Human in the loop for coding agents</a>.</p>

<h2>4. A decision log with ids</h2>
<p>Agents hit decisions constantly: a name, a boundary, a trade off. Every one becomes a numbered item with lettered options and a recommendation, and I answer with an id and a letter. The answer is written into the repository with the reasoning and the alternatives. Over seven weeks that is more than 140 decisions, and it is why a fresh session can continue the work without re-arguing it. Configuration, naming, test structure and git conflicts never reach me; those are the lead's.</p>

<h2>5. Facts come from scripts</h2>
<p>No agent declares an external fact. "CI is green", "the preview works", "the migration is safe" are not sentences in this system. A script produces JSON with the run id, the commit, the deployment id or the URL, and the agent interprets it. If the script says FAIL, no amount of text turns it into PASS. This sounds pedantic until you have watched a fluent, confident summary describe a deployment that never happened.</p>

<h2>What it produced</h2>
<div class="num"><div><b>17 days</b><span>first commit to first production release</span></div><div><b>445</b><span>pull requests merged, 38 closed unmerged</span></div><div><b>147</b><span>red CI runs: the gates working</span></div><div><b>15</b><span>numbered releases with a security report</span></div></div>
<p>The full story with the evidence read from the GitHub API is in <a href="/writing/one-person-ai-agent-team-445-prs/">445 PRs in seven weeks</a>, and the product itself in the <a href="/work/acervo.html">Acervo case study</a>.</p>

<h2>What it costs, and what it does not replace</h2>
<p>The agent bill was a few hundred francs a month. The expensive part was still judgment: what the product should be, which invariants live in the database, what counts as done. Agents made execution cheap enough that the gates where a human looks became the product. If you take one thing from this: do not start with the agents. Start with the rules for what counts as proof, then let the agents be fast inside them.</p>

<div class="box"><p>Next in the series: <a href="/writing/human-in-the-loop-coding-agents/">Human in the loop for coding agents: the two gates that matter</a>. If you want this set up inside your company: <a href="/ai-product-builder/">AI build and deployment</a>.</p></div>
"""),
"human-in-the-loop-coding-agents": dict(
  tag="agents", title="Human in the loop for coding agents: the two gates that matter",
  desc="Where a person must sit when AI agents write and ship code: the decision gate (one id, one letter) and the release gate (one approval with a security report). Everything else can be automated.",
  meta='Where a person must sit when AI agents write and ship code: the decision gate and the release gate. Everything else can be automated.',
  date="2026-11-04", read="7 min",
  body="""
<p>"Human in the loop" usually means a person watching a stream of output and clicking approve until they stop reading. That is not a gate, it is a ritual. After seven weeks of running an AI engineering team to production, I ended up with exactly two places where a human must act, and a rule for keeping both cheap enough that they are actually used.</p>

<figure class="fig"><svg viewBox="0 0 730 220" role="img" aria-label="Diagram: a ticket flows through build and automated checks; two human gates sit at decision and at release; between them everything is automated">
<defs><marker id="b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#6b6b80"/></marker></defs>
<g font-family="JetBrains Mono,monospace" font-size="11" fill="#9a9aae">
<rect x="20" y="80" width="90" height="56" rx="8" fill="#101018" stroke="rgba(255,255,255,.2)"/><text x="65" y="113" text-anchor="middle">ticket</text>
<rect x="150" y="80" width="110" height="56" rx="8" fill="rgba(34,197,94,.08)" stroke="rgba(34,197,94,.6)"/><text x="205" y="103" text-anchor="middle" fill="#bbf7d0" font-weight="600">GATE 1</text><text x="205" y="121" text-anchor="middle">decision</text>
<rect x="300" y="80" width="90" height="56" rx="8" fill="#101018" stroke="rgba(255,255,255,.2)"/><text x="345" y="113" text-anchor="middle">build</text>
<rect x="420" y="80" width="90" height="56" rx="8" fill="rgba(245,158,11,.06)" stroke="rgba(245,158,11,.5)"/><text x="465" y="106" text-anchor="middle" fill="#fcd34d">checks</text><text x="465" y="122" text-anchor="middle" fill="#fcd34d">pen test</text>
<rect x="550" y="80" width="110" height="56" rx="8" fill="rgba(34,197,94,.08)" stroke="rgba(34,197,94,.6)"/><text x="605" y="103" text-anchor="middle" fill="#bbf7d0" font-weight="600">GATE 2</text><text x="605" y="121" text-anchor="middle">release</text>
<g fill="none" stroke="#6b6b80" stroke-width="1.2" marker-end="url(#b)"><path d="M110 108 L150 108"/><path d="M260 108 L300 108"/><path d="M390 108 L420 108"/><path d="M510 108 L550 108"/><path d="M660 108 L690 108"/></g>
<text x="693" y="112" fill="#5eead4" font-size="11">prod</text>
<path d="M300 160 L510 160" stroke="rgba(255,255,255,.18)" stroke-dasharray="3 3"/><text x="405" y="182" text-anchor="middle" font-size="10" fill="#6b6b80">automated, read by scripts, never declared</text>
<text x="205" y="60" text-anchor="middle" font-size="10" fill="#6b6b80">one id, one letter</text><text x="605" y="60" text-anchor="middle" font-size="10" fill="#6b6b80">one approval, one report</text>
</g></svg><figcaption>Two gates. Both answered in seconds, both logged, neither skippable.</figcaption></figure>

<h2>Gate 1: the decision</h2>
<p>Agents stop when they hit a question that changes the product: a boundary, a trade off, a scope. They do not guess. The lead writes the question in a fixed format: a one line question, lettered options, a recommendation with the reason, and what happens if nobody answers. I reply with the id and the letter. "014-3 B". Nothing else.</p>
<p>Three things make this a real gate. The format is fixed, so I can answer twenty in ten minutes. The answer is recorded in the repository with the reasoning, so it is never re-asked. And the list of what gets escalated is closed: architecture, data model, security, destructive migrations, new infrastructure, scope, irreversible operations, large behaviour changes. Names, configuration, test structure and git conflicts never reach me. If they did, I would stop reading, and the gate would become the ritual I described above.</p>

<h2>Gate 2: the release</h2>
<p>Code reaches main through automated checks and an agent review. It reaches production through one human command, and only when three things are true for the exact commit being promoted: all required checks are green on that commit (not an earlier one), the security agent's penetration test says PASS for that commit, and the pre-promotion queries about data compatibility have been run. The approval is logged with who and when. The person approving cannot be the agent that built it, by construction: no agent holds the credentials the workflow uses.</p>
<p>On October 15 the pen test came back FAIL on a rule unrelated to the feature being promoted. The gate held. The feature shipped behind a flag and the rule was fixed first. That is what the gate is for: not to review every line, but to make "no" cheap at the one moment where "yes" is irreversible.</p>

<h2>What is not a human gate</h2>
<ul>
<li><b>Reading every pull request.</b> At 445 merges in seven weeks, nobody does. The reviewer agent returns concrete faults; the automated checks are the floor. I read the ones the lead flags and the ones that touch security.</li>
<li><b>Watching the agents work.</b> They work in tramos: write a file, check, write the next. A silent ten minute run is killed, not supervised.</li>
<li><b>Declaring facts.</b> Whether a deployment is live is read from a script with the deployment id, not from a person looking at a page and saying so. The human gates decide; they do not verify. Verification belongs to scripts, and the rules for it are in <a href="/writing/green-check-is-not-proof/">Why a green check is not proof</a>.</li>
</ul>

<h2>Why two and not five</h2>
<p>Every gate you add has a cost that compounds: the agents wait, the human skims, and skimming is worse than absence because it looks like review. Two gates, both with a fixed format and a closed list of triggers, survived seven weeks and 15 releases without being skipped once. Five would have been skipped by week two.</p>

<div class="box"><p>This is part of a series on running AI agent teams. The hub: <a href="/writing/ai-agent-teams-software-development/">AI agent teams for software development</a>. The numbers: <a href="/writing/one-person-ai-agent-team-445-prs/">445 PRs in seven weeks</a>. The product: <a href="/work/acervo.html">Acervo</a>. If you want the gates set up in your team: <a href="/ai-product-builder/">AI build and deployment</a>.</p></div>
"""),
"one-person-ai-agent-team-445-prs": dict(
  tag="agents", title="445 PRs in seven weeks: what a one person team with AI agents actually looks like",
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

<div class="box"><p>This post is part of a series: the hub is <a href="/writing/ai-agent-teams-software-development/">AI agent teams for software development</a>, and the gates are in <a href="/writing/human-in-the-loop-coding-agents/">Human in the loop for coding agents</a>. The full case, with the evidence from the GitHub API, the data model, the promotion flow and the day the security gate said no: <a href="/work/acervo.html">Acervo, the case study</a>. If you want this for your company: <a href="/ai-product-builder/">AI build and deployment</a>.</p></div>
"""),
"green-check-is-not-proof": dict(
  tag="agents", title="Why a green check is not proof: the gates between an AI agent and production",
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

<div class="box"><p>Part of a series: <a href="/writing/ai-agent-teams-software-development/">AI agent teams for software development</a> and <a href="/writing/human-in-the-loop-coding-agents/">the two human gates</a>. The failure story, beat by beat, with the run ids, is in the <a href="/work/acervo.html#s10">Trust chapter of the Acervo case</a>. If your team is introducing agents and wants the guardrails with them: <a href="/ai-product-builder/">how I set that up</a>.</p></div>
"""),
"checkout-conversion-ten-experiments": dict(
  tag="conversion", title="Checkout conversion: the ten experiments behind +11%",
  desc="At GetYourGuide, 38% of converters left checkout and came back with no re-entry experience. Ten experiments, four EU markets, +11% conversion, and the ones that lost.",
  meta='38% of converters left checkout and came back to no memory of their cart. Ten experiments across four EU markets, +11% conversion, and the ones that lost.',
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
"row-level-security-tests-ai-agents": dict(
  title="Row level security with AI agents: tests that run as the user who must not get in",
  desc="How to keep multi tenant isolation honest when agents write the migrations: every rule lives in the database, every policy has a test that runs as the wrong user, and the reviewer breaks a policy on purpose.",
  meta='Keeping multi tenant isolation honest when agents write migrations: rules in the database, a test per policy run as the wrong user, policies broken on purpose.',
  date="2026-11-04", read="7 min", tag="agents",
  body="""
<p>When AI agents write your database migrations, the risk is not that they forget row level security. They are diligent; they add the policy. The risk is that the policy looks right, the test is green, and the test never actually tried to cross the tenant boundary. On Acervo, a platform where each car collection is a tenant and the data is someone's private property, that failure mode was the one I designed against first.</p>

<h2>The rule: every invariant has a home and a test</h2>
<p>Every rule in the domain model is tagged with where it lives: in the database (a constraint, a policy, a trigger) or in the application (a server action). Nothing lives only in the frontend. Hiding a column in the interface is not a guarantee, and an agent will happily "fix" a permissions bug by hiding a button.</p>
<p>Every table has RLS enabled before it has data, and every policy has a test that runs <em>as the role that must not pass</em>. The suite is written in pgTAP and sets the JWT claims and the role to a user from another collection, then asserts zero rows. Not "the right user sees their rows": that test passes with RLS switched off. The test that matters is the negative one.</p>

<figure class="fig"><svg viewBox="0 0 720 200" role="img" aria-label="Diagram: a test sets the role to a user from collection B and queries collection A's table; the expected answer is zero rows; a second test breaks the policy on purpose and expects the suite to go red">
<g font-family="JetBrains Mono,monospace" font-size="11" fill="#9a9aae">
<rect x="20" y="40" width="200" height="110" rx="8" fill="#101018" stroke="rgba(255,255,255,.2)"/><text x="120" y="66" text-anchor="middle" fill="#f4f4f6" font-weight="600">test, as user of B</text><text x="120" y="90" text-anchor="middle">set role, set jwt claims</text><text x="120" y="108" text-anchor="middle">select * from A.cars</text><text x="120" y="132" text-anchor="middle" fill="#bbf7d0">expect 0 rows</text>
<rect x="260" y="40" width="200" height="110" rx="8" fill="#101018" stroke="rgba(255,255,255,.2)"/><text x="360" y="66" text-anchor="middle" fill="#f4f4f6" font-weight="600">reviewer, on purpose</text><text x="360" y="90" text-anchor="middle">drop one isolation policy</text><text x="360" y="108" text-anchor="middle">run the suite</text><text x="360" y="132" text-anchor="middle" fill="#fca5a5">expect red</text>
<rect x="500" y="40" width="200" height="110" rx="8" fill="rgba(239,68,68,.06)" stroke="rgba(239,68,68,.5)"/><text x="600" y="66" text-anchor="middle" fill="#fca5a5" font-weight="600">still green?</text><text x="600" y="90" text-anchor="middle">the tests do not test</text><text x="600" y="108" text-anchor="middle">what they claim</text><text x="600" y="132" text-anchor="middle" fill="#fca5a5">PR blocked</text>
</g></svg><figcaption>Two tests per policy: one as the wrong user, one that proves the first can fail.</figcaption></figure>

<h2>Break a policy on purpose</h2>
<p>A negative test can still lie. If the test's setup is wrong, the user it impersonates is a member of nothing, and zero rows comes back for a reason that has nothing to do with the policy. So the rule for reviewing any change to security is: the reviewer deletes one isolation policy, runs the suite, and confirms it goes red. If it stays green, the pull request is blocked, whatever else it does. It is the cheapest proof I know that a suite tests what it says.</p>
<p>It caught a real one. Five new triggers written to run with the caller's privileges put an existing test in red for the wrong reason: at a lower auth level the user was a member of nothing, RLS hid the row, and the coherence check concluded "not your tenant" on perfectly coherent data, masking the real denial. The fix was not to adjust the expectation. It was to recognise that a coherence invariant is a property of the data, not of the observer, run it with definer rights, and let RLS do the denying with the right message.</p>

<h2>Three habits that keep it true over 99 migrations</h2>
<ul>
<li><b>Functions carry a pinned search path.</b> Every security function sets it explicitly. A function that resolves names from the caller's path is an injection surface, and an agent will not think of that unless the rule is written down.</li>
<li><b>Foreign keys that cross tenants are a leak and a lever.</b> A reference from one collection's row to another collection's rule does not only let the wrong person read; it can occupy a unique slot the other tenant needed, with an error their own RLS will not let them understand. Every cross table reference gets a check that both sides belong to the same collection.</li>
<li><b>Suites that share a database do not share state.</b> Each starts from its own reset. A security test red because of rows another suite left behind gets read as a regression and chased where it is not.</li>
</ul>

<h2>Pending users read zero rows, by the database</h2>
<p>Registration is open; access is not. A new account is pending until a person approves it, and pending means zero rows from any table, guaranteed by RLS, with a test that proves it, never by the interface. Who approved whom, and when, goes to the audit log. This is the pattern for anything an agent might be tempted to enforce in a component: if it must be true, it is true in the database, and there is a test that runs as the person it must be true against.</p>

<div class="box"><p>Part of the series on running AI agent teams: the hub is <a href="/writing/ai-agent-teams-software-development/">AI agent teams for software development</a>, the verification rules are in <a href="/writing/green-check-is-not-proof/">Why a green check is not proof</a>, and the data model is in the <a href="/work/acervo.html#s08">Acervo case, chapter 08</a>. If you want this discipline in your own build: <a href="/ai-product-builder/">AI build and deployment</a>.</p></div>
"""),
"cost-to-build-mvp-with-ai-agents": dict(
  title="How much does it cost to build an MVP with AI agents? Real numbers from one build",
  desc="What a production MVP built with an AI agent team actually costs: the agent bill, the infrastructure, the human time, and where the money really goes. Numbers from seven weeks on Acervo.",
  meta='What a production MVP built with an AI agent team really costs: agent usage, infrastructure, human time, and where the money actually goes.',
  date="2026-11-04", read="6 min", tag="product",
  body="""
<p>Everyone asks the same question in the first call: what does it cost? Here is what one build cost, with the caveat that it was a build I ran end to end for one client, so the human time was mine and the decisions were fast. Treat the numbers as an honest floor, not a quote. The method that produced them is in <a href="/writing/how-to-build-an-mvp-with-ai-agents/">how to build an MVP with AI agents</a>.</p>

<div class="num"><div><b>7 weeks</b><span>from first commit to 15 releases in production</span></div><div><b>~CHF 300</b><span>per month in agent usage, passed through at cost</span></div><div><b>~CHF 60</b><span>per month in hosting, database and monitoring at MVP scale</span></div><div><b>1 person</b><span>scoping, deciding, approving. Zero engineers on payroll</span></div></div>

<h2>Where the money does not go</h2>
<p>Not to writing code. That is the part that collapsed. 445 pull requests in seven weeks with an agent bill in the low hundreds of francs a month. Infrastructure at MVP scale is a rounding error: a hosted Postgres with auth and storage, a frontend host, error tracking. All on plans that cost less than a lunch in Zurich.</p>

<h2>Where it goes</h2>
<ol>
<li><b>Scoping.</b> Week one was spent on what the product must do, what it must never do, the data model and the security boundaries, written as tickets with acceptance criteria. This is the week that decides whether the following six produce a product or a pile of features. It is human time, and it is the most expensive line.</li>
<li><b>Deciding.</b> Agents stop at every real decision and ask. Over seven weeks that was more than 170 recorded decisions, each answered in seconds because the format is fixed, but each requiring someone who knows what the product is for. You cannot outsource this to the agents without getting their guess.</li>
<li><b>Verification.</b> Reading what the gates say instead of trusting their colour, opening the deployment by URL, running the pen test before every release. This is what separates a demo from something you can put a customer on. It is a fixed cost per release, which is why the releases are batched into numbered sets instead of shipped one by one.</li>
<li><b>Design.</b> A brand, a token system, 26 components. Agents built the components from the tokens; the taste and the decisions were human. Skipping this is how MVPs end up looking like every other agent built app, which customers notice.</li>
</ol>

<h2>How to read a quote</h2>
<p>When I quote a build for a client, the first version is a fixed price for a sprint of two to six weeks, with the agent costs passed through at cost. What varies the price is almost entirely scope clarity: a client who can say what the product must never do saves a week. A client who wants to find out by building pays for the finding out, which is a legitimate thing to pay for, but it should be called that.</p>
<p>What should make you suspicious: a quote that is mostly "development hours". If the building is being done by agents, the hours that matter are scoping, deciding and verifying, and an honest quote says so.</p>

<h2>What you get for it</h2>
<p>Real code in a repository you own, with tests, a release process and a decision log, that any engineer can continue. Not a prototype on a no code platform and not a chat transcript. The <a href="/work/acervo.html">Acervo case</a> shows the artefacts: the data model, the promotion flow, the evidence from the CI record.</p>

<div class="box"><p>How the build is run: <a href="/writing/ai-agent-teams-software-development/">AI agent teams for software development</a>. The human gates that make it safe: <a href="/writing/human-in-the-loop-coding-agents/">Human in the loop for coding agents</a>. To talk about yours: <a href="/ai-product-builder/">AI build and deployment</a>.</p></div>
"""),
"fractional-product-manager-vs-product-consultant": dict(
  title="Fractional product manager vs product consultant: which one do you actually need?",
  desc="A consultant diagnoses and recommends. A fractional product manager owns outcomes inside your team for a period. How to tell which one your company needs, and what each should cost you.",
  meta='A consultant diagnoses and recommends; a fractional product manager owns outcomes inside your team. How to tell which one you need, and what each costs.',
  date="2026-11-04", read="5 min", tag="product",
  body="""
<p>The two titles get used interchangeably, and companies hire the wrong one all the time: a consultant when they needed someone to own the roadmap, a fractional lead when they needed a second opinion. The difference is not seniority or price. It is who owns the outcome.</p>

<h2>The consultant</h2>
<p>Comes in with a question, leaves with an answer. Audits the funnel, reviews the roadmap, runs the workshop, writes the recommendation. Owns the quality of the diagnosis; does not own what happens next. Right when you have a specific question, a team that can execute, and a decision maker who will act on the answer. Wrong when the answer is "you need someone to run this", because the consultant is already gone.</p>

<h2>The fractional product manager</h2>
<p>Sits inside the team for two or three days a week over months, owns the roadmap and the outcomes, makes the daily calls, and is judged on whether the number moved. Right when the founder is still the product manager and it has stopped scaling, when you are between hires, or when the product function does not exist yet and someone has to build it. Wrong when what you need is a deck for the board, or when nobody on your side will own the product after they leave.</p>

<h2>Four questions that settle it</h2>
<ol>
<li><b>Is there a decision maker who will act on a recommendation?</b> If yes, a consultant works. If the recommendation would land on nobody's desk, you need the fractional lead.</li>
<li><b>Is the problem known?</b> "Checkout converts badly" is a consultant's problem. "We do not know what to build next quarter" is a fractional lead's.</li>
<li><b>How long until the next hire?</b> If a full time product lead starts in two months, a consultant bridges. If the search has not started, the fractional lead is the bridge and often helps run the search.</li>
<li><b>Who executes?</b> A consultant assumes your team ships. If your team is two engineers and no designer, the fractional lead needs to be able to do, not just direct.</li>
</ol>

<h2>What each should cost</h2>
<p>A consulting engagement is priced per deliverable: an audit, a plan, a workshop series. A fractional engagement is priced per days per week, with a minimum term of three months, because owning an outcome in less than that is theatre. Both should come with a first call where the person tells you honestly which one you need, including when it is neither.</p>

<h2>Where I sit</h2>
<p>I do both, and I say which one I think you need on the first call. The thing I bring that is less common is that I also build: on Acervo I shipped with AI agent teams, so an engagement with me can include working software, not only a roadmap. The details are on <a href="/product-consultant-zurich/">Product consultant, Zurich</a> and <a href="/ai-product-builder/">AI build and deployment</a>.</p>

<div class="box"><p>Related: <a href="/writing/checkout-conversion-ten-experiments/">the ten checkout experiments</a>, which is the consultant kind of work, and <a href="/writing/one-person-ai-agent-team-445-prs/">445 PRs in seven weeks</a>, which is the building kind.</p></div>
"""),
"figma-design-system-that-mirrors-code": dict(
  title="A Figma design system that mirrors the codebase: tokens first, then components, then screens",
  desc="How to build a design system so that Figma and code say the same thing: a single token source exported to CSS by script, a component library that consumes it, and checks that fail when a raw value sneaks in.",
  meta='A design system where Figma and code say the same thing: one token source exported to CSS by script, components that consume it, and checks against raw values.',
  date="2026-11-04", read="7 min", tag="design",
  body="""
<p>Most design systems die the same way: Figma says 44 and the code says 42, and nobody notices until someone builds on top of the wrong one. On Acervo, where the code is written by agents at speed, that drift would have been fatal within a week. So the system was set up to make drift expensive to introduce and cheap to catch.</p>

<figure class="fig"><svg viewBox="0 0 720 150" role="img" aria-label="Diagram: tokens file feeds a components library which feeds screens; a script exports tokens to CSS; lint checks fail on raw values">
<defs><marker id="c" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#6b6b80"/></marker></defs>
<g font-family="JetBrains Mono,monospace" font-size="11" fill="#9a9aae">
<rect x="20" y="40" width="130" height="56" rx="8" fill="#101018" stroke="#2dd4bf"/><text x="85" y="64" text-anchor="middle" fill="#5eead4" font-weight="600">Tokens</text><text x="85" y="82" text-anchor="middle">the source</text>
<rect x="200" y="40" width="140" height="56" rx="8" fill="#101018" stroke="rgba(255,255,255,.2)"/><text x="270" y="64" text-anchor="middle" fill="#f4f4f6" font-weight="600">Components</text><text x="270" y="82" text-anchor="middle">consumes tokens</text>
<rect x="390" y="40" width="130" height="56" rx="8" fill="#101018" stroke="rgba(255,255,255,.2)"/><text x="455" y="64" text-anchor="middle" fill="#f4f4f6" font-weight="600">Screens</text><text x="455" y="82" text-anchor="middle">consume components</text>
<rect x="570" y="40" width="130" height="56" rx="8" fill="rgba(245,158,11,.06)" stroke="rgba(245,158,11,.5)"/><text x="635" y="64" text-anchor="middle" fill="#fcd34d" font-weight="600">tokens.css</text><text x="635" y="82" text-anchor="middle">by script, checked</text>
<g fill="none" stroke="#6b6b80" stroke-width="1.2" marker-end="url(#c)"><path d="M150 68 L200 68"/><path d="M340 68 L390 68"/><path d="M85 96 L85 125 L635 125 L635 96"/></g>
<text x="360" y="140" text-anchor="middle" font-size="10" fill="#6b6b80">no layer redefines a value from the layer above; no raw value survives lint</text>
</g></svg><figcaption>Three files, one direction. The code reads from the top of the chain, not from a screenshot.</figcaption></figure>

<h2>One source, three files, one direction</h2>
<p>Tokens is the source: colour, type, spacing, radii, shadows. Components consumes Tokens and publishes the library. Screens consume Components. No file skips a link, and no layer redefines a value from above. When the library was started from a kit, the kit's six colour collections were kept only as a translation table: every variable resolves to a token within two hops, with no literals and no dead ends, and that is measured by a script, not by looking.</p>

<h2>The code reads tokens by script</h2>
<p>A script exports the token file to CSS variables and writes the token version it exported from into the header of the CSS. Lint runs the same script in check mode: if the exported CSS does not match the current tokens, the build is red. A second check fails on any raw value in a component (a hex, a pixel size that is not a token), and a third measures contrast on the rendered page, not on declared pairs, because a utility that merges class names once dropped a colour silently and the primary button rendered ink on ink while every declared pair passed.</p>

<h2>Figma traps that only show in numbers</h2>
<p>Everything that went wrong in Figma shared one shape: the component looked right and what rendered was wrong. Fixing a master does not fix instances that were resized by hand; after correcting two components, 192 instances were still off size and pointed at the right master. Cloning a variant drops the property bindings of its layers, so the instance holds the right text and nothing displays it. Binding a colour variable to a paint built in black keeps the literal black. None of these are visible in a screenshot. All are visible by reading a number, so the design agent's mandate is: measure before, change, measure after, and report with node ids.</p>

<h2>Who owns the library</h2>
<p>A design agent, continuously, with one limit: it corrects, it does not design. If a value can be pointed at (the code, a verified screen), the agent applies it. If a value would have to be invented, it is escalated as a decision with a measurement and a recommendation. That line kept the library honest when a component was built at 56 pixels "because it felt like garage mode" and nobody could say where the 56 came from. The ticket said 44.</p>

<h2>What it bought</h2>
<p>Twenty six components in the library, every screen built from them, a light and a dark mode from the same tokens, and a brand that an agent cannot drift from by accident. More in the <a href="/work/acervo.html#s04">brand chapter of the Acervo case</a>, and the service is <a href="/ux-design-consultant/">UX and product design consulting</a>.</p>

<div class="box"><p>Part of the series: <a href="/writing/ai-agent-teams-software-development/">AI agent teams for software development</a>. The checks that make "green" mean something: <a href="/writing/green-check-is-not-proof/">Why a green check is not proof</a>.</p></div>
"""),
"instrument-the-gaps-not-the-stages": dict(
  title="Instrument the gaps, not the stages: funnel analytics that find the real leak",
  desc="Stage by stage funnels hide where people actually drop: the back button, the tab switch, the return visit. How to rebuild a funnel per user and find the leak nobody measured.",
  meta='Stage funnels hide where people drop: the back button, the tab switch, the return visit. How to rebuild the funnel per user and find the leak.',
  date="2026-11-04", read="6 min", tag="conversion",
  body="""
<p>Every analytics setup I have inherited counts people at each step of the funnel. Product page, cart, checkout step one, payment, confirmation. The numbers are right and the picture is wrong, because the leak is almost never inside a stage. It is between stages, in the moments the stage counters cannot see.</p>

<h2>What stage counters miss</h2>
<ul>
<li><b>The back button.</b> A user reaches checkout, goes back to compare, returns. Two checkout entries, one person, and a stage funnel counts a drop that did not happen and misses the friction that did.</li>
<li><b>The tab switch.</b> Opens the price in a new tab, opens the competitor, comes back forty minutes later. Session timed out; a new session starts at step one.</li>
<li><b>The return visit.</b> Comes back the next day with no memory of the cart. At GetYourGuide this was the number that changed everything: 38% of the people who eventually converted had left checkout and come back, and the product treated them like strangers.</li>
</ul>

<h2>Rebuild the funnel per user</h2>
<p>The fix is a query, not a tool. Take every user who reached the final step in a period, and walk their events backwards: how many checkout entries, how many hours between the first and the last, which step they left from each time. Then do the same for users who did not convert. The gap between the two populations is your leak, and it is usually not a step. It is a re-entry with no memory, a price that changed between visits, a form that cleared.</p>
<p>Three dimensions make the query useful: <em>entries per converter</em> (if the median is above one, re-entry is your biggest surface), <em>time to convert</em> (if it is hours, the session model is lying to you), and <em>exit step on the first visit</em> (which tells you where to put the memory).</p>

<h2>Then instrument what you found</h2>
<p>Only now add events, and add them for the gaps: a <code>checkout_reentry</code> event with the step and the hours since last exit, a <code>cart_restored</code> event, a <code>price_changed_since_last_visit</code> event. These are the events that will tell you whether the fix worked, and they are the ones no default setup ships with.</p>

<h2>What this looked like twice</h2>
<p>At GetYourGuide it became ten experiments and +11% checkout conversion, with the single largest lift from re-entry: a returning visitor lands on the step they left, with their choices intact. At a co-living platform the same query found the drop between application and booking was people returning after the roommate conversation, and the redesign took booking conversion up 34%. Different products, same blind spot. The <a href="/writing/checkout-conversion-ten-experiments/">ten experiments</a> are written up separately.</p>

<h2>A note on tools</h2>
<p>Any analytics product can do this if it exports raw events; most cannot do it in their funnel UI, which is why the funnel UI keeps telling you payment is the problem. Session recordings are the fastest way to see a re-entry with your own eyes; the per user query is how you know how many there are.</p>

<div class="box"><p>If your funnel has a leak you cannot find: <a href="/cro-ecommerce-consultant/">how a CRO engagement runs</a>. The case: <a href="/work/checkout.html">GetYourGuide checkout redesign</a>.</p></div>
"""),
"ticket-to-production-in-five-hours": dict(
  title="From ticket to production in five hours: a release process for a one person team",
  desc="One real change, end to end: ticket at 14:35, pull request at 16:56, fourteen checks, pen test PASS, merge, promotion at 19:50, served at 19:54. The process that makes that routine and safe.",
  meta='One real change end to end: ticket at 14:35, fourteen checks, pen test PASS, served at 19:54. The process that makes that routine and safe.',
  date="2026-11-04", read="6 min", tag="agents",
  body="""
<p>Here is one change on Acervo, as recorded by the ticket, the pull request, the CI run and the deployment. Not a highlight: a Tuesday.</p>

<ol class="steps">
<li><div><b>14:35, ticket written</b><span>A numbered ticket with a measurable acceptance criterion and valid metadata. Without both, the lead returns it before starting.</span></div></li>
<li><div><b>Branch from main</b><span>One branch per ticket, from an up to date main, never from another ticket's branch. The worker gets its own worktree and database.</span></div></li>
<li><div><b>16:56, pull request opened</b><span>By the lead, after integrating the worker's output and the reviewer's list of faults. The PR carries screenshots and the preview URL with its commit.</span></div></li>
<li><div><b>Fourteen checks</b><span>Five required by the branch ruleset (lint, types, tests, auth templates, secrets) plus the browser suite and the house checks. All read on the exact commit to be merged, not an earlier one.</span></div></li>
<li><div><b>17:20, pen test PASS</b><span>The security agent runs the full test against local and staging and writes a report with a verdict for that commit.</span></div></li>
<li><div><b>Merge</b><span>The lead merges, only with every required check green on that commit. It does not merge on anyone's say so, including mine.</span></div></li>
<li><div><b>19:50, promotion</b><span>A human command names the commit. The workflow holds the credentials; no person and no agent does. Migrations run before the deploy and are compatible with the previous code by rule: add first, remove in a later release.</span></div></li>
<li><div><b>19:54, served</b><span>The final check fetches the production domain and looks for the content. A deployment that reports READY can serve a 404; the first promotion did exactly that, so the check reads the page, not the status.</span></div></li>
</ol>

<h2>Why it is five hours and not five minutes</h2>
<p>Because three of the steps are human and two are slow on purpose. The ticket takes thought. The merge waits for every check on the exact commit. The promotion waits for a security report. Everything between those points is agents and scripts, and that is where the hours went from days to minutes. The human gates did not get faster; they got cheaper, which is what lets them stay.</p>

<h2>Why it is routine</h2>
<p>Because nothing in it depends on memory. The ticket has a schema. The decision format is fixed. The checks are the same fourteen. The promotion is one command with one input. A process that depends on someone remembering a step is a process that skips the step on the day it matters, and with agents producing 445 merges in seven weeks, that day comes weekly.</p>

<h2>What I would copy first</h2>
<ul>
<li>Read checks on the commit you are merging. Not the branch, the commit.</li>
<li>Make the final deployment check fetch the real page by its domain.</li>
<li>Migrations compatible with the previous version, always. A deploy that fails after migrating must not break what is running.</li>
<li>One human command for production, logged, with the secrets in the workflow and nowhere else.</li>
</ul>

<div class="box"><p>The whole promotion flow with its lanes is in the <a href="/work/acervo.html#s06">Acervo case, chapter 06</a>. The series: <a href="/writing/ai-agent-teams-software-development/">AI agent teams for software development</a> and <a href="/writing/human-in-the-loop-coding-agents/">the two human gates</a>. To set this up for your team: <a href="/ai-product-builder/">AI build and deployment</a>.</p></div>
"""),

}

POSTS.update(BUILD_POSTS)
TAGS = {"build":"Building with AI agents","agents":"AI agent teams","conversion":"Conversion and funnels","design":"Design systems","product":"Product and consulting"}

def esc(s): return html.escape(s, quote=True)

def series_box(slug, d):
    tag = d.get("tag")
    others = [(k,v) for k,v in POSTS.items() if v.get("tag")==tag and k!=slug]
    if not others: return ""
    hub = [(k,v) for k,v in others if v.get("hub")]
    rest = [(k,v) for k,v in others if not v.get("hub")]
    items = "".join(f'<li><a href="/writing/{k}/">{esc(v["title"])}</a>{" <em>(start here)</em>" if v.get("hub") else ""}</li>' for k,v in hub+rest)
    return f'<nav class="series" aria-label="In this series"><span class="series__k">In this series: {esc(TAGS[tag])}</span><ul>{items}</ul></nav>'


CTA = {
  "build":      ("Working on something like this?", "This is how I build products with AI agent teams, from scope to production.", "/ai-product-builder/", "Discuss a product idea"),
  "agents":     ("Working on something like this?", "This is the method behind how I build: AI native development with human gates.", "/ai-product-builder/", "Discuss a product idea"),
  "product":    ("Working on a product decision like this?", "Discovery, direction and ownership of outcomes is the core of how I lead product work.", "/product-consultant-zurich/", "Explore a product challenge"),
  "design":     ("Working on a design problem like this?", "Research, flows, interface and design systems are the hands-on part of my work.", "/ux-design-consultant/", "Discuss a design problem"),
  "conversion": ("Working on a funnel like this?", "Finding the leak and proving the fix is what the conversion work looks like.", "/cro-ecommerce-consultant/", "Explore a conversion opportunity"),
}
def cta_block(d):
    h, p, href, label = CTA.get(d.get("tag",""), CTA["build"])
    return f'<div class="cta"><h2>{esc(h)}</h2><p>{esc(p)} <a href="{href}">{esc(label)} &#8594;</a> Or <a href="mailto:inigoangulo@gmail.com">email me</a>.</p></div>'

def faq_block(d):
    faq = d.get("faq")
    if not faq: return ""
    items = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q,a in faq)
    return f'<section class="faq"><h2>Questions people ask</h2>{items}</section>'

def page(slug, d):
    url = f"https://inigoangulo.com/writing/{slug}/"
    faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in d.get("faq",[])]} if d.get("faq") else None
    ld = {"@context":"https://schema.org","@type":"Article","headline":d["title"],"description":d.get("meta",d["desc"]),"datePublished":d["date"],"dateModified":d.get("updated",d["date"]),"author":{"@type":"Person","@id":"https://inigoangulo.com/#person","name":"Inigo Angulo","url":"https://inigoangulo.com/"},"publisher":{"@type":"Person","name":"Inigo Angulo"},"mainEntityOfPage":url,"image":"https://inigoangulo.com/img/og-home.png","keywords":TAGS.get(d.get("tag",""),""),"articleSection":TAGS.get(d.get("tag",""),""),"inLanguage":"en"}
    bc = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inigo Angulo","item":"https://inigoangulo.com/"},{"@type":"ListItem","position":2,"name":"Writing","item":"https://inigoangulo.com/writing/"},{"@type":"ListItem","position":3,"name":d["title"],"item":url}]}
    nice = datetime.date.fromisoformat(d["date"]).strftime("%B %-d, %Y")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(d["title"])} / Inigo Angulo</title>
<meta name="description" content="{esc(d.get("meta",d["desc"]))}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">\n<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<meta property="og:title" content="{esc(d["title"])}">
<meta property="og:description" content="{esc(d.get("meta",d["desc"]))}">
<meta property="og:image" content="https://inigoangulo.com/img/og-home.png">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
<link rel="stylesheet" href="/services/services.css?v={VER}">
<style>{CSS}</style>
{GA}
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(bc,ensure_ascii=False)}</script>
{('<script type="application/ld+json">'+json.dumps(faq_ld,ensure_ascii=False)+'</script>') if faq_ld else ''}
</head>
<body>
{header('writing',TAGS.get(d.get('tag',''),'Writing'))}{mobmenu('writing')}
<script src="/services/bar.js?v={VER}" defer></script>
<script src="/services/copy.js?v={VER}" defer></script>
<main><article class="art">
<span class="k">Writing</span>
<h1>{esc(d["title"])}</h1>
<div class="meta"><span>Inigo Angulo</span><span>{nice}</span><span>{d["read"]} read</span><a class="tag" href="/writing/#{d.get("tag","")}">{esc(TAGS.get(d.get("tag",""),""))}</a></div>
{series_box(slug,d)}
{d["body"]}
{kit_box(slug)}
{faq_block(d)}
{cta_block(d)}
</article></main>
{FOOTER}
</body>
</html>
'''

def index():
    order = sorted(POSTS.items(), key=lambda kv: (not kv[1].get("hub"), kv[1]["date"]), reverse=False)
    order = sorted(POSTS.items(), key=lambda kv: kv[1]["date"], reverse=True)
    def card(s,d):
        words = esc(" ".join([d["title"], d["desc"], TAGS.get(d.get("tag",""),""), s.replace("-"," ")]).lower())
        return (f'<a class="post{" post--hub" if d.get("hub") else ""}" data-tag="{d.get("tag","")}" data-s="{words}" href="/writing/{s}/">'
                f'<span class="k" style="margin-bottom:6px">{datetime.date.fromisoformat(d["date"]).strftime("%B %-d, %Y")} / {d["read"]}{" / start here" if d.get("hub") else ""}</span>'
                f'<h2>{esc(d["title"])}</h2><p>{esc(d["desc"])}</p></a>')
    groups = ""
    for k,label in TAGS.items():
        members = [(s,d) for s,d in order if d.get("tag")==k]
        members = [m for m in members if m[1].get("hub")] + [m for m in members if not m[1].get("hub")]
        if not members: continue
        groups += f'<section class="grp" data-tag="{k}" id="{k}"><h2 class="grp__h">{esc(label)} <span>{len(members)}</span></h2>{"".join(card(s,d) for s,d in members)}</section>'
    chips = '<a class="chip on" href="#" data-f="">All</a>' + "".join(f'<a class="chip" href="#{k}" data-f="{k}">{esc(v)}</a>' for k,v in TAGS.items())
    blog_ld = {"@context":"https://schema.org","@type":"Blog","name":"Writing by Inigo Angulo","url":"https://inigoangulo.com/writing/","author":{"@type":"Person","@id":"https://inigoangulo.com/#person","name":"Inigo Angulo"},"blogPost":[{"@type":"BlogPosting","headline":d["title"],"url":f"https://inigoangulo.com/writing/{s}/","datePublished":d["date"]} for s,d in order]}
    n = len(order)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Writing: building with AI agents, product, conversion / Inigo Angulo</title>
<meta name="description" content="Notes from building products with AI agent teams, running experiments on checkout funnels, and deciding what is worth building. {n} articles in four series.">
<link rel="canonical" href="https://inigoangulo.com/writing/">
<link rel="alternate" type="application/rss+xml" title="Inigo Angulo, writing" href="https://inigoangulo.com/writing/feed.xml">
<meta property="og:title" content="Writing: building with AI agents, product, conversion"><meta property="og:description" content="Notes from building products with AI agent teams, running experiments on checkout funnels, and deciding what is worth building."><meta property="og:image" content="https://inigoangulo.com/img/og-home.png"><meta property="og:url" content="https://inigoangulo.com/writing/">
<script type="application/ld+json">{json.dumps(blog_ld,ensure_ascii=False)}</script>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">\n<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="/services/services.css?v={VER}">
<style>
.list{{max-width:760px;margin:0 auto;padding:110px 24px 40px}}
.intro{{color:var(--t2);font-size:1.02rem;max-width:640px;margin:0 0 24px}}
.search{{position:relative;margin:0 0 14px}}
.search input{{width:100%;height:50px;border:1px solid var(--b2);border-radius:12px;background:var(--glass);color:var(--t1);font-family:var(--s);font-size:1rem;padding:0 44px 0 44px;outline:none;transition:border-color .2s,box-shadow .2s}}
.search input::placeholder{{color:var(--t3)}}
.search input:focus{{border-color:var(--acb);box-shadow:0 0 0 3px var(--acg2)}}
.search svg{{position:absolute;left:16px;top:17px;width:16px;height:16px;color:var(--t3);pointer-events:none}}
.search kbd{{position:absolute;right:14px;top:15px;font-family:var(--m);font-size:.66rem;color:var(--t3);border:1px solid var(--b1);border-radius:6px;padding:3px 6px;pointer-events:none}}
.chips{{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 26px}}
.chip{{font-family:var(--m);font-size:.72rem;color:var(--t2);border:1px solid var(--b2);border-radius:999px;padding:7px 12px;transition:color .2s,border-color .2s}}
.chip.on,.chip:hover{{color:var(--ac2);border-color:var(--acb)}}
.grp{{margin:0 0 34px;padding:0;border-top:none}}
.grp__h{{font-family:var(--m);font-size:.7rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--t3);margin:0 0 12px;display:flex;align-items:center;gap:10px}}
.grp__h::after{{content:"";flex:1;height:1px;background:var(--b1)}}
.grp__h span{{color:var(--ac2)}}
.post{{display:block;border:1px solid var(--b1);border-radius:12px;padding:20px 22px;margin-bottom:12px;background:var(--glass);transition:border-color .2s,transform .2s}}
.post:hover{{border-color:var(--acb);transform:translateY(-2px)}}
.post h2{{font-size:1.18rem;margin:0 0 6px}}.post p{{font-size:.93rem;margin:0}}.post .k::before{{content:""}}
.post--hub{{border-color:var(--acb);background:var(--acg2)}}
.post.hide,.grp.hide{{display:none}}
.empty{{display:none;color:var(--t3);font-family:var(--m);font-size:.8rem;padding:30px 0}}.empty.show{{display:block}}
.kitban{{display:flex;align-items:center;gap:14px;border:1px solid var(--acb);background:var(--acg2);border-radius:12px;padding:14px 18px;margin:0 0 22px;transition:border-color .2s,transform .2s}}.kitban:hover{{transform:translateY(-2px);border-color:var(--ac)}}.kitban__k{{flex:none;font-family:var(--m);font-size:.64rem;letter-spacing:.14em;text-transform:uppercase;color:#000;background:var(--ac);border-radius:6px;padding:4px 8px}}.kitban__t{{flex:1;font-size:.92rem;color:var(--t2);line-height:1.45}}.kitban__t b{{color:var(--t1);font-weight:600}}.kitban__a{{flex:none;font-family:var(--m);font-size:.72rem;color:var(--ac2)}}@media(max-width:700px){{.kitban{{flex-wrap:wrap}}.kitban__a{{width:100%}}}}
.count{{font-family:var(--m);font-size:.68rem;color:var(--t3);margin:-14px 0 20px}}
mark{{background:rgba(45,212,191,.22);color:var(--t1);border-radius:3px;padding:0 2px;box-shadow:0 0 0 1px rgba(45,212,191,.18)}}
@media(max-width:700px){{.search kbd{{display:none}}.list{{padding-top:96px}}}}
</style>
{GA}
</head>
<body>
{header('writing','Writing')}{mobmenu('writing')}
<script src="/services/bar.js?v={VER}" defer></script>
<script src="/services/copy.js?v={VER}" defer></script>
<main><div class="list"><div class="pt" style="margin-bottom:22px"><p class="pt__tag">Writing</p><h1 class="pt__h">What I learned shipping, written down.</h1></div><p class="intro">{n} articles in four series: building products with AI agent teams, the gates between an agent and production, conversion experiments on real funnels, and design systems that match the code. Each series has a place to start.</p>
<a class="kitban" href="/writing/kit/"><span class="kitban__k">Kit</span><span class="kitban__t"><b>{len(KIT)} templates, checklists and prompts</b> from the method, ready to copy: CLAUDE.md, tickets, release gates, MVP scope, checkout audit.</span><span class="kitban__a">Open the kit &#8594;</span></a>
<form class="search" role="search" onsubmit="return false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg><input id="q" type="search" placeholder="Search {n} articles: tickets, CLAUDE.md, checkout, RLS, cost..." aria-label="Search articles" autocomplete="off"><kbd>/</kbd></form>
<div class="chips">{chips}</div>
<p class="count" id="count"></p>
{groups}
<p class="empty" id="empty">Nothing matches. Try a shorter word, or <a href="mailto:inigoangulo@gmail.com">ask me</a>.</p>
<script>(function(){{var q=document.getElementById("q"),chips=document.querySelectorAll(".chip"),posts=document.querySelectorAll(".post"),grps=document.querySelectorAll(".grp"),count=document.getElementById("count"),empty=document.getElementById("empty"),f="";
posts.forEach(function(p){{p.querySelectorAll("h2,p").forEach(function(el){{el.dataset.t=el.textContent}})}});
function esc(w){{return w.replace(/[.*+?^${{}}()|[\\]\\\\]/g,"\\\\$&")}}
function mark(el,t){{var raw=el.dataset.t;if(!t.length){{el.textContent=raw;return}}var re=new RegExp("("+t.map(esc).join("|")+")","gi"),parts=raw.split(re);el.textContent="";parts.forEach(function(s,i){{if(!s)return;if(i%2){{var m=document.createElement("mark");m.textContent=s;el.appendChild(m)}}else el.appendChild(document.createTextNode(s))}})}}
function apply(){{var t=q.value.trim().toLowerCase().split(/\\s+/).filter(Boolean),n=0;chips.forEach(function(c){{c.classList.toggle("on",c.dataset.f===f)}});
posts.forEach(function(p){{var ok=(!f||p.dataset.tag===f)&&t.every(function(w){{return p.dataset.s.indexOf(w)>-1}});p.classList.toggle("hide",!ok);if(ok){{n++;p.querySelectorAll("h2,p").forEach(function(el){{mark(el,t)}})}}}});
grps.forEach(function(g){{var k=g.querySelectorAll(".post:not(.hide)").length;g.classList.toggle("hide",!k);var c=g.querySelector(".grp__h span");if(c){{c.textContent=k}}}});
count.textContent=(t.length||f)?n+" of "+posts.length+" articles":"";empty.classList.toggle("show",n===0)}}
chips.forEach(function(c){{c.addEventListener("click",function(e){{e.preventDefault();f=c.dataset.f;history.replaceState(null,"",f?"#"+f:"/writing/");apply()}})}});
q.addEventListener("input",apply);
document.addEventListener("keydown",function(e){{if(e.key==="/"&&document.activeElement!==q){{e.preventDefault();q.focus()}}if(e.key==="Escape"&&document.activeElement===q){{q.value="";apply();q.blur()}}}});
var h=location.hash.slice(1);if(h&&document.querySelector('.chip[data-f="'+h+'"]')){{f=h}}apply()}})();</script></div></main>
{FOOTER}
</body>
</html>
'''

def feed():
    order = sorted(POSTS.items(), key=lambda kv: kv[1]["date"], reverse=True)
    items = "".join(f"<item><title>{esc(d['title'])}</title><link>https://inigoangulo.com/writing/{s}/</link><guid>https://inigoangulo.com/writing/{s}/</guid><pubDate>{datetime.datetime.combine(datetime.date.fromisoformat(d['date']),datetime.time(8)).strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate><description>{esc(d['desc'])}</description></item>" for s,d in order)
    return f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Inigo Angulo, writing</title><link>https://inigoangulo.com/writing/</link><description>Notes on building product with AI agent teams, conversion experiments and design systems.</description><language>en</language>{items}</channel></rss>'

# ---------- Kit ----------
KIT_CTA = {"build": "agents", "lead": "product", "optimize": "conversion"}
KIT_CSS = '''
.kitbox{display:flex;gap:14px;align-items:center}.kitbox .kitban__k{flex:none;font-family:var(--m);font-size:.62rem;letter-spacing:.14em;text-transform:uppercase;color:#000;background:var(--ac);border-radius:6px;padding:4px 8px}
.art .kmeta{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0 26px}
.art .kpill{font-family:var(--m);font-size:.68rem;color:var(--t2);border:1px solid var(--b2);border-radius:999px;padding:4px 10px}
.art .kpill--ac{color:var(--ac2);border-color:var(--acb)}
.art .lede{font-size:1.12rem;color:var(--t1)}
.art ol.use{counter-reset:u;list-style:none;margin:0 0 10px;padding:0}
.art ol.use li{counter-increment:u;position:relative;padding:0 0 0 38px;margin:0 0 12px}
.art ol.use li::before{content:counter(u);position:absolute;left:0;top:1px;width:24px;height:24px;border-radius:7px;border:1px solid var(--acb);color:var(--ac2);font-family:var(--m);font-size:.7rem;display:grid;place-items:center}
.kb{margin:24px 0 0}
.kb__h{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0 0 -12px;padding:0 2px}
.kb__h span{font-family:var(--m);font-size:.7rem;color:var(--t3);letter-spacing:.04em}
.kb__h span b{color:var(--t1);font-weight:500}
.kb__dl{display:inline-flex;align-items:center;gap:6px;font-family:var(--m);font-size:.7rem;color:var(--ac2)!important;border:none!important}
.kb__dl svg{width:13px;height:13px}
.art .kb pre{white-space:pre-wrap;word-break:break-word}.kb .cb>pre{padding-top:54px}
.kb--prompt pre{background:linear-gradient(180deg,rgba(45,212,191,.05),rgba(45,212,191,.015));border-color:var(--acb)}
.art .log{list-style:none;margin:0;padding:0;border-left:1px solid var(--b2)}
.art .log li{position:relative;padding:0 0 14px 20px;margin:0}
.art .log li::before{content:"";position:absolute;left:-4px;top:7px;width:7px;height:7px;border-radius:50%;background:var(--ac);box-shadow:0 0 10px var(--acg)}
.art .log b{font-family:var(--m);font-size:.74rem;color:var(--ac2);font-weight:500;margin-right:8px}
.art .log em{font-style:normal;font-family:var(--m);font-size:.7rem;color:var(--t3);margin-right:8px}
.krel{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:14px 0 0}
.kcard{display:flex;flex-direction:column;gap:8px;border:1px solid var(--b1);border-radius:12px;padding:18px;background:var(--glass);color:inherit!important;transition:border-color .2s,transform .2s}
.kcard:hover{border-color:var(--acb);transform:translateY(-2px)}
.kcard__k{font-family:var(--m);font-size:.64rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ac)}
.kcard h2,.kcard h3{font-size:1.02rem;margin:0;color:var(--t1);line-height:1.3;max-width:none}
.kcard p{font-size:.88rem!important;color:var(--t2);margin:0!important;line-height:1.5!important}
.kcard__f{margin-top:auto;padding-top:6px;font-family:var(--m);font-size:.66rem;color:var(--t3)}
@media(max-width:700px){.krel{grid-template-columns:1fr}}
'''
DL_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11m0 0l-4.5-4.5M12 15l4.5-4.5M5 20h14"/></svg>'

def kit_box(slug):
    k = ARTICLE_TO_KIT.get(slug)
    if not k: return ""
    d = KIT[k]
    return f'<div class="box kitbox"><span class="kitban__k">Kit</span><p>Copy the {esc(d["kind"].lower())}: <a href="/writing/kit/{k}/">{esc(d["short"])}</a>, with a prompt to use it and its changelog.</p></div>'

def kit_card(k, tag="h3"):
    d = KIT[k]
    return (f'<a class="kcard" href="/writing/kit/{k}/" data-cap="{d["cap"]}"><span class="kcard__k">{esc(d["kind"])} / {esc(KIT_CAPS[d["cap"]])}</span>'
            f'<{tag}>{esc(d["short"])}</{tag}><p>{esc(d["card"])}</p><span class="kcard__f">v{d["version"]} / {esc(d["file"])}</span></a>')

def kit_head(title, desc, url, extra_css, lds):
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>\n' for x in lds)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} / Inigo Angulo</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="https://inigoangulo.com/img/og-home.png">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
<link rel="stylesheet" href="/services/services.css?v={VER}">
<style>{CSS}{KIT_CSS}{extra_css}</style>
{GA}
{ld}</head>
<body>
{header('writing','Kit')}{mobmenu('writing')}
<script src="/services/bar.js?v={VER}" defer></script>
<script src="/services/copy.js?v={VER}" defer></script>
'''

def kit_page(k, d):
    url = f"https://inigoangulo.com/writing/kit/{k}/"
    last = d["changelog"][0][1]
    nice = datetime.date.fromisoformat(last).strftime("%B %-d, %Y")
    blocks = "".join(
        f'<div class="kb"><div class="kb__h"><span>{esc(label)}: <b>{esc(fn)}</b></span><a class="kb__dl" href="/writing/kit/{k}/{fn}" download="{fn}" data-dl="{k}">{DL_ICON}Download</a></div><pre><code>{esc(body.rstrip())}</code></pre></div>'
        for label, fn, body in d["blocks"])
    plabel, ptext = d["prompt"]
    prompt = f'<h2>Prompt to use it</h2><div class="kb kb--prompt"><div class="kb__h"><span>{esc(plabel)}</span></div><pre><code>{esc(ptext.rstrip())}</code></pre></div>'
    use = "".join(f"<li>{esc(x)}</li>" for x in d["use"])
    log = "".join(f'<li><b>v{v}</b><em>{datetime.date.fromisoformat(dt).strftime("%b %-d, %Y")}</em>{esc(t)}</li>' for v, dt, t in d["changelog"])
    aslug, atitle = d["article"]
    rel = "".join(kit_card(r) for r in d["related"])
    h, p, href, lab = CTA[KIT_CTA[d["cap"]]]
    ld = {"@context":"https://schema.org","@type":"CreativeWork","name":d["title"],"description":d.get("meta",d["desc"]),"url":url,"version":d["version"],"dateModified":last,
          "author":{"@type":"Person","@id":"https://inigoangulo.com/#person","name":"Inigo Angulo"},"isPartOf":{"@type":"CollectionPage","name":"Kit","url":"https://inigoangulo.com/writing/kit/"},"inLanguage":"en"}
    bc = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inigo Angulo","item":"https://inigoangulo.com/"},{"@type":"ListItem","position":2,"name":"Writing","item":"https://inigoangulo.com/writing/"},{"@type":"ListItem","position":3,"name":"Kit","item":"https://inigoangulo.com/writing/kit/"},{"@type":"ListItem","position":4,"name":d["short"],"item":url}]}
    return kit_head(d["title"], d.get("meta",d["desc"]), url, "", [ld, bc]) + f'''<main><article class="art">
<span class="k"><a href="/writing/" style="color:inherit">Writing</a> / <a href="/writing/kit/" style="color:inherit">Kit</a></span>
<h1>{esc(d["title"])}</h1>
<div class="kmeta"><span class="kpill kpill--ac">{esc(d["kind"])}</span><span class="kpill">{esc(KIT_CAPS[d["cap"]])}</span><span class="kpill">v{d["version"]}</span><span class="kpill">Updated {nice}</span></div>
<p class="lede">{esc(d["desc"])}</p>
<h2>How to use it</h2>
<ol class="use">{use}</ol>
{blocks}
{prompt}
<div class="box"><p>Why it looks like this, and where each part came from: <a href="/writing/{aslug}/">{esc(atitle)}</a>.</p></div>
<h2>Changelog</h2>
<ul class="log">{log}</ul>
<h2>More from the kit</h2>
<div class="krel">{rel}</div>
<div class="cta"><h2>{esc(h)}</h2><p>{esc(p)} <a href="{href}">{esc(lab)} &#8594;</a> Or <a href="mailto:inigoangulo@gmail.com">email me</a>.</p></div>
</article></main>
<script>document.querySelectorAll("[data-dl]").forEach(function(a){{a.addEventListener("click",function(){{if(window.siteSnack)siteSnack("Downloading "+a.getAttribute("download"));if(window.gtag)try{{gtag("event","kit_download",{{item:a.dataset.dl,file:a.getAttribute("download")}})}}catch(e){{}}}})}})</script>
{FOOTER}
</body>
</html>
'''

def kit_index():
    url = "https://inigoangulo.com/writing/kit/"
    title = "Kit: templates, checklists and prompts for building with AI agents"
    desc = 'Six free templates, checklists and prompts for building with AI agent teams: CLAUDE.md, tickets, escalation, release gates, MVP scope, checkout audit.'
    groups = f'<div class="kgrid">{"".join(kit_card(k) for k in KIT_ORDER)}</div>'
    chips = '<a class="chip on" href="#" data-f="">All</a>' + "".join(f'<a class="chip" href="#{c}" data-f="{c}">{esc(l)}</a>' for c, l in KIT_CAPS.items())
    ld = {"@context":"https://schema.org","@type":"CollectionPage","name":title,"description":desc,"url":url,"hasPart":[{"@type":"CreativeWork","name":KIT[k]["title"],"url":f"{url}{k}/"} for k in KIT_ORDER]}
    css = '''.list{max-width:900px;margin:0 auto;padding:110px 24px 40px}.intro{color:var(--t2);font-size:1.02rem;max-width:640px;margin:0 0 22px}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 26px}.chip{font-family:var(--m);font-size:.72rem;color:var(--t2);border:1px solid var(--b2);border-radius:999px;padding:7px 12px;transition:color .2s,border-color .2s}.chip.on,.chip:hover{color:var(--ac2);border-color:var(--acb)}
.grp{margin:0 0 34px}.grp.hide{display:none}.grp__h{font-family:var(--m);font-size:.7rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--t3);margin:0 0 12px;display:flex;align-items:center;gap:10px}.grp__h::after{content:"";flex:1;height:1px;background:var(--b1)}.grp__h span{color:var(--ac2)}
.kcard.hide{display:none}.kgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}.kgrid .kcard{padding:22px}.kgrid .kcard h3{font-size:1.15rem}
.knote{max-width:none;font-family:var(--m);font-size:.72rem;color:var(--t3);line-height:1.6;border-top:1px solid var(--b1);padding-top:18px;margin-top:10px}
@media(max-width:700px){.kgrid{grid-template-columns:1fr}.list{padding-top:96px}}'''
    return kit_head(title, desc, url, css, [ld]) + f'''<main><div class="list">
<div class="pt" style="margin-bottom:22px"><p class="pt__tag"><span><a href="/writing/" style="color:inherit">Writing</a> / Kit</span></p><h1 class="pt__h pt__h--wide">The kit. What I actually use, ready to copy.</h1></div>
<p class="intro">Templates, checklists and prompts from the way I scope, build and ship products with AI agent teams. Neutral versions of the real thing: copy them, adapt them, break them. Each one links to the article that explains why it looks the way it does, and keeps a changelog of what changed and what incident changed it.</p>
<div class="chips">{chips}</div>
{groups}
<p class="knote">Free to use, no sign up. Every block has a copy button and a download. If something here stops working for you, <a href="mailto:inigoangulo@gmail.com" style="color:var(--ac2)">tell me</a> and it goes in the changelog.</p>
</div></main>
<script>(function(){{var chips=document.querySelectorAll(".chip"),grps=document.querySelectorAll(".grp"),f="";function apply(){{chips.forEach(function(c){{c.classList.toggle("on",c.dataset.f===f)}});document.querySelectorAll(".kgrid .kcard").forEach(function(g){{g.classList.toggle("hide",!!f&&g.dataset.cap!==f)}})}}
chips.forEach(function(c){{c.addEventListener("click",function(e){{e.preventDefault();f=c.dataset.f;history.replaceState(null,"",f?"#"+f:"/writing/kit/");apply()}})}});var h=location.hash.slice(1);if(h&&document.querySelector('.chip[data-f="'+h+'"]'))f=h;apply()}})();</script>
{FOOTER}
</body>
</html>
'''

def write_kit():
    os.makedirs("writing/kit", exist_ok=True)
    open("writing/kit/index.html", "w").write(kit_index())
    for k in KIT_ORDER:
        d = KIT[k]
        os.makedirs(f"writing/kit/{k}", exist_ok=True)
        open(f"writing/kit/{k}/index.html", "w").write(kit_page(k, d))
        for label, fn, body in d["blocks"]:
            open(f"writing/kit/{k}/{fn}", "w").write(body.rstrip() + "\n")

if __name__ == "__main__":
    write_kit()
    os.makedirs("writing", exist_ok=True)
    open("writing/feed.xml","w").write(feed())
    open("writing/index.html","w").write(index())
    for s,d in POSTS.items():
        os.makedirs(f"writing/{s}", exist_ok=True)
        open(f"writing/{s}/index.html","w").write(page(s,d))
        print("built", s)
