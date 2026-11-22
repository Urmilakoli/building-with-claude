# Record-keeping system 🗂️

**Date:** 22 Nov 2026

## The request (my universal command)

> Whatever I tell Claude to create, make a step-by-step record in my GitHub, with a proper README and every file used, as proof that I'm building with Claude's help. Also keep a digital diary in a girly vintage design. Put each thing in the right folder: the diary for personal growth and learning for future reference. Keep building an app that adapts to my learning pattern, keep making revision notes so I remember, and track my improvement in English, conversation, knowledge, research and the other skills I need.

## How it works from now on

| What I ask for | Where it goes |
|---|---|
| Anything Claude builds (pages, apps, code, automations, documents) | **This public repo**, in the matching folder, with a step-by-step README and a new line in `COMMANDS_LOG.md` |
| Personal growth, reflections, skills progress | **Private diary repo** (`building-with-claude-diary`): a diary entry and the skills tracker |
| Things I learn | **Diary repo** `revision-notes/`, plus new cards in the Smart Revision App |

### Folders in this repo
- `learning/`: lessons, study plans, learning tools
- `apps/`: apps built for me
- `automations/`: scheduled tasks and reminders
- `career/`: CV, job search, portfolio (created the first time I use it)
- `system/`: this record-keeping system

### Standard README for every project
1. The request
2. What was built
3. Steps, in order
4. Files table
5. How to run, open or rebuild it (with commands clearly marked)
6. What I learned

## Honest limits

- Claude updates these repos **when I ask for something in a chat**. It doesn't run continuously in the background between chats.
- GitHub repos can't be created from inside Claude, so I create a new repo myself the first time, then Claude pushes to it.
