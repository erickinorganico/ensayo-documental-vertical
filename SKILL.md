---
name: ensayo-documental-vertical
description: Edita una locución (video-ensayo, reflexión, crítica social) como video vertical 9:16 en HyperFrames con el estilo "Pensamientos Inorgánicos · café": cortes muy rápidos a la voz, frase blanca que se arma palabra por palabra al centro sobre negro, palabras gigantes en mayúsculas sobre metraje, collage de fotos de archivo (Wikimedia Commons), documentos con resaltador amarillo, notificaciones y ventanas tipo macOS con halo, gag pixel-art, destellos cálidos entre secciones, subtítulos amarillos Roboto, grade "documental" (sombras petróleo, luces ámbar, grano, viñeta), música documental bajo la voz y ~140 efectos de sonido pegados a los cortes. Úsala cuando Erick pida "edítalo como el del café", "mismo estilo que Wikimedia Vertical", o un video-ensayo vertical con archivo y motion editorial.
---

# Ensayo documental vertical (estilo "Wikimedia Vertical")

Proyecto de referencia (léelo si dudas de algo; no lo modifiques):
`C:\Users\erick\.hyperframes-studio\Wikimedia Vertical` — 100.9 s, 1080×1920, 30 fps, 15 secciones en `compositions/v5/`.
Escenas que conviene abrir como ejemplo vivo: `v5-apertura.html` (destellos + frase que se arma), `v5-historia.html` (montaje de archivo a 0.53 s), `v5-sistema.html` (enciclopedia con resaltador + palabras gigantes), `v5-pendientes.html` (celular, lista, notas que caen), `v5-cansado.html` (notificaciones), `v5-han.html` (reproductor + retrato + libro), `v5-ay-mama.html` (pivote negro con trazo SVG), `v5-gusto.html` (cierre blanco, objeto central, serif), `v5-acentos.html` (destellos globales), `subtitulos.html`.

Antes de construir, carga `/hyperframes` (contrato), y `/media-use` para metraje, grade y sonido. Esta skill dice **cómo se ve y se corta**; el contrato de HyperFrames manda sobre cualquier cosa aquí.

## Entradas

- Una locución ya mezclada (WAV/MP3) o un video con voz. **La mezcla de voz no se toca**: va en su propia `<audio id="mezcla-final">` a volumen 1, intacta de principio a fin.
- Transcripción con tiempos por palabra (`voice.transcribeAudio`, o el transcript que ya traiga la app). Todo el corte se rige por esas palabras.
- Opcional: SRT existente, guion, imágenes aportadas.

## Estructura del proyecto

- `index.html` raíz 1080×1920, 30 fps, `data-duration` = fin de la última sección. Solo hosts:
  - Pista 1: una sección por idea del guion (5–15 s cada una; normalmente 12–16 secciones en ~100 s), encadenadas sin huecos.
  - Pista 2: `acentos` (overlay de destellos, toda la duración, z-index 40).
  - Pista 3: `subtitulos` (`data-track-kind="captions"`, z-index 50).
  - Audio: pista 0 mezcla, pista 4 música, pistas 5–6 efectos (`sfx-000`, `sfx-001`…).
- Cada sección corta su escena **en las palabras**: los límites de sección caen al inicio de una frase del transcript.
- Prefijo corto de ids por sección (`ap-`, `hi-`, `si-`…). Todo elemento temporizado escrito en el HTML con id estable.

## Gramática visual

Fondo base negro. Paleta: blanco, negro, amarillo resaltador `#f6e04a`, amarillo subtítulo `#ecd828`, papel `#f4efe2`/`#f3efe6`, rojo insignia `#f03e3e`, halo cian-lila-rosa `#b8eef7 → #d9b3f2 → #f6c4ee`, destello cálido `#fff6e6 → #ffe2b8 → #f3b878`.

Tipografía (fuentes en `assets/fonts/`, copiar desde el proyecto de referencia con sus OFL):
- Frases del narrador: Plus Jakarta Sans 600, 44–45 px, blanco, `letter-spacing:-.02em`, una línea, centradas.
- Palabra de impacto: Montserrat 900, 100 px, MAYÚSCULAS, blanco con sombra suave, sobre metraje.
- Documentos y libros: EB Garamond / Playfair Display itálica.
- Gag de videojuego: Press Start 2P dentro de caja azul `#24466b` con borde dorado.
- Subtítulos: Roboto 500, 50 px / 62 px, `#ecd828`, sombra negra fina, `top:1480px`, ancho 900 px, 2–5 palabras por bloque.

