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

function Invoke-CheckedCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Command,

        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE`: $Command $($Arguments -join ' ')"
    }
}

if (-not (Test-Path $VenvPython)) {
    Invoke-CheckedCommand $PythonPath -m venv $VenvDir
}

Invoke-CheckedCommand $VenvPython -m pip install --upgrade pip
Invoke-CheckedCommand $VenvPython -m pip install -r (Join-Path $BackendDir "requirements.txt")

if (-not $SkipDev) {
    Invoke-CheckedCommand $VenvPython -m pip install -r (Join-Path $BackendDir "requirements-dev.txt")
}

Write-Host "Backend virtual environment is ready at $VenvDir"
