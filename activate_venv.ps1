# Vision I - Virtual Environment Activation Script (PowerShell)

$VenvPath = ".\.venv\Scripts\Activate.ps1"

if (-Not (Test-Path $VenvPath)) {
    Write-Host "[ERROR] Virtual environment '.venv' not found."
    Write-Host "Create it using: py -3.10 -m venv .venv"
    exit 1
}

& $VenvPath

Write-Host "[INFO] Virtual environment activated."
python --version
