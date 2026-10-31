# Recetas de audio · ensayo cinematográfico PI (aprendidas en Dune v4)

Origen: mezcla aprobada de `Dune-v5-HyperFrames-v4.mp4`. Rutas relativas al expediente `sistema-video/transferencias/claude-dune-20261030/`.
Toda cifra de este documento es la **calibración de esa pieza y esa cama musical**, no una norma universal.

---

## 1. Voz: una sola locución, literal

- Una sola grabación final, intacta: no se regenera, no se recorta ni cambia de velocidad.
  - En Dune: `voz-v5-v4/assets/voz-erick-original.mp3`, 481.76 s, SHA 92579c5e…, ElevenLabs v4 (por Codex).
- **El guion literal y la actuación van en archivos separados.**
  - `GUION-LOCUCION.txt`: literal, sin etiquetas. Es la fuente de subtítulos.
  - `GUION-AUTOTAG-V4.txt`: el mismo texto con auto-tags v4 (`[serious]`, `[conversational]`, `[storytelling]`…) para la síntesis.
  - Los subtítulos se validan contra el literal (`assert "[" not in texto`).
- **Pausas de montaje sin tocar la voz:** se parte en silencios entre palabras y se reubican los segmentos.
  ```html
  <audio id="voz-1" src="assets/audio/voz.mp3" data-start="0.6"   data-media-start="0"      data-duration="10.348" data-fade-in="0.02" data-fade-out="0.02">
  <audio id="voz-2" src="assets/audio/voz.mp3" data-start="12.25" data-media-start="10.348" data-duration="...">
  ```
  En Dune: 1.3 s de pausa tras la cita y 1.9 s para el grito real «Lisan al-Gaib». Los subtítulos se recalculan con el mapa `M(t)` (`construir_v4.py`).
- Verificar al final que el SHA del asset de voz sigue igual al recibo.

## 2. Música: carácter original, aprobación humana, una sola cama

- **Dirección por carácter, no por copia.**
  - Se analizan localmente las referencias que da Erick (escala, subgraves, drones, texturas vocales sin letra, percusión profunda, arco de tensión).
  - El resultado se describe en texto para la generación.
  - No se sube la banda original ni se describe un *audio-conditioning* que no existe.
  - La OST de una película no se vuelve recurso autorizado porque se pida su «sonido».
- **Perfil espectral como filtro previo** (no sustituye la escucha). Fuente: `produccion-hyperframes-v2/herramientas/analizar_musica.py`.
  - Mide energía 20–80 / 80–250 / 250–2k / 2–8k Hz, centroide, ataques/s, rango y arco.
  - En Dune descartó la pista heroica «Crusade» (centroide ≈460 Hz, sub 0.14) frente a candidatas oscuras (sub 0.5+).
  - La decisión final fue de Erick, por escucha: rechazó R1 y aprobó la muestra r2 de 45 s.
- **De muestra aprobada a cama completa** (hecho por Codex): los primeros 40 s son la grabación real aprobada, un crossfade de 5 s y la continuación generada. Cama de 490 s, ajustada a ≈ −26/−28 LUFS, TP −6.
  - Se integra como copia exacta, comprobada por SHA, y **reemplaza** toda música anterior.
  - Comprobar que no queda otra cama: `grep` de camas anteriores en `index.html` = 0.
- Una sola pista desde t=0, recortada al timeline real con `data-fade-out="3.5"`.

### Ducking (automatización `data-automation` de HyperFrames)

Fuente: `lane()` en el builder.

```python
def lane(t0, t1, alto, bajo):              # alto en pausas, bajo bajo la voz
    pts = [(0, alto)]
    for a, z in habla:                     # tramos de voz (palabras fusionadas si el hueco < 1.1 s)
        pts += [(a-t0-0.35, alto), (a-t0, bajo), (z-t0, bajo), (z-t0+0.45, alto)]
    for a, z, v in DIPS:                   # huecos narrativos
        pts += [(a-t0-0.05, bajo), (a-t0, v), (z-t0, v), (z-t0+0.4, alto)]
    # orden estricto de t, ≤512 puntos por carril
```

Calibración para **esta** cama de −26.1 LUFS:

| Momento | Valor |
|---|---|
| Pausas | 0.9 |
| Bajo la voz | 0.22 (0.32 en la primera pasada) |
| Pivotes | 0.05 |
| Grito Lisan (de −0.4 s a +0.6 s tras el hueco) | 0.03 |

Otra cama, otro nivel: se vuelve a medir.

## 3. Medición de la relación voz/resto (sin render extra)

Fuente: `herramientas/ensamblar_v4.py`.

