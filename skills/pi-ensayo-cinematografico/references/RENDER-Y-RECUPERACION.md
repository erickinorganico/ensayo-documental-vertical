# Render y recuperación · ensayo cinematográfico PI (medido en Dune v4)

- **Entorno medido:** HyperFrames CLI **0.8.223** (render, renderer y editable final) y Tesseract **0.4.0** (`tsrct`, para piezas 2.5D/3D integradas como clip). Windows 11, CPU de 16 núcleos y GPU AMD 780M.
- **Pieza de referencia:** 488.4 s a 30 fps, 9 segmentos.
- Rutas relativas al expediente `sistema-video/transferencias/claude-dune-20261030/produccion-hyperframes-v2/`.
- El repo no incluye medios: estas recetas no prometen un render autónomo sin el material del expediente.

---

## 1. Fallos medidos y su causa

| Síntoma | Causa medida | Solución |
|---|---|---|
| `net::ERR_INSUFFICIENT_RESOURCES`, `media_readiness_timeout`, «no forward progress» | Una página con 231 `<video>` + 246 `<audio>` excede los reproductores de Chrome. Con 1 escena aislada: EXIT 0 | Render **por segmentos** de escenas consecutivas con **≤35–36 videos por página** (medido en este equipo) |
| Cada `<video>` cargaba un tráiler de 26 MB | Fuente completa referenciada cientos de veces | `cortar()`: un mp4 por toma, sólo el tramo, 30 fps, `-g 15`, sin audio |
| `VIDEO_SOURCE_UNRENDERABLE` | `data-duration` mayor que el archivo | Recorte con cámara lenta ≤2× más `tpad` de retención; `validar_videos.py` antes de render |
| `PLAN_TOO_LARGE` (2.38 GiB > 2 GiB) | El render **local copia toda la carpeta raíz** (incluye renders, datos y dot-folders) y **no aplica `.hyperframesignore`** (medido) | Raíz ligera `_render/` con enlaces duros |
| `render_cancelled_parent_exited` | Se cerró el proceso que lanzó el render durante la extracción | Lanzar con `Start-Process -WindowStyle Hidden` y reanudar |
| `ffmpeg_timeout` (retryable) | Contención de CPU con otra tarea pesada | No correr mediciones pesadas en paralelo; segundo pase automático |
| Snapshot: `Runtime.callFunctionOn timed out` | 37 tiempos en una llamada | Lotes de 4 tiempos con `--timeout 180000`, o cuadros del MP4 real con ffmpeg |
| Bloque del registro desaparecido | El builder borraba `compositions/*.html` | Excluir los bloques del registro del borrado |
| `$args` vacío en PowerShell | Es una variable automática reservada | Usar `$cli` |

## 2. Raíz ligera con enlaces duros

Fuente: `herramientas/preparar_render.py`.

Pseudocódigo histórico; antes de reemplazar una carpeta, resolver su ruta absoluta y comprobar que pertenece al proyecto y que ningún lote la usa:

```text
recrear_carpeta_verificada("_render")
for f in walk("assets"): os.link(f, "_render/"+f)          # enlace duro: sin duplicar disco
copytree("compositions", "_render/compositions"); copy(*.html, hyperframes.json, package.json)
```

- **Peligro:** un enlace duro comparte el contenido. Editar un asset dentro de `_render/` **modifica la fuente**. Nunca se edita ahí; se regenera desde el proyecto.
- **No regenerar `_render/` mientras un lote lo usa.** Para cambiar sólo el audio, copiar únicamente `seg-audio.html`.
- Antes de reemplazar, comparar que las raíces visuales y las compositions son idénticas (`cmp`).

## 3. Segmentación y audio separado

Fuente: `herramientas/segmentar.py` (escribe `seg/plan.json`).

- **Agrupar escenas consecutivas** hasta 36 videos o 75 s. Cortes en **cuadro exacto** (`round(t*30)/30`), comprobando `Σframes == frames_totales`.
- **Por segmento:** `seg-NN.html` sin audio, con los hosts de sus escenas re-basados.
  - Subtítulos y destellos se regeneran re-basados al segmento (`compositions/seg/`).
  - Fugas de luz y partículas sólo si caen **enteras** dentro del segmento (`a0 ≤ st && st+du ≤ a1`).
- **Una raíz `seg-audio.html`** con toda la mezcla (voz, música con automatización, SFX) sobre negro; la renderiza HF. Para medir voz/música **no se renderizan 8 min de negro adicionales**: se calcula el residuo offline (ver RECETAS-AUDIO §3).
- **Ensamblado** (`ensamblar_v4.py`): `concat -c copy` del video sin recodificar, más mux con el audio HF. Sólo el audio se procesa: ganancia medida, limitador, AAC 256k.
- Tras renderizar, mover `seg-*.html` a `seg/raices/`. Si quedan en la raíz, `lint` falla con `multiple_root_compositions`.

