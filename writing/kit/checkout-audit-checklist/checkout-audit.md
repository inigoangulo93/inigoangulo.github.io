# 1. Rebuild the funnel per user (not per session)
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
