# MVP scope: <product>

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
