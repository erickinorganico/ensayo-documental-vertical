# Recetas visuales · ensayo cinematográfico PI (aprendidas en Dune v4)

Origen: pieza aprobada `Dune-v5-HyperFrames-v4.mp4` (488.4 s, 16:9, SHA fac35157…). Las rutas de fuente son relativas al expediente
`sistema-video/transferencias/claude-dune-20261030/` y apuntan a la implementación real. El repo no contiene ese material.

**Regla de traslado.** Un tema nuevo conserva la gramática, no las cifras de Dune. No son metas: desierto, Dune, 37 escenas, 8 min, 122 SFX, la paleta arena ni el rojo PI. Cada número de este documento es una calibración de esa pieza y se vuelve a medir en la siguiente.

---

## 1. Tipografía y jerarquía

- **Montserrat Black 900 real.** Es el archivo OFL `Montserrat-Black.ttf` (github JulietaUla/Montserrat) con `@font-face`. Fuente en `produccion-hyperframes-v2/herramientas/kit16x9.css` y `construir_v4.py` (`KIT`).
  - Nunca simular el peso 900 con otra familia ni con `font-weight` sobre Inter.
  - ```css
    @font-face{font-family:MontBlack;src:url('assets/fonts/Montserrat-Black.ttf');font-weight:900}
    .big{font-family:MontBlack,sans-serif;font-weight:900;font-size:170px;text-transform:uppercase;line-height:1}
    .cap{font-family:MontBlack;font-weight:900;font-size:40px;color:#ecd828;top:925px;width:1400px}  /* subtítulos 16:9 */
    ```
- **Roles.**
  - Palabra gigante: 150–300 px, 1–1.3 s, entra con `back.out(2.4)` y sale con `power2.in`.
  - Rótulo o tag: 34 px con barra amarilla.
  - Documento: EB Garamond / Playfair sobre papel `#f4efe2` con resaltador `#f6e04a` que crece en la palabra dicha.
  - Subtítulo: amarillo, literal, 3–7 palabras.
- **Sin duplicados.** Si el texto en pantalla ya dice la frase (máquina de escribir, frase armada, cierre serif), esa ventana va sin subtítulo: lista `NOCAP` en el builder.
- **Fuera de esta gramática:** notificaciones tipo macOS, tarjetas pastel, fondos degradados de colores y gags largos de la plantilla café. Erick los rechazó explícitamente. La sátira entra breve e integrada: un feed oscuro de 2–3 s, una firma sellada, palabras gigantes sobre metraje.

## 2. Máquina de escribir sincronizada con la voz

Fuente: `construir_v4.py` → `maquina()` (apertura) y `maquina_frase()` (monólogo).

Pseudocódigo (los tiempos T/TE y los arrays proceden del proyecto):

```text
for i in range(i0, i1 + 1):                    # palabras del literal
    a, z = T(i), TE(i)                         # inicio/fin de la palabra en el reloj del montaje
    for k, ch in enumerate(W[i]["w"]):         # cada carácter dentro de la duración de su palabra
        t = a + (z - a) * k / len(W[i]["w"])
        tl.fromTo(f"#c{i}_{k}", {opacity:0}, {opacity:1, duration:0.01, immediateRender:true}, t)
```

- Las frases consecutivas no se encadenan: cada una sale 0.12 s antes de que empiece la siguiente. En v4 se corrigió un encimado real.
- **No envolver con «» si el literal ya los trae.** Pasó: «« duplicado.
- **Honestidad de tiempos.** En Dune no había ASR local (`whisper-cpp not found`; ningún Python con whisper/vosk). Los tiempos vienen de pausas reales (`ffmpeg silencedetect -35 dB / 0.12 s`) más programación dinámica sobre ritmo silábico (`produccion-tesseract-v1/.work/alinear.py`). Los cortes caen en silencios reales, pero los tiempos dentro de cada frase son **provisionales**. Con ASR local disponible, reemplazar `palabras.json` y reconstruir.

## 3. Texto detrás de personajes (oclusión real con máscara móvil)

Fuente: `construir_v4.py` (rama `ocl` en `toma()`, función `OCL()`). Assets en `assets/oclusion/`. QA en `datos/oclusion-qa/*.png`.

**Orden de capas:** fondo → texto → sujeto recortado. Las tres capas comparten una sola `.cam`, así que la cámara las mueve juntas y el texto vive dentro del plano.

