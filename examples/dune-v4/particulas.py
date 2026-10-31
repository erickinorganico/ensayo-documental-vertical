# Overlays de partículas (feedback PARTICULAS-Y-MUSICA): motas de polvo a contraluz y chispas motivadas, sólo en momentos
# elegidos. Canvas 2D dibujado desde el tiempo del timeline (GSAP onUpdate), PRNG con semilla (mulberry32): determinista,
# seek-safe. Profundidad: 3 planos (tamaño, desenfoque por gradiente, velocidad/parallax). Zona de subtítulos atenuada.
# Uso: después de construir_v4.py →  python herramientas/particulas.py   (escribe compositions/part-*.html e inserta hosts)
import json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R)
m = json.load(open("datos/montaje-v4.json", encoding="utf-8")); E = {e["id"]: e for e in m["escenas"]}
idx = open("index.html", encoding="utf-8").read()
piv = [float(x) for x in re.findall(r'<audio[^>]*src="assets/sfx/impacto-profundo\.wav"[^>]*data-start="([\d.]+)"', idx)]
piv = piv or [float(x) for x in re.findall(r'data-start="([\d.]+)"[^>]*src="assets/sfx/impacto-profundo\.wav"', idx)]
def ventana(esc, a=None, z=None):
    e = E[esc]; a = e["inicio"] + 0.05 if a is None else max(a, e["inicio"] + 0.05); z = e["fin"] - 0.05 if z is None else min(z, e["fin"] - 0.05)
    return round(a, 3), round(z, 3)
# (tipo, escena, inicio, fin, semilla, luz_x, luz_y, densidad, motivo)
P = [("polvo", "cita", 0.7, 11.8, 11, 1300, 330, 55, "desierto a contraluz bajo la cita"),
     ("polvo", "estanca", None, E["estanca"]["inicio"] + 9.0, 23, 960, 220, 45, "haz de luz del salón imperial (estancamiento)"),
     ("polvo", "kwisatz", None, None, 37, 960, 420, 50, "presciencia de Paul (el acortamiento del camino)"),
     ("polvo", "canal", None, None, 41, 960, 300, 38, "corredor de luz bajo el título del canal"),
     ("polvo", "esperanza", None, None, 53, 980, 520, 60, "silueta al atardecer (lo entregaron con esperanza)"),
     ("chispas", "yihad", E["yihad"]["inicio"] + 3.4, E["yihad"]["inicio"] + 13.5, 61, 960, 1080, 42, "fuego de la Yihad Butleriana"),
     ("chispas", "heroes", None, E["heroes"]["inicio"] + 8.0, 67, 960, 1080, 40, "guerra santa en llamas")]
piv = [t for t in piv if any(E[x]["inicio"] <= t < E[x]["fin"] for x in ("liberarte", "producto"))]
for k, t in enumerate(piv):   # estallido breve en el impacto de cada pivote (para liberarte / producto)
    esc = [e for e in m["escenas"] if e["inicio"] <= t < e["fin"]][0]["id"]
    P.append(("estallido", esc, t - 0.05, t + 1.3, 71 + k, 960, 540, 36, "impacto del pivote"))
