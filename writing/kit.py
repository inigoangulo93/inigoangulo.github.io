# The Kit: templates, checklists and prompts from the method, ready to copy.
# Imported by build.py, which links articles to their kit piece and writes the kit pages.
# Every piece is a neutral version: no client names, no internal artefact names.
# To change a piece: edit its text, bump "version" and add a line at the top of "changelog".

CAPS = {"build": "Build", "lead": "Lead", "optimize": "Optimize"}

KIT = {

"claude-md-template": dict(
  cap="build", kind="Template", file="CLAUDE.md", version="1.0",
  title="CLAUDE.md template: the project rules file every agent session reads",
  short="CLAUDE.md template",
  desc="A copyable CLAUDE.md template for AI coding agents: thesis, sources of truth, closed stack, hard rules with the incident behind each, task states, escalation format and conventions.",
  meta='Copyable CLAUDE.md template for AI coding agents: thesis, sources of truth, closed stack, hard rules, task states, escalation format and conventions.',
  card="The seven sections every agent session inherits, in the order an agent reads them, with nine neutral hard rules to start from.",
  article=("claude-md-example-project-rules-file", "CLAUDE.md example: the project rules file, explained"),
  related=["ticket-template", "escalation-format", "release-gate-checklist"],
  use=[
    "Before the first line of code, at the root of the repository.",
    "Fill the angle brackets. Delete nothing structural: an empty section is a decision you have not taken yet.",
    "Every time an incident teaches you something, add a numbered rule with the date and one line on what happened.",
  ],
  blocks=[("The template", "CLAUDE.md", r"""# <Product name>

## Thesis
The user can trust <product> for <one sentence: what it is for, not what it does>.
Principle: the model proposes, a person decides, the system records who.

## Read before touching anything
- docs/architecture.md: how the system fits together
- docs/domain-model.md: entities, states, invariants
- docs/permissions.md: who may see and do what, per role
- docs/design.md: tokens, components, screens
- docs/decisions.md: every decision, by id. Cite the id; do not reopen it.

## Stack, closed
<framework>, <database>, <auth>, <hosting>, <test runner>. Nothing else.
Amendments: <decision id and one line, or "none">.

## Hard rules
1. Build nothing for a hypothetical need. Every piece of infrastructure
   names the MVP requirement it serves. No requirement, no build.
2. Never real data. Seeds, tests and screenshots use synthetic records only.
3. Never secrets in the repository. Production secrets live in the
   deployment environment and are never in an agent's reach.
4. Row level security on every new table, with a test that runs as the
   role that must not get in. No test, no pull request.
5. What a role must not see does not leave the server. Hiding a column
   in the frontend is not a guarantee.
6. No model output writes to an entity. It writes to a proposals table;
   a person decides; the application applies it and logs who decided.
7. Never say a test passed if it was not run. Never say a migration is
   safe without reading it. Never invent a requirement.
8. No agent declares an external fact. A script produces it as JSON and
   the agent interprets it. A run id and a URL, not "CI is green".
9. A test never asserts a behaviour as existing and not introduced by
   this ticket. A suspected bug becomes a ticket; the test is marked
   pending, never green.
<10. Your next rule. YYYY-MM-DD: the incident that produced it.>

## Task states
Report a task only as one of: VERIFIED, IMPLEMENTED, NEEDS_REVIEW,
BLOCKED, DECISION_REQUIRED. "Done" is not a state.
VERIFIED means: the acceptance criterion was checked and the evidence
(run id, URL, query output) is attached.

## Escalation format
DECISION <ticket>-<n>: the question in one line
A) option  B) option  C) option
RECOMMENDATION: <letter>. WHY: one line. IF UNDECIDED: what happens

## Conventions
- Files: <where features, tests and migrations live>
- Commits: <format>, one ticket per pull request, ticket id in the title
- Language: code and commits in <language>, interface in <language>
- A rule that stops applying is struck through with the reason, never deleted.
""")],
  prompt=("Paste into a new session", r"""Read CLAUDE.md and the five documents it lists under "Read before touching anything".
Then, before doing any work, reply with:
1. The thesis in your own words, in one sentence.
2. The three hard rules most likely to apply to the ticket I am about to give you, and why.
3. Anything in CLAUDE.md that contradicts one of the five documents. If nothing does, say so.
Do not write code in this reply."""),
  changelog=[("1.0", "2026-11-05", "First public version. Nine rules, neutralised from a seven week build where the file grew from 12 rules to 29. Rule 7 came from a suite reported green that had skipped every integration test; rule 9 from a green test sitting on top of a bug for three weeks.")],
),

"ticket-template": dict(
  cap="build", kind="Template", file="ticket.md", version="1.0",
  title="Ticket template for AI agents: no room for the reasonable guess",
  short="Ticket template for agents",
  desc="A copyable ticket template for AI coding agents: validated frontmatter, a measurable acceptance criterion, an explicit out of scope list and the decisions already taken, with a filled example.",
  meta='Copyable ticket template for AI coding agents: validated frontmatter, measurable acceptance criteria, explicit out of scope list, and a filled example.',
  card="Frontmatter a script can validate, plus the three fields that stop agents inventing requirements. Blank and filled versions.",
  article=("tickets-for-ai-agents-template", "Writing tickets for AI agents: the template"),
  related=["claude-md-template", "escalation-format", "mvp-scope-one-pager"],
  use=[
    "The human writes the ticket. The lead agent decomposes it. An agent writing its own acceptance criterion is grading its own homework.",
    "Every line under \"What done looks like\" has a number, a role or a test in it. If it does not, it is not a criterion.",
    "Open questions means the ticket is blocked, not started.",
  ],
  blocks=[
("Blank", "ticket.md", r"""---
id: <number>
title: <verb + object, one line>
status: todo
area: <area>
depends_on: [<ticket ids>]
decisions: [<decision ids>]
board: <url of the row on the board>
---

## Why
One sentence linking this to the thesis.

## What done looks like (measurable)
- <role> does <action>; <observable result with a number or a test>.
- <the permission case: who must NOT see or do this, proven by a test that runs as them>.
- <the audit case: what is recorded, by whom, when>.
- Browser test on mobile and desktop passes.

## Out of scope (explicit)
- <adjacent feature> (ticket <id>).
- <adjacent feature>.

## Decisions already taken
- <id>: <one line>.

## Open questions
- None. (If there were, the ticket would be blocked, not started.)
"""),
("Filled example", "ticket-example.md", r"""---
id: 143
title: Invite a teammate to a collection
status: todo
area: team
depends_on: [131]
decisions: [0088, 0091]
board: <url of the row on the board>
---

## Why
Shared collections are the thesis for teams: one record, several people, every change attributed.

## What done looks like (measurable)
- A member with the owner role sends an invitation to an email; the
  invitee receives it within 60 seconds in the test mailbox.
- A pending invitation grants zero rows of any table, proven by a test
  that runs as the pending user.
- Accepting makes the invitee a member with the role chosen by the
  owner; the audit log records who invited and who accepted, with
  timestamps.
- Browser test on mobile and desktop passes.

## Out of scope (explicit)
- Resending or expiring invitations (ticket 144).
- Inviting by link.
- Any change to the roles themselves (decision 0088 fixes them).

## Decisions already taken
- 0088: the four roles and what each may do.
- 0091: invitations are per collection, not per account.

## Open questions
- None.
""")],
  prompt=("Paste before the agent starts a ticket", r"""Before writing any code, review ticket <id> against CLAUDE.md and the decisions log.
Return the ticket to me, without starting, if any of these is true:
- A line under "What done looks like" has no number, role or test in it.
- Two lines contradict each other, anywhere in the ticket.
- The work would touch something listed under "Out of scope".
- It needs a product decision that is not in "Decisions already taken".
If you return it, use the escalation format: one DECISION per gap, three options, your recommendation.
If none is true, reply READY and list the tests you will write first."""),
  changelog=[("1.0", "2026-11-05", "First public version. The template behind every ticket of a seven week build; the out of scope list was the single most effective scope control.")],
),

"escalation-format": dict(
  cap="build", kind="Format", file="escalation.md", version="1.0",
  title="Escalation format for AI agents: decisions in seconds, findable later",
  short="Escalation and decision format",
  desc="A fixed format for AI coding agents to stop and ask a human: stable id, three options, a recommendation, what happens if nobody answers, and the decisions log entry it produces.",
  meta='A fixed format for AI coding agents to stop and ask a human: stable id, three options, a recommendation, and the decisions log entry it produces.',
  card="How an agent stops at a real decision: an id, three options, a recommendation. You answer with a letter.",
  article=("human-in-the-loop-coding-agents", "Human in the loop for coding agents: the two gates"),
  related=["claude-md-template", "ticket-template", "release-gate-checklist"],
  use=[
    "Put the format in CLAUDE.md so every session knows it.",
    "Answer with the id and a letter: \"014-3 B\". Anything longer belongs in the log entry.",
    "The lead agent writes the log entry, citing the id. A decision that only lives in a chat is gone next session.",
  ],
  blocks=[
("The format", "escalation.md", r"""DECISION <ticket>-<n>: the question in one line
A) option  B) option  C) option
RECOMMENDATION: <letter>. WHY: one line. IF UNDECIDED: what happens

DECISIONS REQUIRED: <id>, <id>
ACTIONS FOR YOU: <what to open or check, with the URL>
"""),
("Decisions log entry", "decisions.md", r"""## <ticket>-<n>: <the question in one line>
Date: YYYY-MM-DD
Asked by: <agent role> while working on ticket <id>
Options: A) ...  B) ...  C) ...
Decided: <letter>, by <person>
Why: <one line, from the recommendation or the answer>
Consequences: <what this now rules in or out; tickets that must cite it>
""")],
  prompt=("Paste into CLAUDE.md or a session", r"""When you reach a decision that changes what the product does, who can see what, or what we store, stop and escalate.
Do not guess and do not write paragraphs. Use exactly this format:

DECISION <ticket>-<n>: the question in one line
A) option  B) option  C) option
RECOMMENDATION: <letter>. WHY: one line. IF UNDECIDED: what happens

Group every open decision at the end of your reply under DECISIONS REQUIRED.
Implementation choices that change nothing a user or a role would notice are yours: take them and mention them in one line."""),
  changelog=[("1.0", "2026-11-05", "First public version. Over seven weeks this format carried more than 170 decisions, most answered in under a minute, every one findable later by id.")],
),

"release-gate-checklist": dict(
  cap="build", kind="Checklist", file="release-gate.md", version="1.0",
  title="Release gate checklist for AI agent teams: what counts as proof",
  short="Release gate checklist",
  desc="A merge and release gate checklist for teams shipping with AI coding agents: required checks, skipped jobs that report green, the security verdict on the exact commit, and the human promotion step.",
  meta='Merge and release gate checklist for teams shipping with AI coding agents: skipped jobs that report green, the security verdict, the human promotion.',
  card="The merge gate and the release gate, as checkboxes. Written for the day a skipped check reports green.",
  article=("green-check-is-not-proof", "Why a green check is not proof"),
  related=["claude-md-template", "escalation-format", "ticket-template"],
  use=[
    "Merge gate on every pull request. Release gate before every promotion to production.",
    "A box is ticked with evidence (a run id, a URL, a query output), never with a sentence.",
    "The person who promotes is never the agent that built it, by construction: no agent holds the credentials the workflow uses.",
  ],
  blocks=[("The checklist", "release-gate.md", r"""# Merge gate (every pull request)

- [ ] Lint passes, including the house rules.
- [ ] Types pass in strict mode.
- [ ] Unit, integration and database tests pass. Run id: <id>
- [ ] Secrets scan passes on every commit of the branch, not only the last.
- [ ] Browser tests RAN on this change. Opened the run: <n> steps executed,
      <n> tests passed. A skipped job reports as success; it is not a pass.
- [ ] The browser job filter lists what may skip it, not what triggers it.
- [ ] On any change to database security: one isolation rule was broken on
      purpose and the suite went red. If it stayed green, the tests do not
      test what they claim.
- [ ] Red checks read from the annotations first. Seven failures in four
      seconds are usually one cause, not seven bugs.

# Release gate (every promotion to production)

- [ ] All required checks green on the exact commit being promoted, not an
      earlier one. Commit: <sha>
- [ ] Security agent penetration test against local and staging (never
      production) says PASS for that commit. Report: <link>
      A FAIL blocks the promotion like a red check, even if it is outside
      the feature being shipped.
- [ ] Data compatibility queries run before promotion. Output: <link>
- [ ] No known failure without a ticket. A comment saying "escalated" is
      not an escalation.
- [ ] Promotion is one human command, logged with who and when.
- [ ] The approver is not the agent that built it.
""")],
  prompt=("Paste for the reviewer agent", r"""You are reviewing pull request <number> against the merge gate in docs/release-gate.md.
For every box, report PASS or FAIL with the evidence: a run id, a step count, a URL or a query output.
A job that was skipped is FAIL, not PASS. Say which jobs were skipped and why.
If the change touches database security, break one isolation rule on purpose in a scratch branch,
run the suite, and report whether it went red. If it stayed green, that is the most important finding of the review.
Do not write "looks good". End with: VERDICT: PASS or VERDICT: FAIL, and the boxes that failed."""),
  changelog=[("1.0", "2026-11-05", "First public version. The skipped check rule dates from a navigation redesign merged with eight green checks while the browser tests had not run; twelve went red on the next pull request.")],
),

"mvp-scope-one-pager": dict(
  cap="lead", kind="Template", file="mvp-scope.md", version="1.0",
  title="MVP scope template: one page of invariants before the first prompt",
  short="MVP scope one pager",
  desc="A one page MVP scope template for products built with AI agents: the thesis, one workflow end to end, invariants marked by where they are enforced, and the explicit list of what is not built.",
  meta='One page MVP scope template for products built with AI agents: thesis, one workflow, invariants by where they are enforced, and what is not built.',
  card="Thesis, one workflow, invariants and what is not built. The page that stops a fast build from sprawling.",
  article=("scope-an-mvp-for-ai-agents", "How to scope an MVP for AI agents"),
  related=["claude-md-template", "ticket-template", "escalation-format"],
  use=[
    "Write it before you touch an agent. If you cannot fill it, the week you would spend building is better spent here.",
    "Mark every invariant as enforced in the database, the application, or both. Never only the interface.",
    "Every line under \"Not built\" has a reason. That reason is what turns the tenth proposal into a one line reply.",
  ],
  blocks=[("The template", "mvp-scope.md", r"""# MVP scope: <product>

## 1. Thesis (one sentence)
The user can trust <product> for <what it is for, not what it does>.
Test for every ticket: does this serve the sentence above? If not, it is not built.

## 2. The one workflow, end to end
A path a customer would pay for on its own:
<actor> <does> -> <system does> -> <actor confirms> -> <the record exists, with an audit trail>.
Screens: <list>
Data: <entities touched>
Roles involved: <list>
The second workflow is: <name it here, so it is visibly out>.

## 3. Invariants (hold in every state)
| Invariant | Enforced in |
|---|---|
| <e.g. a pending account reads zero rows of any table> | database |
| <e.g. no model output writes to an entity; a person decides; who is recorded> | database + application |
| <e.g. every business write leaves an audit entry> | database |
| <e.g. sensitive identifiers encrypted before the database, never searchable> | application |
Never "interface only". This table becomes the permissions matrix,
and the permissions matrix becomes the security tests.

## 4. Not built (each with a reason)
- <no search by sensitive identifier>: <reason>
- <no infrastructure for a hypothetical need>: <reason>
- <no queue, no cache layer until a measurement justifies it>: <reason>
- <...>

## What this page produces
CLAUDE.md (thesis, stack, hard rules), the domain model with its
invariants, and the permissions matrix. Tickets cite them; they do not restate them.
""")],
  prompt=("Paste to pressure test the scope", r"""Here is my MVP scope (below). Do not suggest features. Instead:
1. Name every place where the workflow implies a second workflow I have not listed under "Not built".
2. For each invariant, describe one state of the product where it would break, and whether "Enforced in" covers it.
3. List product decisions the workflow needs that the page does not take, in the escalation format.
4. Find any line under "Not built" without a reason.
Be terse. One line per finding.

<paste the scope>"""),
  changelog=[("1.0", "2026-11-05", "First public version. The page took a week to write on a seven week build and was the most valuable week of it.")],
),

"checkout-audit-checklist": dict(
  cap="optimize", kind="Checklist", file="checkout-audit.md", version="1.0",
  title="Checkout audit checklist: find the leak between the steps",
  short="Checkout audit checklist",
  desc="A checkout and funnel audit checklist: rebuild the funnel per user, measure re-entry and time to convert, instrument the gaps, then test against a one page hypothesis. With a SQL sketch.",
  meta='Checkout audit checklist: rebuild the funnel per user, measure re-entry and time to convert, instrument the gaps, then test. With a SQL sketch.',
  card="Rebuild the funnel per user, find the re-entry gap, instrument it, then test with a written hypothesis. SQL included.",
  article=("instrument-the-gaps-not-the-stages", "Instrument the gaps, not the stages"),
  related=["mvp-scope-one-pager", "release-gate-checklist", "escalation-format"],
  use=[
    "Run it before anyone proposes a redesign of payment. Payment is rarely the problem.",
    "The three numbers in step 1 decide where to look. Do not skip to experiments.",
    "Every experiment gets the hypothesis page before anything is built. No peeking, no winners called because the quarter is ending.",
  ],
  blocks=[
("The checklist", "checkout-audit.md", r"""# 1. Rebuild the funnel per user (not per session)
- [ ] Every user who reached the final step in the period, events walked backwards.
- [ ] The same for users who reached checkout and did not convert.
- [ ] Entries per converter. Median above one: re-entry is your biggest surface.
- [ ] Time to convert. Hours, not minutes: the session model is lying to you.
- [ ] Exit step on the first visit: tells you where to put the memory.
- [ ] Watched session recordings of at least ten re-entries, with your own eyes.

# 2. Look for the gaps the stage counters miss
- [ ] Back button: two checkout entries, one person, counted as a drop.
- [ ] Tab switch: session timed out, the return starts again at step one.
- [ ] Return visit: cart, choices and progress lost between days.
- [ ] Price changed between visits, or between product page and last step.
- [ ] A form that cleared.

# 3. Check the commitment moment
- [ ] A returning visitor lands on the step they left, choices intact, one line acknowledging it.
- [ ] Cancellation terms and what happens after booking shown where the decision is made, not in a tab.
- [ ] Everything that can be asked after payment is asked after payment.
- [ ] The total on the product page is the total at the end. Any change explained before the button.

# 4. Instrument what you found
- [ ] checkout_reentry {step, hours_since_last_exit}
- [ ] cart_restored {items, age_hours}
- [ ] price_changed_since_last_visit {delta, reason}

# 5. One page per experiment, before anything is built
- We believe: <the change and the user behaviour it addresses>
- Because: <the evidence from steps 1 to 4>
- Primary metric: <one>   Guardrail: <one>
- Sample size: <n per arm>   Read date: <YYYY-MM-DD>
- If it loses: <what door this closes>
"""),
("SQL sketch: funnel per user", "funnel-per-user.sql", r"""-- Assumes events(user_id, event, ts). Rename to your schema.
-- One row per user who reached checkout in the period.
with checkout_users as (
  select user_id,
         min(ts) filter (where event = 'checkout_start') as first_checkout,
         max(ts) filter (where event = 'purchase')       as purchased_at,
         count(*) filter (where event = 'checkout_start') as checkout_entries
  from events
  where ts >= date '2026-01-01' and ts < date '2026-02-01'
  group by user_id
  having count(*) filter (where event = 'checkout_start') > 0
)
select
  purchased_at is not null                                   as converted,
  count(*)                                                   as users,
  percentile_cont(0.5) within group (order by checkout_entries) as median_entries,
  avg((checkout_entries > 1)::int)                           as share_reentered,
  percentile_cont(0.5) within group (
    order by extract(epoch from purchased_at - first_checkout) / 3600
  )                                                          as median_hours_to_convert
from checkout_users
group by 1;
""")],
  prompt=("Paste with your event schema", r"""Here is my analytics event schema (below). Write one query that rebuilds the checkout funnel per user, not per session, for <period>.
For converters and non converters separately, return: users, median checkout entries, share with more than one entry,
median hours from first checkout entry to purchase, and the most common exit step on the first visit.
State every assumption about event names. Do not invent columns that are not in the schema.

<paste the schema>"""),
  changelog=[("1.0", "2026-11-05", "First public version. The method behind ten experiments and +11% checkout conversion across four EU markets, where 38% of converters had left checkout and come back.")],
),
}

ORDER = ["claude-md-template", "ticket-template", "escalation-format", "release-gate-checklist", "mvp-scope-one-pager", "checkout-audit-checklist"]

# article slug -> kit slug, for the "copy the template" box inside articles
ARTICLE_TO_KIT = {}
for _s in ORDER:
    ARTICLE_TO_KIT.setdefault(KIT[_s]["article"][0], _s)
ARTICLE_TO_KIT.update({"how-to-build-an-mvp-with-ai-agents": "mvp-scope-one-pager",
                       "checkout-conversion-ten-experiments": "checkout-audit-checklist",
                       "ticket-to-production-in-five-hours": "release-gate-checklist"})
