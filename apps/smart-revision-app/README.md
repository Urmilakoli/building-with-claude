# Smart Revision App 🧠

**Date:** 22 Nov 2026 · **Live link:** https://claude.ai/artifact/TdQiUEFr4yC6KdBiMBsfoj

## The request

> "Keep building an app for me in the background with filters for my learning pattern … keep making revisions of the others for me to remember if I forget."

## What was built

A flashcard app built on **spaced repetition**, with all 203 topics from my lessons.

**How it adapts to me:**
- **5 memory boxes (Leitner system).** A correct answer moves a card up one box. Box 1 comes back after 1 day, then 2, 4, 8 and 16 days. A wrong answer sends the card back to box 1 for tomorrow.
- **New cards arrive 5 a day**, in the same order as my 12-week plan.
- **"Weakest subjects first" mode** puts the subjects I get wrong most often at the front of the queue.
- **Subject filters** let me focus on one area.
- **Learning pattern panel:** overall accuracy, strongest and weakest subject, and the time of day when I answer best.

**Each card works in 2 steps:**
1. Recall the big idea from memory, then reveal it. This is called active recall.
2. Answer the quiz question and read the explanation.

**Backup:** progress is saved in the browser. A backup code can be copied and pasted to restore it on another device.

## Steps, in order

1. Extracted the full content of all 11 lessons (story, idea, quiz) into one data file.
2. Designed the app: a card stage, a focus panel, mastery bars, the learning pattern panel and backup.
3. Wrote the scheduling logic: Leitner boxes, due dates, a 5-new-cards-a-day limit, and a weakest-first sort.
4. Generated `smart-revision-app.html` from `app_tpl.html` with all 203 cards embedded.
5. Tested it in a headless browser: answered a card and checked that the box, streak and counters updated.
6. Published it and added it to the "Bored? Learn Something Fun" folder.

## Files

| File | What it does |
|---|---|
| `smart-revision-app.html` | The finished app. Open it in any browser. |
| `app_tpl.html` | App template; the card data is inserted at `{{CARDS}}` |

## Future updates

As I add new topics or lessons, their cards get added here so revision keeps growing with me.