1. **Base:** recorte del plano ya encuadrado al lienzo. Si la fuente trae letterbox, **recortar antes de segmentar** (p. ej. `scale=2573:1448,crop=1920:1080`), para que base y máscara compartan la misma transformación. Si el plano dura menos de lo que el texto necesita para leerse, cámara lenta ≤1.6× sobre el metraje, nunca sobre la voz.
2. **Máscara local, cuadro a cuadro:**
   ```
   npx hyperframes remove-background base.mp4 -o sujeto.webm --quality best --json   # u2net_human_seg, CPU ≈0.35 s/cuadro
   npx hyperframes remove-background foto.jpeg -o sujeto.png                         # fotos
   ```
   La primera vez instala `onnxruntime-node` y descarga pesos en la caché de HyperFrames. Es local y sin pago.
3. **QA obligatorio antes de usar:**
   ```
   ffmpeg -c:v libvpx-vp9 -i sujeto.webm -f lavfi -i color=c=0xd7261e:s=1920x1080 \
     -filter_complex "[1][0]overlay=shortest=1,select='eq(n,5)+eq(n,40)'" ...
   ```
   Revisar sobre rojo: cabello, bordes, que la máscara siga el movimiento y que no haya otro sujeto.
   - Cobertura por cuadro: `alphaextract,signalstats` (YAVG del alfa).
   - Corte oculto: `scdet=threshold=0` en la base.
4. **Fallos encontrados que hay que buscar siempre:**
   - **Corte oculto dentro de un "plano" del tráiler.** T24-028 empezaba con Gurney y luego pasaba a Paul; el detector a umbral 0.30 no lo vio. Se recortó la base desde 1.55 s y se volvió a segmentar.
   - **La máscara falla cuando entra un efecto** (tormenta de arena en la secuencia Arrakis). Limitar la capa recortada a la parte válida: pareja 4.6 s de 5.2 s.
   - **El sujeto centrado tapa el centro de la palabra.** «ALIVIO» sólo dejaba leer «IO». Agrandar el texto, a 430 px, para que las letras rodeen la silueta.
   - **El texto debe salir antes de la siguiente palabra gigante.** Fade-out a `min(t0+d-0.3, t0+tx0+2.0)`.
   - **Anclar a la palabra puede dejar el texto 0.2 s en pantalla.** Si el plano es corto, mostrar el texto desde el inicio del plano.
5. Las capas `sujeto` van sin grade, para no tocar el alfa, y la base va con `capa="limpio"`, para que los colores coincidan.

```html
<div class="cam">
  <video id="base" src="base.mp4" class="clip" data-start="0" data-duration="3" data-media-start="0" muted style="z-index:1"></video>
  <div id="texto" class="clip center" data-start="0" data-duration="3" style="z-index:2"><div class="big ocl-w">QUINCE AÑOS</div></div>
  <video id="sujeto" src="sujeto.webm" class="clip" data-start="0" data-duration="3" data-media-start="0" muted style="z-index:3"></video>
</div>
```

## 4. Tesseract 2.5D/3D nativo → clip integrado en HyperFrames

Fuente: `produccion-hyperframes-v2/.almacen/tesseract-arrakis/` (antes `tesseract-arrakis/`), `parche_arrakis.py`, `ARR()` en el builder.

1. Trabajar en una **copia** del `.tsrct`. Ocultar los textos y las cifras no cotejadas con una acción nativa reversible:
   ```json
   [{"type":"setFxLayerHidden","compositionId":"main","layerId":21,"hidden":true}, ...]
   ```
   En Dune fueron 27 capas, incluida «EJEMPLARES DE MÁS DE 400 M».
2. `tsrct filmstrip` para verificar, luego `tsrct export --fps 30`; sin texto, 31 s en ≈87 s.
3. En HF, ítem de duración **fija** y velocidad real: sin zoom ni punch-in añadidos, porque la pieza trae su propia cámara. Cada tramo se ancla a la frase que lo motiva y conserva su coreografía completa (entrada, transición de arena). Ejemplos: 0.3–12.6 s → «planeta desierto»; 18.9–24.4 s → tras el Lisan. Si la escena es más corta, se recorta por el final, nunca acelerando.
4. **Lecciones de `tsrct` 0.4.0** (de `produccion-tesseract-v1/.work/tesseract_build.py`):
   - `effectId` es entero.
   - El reloj de video se reconstruye con `reanchorFxLayerSourceClock`: `mapping.output.start` es la entrada en la fuente, con `inputOffsetMs=0`.
   - `setFxLayerSpeed` está retirado.
   - Commit y apply sobre el esquema real (`tsrct project schema --document`).

## 5. Grade, texturas y overlays con jerarquía

Fuente: `grade()` en `construir_v4.py`. Siempre por `data-color-grading` (media-treatment), nunca filtros CSS sobre metraje.

