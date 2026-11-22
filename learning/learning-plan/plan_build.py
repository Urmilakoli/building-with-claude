import json, html
D = json.load(open('topics.json'))
MODS = [  # order of study
 ("mind-arcade-01.html", "Mind Arcade: Psychology", "https://claude.ai/artifact/2j2kTpQTVzwqUQkH7ZJjfA", "Psychology & human behaviour"),
 ("think-arcade-11.html", "Think Smarter Arcade", "https://claude.ai/artifact/K2h8eQpCzJLXBrDYAsessb", "Thinking skills: stats, biases, philosophy, art"),
 ("money-arcade-05.html", "Money Arcade: Economics", "https://claude.ai/artifact/5dRYjEPsuwj7jiKDPFfNfb", "Economics & economic systems"),
 ("code-arcade-04.html", "Code Arcade: IT", "https://claude.ai/artifact/TZ1pbNoXm5BJCHCPLWy4Jr", "IT & computer science"),
 ("lab-arcade-03.html", "Lab Arcade: Science", "https://claude.ai/artifact/GUEVYd9YeVn23BpZrftARm", "Science"),
 ("word-arcade-02.html", "Word Arcade: English", "https://claude.ai/artifact/5VWy4SVJEHBkzkavoKhRUL", "English, linguistics & literature"),
 ("time-arcade-06.html", "Time Arcade: Mesopotamia", "https://claude.ai/artifact/WAzajAAcpUDwZp2zVAt371", "History: Mesopotamia"),
 ("empire-arcade-07.html", "Empire Arcade: History", "https://claude.ai/artifact/4fgGr5zEDB7ytQ1u4c5qEH", "History: empires & turning points"),
 ("civic-arcade-09.html", "Civic Arcade: Politics", "https://claude.ai/artifact/D1BmxpxPp3egQ6rkxfiNzb", "Politics & government"),
 ("globe-arcade-08.html", "Globe Arcade: Geopolitics", "https://claude.ai/artifact/NvhhgERnf4JdRushDPx3FZ", "Geopolitics & international relations"),
 ("earth-arcade-10.html", "Earth Arcade: Earth Science", "https://claude.ai/artifact/Ayk7LEJ1frj8qzvBra4uW4", "Earth science"),
]
mods = []
flat = []
for i, (f, name, url, subj) in enumerate(MODS):
    d = D[f]
    mods.append({"name": name, "url": url, "subj": subj, "worlds": d["worlds"], "topics": [t["t"] for t in d["topics"]]})
    for t in d["topics"]:
        flat.append({"m": i, "t": t["t"], "w": t["w"]})
# schedule: 3 topics/day, 6 study days + 1 review day per week
days = []; week = []; weeks = []
for k in range(0, len(flat), 3):
    week.append({"type": "study", "items": flat[k:k+3]})
    if len(week) == 6:
        weeks.append(week); week = []
if week: weeks.append(week)
for w in weeks:
    ms = sorted({it["m"] for d in w for it in d["items"]})
    w.append({"type": "review", "mods": ms})
data = {"mods": mods, "weeks": weeks}
tpl = open('plan_tpl.html').read()
open('learning-plan.html', 'w').write(tpl.replace('{{DATA}}', json.dumps(data, ensure_ascii=False)))
print(len(flat), 'topics', len(weeks), 'weeks', sum(1 for w in weeks for d in w if d['type']=='study'), 'study days')
