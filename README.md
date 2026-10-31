# Estilos audiovisuales · Pensamientos Inorgánicos

Dos estilos de edición conservados por separado para Codex y Claude. **El estilo cinematográfico Dune v4 fue aprobado por Erick el 31/oct/2026 para sus videos serios**, incluyendo guion, audiovisual y música.

| Petición | Entrada |
|---|---|
| «Como Dune», «ensayo serio cinematográfico» | [pi-ensayo-cinematografico](skills/pi-ensayo-cinematografico/SKILL.md) · Tesseract + HyperFrames + ElevenLabs |
| «Como el café», «Wikimedia Vertical» | [ensayo-documental-vertical](SKILL.md) · tratamiento original 9:16 |

El nuevo estilo mantiene Montserrat Black900 real, apertura typewriter a voz, clips variados, escenas nativas Tesseract integradas en movimiento, texto detrás de sujetos mediante máscaras móviles, atmósfera/grano/partículas selectivas, SFX con intención y música subordinada a la locución. No importa las notificaciones ni las tarjetas pastel del café.

## Estilo cinematográfico aprobado

- [Dirección y flujo](skills/pi-ensayo-cinematografico/references/DIRECCION-Y-FLUJO.md): guion, tesis, storyboard, coordinación Codex/Claude y decisiones humanas.
- [Recetas visuales](skills/pi-ensayo-cinematografico/references/RECETAS-VISUALES.md): tipografía, oclusión, profundidad, texturas y partículas.
- [Recetas de audio](skills/pi-ensayo-cinematografico/references/RECETAS-AUDIO.md): voz única, muestra musical aprobada real, continuación/crossfade, ducking y efectos.
- [Render y recuperación](skills/pi-ensayo-cinematografico/references/RENDER-Y-RECUPERACION.md): segmentación, raíz ligera, mezcla aparte y límites comprobados.
- [QA y aceptación](skills/pi-ensayo-cinematografico/references/QA-Y-ACEPTACION.md): revisión real del MP4 y límites de la referencia.
- [Manifiesto aprobado](skills/pi-ensayo-cinematografico/references/DUNE-V4-APROBADO.json), [archivo/dependencias](skills/pi-ensayo-cinematografico/references/ARCHIVO-Y-DEPENDENCIAS.md), [brief reutilizable](skills/pi-ensayo-cinematografico/assets/brief.json) y [código real seleccionado](examples/dune-v4/README.md).

### Instalar la nueva skill

Con Python3, desde el clon:

```powershell
# Instalación por proyecto para ambos agentes:
python scripts/install_style.py

# O instalación a nivel usuario, con los perfiles existentes:
python scripts/install_style.py --target "$env:USERPROFILE/.codex/skills/pi-ensayo-cinematografico" --target "$env:USERPROFILE/.claude/skills/pi-ensayo-cinematografico" --target "$env:USERPROFILE/.claude-cliente/skills/pi-ensayo-cinematografico"
```

El script conserva otras skills y rehúsa sobrescribir archivos divergentes; `--update` respalda los cambios previos de esta skill antes de reemplazarlos. No crea perfiles ni cambia autenticación/modelos. Para macOS/Linux, usar `--target ~/.codex/skills/pi-ensayo-cinematografico --target ~/.claude/skills/pi-ensayo-cinematografico`. La ruta Cliente sólo aplica si ya existe ese perfil.

Montserrat Black900 y su OFL se incluyen con la skill en `assets/fonts/`; copiar ambos juntos al proyecto. Los medios y bancos particulares se resuelven por manifiesto, no por una descarga de película.

Invocar en Codex `$pi-ensayo-cinematografico` o en Claude `/pi-ensayo-cinematografico`. Si el catálogo aún no refresca, pedir leer directamente su SKILL.md.

```text
Haz este ensayo serio con pi-ensayo-cinematografico, como Dune v4 aprobado.
Expediente: [ruta]. Guion: [ruta]. Voz aprobada: [ruta y hash].
Conserva su gramática Tesseract + HyperFrames, Montserrat Black y diseño
sonoro cinematográfico; adapta las metáforas y música al tema.
Reutiliza medios aprobados y las autorizaciones de esta pieza.
```