1. Se renderiza sólo la mezcla HF (raíz de audio).
2. Se coloca la voz en el timeline (segmentos `voz-N`), se alinea por correlación cruzada en 0–40 s (±0.25 s) y se resta para obtener el residuo:
   ```python
   LAG = argmax(xcorr(mezcla[:40s], voz_tl[:40s]));  g = <mezcla, voz>/<voz, voz>
   resto = mezcla - g * roll(voz_tl, LAG)
   rel_dB = 20*log10(rms(voz_tl[w]) / rms(resto[w]))   # ventanas de 1.5 s cada 6 palabras
   ```
3. **Resultados de Dune** (263 ventanas):

   | Mezcla | Mediana | p10 | p90 |
   |---|---|---|---|
   | v3 | +10.6 dB | +4.0 dB | +17.5 dB |
   | v4, cama 0.32 | +13.6 dB | +9.9 dB | — |
   | v4 final, cama 0.22 | +14.1 dB | +10.0 dB | +18.3 dB |

   **Lectura correcta:** el residuo incluye SFX, viento y error de resta. Bajar la música de 0.32 a 0.22 sólo subió la mediana 0.5 dB, porque en los momentos más justos ya no domina la música. Es una medición, no una escucha.
4. **Master:**
   - Mezcla HF a −15.1 LUFS, +1.1 dB medidos y `alimiter=limit=0.89`. Resultado: −14.0 LUFS, LRA 2.0, **−0.8 dBTP**. Quedó 0.2 dB por encima del techo de −1 que se buscaba: **no es objetivo**. Siguiente pieza: limitador a 0.87, o true-peak en dos pasadas.
   - Medir siempre la ganancia (`ebur128`); no suponerla.
5. **A/B para escucha humana:** mismos segundos v(n−1) ↔ v(n) en `renders/v4/comparativa/`.

**No canonizar:**
- las 3 muestras recortadas que trae el máster largo de la música (artefacto de la fuente, no revisado a oído; bajar volumen no lo repara);
- el pico de −0.8 dBTP;
- los tiempos intra-frase aproximados.

## 4. Efectos de sonido: por intención, no por cuota

- **Dune v3** tenía 272 SFX: obturador en cada corte, clics de máquina de escribir, `tic`, `ding`, notificaciones. Erick lo leyó como interfaz.
- **Dune v4** tiene 122, todos con motivo:

| Intención | Recurso (banco local propio) |
|---|---|
| Cambio de escena | whoosh pesado/silbido/profundo, 0.12–0.2 (0.2 en cambio de bloque) |
| Palabra gigante | golpe-sub / impacto-aire, 0.22 |
| Documento / resaltador | papel, 0.2–0.4 |
| Pivote | subida-tension → impacto-profundo → inversa |
| Desierto y masa | rumble 6 s y whoosh largo sobre la tormenta y el gusano; riser y downlifter alrededor del grito; impacto grande en la guerra santa |
| Ambiente | viento del desierto continuo, 0.55 sobre una cama de −30 LUFS |

- **Bancos locales usados:**
  - `assets/sfx/`: earshot del proyecto de referencia Wikimedia Vertical, sonidos hechos en código.
  - `assets/sfx-dune/`: pieza Arrakis propia (`impact_rumble`, `whoosh_long`, `riser`, `downlifter`, `impact_big`) y viento sintetizado.
  - No se extraen sonidos de la banda original.
- **Viento determinista** (`assets/sfx-dune/RECETA.txt`):
  ```
  ffmpeg -f lavfi -i "anoisesrc=color=brown:seed=7:amplitude=0.9:duration=492" -f lavfi -i "anoisesrc=color=pink:seed=11:amplitude=0.5:duration=492" \
   -filter_complex "[0]bandpass=f=420:width_type=o:w=2.2,volume='0.55+0.35*sin(2*PI*t/16)+0.1*sin(2*PI*t/5.9)':eval=frame,volume=2.2[v];\
   [1]highpass=f=3500,lowpass=f=9000,volume='0.5+0.5*sin(2*PI*t/9.1+1.3)':eval=frame,volume=0.35[s];[v][s]amix=normalize=0,loudnorm=I=-30:TP=-6"
  ```
  `tremolo` no acepta frecuencias < 0.1 Hz, por eso las ráfagas lentas van con `volume=…:eval=frame`. Es diseño sonoro, **no** sustituye a la música.
- **Audio con fuente real** (el grito de Stilgar):
  - Sólo el tramo de 1.7 s, con fades.
  - Su nivel se mide (la fuente venía a +3 dBTP) y se coloca a 0.16.
  - La imagen se limita a su plano real; el audio puede seguir en L-cut sobre el plano siguiente.
- **Evitar:** dos SFX solapados en la misma pista (`duplicate_audio_track`) asignando la pista libre más baja; y SFX a menos de 0.12 s uno de otro.

## Límites

- No hubo escucha con Earshot en la sesión de Claude. La evaluación de mezcla fue medición más A/B para Erick.
- El nivel de música bajo voz depende de la cama: recalibrar con la medición del §3 en cada pieza.
