#Requires -Version 5.1
<#
.SYNOPSIS
  Test post-processing pipeline with synthetic CSVs (Windows-native Python).
#>
param(
    [string]$ProjectRoot = (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent)
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Push-Location $ProjectRoot

Write-Host "[pipeline_test] Generating synthetic CSVs..."
python scripts/python/generate_synthetic_csv.py --out data/estimated/aggregated --seeds 20

Write-Host "[pipeline_test] Running statistics..."
python scripts/statistics/compute_statistics.py `
    --input data/estimated/aggregated `
    --output data/estimated/aggregated/statistics

Write-Host "[pipeline_test] Figure dry-run..."
python scripts/python/generate_figures.py `
    --csv data/estimated/aggregated `
    --out Figures/ `
    --dry-run

Write-Host "[pipeline_test] Unit tests..."
python -m unittest scripts/statistics/test_compute_statistics.py -v

Write-Host "[pipeline_test] DONE"
Pop-Location
