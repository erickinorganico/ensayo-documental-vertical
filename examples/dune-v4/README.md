# Código real de Dune v4

Estos cuatro archivos conservan la implementación que produjo el máster aprobado, con la única normalización de finales de línea CRLF→LF. El manifiesto registra hash de fuente y de copia. Se mantienen como **referencia histórica**, sin ejecutar ni cambiar sus supuestos automáticamente:

- `particulas.py`: Canvas/GSAP, semilla y tiempo absoluto; ventanas del montaje Dune.
- `segmentar.py`: raíces HyperFrames por grupos de escenas, tiempos rebajados y audio separado.
- `render-v4.ps1`: lote local persistente/reanudable probado en Dune.
- `ensamblar_v4.py`: concatena imagen, incorpora audio, mide máster y diagnóstico de mezcla.

No ejecutarlos desde esta carpeta: buscan `datos/`, `compositions/`, `assets/`, `seg/` y herramientas del proyecto original. El paquete público no contiene esos medios ni el video de Dune. El ZIP privado del expediente conserva el editable completo; el manifiesto privado identifica medios/dependencias que permanecen allí.

**Mejora necesaria para el próximo proyecto:** el lote original acepta un segmento por cantidad de cuadros. Para reanudar de forma segura, comprobar también huella de entradas (HTML, escenas dependientes, fuentes, clips, SFX, música si corresponde), versión/opciones del renderer y decode; si cambian, invalidar ese segmento. No copiar el criterio histórico de frames como garantía de vigencia. También revisar MAXV/recursos reales en la máquina nueva y no repetir dos pasadas por rutina.

Para el flujo mantenido, cargar `../../skills/pi-ensayo-cinematografico/SKILL.md`. `SOURCE-MANIFEST.json` permite auditar el origen sin empaquetar clips, soundtrack ajeno o datos de cuentas.
