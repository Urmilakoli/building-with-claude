# 12-week learning plan 📅

**Date:** 21 Nov 2026 · **Live link:** https://claude.ai/artifact/FWwH25BqRkGTUpdQ4rfeaN

## The request

> "Now compile all the topics I gave you and make a plan for me so I can learn all of this."

## What was built

One page that brings together all **203 topics** from 11 lessons:
- **Today card:** the next 3 topics, each linking straight to its section of the lesson
- **12 weeks:** 6 study days (3 levels each, about 20 minutes) plus a Sunday games-and-review day
- **Checkboxes** to tick off each day (saved in the browser)
- **Full topic library**, grouped by lesson

Study order: Psychology → Think Smarter → Economics → IT → Science → English → Mesopotamia → Empires → Politics → Geopolitics → Earth Science.

## Steps, in order

1. Extracted every topic from the 11 finished lessons into `topics.json`, using a small Node.js script.
2. Wrote `plan_build.py` to put the topics in study order and split them into days of 3, with 6 study days and 1 review day per week.
3. Designed `plan_tpl.html`: the page layout, the Today card and the checkbox logic.
4. Generated `learning-plan.html`, tested it in a headless browser, and published it.

## Files

| File | What it does |
|---|---|
| `learning-plan.html` | The finished plan page |
| `plan_tpl.html` | Page template |
| `plan_build.py` | Builds the schedule from `topics.json` |
| `topics.json` | Every lesson's topic list |

## How to rebuild

Commands to run in a terminal:

```bash
cd learning/learning-plan
python3 plan_build.py
```
