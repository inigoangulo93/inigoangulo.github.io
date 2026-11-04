#!/usr/bin/env python3
"""Builds the articles under /writing/. Run from the repo root: python3 writing/build.py"""
import json, html, os, subprocess, datetime
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
.art .cta{margin-top:40px}
.art .cta h2{margin:0 0 6px}
'''

POSTS = {
"ai-agent-teams-software-development": dict(
  title="AI agent teams for software development: what actually works in 2026",
  desc="How to run a team of AI coding agents that ships to production: roles with mandates, isolation, gates, a decision log, and the numbers from seven weeks of doing it.",
  date="2026-11-05", read="9 min",
  body="""
<p>Most of what is written about AI coding agents is either a demo or a warning. This is neither. It is the operating model I used to build and run a production platform with eight agents and no engineers on payroll: 445 merged pull requests, 1,456 CI runs and 15 gated releases in seven weeks. The model is not clever. It is a set of boring decisions about who may do what, and it is the reason the numbers are real instead of a story.</p>
<p>This is the hub of a series. Each section links to a deeper piece.</p>

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
  title="Human in the loop for coding agents: the two gates that matter",
  desc="Where a person must sit when AI agents write and ship code: the decision gate (one id, one letter) and the release gate (one approval with a security report). Everything else can be automated.",
  date="2026-11-05", read="7 min",
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

<div class="box"><p>This post is part of a series: the hub is <a href="/writing/ai-agent-teams-software-development/">AI agent teams for software development</a>, and the gates are in <a href="/writing/human-in-the-loop-coding-agents/">Human in the loop for coding agents</a>. The full case, with the evidence from the GitHub API, the data model, the promotion flow and the day the security gate said no: <a href="/work/acervo.html">Acervo, the case study</a>. If you want this for your company: <a href="/ai-product-builder/">AI build and deployment</a>.</p></div>
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

<div class="box"><p>Part of a series: <a href="/writing/ai-agent-teams-software-development/">AI agent teams for software development</a> and <a href="/writing/human-in-the-loop-coding-agents/">the two human gates</a>. The failure story, beat by beat, with the run ids, is in the <a href="/work/acervo.html#s10">Trust chapter of the Acervo case</a>. If your team is introducing agents and wants the guardrails with them: <a href="/ai-product-builder/">how I set that up</a>.</p></div>
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
<link rel="stylesheet" href="/services/services.css?v={VER}">
<style>{CSS}</style>
{GA}
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(bc,ensure_ascii=False)}</script>
</head>
<body>
<header class="bar"><div class="bar__inner"><a class="bar__name" href="/">Inigo Angulo</a><nav class="bar__nav"><a class="bar__btn" href="/#work">Work</a><a class="bar__btn" href="/#how-i-think">How I think</a><a class="bar__btn" href="/#about">About</a><a class="bar__btn on" href="/writing/">Writing</a></nav><a class="bar__cta" href="/#contact">Contact</a></div><div class="bar__mini" aria-hidden="true"><i></i><span>Writing</span></div></header>
<script src="/services/bar.js?v={VER}" defer></script>
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
<link rel="stylesheet" href="/services/services.css?v={VER}">
<style>.list{{max-width:760px;margin:0 auto;padding:110px 24px 40px}}.post{{display:block;border:1px solid var(--b1);border-radius:12px;padding:22px 24px;margin-bottom:14px;background:var(--glass);transition:border-color .2s,transform .2s}}.post:hover{{border-color:var(--acb);transform:translateY(-2px)}}.post h2{{font-size:1.25rem;margin:0 0 8px}}.post p{{font-size:.95rem}}.post .k::before{{content:""}}</style>
{GA}
</head>
<body>
<header class="bar"><div class="bar__inner"><a class="bar__name" href="/">Inigo Angulo</a><nav class="bar__nav"><a class="bar__btn" href="/#work">Work</a><a class="bar__btn" href="/#how-i-think">How I think</a><a class="bar__btn" href="/#about">About</a><a class="bar__btn on" href="/writing/">Writing</a></nav><a class="bar__cta" href="/#contact">Contact</a></div><div class="bar__mini" aria-hidden="true"><i></i><span>Writing</span></div></header>
<script src="/services/bar.js?v={VER}" defer></script>
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
