# Bored? Learn Something Fun 🎈

**Date:** 21 Nov 2026 · **Built with:** Claude · **Type:** interactive HTML lessons

## The request

> "Make a folder where you teach me something when I get bored, in a fun way. After this I will give the topics you need to focus on."

I then sent topic lists as text and as screenshots of Instagram posts I'd saved.

## What was built

11 game-style lessons, **203 topics** in total. Each topic is a "level" with:
- **The story:** a famous experiment, event or person
- **The big idea:** the concept, explained simply and accurately
- **Spot it in real life:** where it shows up in everyday life (often in Berlin)
- **Try it today:** one small action
- **One quiz question**, worth XP, with an explanation

Each lesson also has 2 mini-games and a rank system.

| Lesson | Topics | Live link |
|---|---|---|
| Mind Arcade: Psychology | 25 | https://claude.ai/artifact/2j2kTpQTVzwqUQkH7ZJjfA |
| Word Arcade: English | 14 | https://claude.ai/artifact/5VWy4SVJEHBkzkavoKhRUL |
| Lab Arcade: Science | 10 | https://claude.ai/artifact/GUEVYd9YeVn23BpZrftARm |
| Code Arcade: IT | 11 | https://claude.ai/artifact/TZ1pbNoXm5BJCHCPLWy4Jr |
| Money Arcade: Economics | 27 | https://claude.ai/artifact/5dRYjEPsuwj7jiKDPFfNfb |
| Time Arcade: Mesopotamia | 12 | https://claude.ai/artifact/WAzajAAcpUDwZp2zVAt371 |
| Empire Arcade: History | 13 | https://claude.ai/artifact/4fgGr5zEDB7ytQ1u4c5qEH |
| Globe Arcade: Geopolitics | 28 | https://claude.ai/artifact/NvhhgERnf4JdRushDPx3FZ |
| Civic Arcade: Politics | 28 | https://claude.ai/artifact/D1BmxpxPp3egQ6rkxfiNzb |
| Earth Arcade: Earth Science | 16 | https://claude.ai/artifact/Ayk7LEJ1frj8qzvBra4uW4 |
| Think Smarter Arcade | 19 | https://claude.ai/artifact/K2h8eQpCzJLXBrDYAsessb |

*The live links are private to my account. The HTML files in [`lessons/`](lessons) work for anyone.*

## Steps, in order

1. **Created a private folder** on my Claude Artifacts page to hold all lessons.
2. **Lesson 1 (psychology)** was hand-written as one HTML file: topic data in a JavaScript array, cards rendered from it, quizzes, XP saved in the browser (`localStorage`), and 2 games (Stroop test, false-memory test).
3. **Checked current facts** with web searches before writing (for example the latest WMO climate figures, the ECB's interest rate decisions, euro area inflation, and the Pergamon Museum reopening date).
4. **Turned Lesson 2 into a reusable template** ([`build/template.html`](build/template.html)) with placeholders for colours, fonts, worlds, topics and games.
5. **Wrote a build script** ([`build/build.py`](build/build.py)) that takes a Python data file (`m3.py` … `m11.py`) and generates a full lesson page.
6. **Tested every page** in a headless browser (jsdom): checked that cards render, quizzes score and games run without JavaScript errors.
7. **Published each page** as an artifact and moved it into the folder.

## Files

| File | What it does |
|---|---|
| `lessons/*.html` | The 11 finished lessons. Open in any browser. |
| `build/template.html` | Shared page template with placeholders |
| `build/build.py` | Generates a lesson from a data file |
| `build/m3.py` … `build/m11.py` | Content for lessons 3–11 (worlds, topics, quizzes, games) |

## How to rebuild a lesson

Commands to run in a terminal, from the `build/` folder:

```bash
cd learning/fun-lessons/build
python3 build.py m5.py ../lessons/money-arcade-05.html
```

## What I learned

- Separating **content** (data files) from **design** (template) makes it fast to build many similar pages.
- Facts that change, like interest rates and climate figures, need checking against official sources before they're written down.
- Every page needs testing before it ships, even a "fun" one.
