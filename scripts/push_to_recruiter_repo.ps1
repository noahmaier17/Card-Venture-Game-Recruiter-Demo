# If we are currntthere are any uncommited changes on the current branch (likely main branch), does not run the script
if (git status --porcelain) {
    Write-Host ">> Manually commit all changes/reolve all conflicts on this branch before running this script" -ForegroundColor Red
    exit 1
}

# Checks out the recruiter-demo branch on this repository
Write-Host ">> Checkout recruiter-demo branch" -ForegroundColor Cyan
git checkout recruiter-demo

# Merges the main branch to the recruiter-demo branch IF we do not already have a merge in progress
if (Test-Path ".git/MERGE_HEAD") {
    Write-Host ">> Skipping merge step; merge already in progress" -ForegroundColor Cyan
} else {
    Write-Host ">> Merge main into recruiter-demo branch" -ForegroundColor Cyan
    git merge main
}

# Health check of git status
git status

# Removing git tracking in the recruiter-demo branch that I do not want pushed
git rm -r '.\Storage of Deprecated Things'

# Health check of git status
git status

# Detects if this merge had any conflicts
if (git ls-files -u) {
    Write-Host ">> Merge conflict; resolve and then re-run this script" -ForegroundColor Red
    exit 1
}

# Commits changes IF we have any files to commit
if (-not (git status --porcelain)) {
    Write-Host ">> Nothing to commit to recruiter-demo" -ForeGround Yellow
} else {
    Write-Host ">> Commit changes to recruiter-demo" -ForegroundColor Cyan
    git commit -m "Merge branch 'main' into recruiter-demo"    
}

# Pushs to the remote repository
Write-Host ">> Push recruiter-demo to remote 'demo' repo" -ForegroundColor Cyan
git push demo recruiter-demo

# States the script is complete
Write-Host ">> Script complete; remember to 'checkout main branch' if desired" -ForegroundColor Cyan
