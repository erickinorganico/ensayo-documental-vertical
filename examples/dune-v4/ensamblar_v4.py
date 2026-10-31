# Ensambla v4 (segmentos HyperFrames por copia de flujo + mezcla HyperFrames) y hace QA real:
# técnica, relación voz/música medida en ventanas de habla, A/B v3↔v4 para escucha, cuadros de oclusión/partículas/Lisan.
import hashlib, json, os, re, subprocess
import numpy as np
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R)
def sh(a): return subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL)
V = "renders/v4"; plan = json.load(open("seg/plan.json", encoding="utf-8"))
segs = [f"{V}/seg-{p['seg']:02d}.mp4" for p in plan["segmentos"]]
for f, p in zip(segs, plan["segmentos"]):
    n = int(sh(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", f]).stdout or -1)
    assert abs(n - p["frames"]) <= 1, (f, n, p["frames"])
open(f"{V}/lista.txt", "w", encoding="utf-8").write("".join(f"file '{os.path.abspath(f)}'\n" for f in segs))
r = sh(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{V}/lista.txt", "-an", "-c", "copy", f"{V}/_video.mp4"]); assert r.returncode == 0, r.stderr
# master: la mezcla HF se lleva a -14 LUFS integrados con techo -1 dBTP (la ganancia se mide, no se supone)
e = sh(["ffmpeg", "-nostdin", "-hide_banner", "-nostats", "-i", f"{V}/seg-audio.mp4", "-af", "ebur128", "-f", "null", "-"]).stderr
I0 = float(re.search(r"I:\s+(-?[\d.]+)", e[e.rfind("Summary:"):]).group(1)); gan = round(-14.0 - I0, 2)
OUT = "renders/Dune-v5-HyperFrames-v4.mp4"
r = sh(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"{V}/_video.mp4", "-i", f"{V}/seg-audio.mp4", "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
        "-af", f"volume={gan}dB,alimiter=limit=0.89:attack=3:release=60:level=false", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", "-shortest", OUT])
assert r.returncode == 0, r.stderr
p = json.loads(sh(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,width,height,r_frame_rate,sample_rate,channels:format=duration,size", "-of", "json", OUT]).stdout)
e = sh(["ffmpeg", "-nostdin", "-hide_banner", "-nostats", "-i", OUT, "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr; s = e[e.rfind("Summary:"):]
b = sh(["ffmpeg", "-nostdin", "-hide_banner", "-nostats", "-i", OUT, "-vf", "blackdetect=d=0.4:pix_th=0.05", "-an", "-f", "null", "-"]).stderr
dec = sh(["ffmpeg", "-nostdin", "-v", "error", "-i", OUT, "-f", "null", "-"]).stderr.strip()
# relación voz / (música+SFX+viento) en ventanas de habla: voz colocada en el timeline real vs raíz HF sin voz
SR = 16000
def pcm(path, extra=None):
    a = ["ffmpeg", "-nostdin", "-v", "error", "-i", path] + (extra or []) + ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(a, capture_output=True).stdout, dtype=np.float32)
idx = open("index.html", encoding="utf-8").read()
vozseg = [(float(re.search(r'data-start="([\d.]+)"', t).group(1)), float(re.search(r'data-duration="([\d.]+)"', t).group(1)), float(re.search(r'data-media-start="([\d.]+)"', t).group(1)))
          for t in re.findall(r'<audio id="voz-\d+"[^>]*>', idx)]
mezcla = pcm(f"{V}/seg-audio.mp4"); voz = pcm("assets/audio/voz-erick-original.mp3")
tl = np.zeros_like(mezcla)
for st, du, ms in vozseg:
    a, z = int(st * SR), int((st + du) * SR); seg = voz[int(ms * SR): int(ms * SR) + (z - a)]; tl[a:a + len(seg)] += seg[: len(tl) - a]
# alineación voz-en-timeline ↔ mezcla HF (retardo AAC) por correlación cruzada en 0–40 s, ±0.25 s
_n = 40 * SR; _A = np.fft.rfft(mezcla[:_n], 2 * _n); _B = np.fft.rfft(tl[:_n], 2 * _n)
_cc = np.fft.irfft(_A * np.conj(_B)); _lim = int(0.25 * SR); _c = np.concatenate([_cc[-_lim:], _cc[:_lim + 1]])
LAG = int(np.argmax(_c)) - _lim
tl = np.roll(tl, LAG)
_g = float(np.dot(mezcla[:_n], tl[:_n]) / (np.dot(tl[:_n], tl[:_n]) + 1e-9))   # ganancia efectiva de la voz en la mezcla
sinvoz = mezcla - _g * tl   # residuo = música + viento + SFX + Lisan
W = json.load(open("datos/palabras-alineacion-local.json", encoding="utf-8"))
m4 = json.load(open("datos/montaje-v4.json", encoding="utf-8"))
def M(t): return 0.6 + t + sum(p_["dur"] for p_ in m4["pausas_insertadas"] if t >= p_["t_voz"])
rel = []
for w in W[::6]:
    a = M(w["t0"]); z = a + 1.5
    ia, iz = int(a * SR), int(z * SR)
    if iz > len(tl): break
    rv = np.sqrt(np.mean(tl[ia:iz] ** 2)) + 1e-9; rm = np.sqrt(np.mean(sinvoz[ia:iz] ** 2)) + 1e-9
    rel.append(20 * np.log10(rv / rm))
rel = np.array(rel)
lisan = m4["lisan_t"]; la, lz = int((lisan - 0.3) * SR), int((lisan + 1.6) * SR)
m_lis = 20 * np.log10(np.sqrt(np.mean(sinvoz[la:lz] ** 2)) + 1e-9)
qa = {"mp4": OUT, "ganancia_master_dB": gan, "mezcla_hf_LUFS": I0, "streams": p["streams"], "duracion": float(p["format"]["duration"]), "bytes": int(p["format"]["size"]),
      "LUFS_I": float(re.search(r"I:\s+(-?[\d.]+)", s).group(1)), "LRA": float(re.search(r"LRA:\s+(-?[\d.]+)", s).group(1)),
      "true_peak_dBTP": float(re.search(r"Peak:\s+(-?[\d.]+)", s).group(1)), "negros_>0.4s": re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", b),
      "errores_decodificacion": dec[:400], "sha256": hashlib.sha256(open(OUT, "rb").read()).hexdigest(),
      "voz_sobre_resto_dB_en_habla": {"mediana": round(float(np.median(rel)), 1), "p10": round(float(np.percentile(rel, 10)), 1), "p90": round(float(np.percentile(rel, 90)), 1), "ventanas": int(len(rel))},
      "nivel_resto_en_grito_lisan_dBFS_rms": round(float(m_lis), 1), "alineacion_lag_muestras_16k": LAG, "ganancia_voz_estimada": round(_g, 3), "metodo_relacion": "residuo offline = mezcla HF menos voz colocada y alineada por correlación; sin render extra",
      "notificaciones_en_fuentes": int(sum(open(f, encoding="utf-8").read().count('class="note') for f in ["index.html"] + [f"compositions/{x}" for x in os.listdir("compositions") if x.endswith(".html")])),
      "musica": "assets/musica/dune-r2-cama490s.wav (aprobada r2) única pista musical"}
json.dump(qa, open("renders/QA-HF-v4.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# A/B v3 ↔ v4 (mismos segundos) para escuchar; y cuadros de control
os.makedirs(f"{V}/comparativa", exist_ok=True)
v3 = ".almacen/renders/Dune-v5-HyperFrames-v3.mp4"
for nombre, a, d in (("apertura", 0, 30), ("arrakis", 44, 20), ("lisan", 255, 22), ("cierre", 455, 33)):
    for etq, src in (("v3", v3), ("v4", OUT)):
        if os.path.exists(src): sh(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(a), "-t", str(d), "-i", src, "-c:v", "libx264", "-crf", "23", "-preset", "veryfast", "-c:a", "aac", "-b:a", "192k", f"{V}/comparativa/{nombre}-{etq}.mp4"])
part = json.load(open("datos/particulas-v4.json", encoding="utf-8"))
ts = [37.6, 44.6, 50.0, 202.0, 452.5] + [(x["inicio"] + x["fin"]) / 2 for x in part] + [lisan + 0.4, lisan + 1.2]
args = sum([["-ss", f"{t:.2f}", "-i", OUT] for t in ts], []); cols = 5
sh(["ffmpeg", "-nostdin", "-v", "error", "-y"] + args + ["-filter_complex", "".join(f"[{i}:v]scale=384:216,setsar=1[v{i}];" for i in range(len(ts))) +
    "".join(f"[v{i}]" for i in range(len(ts))) + f"xstack=inputs={len(ts)}:layout=" + "|".join(f"{(i % cols) * 384}_{(i // cols) * 216}" for i in range(len(ts))) + ":fill=black",
    "-frames:v", "1", "renders/QA-v4-control.png"])
sh(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", OUT, "-vf", "fps=1/8,scale=320:180,tile=8x8:padding=3:color=0x222222", "-frames:v", "1", "renders/contacto-HF-v4.png"])
print(json.dumps({k: qa[k] for k in ("duracion", "LUFS_I", "LRA", "true_peak_dBTP", "negros_>0.4s", "errores_decodificacion", "voz_sobre_resto_dB_en_habla", "nivel_resto_en_grito_lisan_dBFS_rms", "notificaciones_en_fuentes")}, ensure_ascii=False))