El CSS compartido de todas las escenas está en `plantillas/kit.css.html` (clases `.cam`, `.vig`, `.dim`, `.center`, `.big`, `.ln`, `.print`, `.tag`, `.serif`, `.hl`, `.win`/`.bar`/`.dot`, `.glow`, `.note`, `.badge`, `.gbox`, `.slip`). Pégalo dentro del `<template>` de cada sección.

### Recursos, en el orden en que suelen aparecer

1. **Apertura de destellos**: 3 planos de 0.13–0.27 s antes de 0.67 s (macro del tema, objeto, textura), cada uno con `.cam` que va de scale 1.15–1.25 a −0.07, `ease:"none"`. Luego negro.
2. **Frase que se arma**: sobre negro, la frase del narrador aparece acumulando palabras al ritmo exacto de cada palabra ("Si necesitas" → "Si necesitas café" → …). Un clip por estado, `.ln` centrado. Al cambiar de idea, reinicia con la nueva frase.
3. **Montaje de archivo**: fotos/videos a pantalla completa con cortes de ~0.5 s. Cada plano en `.cam` alternando zoom 1.00→1.08 y 1.08→1.00, `ease:"none"`. Sin texto encima salvo palabras clave.
4. **Palabra gigante sobre metraje**: un video por palabra (1.2–1.3 s), con `.big` encima ("GUSTO / NECESIDAD / OBLIGACIÓN").
5. **Documento con resaltador**: hoja de papel (enciclopedia, receta, ficha) entra desde abajo `y:260, rotation:6 → y:0, rotation:-2` en 0.55 s `expo.out`, luego push-in lento a 1.18; el subrayado `.hl` crece `backgroundSize 0%→100%` en 0.45 s `power2.out` justo en la palabra dicha.
6. **Collage de impresiones**: 5–6 fotos `.print` (marco papel) que entran desde los bordes, una cada 0.22 s, `x/y ±300 → 0`, 0.45 s `expo.out`, alrededor de una frase central.
7. **Celular / pendientes**: video de mano con celular con push-in, lista que se desliza (`y:-520`, `power1.in`), notas `.slip` amarillas que caen girando (`y:-820, rotation:-30 → 0, -20`, `power2.in`), insignia roja `.badge` que crece con `back.out(3)`.
8. **Notificaciones**: `.note` estilo macOS en la esquina, entrando `opacity 0, x 60 → 1, 0` en 0.35 s `expo.out`, una por frase. Textos escritos como mensajes del narrador a sí mismo, nunca correos reales.
9. **Pivote**: corte a negro total con un trazo SVG (`stroke-dashoffset` 1700→0, 0.8 s) y una palabra que hace pop `scale 0.2→1.15` `back.out(3)` y luego sale disparada a `scale 7` `power3.in`, con halo radial.
10. **Ventana clara con halo**: `.win` blanca con barra de semáforos sobre el `.glow` cian-rosa; reproductor/lector con barra de progreso que avanza (`scaleX`), retrato que entra `scale 1.3 → 1` `expo.out`, libro que sube girado.
11. **Sátira**: fotomontaje recortado en tarjetas que entran `scale .82, y 40 → 1, 0` `expo.out`, con fondo que gira lento (`rotation 0→25`, lineal) y pegatinas `back.out(3)`.
12. **Cierre**: fondo blanco, un objeto pequeño central (video CGI generado, en cámara lenta), texto serif negro a los lados ("¿Cuándo fue … por gusto?") y nombre del canal. Antes, opcional, una galería 3D generada (pedestales con objetos del tema, cámara inclinada que se nivela).

### Ritmo

