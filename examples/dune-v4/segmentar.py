# Render por segmentos (causa medida: con 231 <video> + 246 <audio> en una página Chrome devuelve
# net::ERR_INSUFFICIENT_RESOURCES; una escena aislada renderiza sin error). index.html sigue siendo el editable completo.
# Genera:  seg/seg-NN.html (raíces de video, escenas consecutivas, sin audio, cortes en cuadro exacto)
#          compositions/seg/subtitulos-NN.html y acentos-NN.html (re-basados al segmento)
#          seg/audio.html (toda la mezcla: voz, Lisan, música con envolvente y SFX; sin video)
#          seg/plan.json
import json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R)
FPS = 30; MAXV = 36; MAXD = 75.0
q = lambda t: round(round(t * FPS) / FPS, 4)
import sys
MONTAJE = sys.argv[1] if len(sys.argv) > 1 else "datos/montaje-v4.json"
m = json.load(open(MONTAJE, encoding="utf-8"))
idx = open("index.html", encoding="utf-8").read()
TOTAL = float(re.search(r'id="root"[^>]*data-duration="([\d.]+)"', idx).group(1))
nvid = {e["id"]: open(f"compositions/{e['id']}.html", encoding="utf-8").read().count("<video") for e in m["escenas"]}
segs = []; cur = []
for e in m["escenas"]:
    if cur and (sum(nvid[x["id"]] for x in cur) + nvid[e["id"]] > MAXV or e["fin"] - cur[0]["inicio"] > MAXD):
        segs.append(cur); cur = []
    cur.append(e)
segs.append(cur)
os.makedirs("seg", exist_ok=True); os.makedirs("compositions/seg", exist_ok=True)
head = idx[:idx.index('<div id="root"')]
sub = open("compositions/subtitulos.html", encoding="utf-8").read()
ac = open("compositions/acentos.html", encoding="utf-8").read()
plan = []
cortes = [q(s[0]["inicio"]) for s in segs] + [q(TOTAL)]
for k, s in enumerate(segs):
    a0, a1 = cortes[k], cortes[k + 1]; D = round(a1 - a0, 4)
    hosts = []
    for e in s:
        h = re.search(rf'<div id="h-{e["id"]}"[^>]*></div>', idx).group(0)
        h = re.sub(r'data-start="[\d.]+"', f'data-start="{max(0.0, e["inicio"] - a0):.4f}"', h)
        h = re.sub(r'data-duration="[\d.]+"', f'data-duration="{min(e["fin"], a1) - max(e["inicio"], a0):.4f}"', h)
        hosts.append(h)
    # subtítulos del segmento
    caps = []
    for c in re.findall(r'<div id="sub-\d+" class="clip cap"[^>]*>.*?</div>', sub):
        st = float(re.search(r'data-start="([\d.]+)"', c).group(1)); du = float(re.search(r'data-duration="([\d.]+)"', c).group(1))
        if st + du <= a0 or st >= a1: continue
        ns, ne = max(st, a0), min(st + du, a1)
        c = re.sub(r'data-start="[\d.]+"', f'data-start="{ns - a0:.4f}"', c); c = re.sub(r'data-duration="[\d.]+"', f'data-duration="{ne - ns:.4f}"', c)
        caps.append(c)
    s_head = sub[:sub.index('<div id="root"')]
    open(f"compositions/seg/subtitulos-{k:02d}.html", "w", encoding="utf-8").write(
        s_head + f'<div id="root" data-composition-id="subtitulos-{k:02d}" data-width="1920" data-height="1080" data-duration="{D}">' + "".join(caps) +
        f'<script>window.__timelines=window.__timelines||{{}};window.__timelines["subtitulos-{k:02d}"]=gsap.timeline({{paused:true}});</script></div></template>\n')
    # acentos del segmento
    tws = [(float(t), o) for o, t in re.findall(r'tl\.fromTo\("#ac-f",\{opacity:([\d.]+)\},\{[^}]*\},([\d.]+)\);', ac)]
    tws = [(t - a0, o) for t, o in tws if a0 <= t < a1 - 0.05]
    act = "".join(f'tl.fromTo("#ac-f",{{opacity:{o}}},{{opacity:0,duration:0.28,ease:"power2.out",immediateRender:false}},{t:.3f});' for t, o in tws)
    open(f"compositions/seg/acentos-{k:02d}.html", "w", encoding="utf-8").write(
        f'<template><style>#root{{position:absolute;inset:0;pointer-events:none}}</style><div id="root" data-composition-id="acentos-{k:02d}" data-width="1920" data-height="1080" data-duration="{D}">'
        f'<div id="ac-0" class="clip" data-start="0" data-duration="{D}" style="z-index:5"><div id="ac-f" style="position:absolute;inset:0;background:radial-gradient(circle,#fff6e6 0,#ffe2b8 60%,#f3b878 100%);opacity:0"></div></div>'
        f'<script>const tl=gsap.timeline({{paused:true}});tl.to({{}},{{duration:{D}}},0);{act}window.__timelines=window.__timelines||{{}};window.__timelines["acentos-{k:02d}"]=tl;</script></div></template>\n')
    leaks = []
    for h in re.findall(r'<div id="h-(?:leak|part)-\d+"[^>]*></div>', idx):
        st = float(re.search(r'data-start="([\d.]+)"', h).group(1))
        du = float(re.search(r'data-duration="([\d.]+)"', h).group(1))
        if a0 <= st and st + du <= a1 + 0.01: leaks.append(re.sub(r'data-start="[\d.]+"', f'data-start="{st - a0:.4f}"', h))
    extra = "\n".join(leaks) + "\n" + (f'<div id="h-acentos-{k:02d}" class="clip" data-composition-id="acentos-{k:02d}" data-composition-src="compositions/seg/acentos-{k:02d}.html" data-start="0" data-duration="{D}" data-width="1920" data-height="1080" data-track-index="2" data-track-kind="graphics" style="z-index:40"></div>\n'
             f'<div id="h-subtitulos-{k:02d}" class="clip" data-composition-id="subtitulos-{k:02d}" data-composition-src="compositions/seg/subtitulos-{k:02d}.html" data-start="0" data-duration="{D}" data-width="1920" data-height="1080" data-track-index="3" data-track-kind="captions" style="z-index:50"></div>')
    root = (head.replace("<title>", f"<title>[segmento {k:02d}] ") + f'<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1920" data-height="1080" data-fps="{FPS}">\n'
            + "\n".join(hosts) + "\n" + extra + '\n</div><script>window.__timelines=window.__timelines||{};window.__timelines["main"]=gsap.timeline({paused:true});</script></body></html>\n')
    # las raíces de segmento viven en la raíz del proyecto (rutas assets/ relativas a la raíz)
    open(f"seg-{k:02d}.html", "w", encoding="utf-8").write(root)
    plan.append({"seg": k, "archivo": f"seg-{k:02d}.html", "inicio": a0, "fin": a1, "dur": D, "frames": round(D * FPS), "escenas": [e["id"] for e in s],
                 "videos": sum(nvid[e["id"]] for e in s), "subtitulos": len(caps), "acentos": len(tws)})