### Verificar y archivar

```powershell
python scripts/verify_style.py
# Verificación de binarios en el equipo original:
python scripts/verify_style.py --dossier "RUTA/claude-dune-20261030"
# Congelar código/índice privados en una carpeta NUEVA:
python scripts/archive_reference.py --dossier "RUTA/claude-dune-20261030" --out "RUTA-PRIVADA-NUEVA"
```

`scripts/render_jobs.py PLAN.json` permite ejecutar trabajos locales explícitos con huellas de contenido, control de salida/frames/decode y lock. `--dry-run` calcula huellas sin renderizar. Es una mejora del control de reanudación para piezas futuras; no ejecuta automáticamente el código histórico de Dune. Declarar todas las entradas transitivas (o directorios de assets/compositions sin salidas) y fijar comando/versiones. Las salidas obsoletas se conservan para conciliación; no hay reintento automático.

El repo público no incorpora película, soundtrack ajeno, voz, credenciales ni transcripciones de sesiones. Los medios aprobados se conservan en el expediente local y sus hashes permiten comprobarlos. La música de Dune es original generada con ElevenLabs; las referencias se analizaron localmente para describir carácter, sin subirlas como audio-conditioning. Repetir un prompt no garantiza el mismo audio: la reproducción exacta usa los archivos aceptados.

Las recetas documentan el resultado aprobado y sus límites técnicos. No prometen que un video nuevo se apruebe sin revisión ni que una instalación genere automáticamente el video. No se asigna una licencia nueva a recursos ajenos.

## Estilo café original

Skill de edición de video-ensayo9:16 para HyperFrames: montaje de archivo, tipografía a la voz, collage, documentos resaltados, subtítulos y grade documental. Las instrucciones siguientes describen **sólo el café**.

## Contenido

- `SKILL.md`: guía original, conservada sin cambios.
- `plantillas/grade-documental.json`: preset de color.
- `plantillas/kit.css.html`: estilos compartidos.

## Instalar en otra computadora

La instalación local sirve para **Claude Code y Codex con acceso a archivos**. No instala automáticamente HyperFrames, media-use ni conexiones a proveedores.

### 1. Descargar

Con Git instalado:

```sh
git clone https://github.com/erickinorganico/ensayo-documental-vertical.git
cd ensayo-documental-vertical
```

También puedes usar **Code → Download ZIP** y descomprimir. El repo es público y no necesita credenciales para descargarlo. Instala y autentica el agente que usarás mediante su distribución oficial.

### 2. Instalar la skill completa

Desde la raíz del clon, ejecuta el bloque de tu terminal. Copia `SKILL.md` y `plantillas/` juntos, conservando el nombre de carpeta. No copies sólo el Markdown ni incluyas `.git`.

**Windows · PowerShell:**

```powershell
foreach ($base in @('.claude/skills', '.agents/skills')) {
    $target = Join-Path $base 'ensayo-documental-vertical'
    if (Test-Path -LiteralPath $target) {
        Write-Host "Ya existe; se conserva: $target"
    } else {
        New-Item -ItemType Directory -Path $target -Force | Out-Null
        Copy-Item -LiteralPath 'SKILL.md' -Destination $target
        Copy-Item -LiteralPath 'plantillas' -Destination $target -Recurse
    }
}
```

**macOS/Linux · bash o zsh:**

```sh
for base in .claude/skills .agents/skills; do
  target="$base/ensayo-documental-vertical"
  if [ -e "$target" ]; then
    printf 'Ya existe; se conserva: %s\n' "$target"
  else
    mkdir -p "$target"
    cp SKILL.md "$target/"
    cp -R plantillas "$target/plantillas"
  fi
done
```

