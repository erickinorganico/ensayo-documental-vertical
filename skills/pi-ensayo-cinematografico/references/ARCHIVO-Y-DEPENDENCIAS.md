# Archivo y dependencias

## Qué se conserva

El máster aprobado queda inmutable por versión y SHA256. Conservar además HTML/compositions/scripts/datos/lockfiles de HyperFrames, .tsrct nativos, guion literal/autotags, voz original, muestras y cama musical aprobadas, máscaras, fuentes/OFL, clips usados, SFX y procedencia. Registrar aprobación editorial separada de entrega/QA. Los originales del expediente no se eliminan ni se reemplazan por una nueva generación.

`scripts/archive_reference.py --dossier RUTA --out CARPETA-NUEVA` crea un índice privado de archivos con hash/tamaño, un ZIP de fuentes editables y una copia de mediciones/entregas. No copia grandes medios al repo público ni afirma que el ZIP de código contiene todas las dependencias. Los medios se resuelven en el dossier y quedan en el manifiesto privado. No ejecutar el archivo congelado como plantilla universal: sus scripts contienen supuestos y nombres del caso Dune.

El manifiesto público `DUNE-V4-APROBADO.json` identifica la referencia por rutas relativas al expediente, hash y parámetros medidos. La ruta local al expediente se instala por separado en `local-reference.json` (ignorado por Git), con herramientas/voz/perfil del equipo. No publicar IDs de proveedor, transcripciones de sesiones ni permisos personales como parte del estilo.

## Dependencias probadas

- HyperFrames CLI0.8.223 para la revisión final; GSAP en composiciones HTML. Preservar package/lock/versiones del proyecto.
- Tesseract CLI0.4.0 y formato nativo .tsrct de las escenas aportadas.
- FFmpeg/ffprobe, Python3 y PowerShell7 para render/medición/segmentación.
- Montserrat Black900 real y su OFL. Otros fonts del café no reemplazan esta preferencia.
- Herramientas locales para segmentación humana móvil (u2net_human_seg en la referencia) y Earshot para revisar sonido cuando disponible.
- ElevenLabs para nuevas voces/música sólo cuando lo autorice la pieza. Descargar, instalar o leer la skill no consume por sí mismo ni autoriza generaciones nuevas.

El repo incluye lógica, recetas, brief, componentes demostrativos sin medios ajenos y scripts de archivo/verificación. No instala aplicaciones, crea cuentas ni trae voz/clips/música de Dune. El código de ejemplo demuestra decisiones de tiempo/capas y debe adaptarse a los contratos nativos del renderer instalado.

## Portabilidad y reproducción

Otra computadora necesita medios autorizados del expediente, las versiones compatibles y un mapa de rutas. Antes de renderizar, comprobar disponibilidad y hashes; si falta un clip aprobado, reportarlo y no sustituir silenciosamente por otro. Para reutilizar el lenguaje visual basta un tema nuevo con sus assets; para reproducir el mismo Dune hacen falta todos sus inputs.

La generación de IA es variable: conservar binarios aceptados y sus recibos permite reutilizarlos; volver a pedir el mismo prompt no promete igualdad. Las referencias sonoras de Dune se analizaron localmente y guiaron texto de prompt, sin upload ni audio-conditioning al generador.
