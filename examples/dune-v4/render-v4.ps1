# Render completo v4 por segmentos (persistente y reanudable) dentro de _render/ (espacio ligero < 2 GiB).
# Prepara antes:  python herramientas/segmentar.py ; python herramientas/preparar_render.py
param([int]$Workers = 3, [string]$Calidad = "looks")
$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $PSScriptRoot; $ws = Join-Path $root "_render"; Set-Location $ws
$out = Join-Path $root "renders\v4"; New-Item -ItemType Directory -Force $out | Out-Null
$log = Join-Path $out "_lote.log"
$plan = Get-Content (Join-Path $root "seg\plan.json") -Raw -Encoding UTF8 | ConvertFrom-Json
"LOTE INICIO $(Get-Date -Format o) pid=$PID" | Out-File $log -Append -Encoding utf8
function Cuadros($f) { if (-not (Test-Path $f)) { return -1 }; $n = & ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 $f 2>$null; if ($n) { [int]$n } else { -1 } }
$orden = @(@{n="audio"; f="seg-audio.html"; fr=$plan.frames})   # la relación voz/música se mide offline (ensamblar_v4.py)
foreach ($s in $plan.segmentos) { $orden += @{n=('{0:d2}' -f $s.seg); f=$s.archivo; fr=$s.frames} }
foreach ($pase in 1..2) {
  foreach ($o in $orden) {
    $mp4 = Join-Path $out "seg-$($o.n).mp4"; $c = Cuadros $mp4
    if ([math]::Abs($c - $o.fr) -le 1) { continue }
    "RENDER seg-$($o.n) pase=$pase esperados=$($o.fr) $(Get-Date -Format o)" | Out-File $log -Append -Encoding utf8
    & npx.cmd --yes hyperframes@0.8.223 render --composition $o.f --fps 30 --quality $Calidad --workers $Workers -o $mp4 *> (Join-Path $out "seg-$($o.n).log")
    $c = Cuadros $mp4
    "FIN seg-$($o.n) exit=$LASTEXITCODE cuadros=$c esperados=$($o.fr) $(Get-Date -Format o)" | Out-File $log -Append -Encoding utf8
  }
}
"LOTE FIN $(Get-Date -Format o)" | Out-File $log -Append -Encoding utf8