Ambos bloques crean una instalación **por proyecto** en el clon. Para otro proyecto, copia esa carpeta `ensayo-documental-vertical` a su `.claude/skills/` o `.agents/skills/`. Para usarla en todos tus proyectos, usa `~/.claude/skills/ensayo-documental-vertical/` en Claude Code o `~/.agents/skills/ensayo-documental-vertical/` en Codex. En Windows, `~` es tu carpeta de usuario. No sobreescribas otra instalación personalizada sin respaldarla.

### 3. Usar en Claude Code

Inicia `claude` desde la carpeta del proyecto con la skill instalada o abre ese proyecto local. Escribe:

```text
/ensayo-documental-vertical
```

Después adjunta o indica la ruta de la locución y sus tiempos por palabra. Si la skill no aparece en el menú `/`, abre una nueva sesión y comprueba `.../ensayo-documental-vertical/SKILL.md`.

### 4. Usar en Codex

Abre el proyecto en la app, extensión o CLI. En CLI/extensión consulta `/skills` o menciona:

```text
$ensayo-documental-vertical
```

También puedes pedirla por su nombre. Si no se detecta, reinicia Codex y revisa la ubicación `.agents/skills/ensayo-documental-vertical/SKILL.md`.

Prompt inicial para ambos:

```text
Usa ensayo-documental-vertical. Lee su SKILL.md y ambas plantillas.
Tengo esta locución ya aprobada: [RUTA AL AUDIO], y estos tiempos:
[RUTA AL TRANSCRIPT/SRT]. No alteres ni regeneres la voz.
Revisa si HyperFrames y media-use están disponibles. Si falta una herramienta
o el proyecto de referencia, dilo. Primero propón secciones, cortes y assets
con créditos. No generes medios pagados ni publiques.
```

### 5. Dependencias y recursos que debes proporcionar

- **HyperFrames y media-use:** son dependencias externas citadas por la skill. Instálalas/configúralas por sus fuentes oficiales; no vienen en este repo. Pide al agente comprobar su disponibilidad antes de ejecutar sus comandos.
- **Referencia Wikimedia Vertical:** la ruta de Windows de `SKILL.md` pertenece al equipo original. Proporciona tu propia copia autorizada o indica explícitamente que trabajarás desde las plantillas sin ese ejemplo. No se descarga con Git.
- **Audio y transcript:** proporciona la locución aprobada, alineación por palabra o SRT. Transcribir no equivale a generar voz; un servicio pagado requiere autorización propia.
- **Assets, fuentes y sonido:** faltan medios de referencia, bancos de efectos y tipografías. Obtén recursos autorizados, conserva sus licencias/OFL y registra créditos. Los nombres de proveedores y llamadas de la guía son referencias, no conexiones instaladas.
- **Codex:** adapta las llamadas específicas de Claude a herramientas realmente disponibles; no des por hecho que un conector existe por leer su nombre.
- **Cowork o nube de Claude:** la instalación local no sincroniza la skill ni sus medios. Habilita la skill para tu cuenta cuando esa modalidad lo requiera y aporta sólo los archivos pertinentes del proyecto.

Este repo contiene instrucciones y plantillas, **no un renderer autónomo ni el proyecto completo del video de referencia**. La comprobación inicial es que el agente pueda identificar la skill y leer ambos archivos de `plantillas/`; un video terminado requiere el entorno y los recursos anteriores.

### Actualizar

Conserva tus cambios y usa `git pull --ff-only` en el clon. Las copias en carpetas de skills no se actualizan automáticamente: compáralas, respáldalas y reemplázalas conscientemente. Los comandos anteriores omiten destinos existentes.

Instalar esta skill no autoriza servicios pagados ni publicación. Mantén la voz aprobada, verifica licencias y revisa el exportado con sonido. No se ha asignado una licencia de software nueva.

Documentación de referencia: [skills en Claude Code](https://code.claude.com/docs/en/skills) y [skills en Codex](https://developers.openai.com/codex/skills/).

Origen: carpeta local de la skill aportada por Erick, snapshot 30/oct/2026. Los tres archivos originales se conservan byte por byte; `SNAPSHOT.json` contiene sus hashes.
