# Merge gate (every pull request)

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