# raíz de audio: toda la mezcla de index.html, sin video
auds = re.findall(r"<audio[^>]*></audio>", idx)
open("seg-audio.html", "w", encoding="utf-8").write(
    head.replace("<title>", "<title>[mezcla de audio] ") + f'<div id="root" data-composition-id="main" data-start="0" data-duration="{q(TOTAL)}" data-width="1920" data-height="1080" data-fps="{FPS}">\n'
    f'<div id="negro" class="clip" data-start="0" data-duration="{q(TOTAL)}" style="background:#000"></div>\n' + "\n".join(auds) +
    '\n</div><script>window.__timelines=window.__timelines||{};window.__timelines["main"]=gsap.timeline({paused:true});</script></body></html>\n')
auds_sv = [a for a in auds if 'id="voz-' not in a]
open("seg-audio-sinvoz.html", "w", encoding="utf-8").write(
    head.replace("<title>", "<title>[mezcla sin voz: medición] ") + f'<div id="root" data-composition-id="main" data-start="0" data-duration="{q(TOTAL)}" data-width="1920" data-height="1080" data-fps="{FPS}">\n'
    f'<div id="negro" class="clip" data-start="0" data-duration="{q(TOTAL)}" style="background:#000"></div>\n' + "\n".join(auds_sv) +
    '\n</div><script>window.__timelines=window.__timelines||{};window.__timelines["main"]=gsap.timeline({paused:true});</script></body></html>\n')
json.dump({"total": q(TOTAL), "frames": round(q(TOTAL) * FPS), "segmentos": plan, "audios": len(auds)}, open("seg/plan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
assert sum(p["frames"] for p in plan) == round(q(TOTAL) * FPS)
for p in plan: print(p["seg"], p["inicio"], p["fin"], p["videos"], "videos", p["escenas"])
print("segmentos", len(plan), "audios", len(auds))
