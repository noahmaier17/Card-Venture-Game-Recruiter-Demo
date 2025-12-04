# Checks out the recruiter-demo branch on this repository
Write-Host ">> Checkout recruiter-demo branch" -ForegroundColor Cyan
git checkout recruiter-demo

# Merges the main branch to the recruiter-demo branch
Write-Host ">> Merge main into recruiter-demo branch" -ForegroundColor Cyan
git merge main

# 

# Detects if this merge had any conflicts
if ($LASTEXITCODE -ge 1) {
    Write-Host ">> Merge conflict; resolve and then re-run this script" -ForegroundColor Red
    exit 1
}

# Pushs to the remote repository
Write-Host ">> Push recruiter-demo to remote 'demo' repo" -ForegroundColor Cyan
git push demo recruiter-demo

# Checks out the main branch
Write-Host ">> Checkout main branch" -ForegroundColor Cyan
git checkout main

# States the script is complete
Write-Host ">> Script complete" -ForegroundColor Cyan