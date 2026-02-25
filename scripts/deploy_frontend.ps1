# ======================================================
# Script: Updates remote-hosted S3 frontend.
# ======================================================

# Runs the pytest suite to ensure correctness
# Write-Host ">> Running pytest suite" -ForegroundColor Cyan
# pytest

# Logs into aws
Write-Host ">> Logging into AWS" -ForegroundColor Cyan
aws login

# Changes directory
Write-Host ">> Changing directory" -ForegroundColor Cyan
Set-Location $PSScriptRoot
Set-Location "../web_app/frontend"

# Builds the front end
Write-Host ">> Building frontend" -ForegroundColor Cyan
npm run build

# Syncs the AWS S3 bucket, replacing the old frontend data with the new data
Write-Host ">> Syncing to AWS S3" -ForegroundColor Cyan
aws s3 sync dist/ s3://deck-building-card-game-frontend --delete

# Removes what is cached in AWS CloudFront to force an update with the new S3 bucket
Write-Host ">> Force-updating AWS CloudFront cache" -ForegroundColor Cyan
aws cloudfront create-invalidation --distribution-id E2DRS88F59FNK2 --paths "/*" *> $null

# States the script is complete
Write-Host ">> Script complete" -ForegroundColor Cyan