# If there are any uncommited changes on the current branch, does not run the script
if (git status --porcelain) {
    Write-Host ">> Manually commit all changes/resolve all conflicts on this branch before running this script" -ForegroundColor Red
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
    git merge main -m "Merge branch 'main' into recruiter-demo"
}

# Removing git tracking within the recruiter-demo branch of files I do not want tracked
git rm -r '.\Storage of Deprecated Things'

# Detects if this merge had any conflicts
if (git ls-files -u) {
    git status
    Write-Host ">> Merge conflict; resolve and then re-run this script" -ForegroundColor Red
    exit 1
}

# Commits changes IF we have any files to commit (likely the file removals from earlier)
if (git status --porcelain) {
    Write-Host ">> Commit changes to recruiter-demo" -ForegroundColor Cyan
    git commit -m "Commit changes from 'main' to recruiter-demo"
} else {
    Write-Host ">> Nothing to commit to recruiter-demo" -ForegroundColor Yellow
}

# Pushs to the remote repository
Write-Host ">> Push recruiter-demo to remote 'demo' repo" -ForegroundColor Cyan
git push demo recruiter-demo

# States the script is complete
Write-Host ">> Script complete; remember to 'checkout main branch' if desired" -ForegroundColor Cyan
