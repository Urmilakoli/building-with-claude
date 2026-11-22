# 🎓 Urmila's MBA University

**Date:** 22 Nov 2026 · **Live portal:** https://claude.ai/artifact/K3Hqa8uma9bZbN6g16EwzX

## The request

> "Make it as if it's my own MBA university." … "Connect Ollama also." … "Where a Python script is needed, use it." … "It should be AI-generated."

## What was built

### 1. The university portal (`index.html`)
My 11 lessons, turned into a university programme:
- **Crest, motto and student ID card**, with live credits (ECTS) and GPA
- **3 terms** (23 Nov 2026 to 14 Feb 2027), matching my 12-week plan
- **5 schools and 11 courses**, each with a code (PSY 101, ECO 201, …), credits and term. "Enter classroom" opens the lesson.
- **Transcript:** I enter my quiz score for each course, and it calculates the German grade (1.0–5.0), credits earned and GPA
- **Capstone, CAP 300:** a one-page finance and risk memo with a grading rubric
- **Diploma:** unlocks when all 60 ECTS are earned. It's clearly labelled as a personal programme, not an accredited degree.
- **AI tutor (Ollama):** explain a topic, quiz me, grade my memo, fix my English, or ask anything
- **AI-generated electives:** courses written by `mba_ai.py` appear here automatically

### 2. The AI helper (`mba_ai.py`), using Ollama on my own computer
Uses only Python's standard library. Commands:

| Command | What it does |
|---|---|
| `python3 mba_ai.py check` | Checks that Ollama is running and lists my models |
| `python3 mba_ai.py serve` | Opens the portal at `http://localhost:8000` with the AI tutor connected |
| `python3 mba_ai.py new-course "Corporate Finance" --code "FIN 310"` | The AI writes a full new course (syllabus, then each level) as an interactive lesson |
| `python3 mba_ai.py core` | The AI writes 8 classic MBA core courses: Accounting, Corporate Finance, Marketing, Strategy, Operations, Leadership, Financial Risk Management, Entrepreneurship |
| `python3 mba_ai.py grade memo.txt` | The AI grades my capstone memo against the rubric |
| `python3 mba_ai.py ask "What is working capital?"` | Asks the AI a quick question |

Add `--model llama3.2` before the command to choose a model.

## Setup on my computer (one time)

Commands to run in Terminal (macOS) or PowerShell (Windows):

```bash
# 1. Install Ollama from https://ollama.com/download and open the app, then:
ollama pull llama3.2

# 2. Get this repo
git clone https://github.com/Urmilakoli/building-with-claude.git
cd building-with-claude/learning/mba-university

# 3. Check, then open the university with the AI tutor connected
python3 mba_ai.py check
python3 mba_ai.py serve
```

On Windows, use `python` instead of `python3`.

Then, in a second terminal, generate the MBA core courses. This takes a while; each level is a separate AI call:

```bash
cd building-with-claude/learning/mba-university
python3 mba_ai.py core
```

### Why the tutor only works locally
The online portal can't reach programs on my computer (the browser blocks it). Opened from `http://localhost:8000`, it can, and Ollama allows localhost by default, so no extra settings are needed.

## Steps, in order

1. Mapped the 11 lessons to schools, course codes and ECTS credits (in proportion to the number of topics, 53.5 credits) plus a 6.5-credit capstone, for 60 ECTS in total.
2. Mapped courses to 3 terms using the dates in my learning plan.
3. Designed the portal: crest, ID card, calendar, courses, transcript with German grading, capstone and diploma.
4. Added the Ollama tutor: it calls `http://localhost:11434/api/tags` to list models and `/api/chat` to answer, with 5 tutor modes.
5. Wrote `mba_ai.py`. To keep small local models reliable, it generates each course in 2 stages (syllabus first, then each level separately), asks for JSON, validates every field, and retries up to 3 times. It then builds the lesson with the same template as my 11 original lessons.
6. **Tested without a real Ollama:** ran a mock Ollama server and checked `check`, `new-course` (generated a 4-level course that rendered with no errors), and `grade`. Opened the portal in headless Chrome to confirm the tutor connects and the AI elective appears.
7. Published the portal and saved everything here.

## Files

| File | What it does |
|---|---|
| `index.html` | The university portal |
| `portal_template.html` | Portal template (course data is inserted into it) |
| `mba_ai.py` | AI helper using Ollama: serve, new-course, core, grade, ask |
| `courses/` | AI-generated courses (`.html`, `.json`) and `index.json`, the list the portal reads |

## Honest notes
- AI-generated courses come from a small local model, so they're marked "AI-generated: double-check facts". The 11 original courses were researched and fact-checked.
- Grades are self-reported from quiz scores; the lessons and the portal can't share data automatically.

## What I learned
- How to connect a web page to a local AI model through Ollama's API.
- Why browsers block web pages from calling programs on your computer, and how running a local server solves that.
- How to make AI output reliable: structured JSON, validation and retries.
