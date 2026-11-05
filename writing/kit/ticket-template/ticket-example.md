---
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
