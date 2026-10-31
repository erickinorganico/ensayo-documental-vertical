# Ensayo documental vertical

Skill de edición de video-ensayo 9:16 para HyperFrames: montaje de archivo, tipografía a la voz, collage, documentos resaltados, subtítulos y grade documental.

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
