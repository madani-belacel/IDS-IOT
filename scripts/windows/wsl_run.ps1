#Requires -Version 5.1
<#
.SYNOPSIS
  Detect WSL2 and optionally run a bash command inside Ubuntu.
.EXAMPLE
  .\scripts\windows\wsl_run.ps1 -Command "cd /mnt/c/path/IDS_IOT && ./SIMULATION_CAMPAIGN_READY/run_campaign.sh --dry-run"
#>
param(
    [Parameter(Mandatory = $false)]
    [string]$Command = "echo WSL OK",
    [string]$Distro = "Ubuntu-22.04"
)

$wsl = Get-Command wsl -ErrorAction SilentlyContinue
if (-not $wsl) {
    Write-Error "WSL not installed. Run: wsl --install -d Ubuntu-22.04"
}

$distros = (& wsl -l -v 2>&1) -join "`n"
if ($distros -notmatch [regex]::Escape($Distro)) {
    Write-Warning "Distro '$Distro' not found. Available:`n$distros"
    Write-Host "Install: wsl --install -d Ubuntu-22.04"
}

Write-Host "[wsl_run] Executing in WSL ($Distro): $Command"
& wsl -d $Distro -- bash -lc $Command
exit $LASTEXITCODE
