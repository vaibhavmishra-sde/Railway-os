[CmdletBinding()]
param(
    [switch]$SkipDev
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$BackendDir = Join-Path $RepoRoot "backend"
$VenvDir = Join-Path $BackendDir ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"

$PythonCommand = Get-Command python -ErrorAction Stop
$PythonPath = if ($PythonCommand.Path) { $PythonCommand.Path } else { $PythonCommand.Source }

if (-not (Test-Path $VenvPython)) {
    & $PythonPath -m venv $VenvDir
}

& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install -r (Join-Path $BackendDir "requirements.txt")

if (-not $SkipDev) {
    & $VenvPython -m pip install -r (Join-Path $BackendDir "requirements-dev.txt")
}

Write-Host "Backend virtual environment is ready at $VenvDir"
