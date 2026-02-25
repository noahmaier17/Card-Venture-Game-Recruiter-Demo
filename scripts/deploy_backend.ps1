# ======================================================
# Script: Updates remote-hosted Lambda backend/website.
# ======================================================

# Activates the virtual environment that zappa requires
Write-Host ">> Activating virtual environment" -ForegroundColor Cyan
& ".\.venv\Scripts\Activate.ps1"

# Runs the pytest suite to ensure correctness
Write-Host ">> Running pytest suite" -ForegroundColor Cyan
pytest

# Logs into aws
Write-Host ">> Logging into AWS" -ForegroundColor Cyan
aws login

# Updating zappa deployment
Write-Host ">> Updating zappa deployment" -ForegroundColor Cyan
zappa update dev

# States the script is complete
Write-Host ">> Script complete" -ForegroundColor Cyan