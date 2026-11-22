# Daily learning reminder ⏰

**Date:** 21 Nov 2026 · **Type:** Claude scheduled task with push notifications

## The request

I said yes to a daily reminder at **8:00 (Berlin time)**, with the plan starting **Monday 23 Nov 2026**.

## What was built

A scheduled task that runs every morning at **7:38** Berlin time. It's set slightly before 8:00 because tasks scheduled exactly on the hour can be delayed.
- It looks up today's date in a fixed schedule (23 Nov 2026 to 10 Feb 2027).
- It sends a push notification with that day's 3 topics and their links.
- On Sundays it sends a games-and-review message, and on 10 Feb 2027 it sends a "plan complete" message.

## Steps, in order

1. Asked me two questions: what time, and which start date.
2. Generated a dated schedule from the learning plan with Python: Monday to Saturday are study days, Sunday is review.
3. Spot-checked the dates and day numbers against the plan page.
4. Wrote the task instructions ([`reminder-instructions.txt`](reminder-instructions.txt)) and created the scheduled task with push notifications turned on.

## Files

| File | What it does |
|---|---|
| `reminder-instructions.txt` | The exact instructions the scheduled task follows each morning, including the full schedule |

## Limitation

The reminder follows calendar dates, not my ticks on the plan page. If I fall behind, I continue from the first unticked day on the plan page.
