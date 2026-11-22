import json, sys, os, importlib.util

def build(m):
    h = open(os.path.join(os.path.dirname(__file__), 'template.html')).read()
    v = m['vars']
    vars_css = (":root{color-scheme:light dark;--bg:light-dark(#ffffff,%s);--ink:light-dark(#15161c,#f1f0ec);"
                "--soft:light-dark(%s,%s);--field:%s;--fieldInk:%s;--sun:%s;--blue:light-dark(%s,%s);"
                "--line:light-dark(%s,%s);--card:light-dark(#ffffff,%s);--mute:light-dark(#545768,#b6b8c6);"
                "--tint:%s;--shadow:%s;--hf:%s}") % (
        v['dark'], v['soft'], v['softD'], v['field'], v['fieldInk'], v['sun'], v['acc'], v['accD'],
        v['line'], v['lineD'], v['cardD'], v['tint'], v['shadow'], v['hf'])
    fonts = '<link href="https://fonts.googleapis.com/css2?%s&family=Nunito:wght@400;600;800&display=swap" rel="stylesheet">' % m['font']
    hero = f'''<header class="band hero"><div class="wrap">
  <div>
    <p class="small" style="color:{v['kick']};margin:0 0 8px;font-weight:800">Bored? Learn something fun · {m['num']}</p>
    <h1>{m['h1']}</h1>
    <p>{m['intro']}</p>
    <div class="jump" id="jump"></div>
  </div>
  <div class="map">
    <svg viewBox="0 0 520 380" role="img" aria-label="Map of the worlds in this module">
      <ellipse cx="260" cy="352" rx="200" ry="16" style="fill:var(--shadow)" opacity=".6"/>
      <g id="lobes"></g>
    </svg>
  </div>
  <div class="xp"><b id="rank">{m['ranks'][0][1]}</b> <span class="small" id="xpnum"></span><div class="bar"><i id="xpbar"></i></div><span class="small" id="xpnext"></span></div>
</div></header>
'''
    gh = ''.join(f'''    <div class="game">
      <h3>{g['title']}</h3>
      <p class="small">{g['desc']}</p>
      <div class="stage" id="{g['id']}"><button class="btn solid" id="{g['id']}Go">Start</button></div>
      <p class="small" id="{g['id']}Out">{g['note']}</p>
    </div>
''' for g in m['games'])
    games = f'''<section class="band games" id="games"><div class="wrap">
  <div class="whead"><div><h2>{m['gamesTitle']}</h2><p>{m['gamesBlurb']}</p></div></div>
  <div class="grid">
{gh}  </div>
</div></section>
'''
    data = ("const W=%s;\nconst T=%s;\nconst KEY=%s;let S={seen:{},quiz:{},games:{}};\n"
            "try{const r=localStorage.getItem(KEY);if(r)S=Object.assign(S,JSON.parse(r))}catch(e){}\n"
            "const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}};\n"
            "const RANKS=%s;\nconst MAX=T.length*12+40;\n") % (
        json.dumps(m['worlds'], ensure_ascii=False), json.dumps(m['topics'], ensure_ascii=False),
        json.dumps(m['key']), json.dumps(m['ranks'], ensure_ascii=False))
    gd = ''
    for g in m['games']:
        if 'rounds' in g:
            gd += "document.getElementById(%s).onclick=game(%s,%s,%s,%s,%s);\n" % (
                json.dumps(g['id'] + 'Go'), json.dumps(g['id']), json.dumps(g['id'] + 'Out'),
                json.dumps(g['id']), json.dumps(g['rounds'], ensure_ascii=False), json.dumps(g['done'], ensure_ascii=False))
        else:
            gd += g['js'] + '\n'
    brief = m['brief']
    for k, val in [('{{TITLE}}', m['title']), ('{{FONTS}}', fonts), ('{{VARS}}', vars_css), ('{{HERO}}', hero),
                   ('{{GAMES}}', games), ('{{DATA}}', data), ('{{GAMEDATA}}', gd), ('{{BRIEF}}', brief)]:
        h = h.replace(k, val)
    return h

if __name__ == '__main__':
    p = sys.argv[1]
    spec = importlib.util.spec_from_file_location('mod', p); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    out = sys.argv[2]
    open(out, 'w').write(build(mod.M))
    print('wrote', out)
