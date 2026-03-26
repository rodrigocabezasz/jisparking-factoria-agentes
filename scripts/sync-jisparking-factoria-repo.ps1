<#
.SYNOPSIS
  Copia al clon de jisparking-factoria-agentes los archivos del manifiesto oficial
  desde la raíz del monorepo (padre de la carpeta scripts).

.PARAMETER TargetRepoRoot
  Ruta absoluta al clon local de https://github.com/rodrigocabezasz/jisparking-factoria-agentes
#>
param(
    [Parameter(Mandatory = $true)]
    [string] $TargetRepoRoot
)

$ErrorActionPreference = "Stop"
$Src = Resolve-Path (Join-Path $PSScriptRoot "..")
$Dst = Resolve-Path $TargetRepoRoot

Write-Host "Origen:  $Src"
Write-Host "Destino: $Dst"

function Ensure-Dir([string] $p) {
    if (-not (Test-Path $p)) { New-Item -ItemType Directory -Force -Path $p | Out-Null }
}

# README raíz
Copy-Item (Join-Path $Src "README.md") (Join-Path $Dst "README.md") -Force

Ensure-Dir (Join-Path $Dst "factoria")
$factoriaFiles = @(
    "GUIA_OFICIAL_REG_TELEGRAM.md",
    "GOVERNANCE_STATE_ACTORS.md",
    "openclaw-jislab-map.md",
    "WEB_REG_Y_OPENCLAW.md",
    "PASOS_ACTUALIZAR_OPENCLAW.md",
    "INDICE_DOCUMENTACION.md",
    "PUBLICACION_REPO_GITHUB.md",
    "openclaw.json.example",
    "README_openclaw_json_example.md"
)
foreach ($f in $factoriaFiles) {
    $sf = Join-Path $Src "factoria\$f"
    if (-not (Test-Path $sf)) { Write-Warning "Falta en origen: $sf"; continue }
    Copy-Item $sf (Join-Path $Dst "factoria\$f") -Force
}

foreach ($w in @("workspace-asistente-jislab", "workspace-ops-despliegue-jislab")) {
    $s = Join-Path $Src "factoria\$w"
    if (-not (Test-Path $s)) { Write-Warning "Falta workspace: $s"; continue }
    Copy-Item $s (Join-Path $Dst "factoria\$w") -Recurse -Force
}

Ensure-Dir (Join-Path $Dst "scripts")
foreach ($s in @("export_dev_jis_to_github.py", "factory_reg_post.py", "sync-jisparking-factoria-repo.ps1")) {
    $sf = Join-Path $Src "scripts\$s"
    if (-not (Test-Path $sf)) { Write-Warning "Falta script: $sf"; continue }
    Copy-Item $sf (Join-Path $Dst "scripts\$s") -Force
}

Ensure-Dir (Join-Path $Dst ".agents\Req_JIS")
$agentsDir = Join-Path $Src ".agents\Req_JIS"
if (Test-Path $agentsDir) {
    Copy-Item (Join-Path $agentsDir "*") (Join-Path $Dst ".agents\Req_JIS") -Force
} else {
    Write-Warning "Falta carpeta: $agentsDir"
}

# Evitar duplicado: guía solo en factoria/
$dup = Join-Path $Dst "GUIA_OFICIAL_REG_TELEGRAM.md"
if (Test-Path $dup) {
    Remove-Item $dup -Force
    Write-Host "Eliminado duplicado en raiz: GUIA_OFICIAL_REG_TELEGRAM.md"
}

Write-Host "Listo. Ejecuta git status en el destino y commit + push."
