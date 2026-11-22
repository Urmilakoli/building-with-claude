#!/usr/bin/env python3
"""
Urmila's MBA University: AI helper powered by Ollama (runs on your own computer).

Commands to run in Terminal, from the learning/mba-university folder:

  python3 mba_ai.py check                       # is Ollama running? which models do I have?
  python3 mba_ai.py serve                       # open the university portal with the AI tutor connected
  python3 mba_ai.py new-course "Corporate Finance" --code "FIN 310"   # AI writes a new course
  python3 mba_ai.py core                        # AI writes the 8 classic MBA core courses
  python3 mba_ai.py grade my_memo.txt           # AI grades your capstone memo
  python3 mba_ai.py ask "What is working capital?"

Options: put --model before the command, e.g.  python3 mba_ai.py --model llama3.2 core
         (default: the first model you have installed). new-course and core also take --topics 8

Only Python's standard library is needed. AI-generated courses are marked "AI-generated"
in the portal: small local models can make mistakes, so double-check facts and numbers.
"""
import argparse, json, os, re, sys, time, urllib.request, urllib.error, webbrowser, http.server, socketserver, functools

HERE = os.path.dirname(os.path.abspath(__file__))
OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
COURSES_DIR = os.path.join(HERE, "courses")
BUILD_DIR = os.path.join(HERE, "..", "fun-lessons", "build")

CORE = [
    ("ACC 301", "Financial Accounting", "Balance sheets, income statements, cash flow and how to read a company's numbers"),
    ("FIN 310", "Corporate Finance", "Time value of money, valuation, capital budgeting, cost of capital and risk/return"),
    ("MKT 320", "Marketing Management", "Customers, segmentation, positioning, pricing, branding and digital marketing"),
    ("STR 330", "Business Strategy", "Competitive advantage, Porter's five forces, business models and growth strategy"),
    ("OPS 340", "Operations & Supply Chain", "Processes, capacity, quality, inventory and supply chains"),
    ("LDR 350", "Leadership & Organisational Behaviour", "Motivation, teams, culture, leadership styles and change"),
    ("RSK 360", "Financial Risk Management", "Credit, market, liquidity and operational risk, Basel rules, KYC/AML and model risk"),
    ("ENT 370", "Entrepreneurship & Innovation", "Opportunity spotting, lean start-up, MVPs, funding and pitching"),
]

PALETTES = [  # field, fieldInk, sun, acc, accD, soft, softD, line, lineD, tint, shadow, kick
    ("#6d1a36", "#ffffff", "#a3c3a2", "#6d1a36", "#f2a9bd", "#f7eff1", "#231a1c", "#e8d6db", "#3b2b2f", "#f1e3e7", "#3e0d1e", "#ffd9e3"),
    ("#2d5a4a", "#ffffff", "#f2c14e", "#2d5a4a", "#9fd6c1", "#edf6f2", "#16201c", "#d3e8df", "#2a3d35", "#d9efe5", "#1b3a2f", "#d9f2e8"),
    ("#3a4a8c", "#ffffff", "#ff9b3d", "#3a4a8c", "#aab8f2", "#eef0fa", "#171a28", "#d9ddf2", "#2c3150", "#dde2f6", "#252f5e", "#dfe4ff"),
]

SYSTEM = ("You are an expert MBA professor writing accurate, engaging teaching material for Urmila, "
          "an MSc Data Analytics graduate in Berlin with banking KYC/AML experience, aiming for finance and risk roles. "
          "Use correct, well-established facts only. Never invent statistics, studies or quotes. If unsure of a number, describe it in words instead.")


# ---------- Ollama helpers ----------
def http_json(url, payload=None, timeout=600):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def models():
    try:
        return [m["name"] for m in http_json(OLLAMA + "/api/tags", timeout=5).get("models", [])]
    except (urllib.error.URLError, ConnectionError, TimeoutError, OSError):
        return None

def pick_model(wanted):
    ms = models()
    if ms is None:
        sys.exit("Ollama isn't running. Start the Ollama app (or run: ollama serve), then try again.")
    if not ms:
        sys.exit("Ollama is running but has no models. Run: ollama pull llama3.2")
    if wanted:
        if wanted in ms or any(m.split(":")[0] == wanted for m in ms):
            return next(m for m in ms if m == wanted or m.split(":")[0] == wanted)
        sys.exit(f"Model '{wanted}' isn't installed. Installed: {', '.join(ms)}. Or run: ollama pull {wanted}")
    return ms[0]

