---
name: pi-ensayo-cinematografico
description: Produce ensayos serios de Pensamientos Inorgánicos con el estilo Dune v4 aprobado por Erick, combinando escenas Tesseract, montaje HyperFrames, voz y música ElevenLabs, tipografía Montserrat Black, oclusiones y diseño sonoro cinematográfico. Úsala para «como Dune», «ensayo serio cinematográfico» o una continuación de este tratamiento.
---

# PI · ensayo cinematográfico

Referencia aprobada por Erick el 31/oct/2026: **Dune v5 / HyperFrames v4**, 488.4 s, SHA256 `fac351572ac33b6d4fdaacef7811ea181762c588d4fd093d9f93f74a68233da8`. La aprobación comprende guion, audiovisual y música. Este tratamiento es la preferencia para sus videos serios. No sustituye el estilo café/vertical ni otras líneas de PI.

«Replicar al 100%» significa conservar decisiones, parámetros, materiales aceptados y evidencia de la referencia, adaptando el contenido al nuevo tema; no prometer una generación musical idéntica ni repetir motivos de Dune en todos los ensayos. Para reproducir el archivo exacto, conservar el máster y los assets congelados: las instrucciones solas no regeneran las mismas muestras.

## Entrar y elegir el trabajo

Leer continuidad y expediente de la pieza, instrucciones humanas y [DIRECCION-Y-FLUJO.md](references/DIRECCION-Y-FLUJO.md). Mantener el único `studio.json`, idioma, voz, IDs y calendario existentes. El guion original manda; separar literal y acotaciones. Una obra nueva parte de fuentes comprobadas y una tesis, no de sustituir nombres en Dune.

- **Pieza nueva:** completar [brief.json](assets/brief.json) dentro de su expediente; resolver sólo datos faltantes que impidan avanzar.
- **Cambio en una pieza:** congelar versión vigente y modificar sólo la capa afectada. Si cambia música, conservar renders visuales válidos.
- **Reproducción exacta Dune:** leer [DUNE-V4-APROBADO.json](references/DUNE-V4-APROBADO.json) y [ARCHIVO-Y-DEPENDENCIAS.md](references/ARCHIVO-Y-DEPENDENCIAS.md); verificar archivos/hashes antes de reconstruir.

## Decisiones de estilo

Montserrat **Black real, peso 900**, para apertura/typewriter, titulares y subtítulos de este tratamiento. Texto anclado a voz e idea; jerarquía antes que cantidad. Tipografía detrás de sujetos mediante fondo → texto → recorte móvil real; comprobar máscaras al inicio, medio, cierre y cortes internos.

Archivo real y licencia en `assets/fonts/Montserrat-Black.ttf` y `assets/fonts/OFL-Montserrat.txt`: copiar ambos al proyecto, conservar OFL y verificar carga efectiva.

Predominio de clips variados y pertinentes, atmósfera sostenida cuando la idea la necesita, aceleración en enumeraciones y transiciones con función. No usar un objeto como relleno repetido. El gag «mascota oficial» duró 1.2 s en Dune: ejemplo de brevedad, no rótulo obligatorio.

Tesseract aporta escenas nativas de profundidad, capas, cámara y atmósfera; exportarlas e integrarlas **como movimiento real** en HyperFrames. Un zoom sobre un PNG no acredita el uso de la secuencia animada suministrada. HyperFrames integra montaje, tipografía, oclusiones, subtítulos, efectos y mezcla final.

Grano, desgaste, fugas de luz y glitch responden al material. Motas/polvo y chispas se sitúan con luz, profundidad y tiempo determinista, atenuadas en los subtítulos. No saturar todo con VHS/glitch. **Sin notificaciones de escritorio/móvil, tarjetas pastel ni degradados ajenos al tono**: el feedback de Dune prevalece sobre los recursos café que mencionan notificaciones.

Consultar [RECETAS-VISUALES.md](references/RECETAS-VISUALES.md) al componer y [RECETAS-AUDIO.md](references/RECETAS-AUDIO.md) al sonorizar. La densidad de cortes/SFX y la duración se deciden por el guion; 122 SFX y ocho minutos son datos de Dune, no cuotas.

## Voz, música y aprobación

Reutilizar voz aprobada sin nueva síntesis. Si el encargo autoriza una nueva: Erick Inorganico / ElevenLabs v4 y autotags separados, preservando literal; registrar herramienta/modelo/recibo y alcance. Los autotags de Dune los preparó Codex; no afirmar que se usó Enhance nativo.

Música original con carácter del tema, por debajo de la voz y con espacio para SFX/diálogo. Para nueva dirección musical, escuchar una muestra antes de completar e integrar una pista larga; reutilizar aprobación que ya exista. Conservar el audio aprobado real, no sustituirlo por algo «similar». Análisis de una referencia no significa haber subido su soundtrack al generador. No prometer audio-conditioning si no se utilizó.

Mantener una sola cama activa al reemplazar música. Los coeficientes de Dune son calibración de sus fuentes: verificar mezcla real y A/B, no copiar volumen 0.22 como garantía universal. La voz manda tanto en pasajes intensos como tranquilos.

## Producir, verificar y entregar

Usar [RENDER-Y-RECUPERACION.md](references/RENDER-Y-RECUPERACION.md) para el render local segmentado y sus límites. Fijar versión probada del renderer y dependencias; no instalar versiones nuevas por rutina. Guardar inputs/huellas, frame ranges y recibos; un archivo con los mismos frames pero entradas nuevas está obsoleto.

Revisar apertura/typewriter, cada beat, todos los recortes, transiciones y cierre en **MP4 final**. Escuchar voz/música/efectos y medir clipping, LUFS, picos y sincronía. Un PASS de metadata o una captura bonita no basta. [QA-Y-ACEPTACION.md](references/QA-Y-ACEPTACION.md) distingue metas, mediciones históricas y límites.

Entregar MP4 completo y editable con dependencias/créditos, versión/hash y evidencia real. Si Erick solicita primero Tesseract, mostrar y registrar esa entrega antes de comenzar el derivado HyperFrames. No convertir ese orden particular en un paso obligatorio para todo video nuevo.

Codex coordina assets/audio/QA y Claude composición/montaje mediante el puente ya configurado si el encargo incluye esa colaboración. Un dueño por archivo, brief pequeño, mismo UUID al continuar una pieza, sin llamadas recursivas. Los scripts deterministas no requieren otra conversación. Nunca inferir progreso de un PID viejo ni dar ETA sin medición reciente. Mantener autorizaciones vigentes; instalar esta skill no activa pagos, publicación, conexiones ni recurrencia.
