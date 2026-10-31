# QA y aceptación

## Referencia aprobada vs metas futuras

Dune v4 entregado y aprobado: 1920×1080,30fps,488.4s,H264/AAC48k estéreo,377445479bytes. −14.0 LUFS integrados,−0.8dBTP,LRA2.0; 0 clipping en medición final; decodificación completa sin errores. Voz/resto mediana+14.1dB,p10+10.0,p90+18.3 en263ventanas; lag0muestras a16kHz. El resto por sustracción incluye SFX y error de resta, no es una medida de voz/música aisladas.

Son mediciones de un resultado aprobado, no receta universal de masterización. Para una pieza nueva, comenzar por un techo de true peak≤−1dBTP y nivel integrado apropiado al destino; medir tras AAC y ajustar a escucha. No copiar LRA2.0 como obligación ni intensificar compresión para igualar una cifra.

## Antes de declarar listo

- Guion/voz: literal conservado, pronunciación relevante, cierre íntegro y ningún salto involuntario. Hash de voz original/colocación; si hay hueco por diálogo, registrarlo en timeline.
- Fuentes: comprobar que los planos muestran lo que el inventario dice; recortar logos, títulos, fundidos y cortes internos inesperados cuando perjudican el montaje. No atribuir una etiqueta de clip sólo por su nombre.
- Tipografía: cargar archivo Montserrat Black900 real, tildes correctas, typewriter sincronizado a lo hablado. Evitar que un rótulo sobreviva a la idea.
- Oclusiones: revisar inicio, medio, final y bordes/pelo/manos; mismo encuadre y reloj entre fondo/recorte. Muestrear alrededor de cortes internos y transiciones. Comprobar visualmente, no sólo buscar z-index.
- Variedad: revisar hoja de contacto completa y un inventario por asset/segundos/uso. Repetir con intención narrativa; evitar mismos objetos por falta de selección.
- Partículas/overlays: luz y profundidad motivadas, subtítulos despejados; seek directo y muestreo secuencial al mismo tiempo deben concordar. Glitch/VHS selectivos, nunca suplantan dirección.
- Audio: escuchar apertura, voz tranquila/intensa, transición, diálogo, clímax/cierre; A/B en mismos segundos. Earshot si disponible para análisis/juicio de audio, y declarar cobertura real. Medir niveles/picos/clipping y revisar si ambiente/SFX compiten cuando la música ya está baja.
- MP4: verificar duración, streams, frames/fps y decodificación completa. Detección de negros/silencio produce candidatos, no fallos automáticos: distinguir pausa deliberada, fundido de fuente y fallo técnico.
- Revisión: evidence enlazada a versión/hash. Un cambio invalida QA de la capa afectada, no obliga a repetir todo lo intacto. Preservar editable y dependencias.

## Límites históricos que no se deben copiar como objetivos

- Tiempos dentro de frase en Dune se aproximaron por pausas; no hubo alineación ASR completa. La aprobación humana no convierte esa aproximación en transcripción certificada.
- Tres tramos oscuros de0.5–0.6s de tráiler persistieron hacia1:48,3:28,3:41, además de la pausa de apertura. Revisarlos si se reabre la pieza; no añadir negros por imitación.
- La música fuente larga tuvo3muestras recortadas. La atenuación no reconstruye muestras perdidas; distinguir defecto fuente de clipping final.
- −0.8dBTP quedó0.2dB por encima de la meta−1. No elevar el techo de otras piezas por ese precedente.
- Los clips cinematográficos no son CC ni se certificó fair use por el tipo ensayo. Mantener procedencia/licencias y no empaquetar películas ni soundtrack ajeno como recursos libres.

La valoración explícita de Erick aprueba esta versión completa. No afirmar que todos los problemas históricos son beneficios de estilo ni alterar el máster aprobado para «normalizarlo» sin encargo.