def chat(model, prompt, as_json=False, temperature=0.4):
    body = {"model": model, "stream": False, "options": {"temperature": temperature},
            "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}]}
    if as_json:
        body["format"] = "json"
    out = http_json(OLLAMA + "/api/chat", body)
    return out.get("message", {}).get("content", "")

def chat_json(model, prompt, check, tries=3):
    """Ask for JSON and retry until `check(obj)` passes."""
    last = None
    for attempt in range(1, tries + 1):
        raw = chat(model, prompt, as_json=True)
        try:
            obj = json.loads(raw)
            err = check(obj)
            if not err:
                return obj
            last = err
        except json.JSONDecodeError as e:
            last = f"invalid JSON ({e})"
        print(f"   ↻ retry {attempt}: {last}")
    raise RuntimeError(f"The model didn't return usable JSON after {tries} tries: {last}")


# ---------- course generation ----------
def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def check_outline(o):
    w = o.get("worlds")
    if not isinstance(w, list) or not 2 <= len(w) <= 5:
        return "need 2-5 worlds"
    for x in w:
        if not x.get("name") or not isinstance(x.get("topics"), list) or not x["topics"]:
            return "each world needs a name and topics"
    return None

def check_topic(t):
    for k in ["hook", "story", "idea", "real_life", "try_it", "question", "options", "answer_index", "explanation"]:
        if k not in t:
            return f"missing '{k}'"
    if not isinstance(t["options"], list) or len(t["options"]) != 3:
        return "options must be a list of exactly 3"
    if t["answer_index"] not in (0, 1, 2):
        return "answer_index must be 0, 1 or 2"
    return None

def generate_course(model, code, title, focus, n_topics):
    print(f"\n📚 {code} {title}: planning the syllabus with {model}…")
    outline = chat_json(model, f"""Design the syllabus for an MBA course "{title}" ({focus}).
Return JSON: {{"blurb": "one sentence", "worlds": [{{"name": "unit name", "blurb": "one sentence", "topics": ["topic title", ...]}}]}}
Use 3 or 4 units and exactly {n_topics} topics in total. Topic titles: 2-6 words.""", check_outline)
    worlds, topics = [], []
    for wi, w in enumerate(outline["worlds"]):
        wid = f"u{wi+1}"
        worlds.append({"id": wid, "name": w["name"][:60], "short": w["name"].split()[0][:12], "blurb": w.get("blurb", "")})
        for tt in w["topics"]:
            print(f"   ✍️  writing level: {tt}")
            t = chat_json(model, f"""Write one level of the MBA course "{title}" about the topic "{tt}".
Return JSON with these keys:
"hook": a catchy one-line teaser (max 15 words),
"story": 2-3 sentences about a real, well-known case, company or event that illustrates it (no invented details),
"idea": the core concept explained simply in 4-6 sentences, with correct definitions,
"real_life": one sentence linking it to banking, fintech or everyday life in Berlin,
"try_it": one small practical action to do today,
"question": one multiple-choice question testing understanding,
"options": a list of exactly 3 answer options,
"answer_index": the index (0, 1 or 2) of the correct option,
"explanation": one or two sentences explaining why it's correct.""", check_topic)
            topics.append({"w": wid, "t": tt, "h": t["hook"], "s": t["story"], "i": t["idea"], "l": t["real_life"],
                           "y": t["try_it"], "q": t["question"], "o": [str(x) for x in t["options"]],
                           "a": int(t["answer_index"]), "e": t["explanation"]})
    return outline.get("blurb", focus), worlds, topics

def layout(worlds):
    spots = [(150, 125, 88), (352, 115, 88), (400, 258, 78), (185, 268, 82), (275, 190, 60)]
    for w, (x, y, r) in zip(worlds, spots):
        w.update({"x": x, "y": y, "r": r})
    return worlds

def build_course_html(code, title, blurb, worlds, topics, palette_i):
    sys.path.insert(0, BUILD_DIR)
    import build  # the same template engine as the 11 original lessons
    p = PALETTES[palette_i % len(PALETTES)]
    rounds = [{"p": t["q"], "o": t["o"], "a": t["a"], "e": t["e"]} for t in topics[:8]]
    M = {"title": f"{code}: {title}", "num": f"Urmila's MBA University · {code} · AI-generated", "key": "umu-" + slug(code),
         "brief": f"/* VOICE: MBA professor, AI-generated with Ollama\n   IDEA: course {code} as an arcade map\n   PICTURE: unit bubbles\n   COLOUR and TYPE: university palette; EB Garamond titles\n   LAYOUT: hero, units, quick-fire exam ",
         "font": "family=EB+Garamond:wght@600;700",
         "vars": {"dark": "#15110f", "soft": p[5], "softD": p[6], "field": p[0], "fieldInk": p[1], "sun": p[2], "acc": p[3], "accD": p[4],
                  "line": p[7], "lineD": p[8], "cardD": "#1c1517", "tint": p[9], "shadow": p[10], "hf": "'EB Garamond',Georgia,serif", "kick": p[11]},
         "h1": f"{code}: {title}",
         "intro": f"{blurb} {len(topics)} levels. ⚠️ AI-generated with a local model: double-check facts and numbers before relying on them.",
         "ranks": [[0, "Fresher"], [len(topics) * 3, "Scholar"], [len(topics) * 7, "Top of the class"], [len(topics) * 12 + 20, "Dean's list"]],
         "worlds": layout(worlds), "topics": topics,
         "gamesTitle": "Final exam", "gamesBlurb": "A quick-fire exam from this course's levels.",
         "games": [{"id": "ex", "title": "Quick-fire exam", "desc": f"{len(rounds)} questions from {code}.", "note": "Pass mark: 50%.",
                    "done": "Exam complete. Enter your score on your transcript.", "rounds": rounds}]}
    return build.build(M)

def save_course(code, title, blurb, worlds, topics, model):
    os.makedirs(COURSES_DIR, exist_ok=True)
    reg_path = os.path.join(COURSES_DIR, "index.json")
    reg = json.load(open(reg_path)) if os.path.exists(reg_path) else []
    reg = [c for c in reg if c["code"] != code]
    s = slug(code)
    html = build_course_html(code, title, blurb, worlds, topics, len(reg))
    json.dump({"code": code, "title": title, "blurb": blurb, "model": model, "worlds": worlds, "topics": topics},
              open(os.path.join(COURSES_DIR, s + ".json"), "w"), ensure_ascii=False, indent=1)
    open(os.path.join(COURSES_DIR, s + ".html"), "w", encoding="utf-8").write(html)
    reg.append({"code": code, "title": title, "blurb": blurb, "n": len(topics), "ects": 5, "file": f"courses/{s}.html",
                "model": model, "created": time.strftime("%Y-%m-%d")})
    json.dump(reg, open(reg_path, "w"), ensure_ascii=False, indent=1)
    print(f"✅ Saved courses/{s}.html ({len(topics)} levels). It now appears in the portal under 'AI-generated electives'.")


# ---------- commands ----------
def cmd_check(a):
    ms = models()
    if ms is None:
        print("❌ Ollama isn't reachable at", OLLAMA, "\n   Install it from https://ollama.com/download, open the app, then run: ollama pull llama3.2")
    elif not ms:
        print("⚠️  Ollama is running but has no models. Run: ollama pull llama3.2")
    else:
        print("✅ Ollama is running. Models:", ", ".join(ms))

def cmd_serve(a):
    port = a.port
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=HERE)
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        url = f"http://localhost:{port}/index.html"
        print(f"🎓 Urmila's MBA University is open at {url}\n   The AI tutor connects to Ollama automatically. Press Ctrl+C to stop.")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nBye! 👋")

