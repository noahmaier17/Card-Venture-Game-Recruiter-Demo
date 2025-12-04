# If there are any uncommited changes on the current branch (likely main branch), does not run the script
git checkout main
if (git status --porcelain) {
    Write-Host ">> Commit all changes before running this script" -ForegroundColor Red
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
if (-not (git ls-files -u)) {
    Write-Host ">> Merge conflict; resolve and then re-run this script" -ForegroundColor Red
    exit 1
}

# Commits changes IF we have any files to commit
if (git status --porcelain) {
    Write-Host ">> No changes ready to be commit" -ForeGround Red
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
