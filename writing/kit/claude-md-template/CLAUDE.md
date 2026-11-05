# <Product name>

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