def cmd_new(a):
    model = pick_model(a.model)
    blurb, worlds, topics = generate_course(model, a.code, a.title, a.focus or a.title, a.topics)
    save_course(a.code, a.title, blurb, worlds, topics, model)

def cmd_core(a):
    model = pick_model(a.model)
    for code, title, focus in CORE:
        if os.path.exists(os.path.join(COURSES_DIR, slug(code) + ".html")) and not a.redo:
            print(f"⏭️  {code} already exists (use --redo to regenerate)")
            continue
        blurb, worlds, topics = generate_course(model, code, title, focus, a.topics)
        save_course(code, title, blurb, worlds, topics, model)

def cmd_grade(a):
    model = pick_model(a.model)
    memo = open(a.file, encoding="utf-8").read()
    print(chat(model, f"""Grade this MBA capstone memo out of 100 with this rubric:
clear problem (20), correct use of at least five concepts from five different courses (40), evidence and data (20), clear writing (20).
Give the score per criterion, the total, the German grade (1.0-5.0, 50% = 4.0 pass), the two biggest strengths and the three most important improvements.

MEMO:
{memo}""", temperature=0.2))

def cmd_ask(a):
    print(chat(pick_model(a.model), " ".join(a.question)))

def main():
    ap = argparse.ArgumentParser(description="Urmila's MBA University: AI helper (Ollama)")
    ap.add_argument("--model", help="Ollama model name, e.g. llama3.2")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check").set_defaults(f=cmd_check)
    s = sub.add_parser("serve"); s.add_argument("--port", type=int, default=8000); s.set_defaults(f=cmd_serve)
    n = sub.add_parser("new-course"); n.add_argument("title"); n.add_argument("--code", required=True)
    n.add_argument("--focus"); n.add_argument("--topics", type=int, default=8); n.set_defaults(f=cmd_new)
    c = sub.add_parser("core"); c.add_argument("--topics", type=int, default=8); c.add_argument("--redo", action="store_true"); c.set_defaults(f=cmd_core)
    g = sub.add_parser("grade"); g.add_argument("file"); g.set_defaults(f=cmd_grade)
    q = sub.add_parser("ask"); q.add_argument("question", nargs="+"); q.set_defaults(f=cmd_ask)
    a = ap.parse_args()
    a.f(a)

if __name__ == "__main__":
    main()