| Capa | Dónde | Efectos (`effects`) |
|---|---|---|
| `cine` | Todo el metraje | `filmArtifacts: 0.14` + grade documental (contrast 0.2, sat −0.22, blacks −0.14, grain 0.18, vignette 0.34) |
| `archivo` | Material de 1963–1984, capturas | `filmArtifacts: 0.42` |
| `moderno` | Bloque IA contemporáneo (servidores) | `chromaticAberration: 0.18, digitalGlitch: 0.06` |
| `limpio` | Bases de oclusión | Sin efectos |
| Fondos bajo documentos | Video atenuado | `exposure −0.8, blur 0.3` |

- **Transiciones fuertes:** bloque del registro `organic-light-leak-overlay`, sólo en cambios de bloque argumental.
  - Cambiar su `<script src>` del CDN a `assets/gsap.min.js`.
  - Protegerlo del borrado del builder (`"light-leak" not in f`).
  - Que empiece **dentro** de la escena, para no cruzar segmentos.
- **Destellos suaves** (opacidad 0.16) en los demás cambios.
- **Un solo elemento destello animado** en vez de N gradientes. Con 37 elementos *heavy overlay* el check avisa de riesgo de cuadros negros.
- Glitch y VHS sólo con motivo (era moderna). Nunca un filtro de deterioro uniforme ni sobre caras o subtítulos.

## 6. Partículas: polvo a contraluz y chispas motivadas

Fuente: `herramientas/particulas.py`. Registro de ventanas en `datos/particulas-v4.json`.

- **Canvas 2D** dibujado desde el tiempo del timeline (GSAP `onUpdate`, seek-safe) con PRNG `mulberry32(semilla)`. Sin `Math.random`, sin `requestAnimationFrame`.
  ```js
  var st={t:0}; tl.to(st,{t:D,duration:D,ease:"none",onUpdate:()=>draw(st.t)},0); draw(0);
  // polvo: z∈[0.25,1] → tamaño 1.6+7z², deriva (8+22z)·t, alfa ∝ exp(-dist(luz)/620); atenuar y>860 (subtítulos)
  // chispas: vida 0.9–2.4 s cíclica por partícula, ascenso (170+260z)·edad, parpadeo sin(38·edad), estela corta
  ```
- **Profundidad:** 3 planos por tamaño, suavidad de gradiente y parallax. La intensidad está ligada a un punto de luz por ventana. La franja de subtítulos se atenúa.
- **Selectivo, nunca uniforme.**
  - Polvo: contraluz, presciencia, haz de luz, atardecer.
  - Chispas: fuego y guerra.
  - Estallido de 1.2 s sólo en los pivotes con impacto narrativo. Se quitó uno en una piedra porque no tenía motivo.
- **Cada ventana dentro de una sola escena,** para que no cruce segmentos de render.
- **Calibración tras ver el render:** las chispas sobre fuego eran casi invisibles. Se subieron a radio 1.8+4.4z y alfa ×1.35 con tope 1. Revisar siempre en el MP4 real.

## 7. Variedad, repetición y ritmo por idea

- Una escena por idea del guion; el corte se ancla a la palabra (corte 0.10–0.12 s antes).
- **Inventario por asset** (`datos/montaje-v4.json → repetidos`):
  - Ninguna imagen fija más de 3.5–4 s.
  - Un motivo sólo vuelve con función. El cubo/aguja quedó en 3 usos de ≤4 s cada uno.
  - Relleno de fondos con un *pool* de planos limpios no usados (`relleno()`), antes que repetir fotos.
- **Planos de tráiler:** detección fina de cortes (`scene>0.12`) más vetos manuales (logos, créditos, fechas, subtítulos quemados).
  - Las etiquetas de terceros (Codex) son propuestas: verificar el contenido, porque «cosechadora» resultó ser el barón.
  - Planos que abren en fundido negro: no ponerlos al inicio de una escena, o recortar por luma (`signalstats` YAVG).
- **Videos de archivo más cortos que su hueco:** cámara lenta ≤2× más retención final. Nunca pedir a un `<video>` más segundos de los que tiene; lo valida `validar_videos.py`.
- Clips integrados (Arrakis, oclusiones) con duración fija; los demás absorben el ajuste.
- **No se empaqueta material ajeno** (tráileres, fotos de galería, compilación Lisan) en el repo. Las recetas describen el método; cada expediente trae su fuente y su crédito en pantalla.

## Límites conocidos

- La máscara local (u2net_human_seg) falla con sujetos pequeños o partículas densas, y con sujetos no humanos. Siempre hay que hacer QA sobre rojo.
- La alineación sin ASR es provisional dentro de cada frase.
- Los tres tramos oscuros de 0.5–0.6 s que quedaron en Dune (fundidos de la fuente) **no son un rasgo de estilo**; son pendiente de pulido.
