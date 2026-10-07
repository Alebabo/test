[CmdletBinding()]
param([ValidateSet('Daily','WatchC24','Automation')][string]$Mode = 'Automation')
$ErrorActionPreference = 'Stop'
# Separate entrypoint: the original Reddit-only script remains available.
$python = Get-Command py -ErrorAction SilentlyContinue
if ($python) {
    & $python.Source -3 (Join-Path $PSScriptRoot 'monitor.py') --mode $Mode --quiet
} else {
    $python = Get-Command python -ErrorAction Stop
    & $python.Source (Join-Path $PSScriptRoot 'monitor.py') --mode $Mode --quiet
}
exit $LASTEXITCODE
