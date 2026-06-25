#Requires -Version 5.1
<#
.SYNOPSIS
  Compile main-ieee.tex and report page count (Windows / MiKTeX / TeX Live).
.EXAMPLE
  .\scripts\windows\compile_check.ps1
#>
param(
    [string]$ProjectRoot = (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent),
    [int]$MinPages = 11,
    [int]$MaxPages = 13
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Push-Location $ProjectRoot

function Find-TeXCommand([string]$Name) {
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $miktex = Join-Path $env:LOCALAPPDATA "Programs\MiKTeX\miktex\bin\x64\$Name.exe"
    if (Test-Path $miktex) { return $miktex }
    return $null
}

$pdflatex = Find-TeXCommand "pdflatex"
$bibtex = Find-TeXCommand "bibtex"

if (-not $pdflatex) {
    Write-Error "pdflatex not found. Install MiKTeX or TeX Live."
}

Write-Host "[compile_check] Using pdflatex: $pdflatex"

& $pdflatex -interaction=nonstopmode main-ieee.tex | Out-Null
if ($bibtex) {
    & $bibtex main-ieee 2>&1 | Out-Null
    & $pdflatex -interaction=nonstopmode main-ieee.tex | Out-Null
    & $pdflatex -interaction=nonstopmode main-ieee.tex | Out-Null
}

$pdf = Join-Path $ProjectRoot "main-ieee.pdf"
if (-not (Test-Path $pdf)) {
    Write-Error "main-ieee.pdf was not produced. Check main-ieee.log"
}

$pages = $null
try {
    Add-Type -AssemblyName System.Drawing
} catch {}

# Fallback: parse log for page count
$logPath = Join-Path $ProjectRoot "main-ieee.log"
if (Test-Path $logPath) {
    $log = Get-Content $logPath -Raw
    if ($log -match "Output written on main-ieee\.pdf \((\d+) page") {
        $pages = [int]$Matches[1]
    }
}

if (-not $pages) {
    Write-Warning "Could not detect page count from log."
} else {
    $ok = ($pages -ge $MinPages -and $pages -le $MaxPages)
    $status = if ($ok) { "OK" } else { "OUT_OF_RANGE" }
    Write-Host "[compile_check] Pages: $pages (target $MinPages-$MaxPages) -> $status"
    if (-not $ok) { exit 2 }
}

# Check for undefined citations
if (Test-Path $logPath) {
    $undef = Select-String -Path $logPath -Pattern "Citation .* undefined" -AllMatches
    if ($undef) {
        Write-Warning "Undefined citations found:"
        $undef | ForEach-Object { Write-Warning $_.Line.Trim() }
        exit 3
    }
}

Write-Host "[compile_check] PDF ready: $pdf"
Pop-Location
exit 0