## 4. Lote persistente y reanudable

Fuente: `herramientas/render-v4.ps1`.

```powershell
Start-Process pwsh -ArgumentList "-NoProfile","-File","herramientas\render-v4.ps1" -WindowStyle Hidden -PassThru   # sobrevive a la sesión
foreach ($pase in 1..2) { foreach ($o in $orden) {
  if (Cuadros $mp4 ≈ $o.fr) { continue }                      # reanudable
  npx.cmd --yes hyperframes@0.8.223 render --composition $o.f --fps 30 --quality looks --workers 3 -o $mp4 *> seg.log } }
```

**Mejora pendiente.** En Dune la reanudación sólo comparaba **número de cuadros**. Eso no distingue un segmento obsoleto con la misma duración, que fue un riesgo real cuando cambió el relleno. La próxima versión debe guardar una **huella** junto a cada salida y saltar sólo si coinciden las tres comprobaciones:

```text
huella = sha256(seg-NN.html + compositions usadas + hash del contenido de cada asset + versión/opciones CLI)
saltar = huella == guardada AND frames == esperados AND ffmpeg -v error -i mp4 -f null - sin errores
```

**Reglas de operación:**
- **Antes de lanzar,** listar procesos propios (`Win32_Process` con `render-*.ps1|hyperframes … render`) y leer el último log. Si hay uno vivo, no se duplica. Un proceso ajeno (otro proyecto) no se toca.
- **Un PID que ya no existe** no es un render activo. Conciliar primero logs, descendientes y transacciones; sólo limpiar una transacción abortada tras verificar su ruta absoluta dentro de la raíz esperada y que ningún proceso la usa.
- **Progreso real** = `@hf-progress` o `frame N/M` en el log del segmento. No se inventan ETA; se informa el último dato y su hora.
- **Esperas acotadas** (consultas de hasta60s para conservar comunicación). El render vive en el proceso oculto, no en la espera.
- **Render selectivo:** si sólo cambia el audio, se re-renderiza sólo `seg-audio`; si cambia una escena, sólo su segmento. El resto se reutiliza.
- **Recibos:** `renders/v4/_lote.log` (INICIO, RENDER, FIN con exit y cuadros), logs por segmento y `QA-*.json` con SHA del MP4.
- **Bucles de audio:** un `<audio>` con `-stream_loop -1` como entrada infinita bloqueó un mux. Las camas en bucle se pre-renderizan a duración finita.

## 5. QA mínimo antes de entregar

- **Video:** `ffprobe` (dimensiones, fps, duración); `ffmpeg -v error -f null` sin errores; `blackdetect` (d 0.4, pix_th 0.05), explicando cada negro.
- **Audio:** `ebur128` (I, LRA, true peak) y relación voz/resto por ventanas.
- **Fuentes:** búsqueda de patrones rechazados (`class="note"`, `notificacion.wav`, `ding-N.wav` = 0); `hyperframes lint` con 0 errores. El `check` completo puede tardar >10 min con navegador.
- **Cuadros del MP4 real** en los momentos de riesgo: oclusiones, partículas, pivotes, cortes y negros detectados. Se miran; no basta con metadatos.
- **Integridad de versiones previas** (SHA) y SHA de la voz igual al recibo.

## 6. Dependencias y límites

- **Dependencias:** Node/npx (hyperframes 0.8.223 fijado en `package.json`), Chrome que gestiona HF, ffmpeg/ffprobe, Python 3 con numpy y Pillow, `tsrct` 0.4.0 para piezas Tesseract y PowerShell 7 para los lotes.
- **Tiempos en este equipo** (Dune): segmento de ≈60 s en 3–5 min (`looks`, 3 workers); mezcla de 488 s en ≈7 min; máscara local ≈0.35 s/cuadro.
- **Lo que no está resuelto:**
  - El lote histórico de Dune no implementó huellas. El repo añade `scripts/render_jobs.py` para piezas futuras: contenido de entradas explícitas, comando/versiones, hash de salida, frames y decode; no reemplaza el lote ni altera el máster aprobado. Hay que declarar todas las dependencias transitivas, o directorios completos de entradas sin renders. Una salida obsoleta se conserva y exige conciliar o elegir nueva versión; no se sobreescribe ni se reintenta automáticamente.
  - Snapshot masivo en una llamada.
  - `.hyperframesignore` en render local.
  - Render reproducible sin los medios del expediente.
