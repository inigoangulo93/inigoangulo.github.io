# The "Building with AI agents" series. Imported by build.py and merged into POSTS.

BUILD_POSTS = {

"how-to-build-an-mvp-with-ai-agents": dict(
  tag="build", hub=True, title="How to build an MVP with AI agents: the full method, from scope to production",
  desc="A step by step method for building a real MVP with AI coding agents: how to scope it, the project rules file, tickets agents cannot misread, the team structure, the gates before production, and what it costs. From a build that shipped 445 PRs in seven weeks.",
  date="2026-11-04", read="12 min",
  faq=[
    ("Can a non technical founder build an MVP with AI agents?","Yes, up to a point. Agents write the code; they do not decide what the product is, what it must never do, or whether a green check means anything. If you can write a one page scope and read a test result, you can run the method. If you cannot, you need one person who can, part time."),
    ("How long does it take to build an MVP with AI agents?","For a focused product with one core workflow, two to four weeks of calendar time is realistic when scope is written before the first prompt. The build I ran for a private client went from first commit to a first gated release in 17 days and to 15 releases in seven weeks. The time that does not compress is deciding, verifying and design."),
    ("Which tool do you use, Claude Code or Cursor?","The method does not depend on the tool. I use Claude Code because it runs multiple agents with their own mandate files and worktrees, which is what the team structure needs. The rules file, ticket template and gates work with any agent that reads files from the repository."),
    ("What is the biggest mistake people make?","Starting to build before writing what the product must never do. Agents are excellent at adding features and terrible at knowing which feature breaks the thesis. Every expensive failure I have seen traces back to a missing invariant, not to a wrong line of code."),
  ],
  body="""
<p>This is the method I use to build a production MVP with a team of AI coding agents, written as steps you can follow. It is not a weekend tutorial and it is not a warning. It is what produced 445 merged pull requests, 15 gated releases and a product with paying customers in seven weeks, with one person scoping, deciding and approving, and no engineers on payroll. Every step links to a deeper piece.</p>

<div class="num"><div><b>7</b><span>steps, in the order they have to happen</span></div><div><b>1</b><span>page of scope before the first prompt</span></div><div><b>5</b><span>checks before main accepts a merge</span></div><div><b>0</b><span>agents with production credentials</span></div></div>

<h2>Step 0: decide whether agents are the right tool</h2>
<p>Agents compress the writing of code. They do not compress deciding what to write, verifying that what was written works, or designing something a customer wants to look at. If your product's risk is in the code (a hard algorithm, a novel integration), agents help less than you hope. If the risk is in the product (will anyone pay, does the workflow hold up), agents are the cheapest way ever invented to find out, because the first version costs weeks instead of quarters.</p>
<p>The test: can you write, in one page, what the product must do, what it must never do, and who may see what? If yes, go. If no, the week you would spend building is better spent writing that page, and you should not touch an agent until it exists.</p>

<h2>Step 1: scope the MVP as invariants, not features</h2>
<p>A feature list tells an agent what to add. An invariant tells it what it may never break. The second is what keeps a fast build from turning into a pile of features that contradict each other.</p>
<p>My scope document has four parts: the thesis in one sentence (what the user can trust the product for), the one workflow the MVP must prove, the invariants (the things that must hold in every state, each marked as enforced in the database, in the application, or both), and the explicit list of what is not built. That last list is the one that saves the most money, because agents will happily build everything you do not forbid.</p>
<p>Read the detail in <a href="/writing/scope-an-mvp-for-ai-agents/">how to scope an MVP for AI agents</a>.</p>

<h2>Step 2: write the project rules file before the first line of code</h2>
<p>Every agent session starts by reading one file at the root of the repository. In Claude Code it is called CLAUDE.md; other tools have an equivalent. It is the single highest leverage artefact of the whole build, because it is the only thing that is true in every session, for every agent, after every context reset.</p>
<p>Mine holds: the thesis, the fixed stack with an explicit "nothing else", the hard rules (numbered, each with the incident that produced it), what counts as proof, the states a task can be reported in, and how an agent escalates a decision to me. It grew from 12 rules to 29 over seven weeks, and every addition has a date and a reason. A rules file without reasons gets argued with; one with reasons gets followed.</p>
<p>The structure, with a neutral example, is in <a href="/writing/claude-md-example-project-rules-file/">CLAUDE.md example: the project rules file</a>.</p>

<h2>Step 3: turn the scope into tickets agents cannot misread</h2>
<p>An agent given "add user invitations" will invent the half of the requirement you did not write. A ticket with a measurable acceptance criterion, a list of what is out of scope, and the decisions that are already taken cannot be invented around. The template is short and the discipline is total: no ticket, no work; no acceptance criterion, the ticket goes back.</p>
<p>The template, and the three fields that stop the most expensive mistakes, are in <a href="/writing/tickets-for-ai-agents-template/">writing tickets for AI agents</a>.</p>

<h2>Step 4: structure the team so that trust comes from the edges</h2>
<p>One agent doing everything works for a demo and fails at the first week of real scope, because it cannot review its own work and it holds every credential. The structure that held: a lead that decomposes tickets, assigns work and integrates but does not merge; workers with a mandate each (frontend, backend, data, design) that write only in the files they are assigned; a reviewer that returns a list of concrete faults; a security agent that runs a full penetration test before every release; and a verifier that can only answer from the output of a script.</p>
<p>The rule that mattered most: the orchestrator does not write code, and no agent to the right of it holds production credentials. The detail is in <a href="/writing/ai-agent-team-structure-solo-builder/">AI agent team structure for a solo builder</a>, and the operating model with its numbers is in <a href="/writing/ai-agent-teams-software-development/">AI agent teams for software development</a>.</p>

<figure class="fig"><svg viewBox="0 0 720 150" role="img" aria-label="The seven steps of the method as a horizontal sequence: scope, rules file, tickets, team, gates, release, measure">
<g font-family="JetBrains Mono,monospace" font-size="11" fill="#9a9aae">
<defs><marker id="b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#6b6b80"/></marker></defs>
<g fill="none" stroke="#6b6b80" stroke-width="1.2" marker-end="url(#b)"><path d="M100 60 L118 60"/><path d="M200 60 L218 60"/><path d="M300 60 L318 60"/><path d="M400 60 L418 60"/><path d="M500 60 L518 60"/><path d="M600 60 L618 60"/></g>
<rect x="20" y="36" width="80" height="48" rx="8" fill="rgba(34,197,94,.08)" stroke="rgba(34,197,94,.55)"/><text x="60" y="64" text-anchor="middle" fill="#bbf7d0">scope</text>
<rect x="120" y="36" width="80" height="48" rx="8" fill="rgba(34,197,94,.08)" stroke="rgba(34,197,94,.55)"/><text x="160" y="64" text-anchor="middle" fill="#bbf7d0">rules</text>
<rect x="220" y="36" width="80" height="48" rx="8" fill="rgba(34,197,94,.08)" stroke="rgba(34,197,94,.55)"/><text x="260" y="64" text-anchor="middle" fill="#bbf7d0">tickets</text>
<rect x="320" y="36" width="80" height="48" rx="8" fill="#101018" stroke="rgba(255,255,255,.2)"/><text x="360" y="64" text-anchor="middle" fill="#f4f4f6">team</text>
<rect x="420" y="36" width="80" height="48" rx="8" fill="rgba(245,158,11,.06)" stroke="rgba(245,158,11,.5)"/><text x="460" y="64" text-anchor="middle" fill="#fcd34d">gates</text>
<rect x="520" y="36" width="80" height="48" rx="8" fill="rgba(245,158,11,.06)" stroke="rgba(245,158,11,.5)"/><text x="560" y="64" text-anchor="middle" fill="#fcd34d">release</text>
<rect x="620" y="36" width="80" height="48" rx="8" fill="#101018" stroke="#2dd4bf"/><text x="660" y="64" text-anchor="middle" fill="#5eead4">measure</text>
<text x="20" y="120" font-size="10" fill="#6b6b80">green: human work that does not compress / amber: where agents are checked / the first three steps happen before any code</text>
</g></svg><figcaption>The order is the method. Teams that start at "team" or "gates" rebuild the first three steps later, at ten times the price.</figcaption></figure>

<h2>Step 5: put gates between the agents and main</h2>
<p>Volume is the problem agents create. Ten times the pull requests, the same number of eyes. The answer is not reading faster, it is gates that mean something: lint with house rules, strict types, unit and database tests, a secrets scan on every commit of the branch, browser tests on every change that is not documentation. And the rule under all of them: a skipped check does not count as green, and nothing is declared, everything is produced by a script with an identifier.</p>
<p>Why that matters, with the incident that taught it, is in <a href="/writing/green-check-is-not-proof/">why a green check is not proof</a>. The specific case of database security, where the test has to run as the user who must not get in, is in <a href="/writing/row-level-security-tests-ai-agents/">row level security with AI agents</a>.</p>

<h2>Step 6: release through one human gate, in numbered sets</h2>
<p>Agents deploy to production through a workflow that holds the secrets; they never see them. Before each promotion, a security agent runs a full penetration test against local and staging, never production, and writes a verdict. A FAIL blocks the release like a red check. Then one human command, logged with who and when. Releases are batched into numbered sets because verification is a fixed cost per release and it is the cost that does not compress.</p>
<p>The two gates where a human must sit, and why those two and not more, are in <a href="/writing/human-in-the-loop-coding-agents/">human in the loop for coding agents</a>. The full path from ticket to production is in <a href="/writing/ticket-to-production-in-five-hours/">from ticket to production in five hours</a>.</p>

<h2>Step 7: measure the build, not the activity</h2>
<p>Four numbers told me whether the method was working: pull requests merged per week (volume), the share of CI runs that went red for a reason that was not the code (noise), decisions escalated per week (whether the scope was holding), and releases with a PASS verdict (trust). Lines of code and agent hours are activity; none of them predicts whether a customer can use the product.</p>
<p>What the whole thing costs, split into agent usage, infrastructure and human time, is in <a href="/writing/cost-to-build-mvp-with-ai-agents/">how much it costs to build an MVP with AI agents</a>.</p>

<h2>Where it goes wrong</h2>
<p>Every failure I hit in seven weeks fits one of eight patterns, and each has a gate now. The three most expensive: a check that reported green without running; a ticket that contradicted itself eighty lines apart and an agent that built on the wrong half; and a test written to document a bug, which then protected the bug. The full list, with the gate for each, is in <a href="/writing/where-ai-coding-agents-fail/">where AI coding agents fail on real products</a>.</p>

<div class="box"><p><strong>Want this run for your product?</strong> I scope, design and build MVPs this way in fixed price sprints, with the agent costs passed through. See <a href="/ai-product-builder/">AI product builder</a>, or <a href="https://cal.com/inigoangulo/30min">book thirty minutes</a>.</p></div>
"""),

"scope-an-mvp-for-ai-agents": dict(
  tag="build", title="How to scope an MVP for AI agents: the one workflow rule and the list of what you will not build",
  desc="Scoping an MVP that AI coding agents will build is different from scoping one for a team. Four parts: the thesis, one workflow, invariants marked by where they are enforced, and the explicit list of what is not built. With a worked example.",
  date="2026-11-04", read="7 min",
  faq=[
    ("How many features should an MVP built with AI agents have?","One workflow, end to end, that proves the thesis. Not one feature: a workflow has several screens and a data model. But one. Agents make adding a second workflow feel free, and it is not: every workflow multiplies the states the gates have to cover."),
    ("Why write what will not be built?","Because agents build what you do not forbid. A feature list bounds the human team by effort; it does not bound agents, for whom the marginal feature costs minutes. The not built list is the only bound that works."),
    ("What is an invariant in this context?","A statement that must hold in every state of the product, such as 'no proposal from the model writes to an entity; a person decides and the system records who'. Each one is marked with where it is enforced: the database, the application, or both. Never only the interface."),
  ],
  body="""
<p>Scoping an MVP for a human team is about effort: what can four people ship in a quarter. Scoping an MVP for AI agents is about bounds: what must the product never do, and what must always hold, because the effort constraint is gone and nothing else stops the build from sprawling. The scope document I use has four parts and fits on one page. The page took a week to write and it was the most valuable week of the build.</p>

<h2>Part 1: the thesis, in one sentence</h2>
<p>What can the user trust the product for? Not what it does; what it is for. Mine was: the user can trust a single record of their collection, knowing where each item is, what is happening to it, and who made each change. Every ticket for seven weeks was tested against that sentence. A feature that did not serve it was not built, however easy it was.</p>
<p>The thesis goes at the top of the project rules file, so every agent reads it in every session. It is also the sentence an agent uses when it escalates a decision: "this does or does not serve the thesis" is a question I can answer in seconds.</p>

<h2>Part 2: one workflow, end to end</h2>
<p>The MVP proves one workflow. For mine: a user adds an item with a photo, the model proposes the fields, the user confirms, the record exists with an audit trail. Screens, data model, permissions and the model call, for that workflow and nothing else.</p>
<p>The rule is not "one feature". A workflow is a path through the product that a customer would pay for on its own. What the rule forbids is the second path. With agents the second path feels free, because the code arrives in an afternoon. It is not free: every path multiplies the states that the tests, the browser suite and the penetration test have to cover, and those are the costs that do not compress.</p>

<table><thead><tr><th>Scoping for a team</th><th>Scoping for agents</th></tr></thead><tbody>
<tr><td>Bounded by effort: what fits in the quarter</td><td>Bounded by invariants: what must never break</td></tr>
<tr><td>Feature list, prioritised</td><td>One workflow, plus a list of what is not built</td></tr>
<tr><td>Requirements in prose, clarified in meetings</td><td>Requirements as acceptance criteria an agent can test</td></tr>
<tr><td>Security as a phase near the end</td><td>Permissions matrix written before the first screen</td></tr>
<tr><td>Decisions taken in conversation</td><td>Decisions logged with an id, because sessions forget</td></tr>
</tbody></table>

<h2>Part 3: invariants, marked by where they are enforced</h2>
<p>An invariant is something that holds in every state. Mine included: no proposal from the model writes to an entity, a person decides and the system records who; sensitive identifiers are encrypted before they reach the database and are never searchable; a user whose account is pending reads zero rows of any table; every business write leaves an audit entry.</p>
<p>Each invariant carries a mark: enforced in the database, enforced in the application, or both. The one place an invariant is never enforced is only the interface, because hiding a column in the frontend is not a guarantee and an agent will not know the difference unless told. This list becomes the permissions matrix, and the permissions matrix becomes the security tests. Writing it first means the tests exist before the screens do.</p>

<h2>Part 4: what is not built</h2>
<p>This is the part teams skip and the part that saves the most money with agents. Mine said, among other things: no search by sensitive identifier, no identity documents stored anywhere, no infrastructure for a hypothetical need, no second backend, no queue, no cache layer until a measurement justifies it. Each line has a reason.</p>
<p>The effect on the build was immediate. When an agent proposed a cache for a page that loaded in 80 milliseconds, the rules file already said no, with the reason, and the proposal cost one line of reply. Without that list the same proposal costs a conversation, and the tenth such conversation is where scope dies.</p>

<h2>What the page produces</h2>
<p>From this one page come three artefacts that the agents work from: the project rules file (thesis, stack, hard rules), the domain model with its invariants, and the permissions matrix. Tickets reference them instead of restating them. When something is not in one of the three, for an agent it does not exist, which is exactly the property you want: the scope is the documents, not the memory of a conversation.</p>

<div class="box"><p>This is step 1 of <a href="/writing/how-to-build-an-mvp-with-ai-agents/">how to build an MVP with AI agents</a>. Next: <a href="/writing/claude-md-example-project-rules-file/">the project rules file</a>, then <a href="/writing/tickets-for-ai-agents-template/">tickets agents cannot misread</a>. If you want the scoping done with you, that is the first week of an <a href="/ai-product-builder/">AI build sprint</a>.</p></div>
"""),

"claude-md-example-project-rules-file": dict(
  tag="build", title="CLAUDE.md example: the project rules file that made 445 pull requests mergeable",
  desc="What goes in a CLAUDE.md, with a neutral example: thesis, fixed stack, numbered hard rules with the incident behind each, what counts as proof, task states and an escalation format. Why rules without reasons get argued with and rules with reasons get followed.",
  date="2026-11-04", read="8 min",
  faq=[
    ("What is CLAUDE.md?","The file at the root of a repository that Claude Code reads at the start of every session. It is where the rules of the project live: what the product is, which stack is allowed, what an agent may never do, and how it reports. Other agent tools read an equivalent file under another name."),
    ("How long should a CLAUDE.md be?","Mine is about 300 lines after seven weeks, and every line is there because of something that happened. Shorter is better only if nothing is missing. The test is not length, it is whether a fresh agent with no memory would make the same mistake twice."),
    ("Should CLAUDE.md contain code style rules?","A few, where a linter cannot catch them. Most style goes in the linter and the formatter, and the rules file says 'the linter decides'. The file is for decisions a machine cannot take: what the product is for, who decides what, what counts as proof."),
    ("Can I copy your CLAUDE.md?","You can copy the structure, which is in this article. You cannot copy the rules, because each one is the answer to an incident on a specific product. A rule you did not earn is a rule the agents will talk you out of in the first week."),
  ],
  body="""
<p>Every agent session on my build starts by reading one file. It is the only thing that is true in every session, for every agent, after every context reset, and it is why 445 pull requests from eight agents could be merged by one person without reading most of them line by line. Here is what is in it, why each part exists, and a neutral example you can adapt.</p>

<h2>What it is for</h2>
<p>An agent has no memory between sessions. Whatever you told it yesterday is gone, and whatever a colleague agent learned this morning never existed for it. The rules file is the fix: the set of facts and rules that every session inherits. If it is not in the file, for the agents it does not exist. That is the design principle, and it cuts both ways: the file has to carry everything that matters, and nothing that matters may live only in a conversation.</p>

<h2>The structure</h2>
<p>Seven sections, in this order, because the order is how an agent reads it.</p>

<table><thead><tr><th>Section</th><th>What it holds</th><th>Why first readers need it</th></tr></thead><tbody>
<tr><td>Thesis</td><td>One sentence: what the user can trust the product for. One principle: the model proposes, a person decides, the system records who</td><td>Every scope question resolves against it</td></tr>
<tr><td>Read before touching anything</td><td>The five documents that are the source of truth: architecture, domain model, permissions matrix, design, decisions</td><td>Stops an agent inventing a requirement that is written elsewhere</td></tr>
<tr><td>Stack, closed</td><td>The exact stack, and the sentence "nothing else". Amendments listed by decision id</td><td>Agents propose infrastructure for free; this is what says no</td></tr>
<tr><td>Hard rules</td><td>Numbered, each with the date and the incident that produced it</td><td>A rule with a reason is followed; one without is argued with</td></tr>
<tr><td>Task states</td><td>The only words a task may be reported in: VERIFIED, IMPLEMENTED, NEEDS_REVIEW, BLOCKED, DECISION_REQUIRED</td><td>Removes "done" as a word, because it means nothing</td></tr>
<tr><td>Escalation format</td><td>How an agent asks a human a question: a stable id, three options, a recommendation, what happens if nobody answers</td><td>Decisions take seconds instead of conversations</td></tr>
<tr><td>Conventions</td><td>Where files go, how commits are written, which language in code and which in the interface</td><td>The boring consistency that makes diffs readable</td></tr>
</tbody></table>

<h2>A neutral example of the rules section</h2>
<p>These are not my rules; they are the shape of my rules, on a product that does not exist.</p>
<pre><code>## Hard rules

1. Build nothing for a hypothetical need. Every piece of
   infrastructure names the MVP requirement it serves. No
   requirement, no build.
2. Never real data. Seeds, tests and screenshots use synthetic
   records only.
3. Never secrets in the repository. Production secrets live in
   the deployment environment and are never in an agent's reach.
4. Row level security on every new table, with a test that runs
   as the role that must not get in. No test, no pull request.
5. What a role must not see does not leave the server. Hiding a
   column in the frontend is not a guarantee.
6. No model output writes to an entity. It writes to a proposals
   table; a person decides; the application applies it and logs
   who decided.
7. Never say a test passed if it was not run. Never say a
   migration is safe without reading it. Never invent a
   requirement. (Added after an agent reported a suite green
   that had skipped every integration test.)
8. No agent declares an external fact. A script produces it as
   JSON and the agent interprets it. "CI is green" and "the
   preview works" are not sentences; a run id and a URL are.
9. A test never asserts a behaviour as "existing, not introduced
   by this ticket". A suspected bug becomes a ticket and the test
   is marked pending, never green. (Added the day it happened
   three times.)</code></pre>
<p>Notice what each rule has: a boundary that can be checked, and, for the ones that came from incidents, the incident. Rule 7 exists because a test suite reported success with a hundred skipped files. Rule 9 exists because a comment saying "existing behaviour" sat on top of a bug for three weeks and the green test made the fix look like a regression. The reason is not decoration. It is what makes an agent, two weeks later, recognise the same situation in a different shape.</p>

<h2>The escalation format, because it is the part people miss</h2>
<p>Agents stop at real decisions. If they do not have a format for stopping, they either guess or they write three paragraphs. Mine is fixed:</p>
<pre><code>DECISION 014-3: the question in one line
A) option  B) option  C) option
RECOMMENDATION: B. WHY: one line. IF UNDECIDED: what happens

DECISIONS REQUIRED: 014-3, 014-4
ACTIONS FOR YOU: open the preview at &lt;url&gt; and say what is off</code></pre>
<p>I answer with the id and a letter. The lead records the answer in the decisions log, citing the id. Over seven weeks that was more than 170 decisions, most answered in under a minute, every one of them findable later. Without the id, a decision lives in a chat and the next session does not know it was taken.</p>

<h2>How the file grows</h2>
<p>It started at 12 rules. It is 29 now. Every one of the 17 additions has a date, and most have a one line incident. The file never shrinks; a rule that stops applying is struck through with the reason, so the next person knows why it was there. A lessons table lives next to it, one line per incident, with the rule it left. That table is the real history of the build, and it is more useful than the commit log.</p>

<div class="box"><p>This is step 2 of <a href="/writing/how-to-build-an-mvp-with-ai-agents/">how to build an MVP with AI agents</a>. It follows <a href="/writing/scope-an-mvp-for-ai-agents/">scoping as invariants</a> and feeds <a href="/writing/tickets-for-ai-agents-template/">the ticket template</a>. The gates the rules refer to are in <a href="/writing/green-check-is-not-proof/">why a green check is not proof</a>.</p></div>
"""),

"tickets-for-ai-agents-template": dict(
  tag="build", title="Writing tickets for AI agents: the template that stops them inventing requirements",
  desc="A ticket template for AI coding agents: a measurable acceptance criterion, the explicit out of scope list, decisions already taken, and frontmatter a script can validate. The three fields that prevent the most expensive failures, with an example ticket.",
  date="2026-11-04", read="7 min",
  faq=[
    ("How detailed should a ticket for an AI agent be?","Detailed in the three places agents fail: what done looks like (measurable), what is out of scope (explicit), and which decisions are already taken (by id). Everything else can be short, because the agent reads the domain model and the rules file anyway."),
    ("Who writes the tickets, the human or the lead agent?","The human writes the ticket: intent, acceptance criterion, bounds. The lead agent decomposes it into work for the workers. An agent writing its own acceptance criterion is grading its own homework."),
    ("What happens when a ticket is wrong?","It goes back before any work starts. A ticket without a measurable criterion or with invalid frontmatter is returned, by rule. The cost of returning a ticket is minutes; the cost of building against a wrong one is the ticket plus everything that was built on top."),
  ],
  body="""
<p>The most expensive thing an AI coding agent does is not write a bug. It is invent a requirement. Given "add invitations to the team page", an agent will decide who can invite, what happens to a pending invitation after seven days, and whether the email goes out before or after the record exists. All three are product decisions, and it will take them in the most reasonable way, which is not necessarily yours. The ticket template below exists to leave no room for the reasonable guess.</p>

<h2>The rule under the template</h2>
<p>No ticket, no work. No measurable acceptance criterion, the ticket goes back to the human before anything starts. The frontmatter is validated by a script in CI, so a ticket missing a field cannot be worked on. It sounds bureaucratic until the first time an agent builds the wrong half of a self contradicting ticket, which on my build took eighty lines of distance between the two contradictory sentences and cost a day.</p>

<h2>The template</h2>
<pre><code>---
id: 143
title: Invite a teammate to a collection
status: todo
area: team
depends_on: [131]
decisions: [0088, 0091]
baseline: {design: 18, tokens: 7}
board: &lt;url of the row on the board&gt;
---

## Why
One sentence linking this to the thesis.

## What done looks like (measurable)
- A member with the owner role sends an invitation to an
  email; the invitee receives it within 60 seconds in the
  test mailbox.
- A pending invitation grants zero rows of any table,
  proven by a test that runs as the pending user.
- Accepting makes the invitee a member with the role
  chosen by the owner; the audit log records who invited
  and who accepted, with timestamps.
- Browser test on mobile and desktop passes.

## Out of scope (explicit)
- Resending or expiring invitations (ticket 144).
- Inviting by link.
- Any change to the roles themselves (decision 0088 fixes them).

## Decisions already taken
- 0088: the four roles and what each may do.
- 0091: invitations are per collection, not per account.

## Open questions
- None. (If there were, the ticket would be blocked, not started.)</code></pre>

<h2>The three fields that do the work</h2>
<p><strong>What done looks like, measurably.</strong> Every line has a number, a role, or a test in it. "The invitation works" is not a criterion. "The invitee receives it within 60 seconds in the test mailbox" is one, and an agent can make it true and prove it. This is also what the reviewer checks against, so a vague criterion makes the review vague too.</p>
<p><strong>Out of scope, explicitly.</strong> Agents build what you do not forbid. Listing the adjacent features, with the ticket where each one lives, turns "while I was there I also added resending" into a rule violation instead of initiative. On my build this list is the single most effective scope control, more than any conversation.</p>
<p><strong>Decisions already taken, by id.</strong> A decision in a chat is gone next session. A decision with an id in a log is citable, and a ticket that cites it tells the agent "this is settled; do not reopen it". Half the escalations I received in the first two weeks were questions that had already been decided; the field removed them.</p>

<h2>Frontmatter, because a script has to read it</h2>
<p>The fields above the line exist so that scripts can check what humans forget: that the ticket has an id and a status, that its dependencies are merged before it starts, that it cites decisions that exist, that it has a row on the board (the board mirrors the tickets, never the other way), and which version of the design it was built against. A ticket that fails the schema is returned automatically. The validation took an hour to write and has caught something every week since.</p>

<h2>What a ticket is not</h2>
<p>It is not a specification of the implementation. The data model, the permissions and the design live in their own documents, and the ticket references them. A ticket that restates the domain model goes stale the day the model changes, and an agent will follow the stale copy. One source of truth per fact, and the ticket points at it.</p>

<div class="box"><p>This is step 3 of <a href="/writing/how-to-build-an-mvp-with-ai-agents/">how to build an MVP with AI agents</a>. The decisions log it cites is described in <a href="/writing/claude-md-example-project-rules-file/">the project rules file</a>; who takes the ticket from here is in <a href="/writing/ai-agent-team-structure-solo-builder/">the team structure</a>.</p></div>
"""),

"ai-agent-team-structure-solo-builder": dict(
  tag="build", title="AI agent team structure for a solo builder: roles, handoffs and who merges",
  desc="How to structure a team of AI coding agents when one human runs it: a lead that decomposes but does not merge, workers with a mandate and a file boundary each, a reviewer, a security agent and a verifier that can only read. Why the orchestrator never writes code and no agent holds production credentials.",
  date="2026-11-04", read="8 min",
  faq=[
    ("How many agents do you run at once?","Up to five on interface work, in parallel, each in its own worktree. Agents that touch the database run one at a time, because two of them on one local database reset each other. The number that matters is not how many run, it is how many share state: the answer should be none."),
    ("Does the lead agent write code?","No. It decomposes tickets, assigns files, integrates branches and opens the pull request. The moment the orchestrator also writes code it loses the overview, and nobody is left holding it. This is the single structural decision I would not change."),
    ("Who merges to main?","The lead merges, only with every required check green on the exact commit being merged, and only after a human has reviewed what the gates say. Nothing that touches the production release process is merged by an agent; those changes go in their own pull request that only the human merges."),
    ("Is this specific to Claude Code?","The mandate per agent, the worktree per worker and the subagent model map directly onto Claude Code. The structure itself (orchestrate, specialise, review, verify, gate) works with any tool that lets you run more than one agent with different instructions."),
  ],
  body="""
<p>The first version of my agent team was one agent doing everything. It lasted four days. It could not review its own work, it held every credential, and by the second week of real scope it was rebuilding things it had already built because nothing told it they existed. The structure that replaced it is below. It is less clever than it sounds and it held for 445 pull requests.</p>

<h2>The roles</h2>
<table><thead><tr><th>Role</th><th>Mandate</th><th>Never</th></tr></thead><tbody>
<tr><td>Human</td><td>Product, design, scope, money and security. Writes tickets, answers decisions by id, approves releases</td><td>Opens pull requests, reads logs, resolves git conflicts, names things</td></tr>
<tr><td>Lead</td><td>Decomposes tickets, assigns files to workers, integrates, opens the pull request, merges when the gates are green, writes the decisions log</td><td>Writes application code. Merges anything that touches the release process</td></tr>
<tr><td>Workers (frontend, backend, data, design)</td><td>Write only in the files the lead assigned. Report in one of five states</td><td>Apply an instruction that arrives mid task from anyone but the lead; they return it and stop</td></tr>
<tr><td>Reviewer</td><td>Returns a list of concrete faults against the ticket's criteria</td><td>Opinions on style. Approving</td></tr>
<tr><td>Security</td><td>Reviews every change to data access, auth or storage; runs the full penetration test before each release and writes a verdict</td><td>Fixes what it finds. Touches production</td></tr>
<tr><td>Verifier</td><td>Receives claims as JSON, runs the verification script, reports PASS, FAIL or UNVERIFIABLE</td><td>Reads the ticket or the report. Turning a FAIL into a PASS by reasoning</td></tr>
</tbody></table>

<h2>Why the orchestrator does not write code</h2>
<p>The lead's value is the overview: which ticket is in flight, which files are assigned to whom, what the last integration changed. The moment it also writes code it loses that overview to the problem in front of it, and no one else is holding it. Every orchestrator I have seen that also implements ends up merging its own unreviewed work at two in the morning, metaphorically or not. The rule costs some speed on tiny tickets and saves the build on every large one.</p>

<h2>Why workers have a file boundary, not a topic</h2>
<p>"You do the frontend" is a topic; agents interpret topics generously. "You write in these nine files and nothing else" is a boundary a script can check in the diff. The boundary also makes parallel work safe: five workers in five worktrees cannot overwrite each other if their file sets are disjoint. When two tickets need the same file, they run in series. That is the lead's job to see, and it is why the lead needs the overview.</p>

<h2>The handoffs</h2>
<figure class="fig"><svg viewBox="0 0 720 200" role="img" aria-label="Handoffs: human writes ticket to lead; lead assigns to workers in worktrees; workers return branches to lead; lead integrates and opens PR; reviewer and security return faults to lead; verifier reads scripts; human approves release">
<g font-family="JetBrains Mono,monospace" font-size="11" fill="#9a9aae">
<defs><marker id="c" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#6b6b80"/></marker></defs>
<rect x="20" y="70" width="100" height="50" rx="8" fill="rgba(34,197,94,.08)" stroke="rgba(34,197,94,.55)"/><text x="70" y="100" text-anchor="middle" fill="#bbf7d0">ticket</text>
<rect x="170" y="70" width="100" height="50" rx="8" fill="#101018" stroke="rgba(255,255,255,.2)"/><text x="220" y="100" text-anchor="middle" fill="#f4f4f6">lead</text>
<rect x="320" y="20" width="110" height="40" rx="8" fill="#101018" stroke="rgba(255,255,255,.2)"/><text x="375" y="45" text-anchor="middle">worktree A</text>
<rect x="320" y="80" width="110" height="40" rx="8" fill="#101018" stroke="rgba(255,255,255,.2)"/><text x="375" y="105" text-anchor="middle">worktree B</text>
<rect x="320" y="140" width="110" height="40" rx="8" fill="#101018" stroke="rgba(255,255,255,.2)"/><text x="375" y="165" text-anchor="middle">worktree C</text>
<rect x="480" y="40" width="100" height="40" rx="8" fill="rgba(245,158,11,.06)" stroke="rgba(245,158,11,.5)"/><text x="530" y="65" text-anchor="middle" fill="#fcd34d">review</text>
<rect x="480" y="110" width="100" height="40" rx="8" fill="rgba(245,158,11,.06)" stroke="rgba(245,158,11,.5)"/><text x="530" y="135" text-anchor="middle" fill="#fcd34d">verify</text>
<rect x="620" y="70" width="80" height="50" rx="8" fill="rgba(34,197,94,.08)" stroke="rgba(34,197,94,.55)"/><text x="660" y="100" text-anchor="middle" fill="#bbf7d0">approve</text>
<g fill="none" stroke="#6b6b80" stroke-width="1.2" marker-end="url(#c)">
<path d="M120 95 L170 95"/><path d="M270 95 L295 95 L295 40 L320 40"/><path d="M270 95 L320 100"/><path d="M270 95 L295 95 L295 160 L320 160"/>
<path d="M430 40 L455 40 L455 60 L480 60"/><path d="M430 100 L455 100 L455 60"/><path d="M430 160 L455 160 L455 130 L480 130"/>
<path d="M580 60 L600 60 L600 95 L620 95"/><path d="M580 130 L600 130 L600 95"/>
</g>
<text x="20" y="195" font-size="10" fill="#6b6b80">every arrow is a file or a pull request, never a conversation; the lead is the only node with the full map</text>
</g></svg><figcaption>Handoffs are artefacts. If a handoff happens in chat, the next session does not know it happened.</figcaption></figure>

<p>Every handoff is a file: a ticket, a branch, a pull request, a review comment, a JSON of claims. Nothing is handed over in conversation, because conversations do not survive the session. This is also what makes the structure auditable: for any line in production I can walk back to the ticket, the decision ids it cites and the gates it passed.</p>

<h2>The two rules that hold the whole thing</h2>
<p><strong>No agent holds production credentials.</strong> Not read only, not for checking. Deployment happens through a workflow that holds the secrets; agents trigger it and read its log. An agent with a production token can route around every other gate, so the token is the gate.</p>
<p><strong>The lead merges, but not everything.</strong> Anything that executes the production release, or that could request its secrets, lives in its own pull request that only the human merges. Otherwise the agent that merges controls the thing that was supposed to control it.</p>

<h2>What I would change</h2>
<p>Earlier isolation. I lost a day when five agents shared one local database and reset each other. Workers that touch the database now get their own stack with their own ports, and that should have been the rule from day one. Everything else in the structure I would keep, including the parts that felt slow in week one and saved week five.</p>

<div class="box"><p>This is step 4 of <a href="/writing/how-to-build-an-mvp-with-ai-agents/">how to build an MVP with AI agents</a>. The operating model and the numbers are in <a href="/writing/ai-agent-teams-software-development/">AI agent teams for software development</a>; the two places a human must sit are in <a href="/writing/human-in-the-loop-coding-agents/">human in the loop for coding agents</a>. If you want this set up for your product, that is the <a href="/ai-product-builder/">AI product builder</a> engagement.</p></div>
"""),

"where-ai-coding-agents-fail": dict(
  tag="build", title="Where AI coding agents fail on real products: the eight failures I hit and the gate for each",
  desc="Eight failure patterns from seven weeks of building a production product with AI coding agents, each with the gate that now catches it: the green check that did not run, the self contradicting ticket, the test that protected a bug, the fact declared instead of produced, and four more.",
  date="2026-11-04", read="9 min",
  faq=[
    ("Are AI coding agents reliable enough for production?","Yes, with gates; no, without them. None of the eight failures below was a wrong line of code. All were an agent, or a human, trusting something that looked like proof and was not. Reliability comes from the gates, not from the model."),
    ("Which failure is the most common?","The green check that did not run. It appears in five different shapes in my lessons table: a skipped job reporting success, a suite exiting zero with a hundred skipped files, a build that compiled and did not start, a loop over zero elements that passed, a deployment marked ready that served a 404."),
    ("Do agents make the same mistakes as humans?","Mostly, faster and with more confidence. The difference is volume: ten times the changes, the same number of eyes. Which is why the fix is never reading faster; it is making proof mechanical."),
  ],
  body="""
<p>In seven weeks of building a production product with eight AI coding agents, I kept a table: one line per incident, the date, and the rule it left. It has over sixty lines. Reading them back, every one fits one of eight patterns, and none of the eight is "the agent wrote wrong code". They are all a form of trusting something that looked like proof. Here are the eight, each with the gate that now catches it.</p>

<h2>1. The green check that did not run</h2>
<p>A navigation redesign merged with eight green checks. The browser tests had not run: their path filter only triggered on four directories, and the change touched none. A skipped job reports as success. The next pull request ran them, and twelve went red, one of them a product failure. This pattern came back five times in different shapes: a test suite exiting zero with a hundred skipped files because the local stack was down, a build that compiled and then returned 500 on every request, a deployment marked ready that served a 404, a loop asserting over zero elements.</p>
<p><em>Gate:</em> a skipped check does not count as green. Before merging anything with a screen, open the run and read which steps executed and how many tests passed. Filters list what may skip, never what runs. A test that measures elements asserts how many it measured.</p>

<h2>2. The fact declared instead of produced</h2>
<p>An agent wrote "the deployment works". It had not opened it. Another wrote "CI is green" about a commit that was not the one being merged. Both sentences are grammatical and both were false, and nothing in the sentence distinguishes them from true ones.</p>
<p><em>Gate:</em> no agent declares an external fact. A script produces it as JSON with an identifier (pull request number, commit, run id, deployment id, URL) and the agent interprets the JSON. "The preview", "the build" and "CI green" are not phrases on my build. A script in FAIL is not turned into PASS by anyone's text.</p>

<h2>3. The ticket that contradicted itself</h2>
<p>Line 195 of a ticket said a phase was delivered with 42 frames. Line 240 said three of those frames did not exist. I read the second, wrote a false starting condition into a decision, and sent an agent to build something that already existed. The agent, to its credit, checked by two methods before building and found it.</p>
<p><em>Gate:</em> when a ticket says something does not exist, look before building. And a ticket with a measurable criterion and an explicit scope, validated by schema, has fewer places to contradict itself. The <a href="/writing/tickets-for-ai-agents-template/">template</a> exists because of this day.</p>

<h2>4. The test that protected the bug</h2>
<p>A comment on a test said a redirect "returns on localhost, existing behaviour, not introduced by this ticket". It was the bug: the session was lost on every magic link. The green test now asserted the broken behaviour, so fixing it would turn the test red and look like a regression. It sat there for three weeks.</p>
<p><em>Gate:</em> no test asserts a behaviour as pre existing. A suspected bug becomes a ticket the day it is seen, and the test is marked pending with the reference, never green. The same rule covers code: a known failure without a ticket does not exist, and a comment saying "escalated" is not an escalation.</p>

<h2>5. The guard that was retired because another one covered it</h2>
<p>A recovery path was removed with the argument that it was strictly weaker than a database trigger. True in an instant, false over time: the trigger ran once at account creation, the recovery ran on every visit. Removing it locked one user out permanently.</p>
<p><em>Gate:</em> before retiring a redundancy, measure when each copy runs, not only what it checks. Two guards that check the same thing at different moments are not the same guard. The pattern repeated at the design level: two decisions each removed an entry point "because it is in the other place", and together they removed both.</p>

<h2>6. The file transplant that deleted finished work</h2>
<p>Integrating three branches by copying files from each ("checkout other-branch, this file") silently removed work already in main, twice: the branches had an older base, so their copy of the file was older and the copy won. Separately, a conflict resolution script opened a file for writing before reading it, which truncates it, and two files entered main empty. Six checks passed; an empty script exits zero.</p>
<p><em>Gate:</em> a file transplant is only valid for files main has not touched since the branch base; otherwise a real three way merge. After resolving conflicts, diff against the base before pushing: a "keep both sides" resolution cannot remove lines. Generated files are regenerated, never copied.</p>

<h2>7. The number that was too round to be true</h2>
<p>Four sweeps in one day returned a false number: a contrast of 1.39 that was 12.84 measured against the real background, 61 screens without an exit that were 0, 192 instances out of size that were 236, and a grep with an escaped pipe that returned zero of zero of zero. The agent caught all four by checking the instrument before reporting.</p>
<p><em>Gate:</em> a result that confirms what you already suspected gets checked more, not less. A sweep that returns zero is repeated by another method before it is reported. And every count is stated with its scope: "zero out of size" without "on which page" is the same class of sentence as "CI green".</p>

<h2>8. The check that used the same path as the work</h2>
<p>A sweep replaced values by searching for a layer name, which is the structure. The verification searched for the rule (a masked value followed by more than four characters) and found twelve the first pass had missed. Had the verification used the same search, it would have been green by construction.</p>
<p><em>Gate:</em> verify by the criterion, never by the route the work took. A check that repeats the work does not check the work. This is also why the verifier agent never reads the ticket or the report: it only sees claims and a script.</p>

<h2>What the eight have in common</h2>
<p>None is a model failure. Each is a place where something looked like proof: a green badge, a confident sentence, a comment, a round number, a passing check. Agents multiply the volume of those things by ten, and your capacity to inspect them does not grow. The answer is not to read faster. It is to make proof mechanical: scripts that produce facts with identifiers, tests that count what they measured, filters that list what may skip, and a rules file where each of these has its date.</p>

<div class="box"><p>This is the last section of <a href="/writing/how-to-build-an-mvp-with-ai-agents/">how to build an MVP with AI agents</a>. The gates in detail are in <a href="/writing/green-check-is-not-proof/">why a green check is not proof</a>; the rules file where each incident is recorded is in <a href="/writing/claude-md-example-project-rules-file/">the project rules file</a>.</p></div>
"""),
}