- Corte cada 0.4–1.3 s mientras se enumera; planos de 2–3 s solo cuando la voz se detiene en una idea.
- Toda entrada dura 0.22–0.6 s; los movimientos de cámara duran lo que el plano y son lineales. Eases: `expo.out` para entradas, `back.out(2–3)` para pops, `power1.in`/`power3.in` para salidas, `none` para cámaras.
- Cada tween con `immediateRender:true` en `fromTo`, y la línea `tl.to({},{duration:<D>},0)` al inicio para fijar la duración de la escena.
- **Destellos de acento** (`acentos`): un radial cálido a pantalla completa en cada cambio fuerte de sección, `opacity 0.4–0.9 → 0` en 0.28 s `power2.out`. Unos 8 en 100 s, no en cada corte.

## Material

- Fotos de archivo y obras de dominio público de **Wikimedia Commons** (CC0, PD, CC BY, CC BY-SA). Registra autor, licencia y enlace de cada una en `assets/CREDITOS.md`. En `assets/img/` con nombres cortos en español.
- Metraje faltante: `video.generate` (HeyGen Video 1), 5 s, silenciado (`muted`), sin texto ni marcas; las "recreaciones de archivo" se declaran como tales en créditos. Imágenes de apoyo (texturas de madera, papel, sprites pixel-art) con `image.generate`.
- Citas de autores: si es paráfrasis, se señala como paráfrasis en pantalla o créditos.
- **Grade documental en todas las fotos y videos**: aplica `plantillas/grade-documental.json` mediante el grade de HyperFrames (`data-color-grading` / `hyperframes media-treatment`, ver `/media-use`), nunca con filtros CSS. Material saturado (neones, conciertos) lleva saturación extra −0.15.

## Sonido

- Música: `sound.generateMusic` — "documental, cuerdas y piano, contenido, bajo una voz", ~100 s, `data-volume="0.55"`, con recorte de frecuencias (`data-fx-carve` contra `mezcla-final`, fuerza 0.8). Baja en el pivote y se funde al final.
- Efectos: unos 1.4 por segundo (≈140 en 100 s), cada uno su `<audio id="sfx-NNN">` en pistas 5–6, alineados a su pico con el corte o la entrada. Banco usado (copiable desde `assets/v5/sfx/` del proyecto de referencia, generado con earshot `sfx_render`/`kit_render`):

| Momento | Efecto | Volumen |
| --- | --- | --- |
| Palabra que se agrega a la frase | `tic-texto` | 0.35 |
| Corte de foto de archivo | `obturador-dslr` / `obturador-pelicula` / `obturador-rapido` | 0.33–0.4 |
| Entrada de impresión, tarjeta o lista | `swish-corto` / `swish-suave` | 0.15–0.3 |
| Palabra gigante, golpe de idea | `golpe-punch` / `golpe-aire` / `golpe-sub` | 0.4–0.5 |
| Nota amarilla que cae | `nota-cae` | 0.3 |
| Notificación | `notificacion` / `ding-1…5` | 0.3–0.4 |
| Ventana que abre | `ventana` | 0.45 |
| Resaltador / documento | `papel` | 0.4 |
| Check en lista | `check` | 0.4 |
| Reloj, sueño | `tic-reloj`, `latido` | 0.4–0.55 |
| Cambio de sección | `whoosh-*` | 0.3–0.4 |
| Pivote | `subida-tension` → `impacto-*` / `inversa` | 0.32–0.4 |
| Gag pixel-art | `texto-juego` | 0.3–0.35 |

Revisa la mezcla con earshot (`timeline`, luego `critique`); la voz siempre por encima.

## Flujo

1. Lee el transcript y divide el guion en secciones por idea; anota para cada una qué recurso de la lista usa. Evita repetir el mismo recurso en secciones contiguas.
2. Reúne material (Commons primero, luego generado) y créditos.
3. Construye sección por sección en `compositions/`, con el kit CSS y los tiempos sacados de las palabras.
4. Subtítulos desde el transcript (`captions_apply` o bloques escritos a mano con el estilo de arriba si se pide idéntico); conserva texto y tiempos del SRT si lo hay. Sobre fondos claros, respaldo oscuro discreto detrás del amarillo.
5. Acentos, música y efectos.
6. `hyperframes check --json` sin errores, `hyperframes snapshot` en apertura, pivote, documento, cierre y cada cambio de sección; mira los fotogramas antes de entregar.
