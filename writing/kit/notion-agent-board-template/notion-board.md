# Tasks
- Task (title): "<repo ticket number> <verb + object>"
- Status (select): Backlog / To do / In progress / Blocked / Done / Archived
- Owner (person): a real workspace member. Never an agent, never a typed name.
- Area (select): Product and tech / Legal / Sales and growth / Brand /
  Company and finance / Operations
- Priority (select): P0 critical (no launch without it) / P1 high (needed
  for the demo) / P2 medium (can wait a week) / P3 low
- Expected result (text): one sentence. Without it the card does not move
  to To do.
- Acceptance criteria (text): optional summary; the full list is on the card.
- Link (url): the pull request
- Due (date)
- ID (unique id, automatic)

# Decisions
- Decision (title): the question and the answer in one line
- Status (select): In force / Under discussion / Revoked
- Context (text): why it was decided this way
- Proposed by (person)
- Area (select): same options as Tasks
- Date (date)

# Meetings
- Meeting (title), Date (date), Attendees (person)
- Rule: notes are context only. Anything decided moves to Decisions,
  anything to do moves to Tasks.

# Working agreement
- The repo instructs, Notion remembers. No agent instructions in Notion.
- A decision that is not in Decisions does not exist.
- At most 3 cards in progress per person.
- Blocked is raised in chat when it happens, not at the meeting.
- Weekly meeting, 30 minutes: walk the board per person, record decisions,
  move cards. Everyone updates their cards before, not during.
- Done = merged pull request + reviewer PASS.
- A closed card is never reopened. Create a new one and link it.
