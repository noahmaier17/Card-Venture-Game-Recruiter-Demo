# ======================================================
# Script: Updates remote-hosted Lambda backend/website.
# ======================================================

# Activates the virtual environment that zappa requires
Write-Host ">> Activating virtual environment" -ForegroundColor Cyan
& ".\.venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host ">> Installing dependencies" -ForegroundColor Cyan
pip install .

# Runs the pytest suite to ensure correctness
Write-Host ">> Running pytest suite" -ForegroundColor Cyan
pytest

# Logs into aws
Write-Host ">> Logging into AWS" -ForegroundColor Cyan
aws login

# Updating zappa deployment
Write-Host ">> Updating zappa deployment of the Card Service" -ForegroundColor Cyan
zappa update dev

Write-Host ">> Updating zappa deployment of the Entities Service" -ForegroundColor Cyan
zappa update entities-dev

# States the script is complete
Write-Host ">> Script complete" -ForegroundColor Cyan