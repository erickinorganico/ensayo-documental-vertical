# Dirección y flujo del ensayo serio

## Alcance editorial

La preferencia proviene de la aprobación humana del máster Dune v4 (31/oct/2026). Reutilizar su gramática cinematográfica, su integración técnica y su relación entre voz, imagen y sonido. No universalizar el desierto, la paleta ámbar, el grito Lisan, el relato de salvadores ni los mismos clips. Una pieza sobre otro asunto necesita metáforas, material, música y ritmo propios.

La solemnidad visual no borra el cinismo, humor negro, autoimplicación y oralidad de Erick. En un original, conservar metáforas, gags, cierre, negaciones y matices. En guiones nuevos, diferenciar cita comprobada, paráfrasis, interpretación y sátira; evitar inventar vivencias personales. Qwen minimal-v2 es corrector de intervención mínima, no sustituto de su voz. La aprobación de Dune no aprueba automáticamente otro guion.

## Contrato de una pieza

Usar el expediente y `studio.json` actuales. El `assets/brief.json` de esta skill es una entrada de estilo, no un scheduler ni un segundo contrato de producción. Completar:

| Decisión | Resultado verificable |
|---|---|
| Tesis y alcance | Una idea concreta, hechos y límites identificados |
| Guion | Original/versiones, literal separado de acotaciones |
| Voz | Archivo, hash, modelo/voz/recibo si hubo generación |
| Tratamiento | Formato, resolución, ritmo por bloques, metáforas y prohibiciones |
| Material | Inventario con procedencia, duración, ventanas útiles y derechos declarados |
| Timeline | Beats, voces, clips, cámara, texto, música, SFX en el mismo reloj |
| Entrega | Editable, render, portada/copy sólo si pedidos, QA y aprobación por versión |

## Orden útil

1. **Fuentes y guion.** Leer material pertinente; formular la tesis y el recorrido. La referencia tiene 16 párrafos hablados y 1577 palabras; no imponer esa longitud. No producir una nueva voz para probar cambios de montaje.
2. **Voz y tiempos.** Congelar literal y toma existente. Si aún no hay toma y está autorizada, preparar autotags por intención sin alterar texto. Obtener alineación local cuando sea posible; revisar nombres y pausas. No inventar precisión por palabra a partir de estimaciones de lectura.
3. **Mapa visual.** Alternar escala, sujetos, acciones, archivo y motion. Registrar por plano qué idea explica. Medir repeticiones por asset y por encuadre, no sólo por nombre de archivo. Evitar congelados largos que sólo acompañan párrafos.
4. **Tesseract.** Construir escenas que necesiten profundidad y movimiento por capas. Guardar .tsrct, assets y parámetros de cámara. Exportar clips nativos e incorporarlos con ventanas de tiempo reales en HyperFrames.
5. **HyperFrames.** Montar cortes a voz, Montserrat Black, typewriter y texto detrás de sujetos; integrar escenas Tesseract sin aplanarlas a fotos. Usar parte del banco café cuando encaje: papeles, impactos, whooshes y técnicas de composición. No importar su interfaz/notificaciones ni su densidad de chasquidos.
6. **Música y sonido.** Escuchar muestra corta de la nueva dirección si hace falta; mantener muestra aceptada y aprobar su integración dentro del alcance humano. Sustituir camas anteriores, no acumular. Esculpir viento/ambiente, impactos, risers, caídas y silencios narrativos. Ducking con voz/diálogo.
7. **Pasajes críticos.** Ver extractos de apertura, oclusión, transición intensa, diálogo y cierre. Resolver defectos antes de exportar ocho minutos de nuevo. Una nueva aprobación no es necesaria por una corrección técnica ya autorizada.
8. **Render segmentado y mezcla.** Reusar segmentos sólo con entradas idénticas y QA válida. Separar imagen/audio; corregir sólo lo afectado. Medir progreso útil de frames/tiempo reciente, detectar procesos muertos y conciliar antes de reanudar.
9. **Revisión final y entrega.** Decodificar completo, inspeccionar beats y cortes, escuchar mezcla final. Registrar límites reales. Mostrar archivo completo. La aprobación humana se vincula a ese hash; publicar requiere la autorización de publicación correspondiente.

## Reparto Codex ↔ Claude

**Codex:** continuidad/brief, registro humano, procedencia y selección de assets, ElevenLabs cuando esté autorizado, utilidades deterministas, integración, diagnóstico y QA independiente.

**Claude:** lectura de brief acotado, storyboard visual, cámara, composición, animación, oclusiones, montaje HF/Tesseract y documentación de sus decisiones. Puede ejecutar tareas técnicas según ownership acordado.

**Scripts:** medición, montaje reproducible, render, validación y hashes. No llamar a un modelo para cada render o medición.

Conservar el perfil Claude elegido por Erick y modelo/esfuerzo heredados. En Dune fue Cliente/Ai Lab School y sesión `0b2f65bc-3bc8-40c8-9679-f88903e6632e`; ese UUID es antecedente de esa pieza, no el ID para todos los videos nuevos. No copiar credenciales/permisos globales en repositorios. Cada intento registra salida y recibo; un fallo de redirect no justifica duplicar producción.

## Rechazos que dieron forma al estilo

| Antes, rechazado | Decisión aprobada |
|---|---|
| Música genérica o demasiado alta | Dirección musical acorde al tema y voz dominante, mezcla contrastada |
| Cama larga regenerada sólo «parecida» | Primeros 40 s del audio aprobado real y transición de 5 s a continuación |
| Tarjeta de cita pastel/degradado prolongada | Tratamiento oscuro coherente, tipografía y ritmo integrados |
| Cubo/aguja usados como relleno recurrente | Clips variados, motivación por plano y secuencia Arrakis animada real |
| «Mascota oficial» sostenido | Remate breve de 1.2 s |
| Notificaciones a 3:24 y otros bloques | Prohibición completa de notificaciones en este tratamiento |
| Texto gigante tapando rostro | Fondo → texto → sujeto recortado y sincronizado |
| 272 SFX con clics repetitivos | 122 en la referencia final, elegidos por función, sin nueva cuota |
| Render monolítico/carpeta enorme | Segmentos de imagen, raíz ligera, mezcla aparte y recuperación por huellas |

El café original sigue disponible en la raíz del repo; no se modifica para convertirlo en Dune.
