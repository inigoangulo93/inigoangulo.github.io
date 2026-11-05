-- Assumes events(user_id, event, ts). Rename to your schema.
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