JS = r'''
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
var W=1920,H=1080,cv=document.getElementById(ID+"-cv"),ctx=cv.getContext("2d"),rnd=mulberry32(SEED),ps=[];
for(var i=0;i<N;i++){ps.push({x:rnd()*W,y:rnd()*H,z:rnd(),f:rnd()*6.283,v:rnd(),L:0.9+rnd()*1.5,o:rnd()*3,a:rnd()*6.283})}
function env(t){var a=Math.min(1,t/0.8),b=Math.min(1,(D-t)/0.8);return Math.max(0,Math.min(a,b))}
function dot(x,y,r,col,al){var g=ctx.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,"rgba("+col+","+al+")");g.addColorStop(1,"rgba("+col+",0)");ctx.fillStyle=g;ctx.beginPath();ctx.arc(x,y,r,0,6.283);ctx.fill()}
function capta(y){return y>860?Math.max(0,1-(y-860)/120):1}
function draw(t){ctx.clearRect(0,0,W,H);var e=env(t);if(e<=0)return;ctx.globalCompositeOperation="lighter";
 for(var i=0;i<ps.length;i++){var p=ps[i];
  if(TIPO==="polvo"){var z=0.25+0.75*p.z,x=((p.x+(8+22*z)*t+26*Math.sin(t*0.27+p.f))%W+W)%W,y=((p.y-(3+9*z)*t+18*Math.sin(t*0.19+p.f*2))%H+H)%H;
   var d=Math.hypot(x-LX,y-LY),luz=Math.exp(-d/620),r=1.6+7*z*z+(1-z)*5,al=(0.10+0.55*luz)*(0.35+0.65*z)*e*capta(y);
   dot(x,y,r,z>0.7?"255,226,178":"255,209,150",al.toFixed(3))}
  else if(TIPO==="chispas"){var per=p.L+0.6+p.o,ag=((t+p.o*1.7)%per);if(ag>p.L)continue;var u=ag/p.L,z=0.3+0.7*p.z,
   x=p.x+Math.sin(ag*3.1+p.f)*22+40*ag*(p.v-0.5),y=H*(0.98-0.12*p.v)-ag*(170+260*z),fl=0.65+0.35*Math.sin(ag*38+p.f);
   var al=Math.min(1,(1-u)*fl*e*capta(y)*1.35),r=1.8+4.4*z;dot(x,y,r*2.4,"255,140,60",(al*0.45).toFixed(3));dot(x,y,r,"255,214,140",al.toFixed(3));
   ctx.strokeStyle="rgba(255,170,90,"+(al*0.5).toFixed(3)+")";ctx.lineWidth=r*0.7;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x-3,y+10*z);ctx.stroke()}
  else{var ag=t-0.05;if(ag<0||ag>1.25)continue;var ang=p.a,sp=260+620*p.v,u=ag/1.25,
   x=LX+Math.cos(ang)*sp*ag,y=LY+Math.sin(ang)*sp*ag+180*ag*ag,al=(1-u)*(1-u)*e,r=1+2.6*p.z;
   dot(x,y,r*2.2,"255,150,70",(al*0.5).toFixed(3));dot(x,y,r,"255,230,170",al.toFixed(3))}}
 ctx.globalCompositeOperation="source-over"}
var st={t:0},tl=gsap.timeline({paused:true});tl.to(st,{t:D,duration:D,ease:"none",onUpdate:function(){draw(st.t)}},0);draw(0);
window.__timelines=window.__timelines||{};window.__timelines[ID]=tl;
'''
os.makedirs("compositions", exist_ok=True)
for f in os.listdir("compositions"):
    if f.startswith("part-"): os.remove(f"compositions/{f}")
hosts = []; reg = []
for k, (tipo, esc, a, z, seed, lx, ly, n, motivo) in enumerate(P):
    a, z = ventana(esc, a, z); D = round(z - a, 3); cid = f"part-{k:02d}"
    js = (JS.replace("ID+", f'"{cid}"+').replace("window.__timelines[ID]", f'window.__timelines["{cid}"]').replace("SEED", str(seed)).replace("N;", f"{n};", 1)
          .replace("TIPO", f'"{tipo}"').replace("LX", str(lx)).replace("LY", str(ly)).replace("(D-t)", f"({D}-t)").replace("t:D,duration:D", f"t:{D},duration:{D}"))
    open(f"compositions/{cid}.html", "w", encoding="utf-8").write(
        f'<template><style>#root{{position:absolute;inset:0;pointer-events:none}}canvas{{position:absolute;left:0;top:0;width:1920px;height:1080px}}</style>'
        f'<div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080" data-duration="{D}"><canvas id="{cid}-cv" width="1920" height="1080"></canvas>'
        f'<script>{js}</script></div></template>\n')
    hosts.append(f'<div id="h-part-{k:02d}" class="clip" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{a:.3f}" data-duration="{D}" '
                 f'data-width="1920" data-height="1080" data-track-index="5" data-track-kind="graphics" style="z-index:45"></div>')
    reg.append({"id": cid, "tipo": tipo, "escena": esc, "inicio": a, "fin": z, "semilla": seed, "luz": [lx, ly], "particulas": n, "motivo": motivo})
idx = re.sub(r'<div id="h-part-\d+"[^>]*></div>\n?', "", idx)
idx = idx.replace('<div id="h-subtitulos"', "\n".join(hosts) + '\n<div id="h-subtitulos"', 1)
open("index.html", "w", encoding="utf-8").write(idx)
json.dump(reg, open("datos/particulas-v4.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r_ in reg: print(r_["id"], r_["tipo"], r_["escena"], r_["inicio"], r_["fin"], r_["motivo"])
