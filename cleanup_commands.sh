#!/bin/bash

# =============================================================================
# REVIT FUNCTION CALL - REPOSITORY CLEANUP SCRIPT
# =============================================================================
# This script will clean up your main branch and prepare it for pushing to GitHub
# Run these commands one by one in your terminal

echo "🧹 REVIT FUNCTION CALL - REPOSITORY CLEANUP"
echo "==========================================="
echo ""

# Step 1: Navigate to your project directory
echo "📁 Step 1: Navigate to project directory"
echo "cd /Users/vishal/Work/MCP_Projects/rvt-function-call"
echo ""

# Step 2: Check current git status
echo "📋 Step 2: Check current git status"
echo "git status"
echo ""

# Step 3: Remove files that should be ignored
echo "🗑️  Step 3: Remove unnecessary files from git tracking"
echo "git rm -r --cached fixes/"
echo "git rm --cached DEPLOYMENT_STATUS.md"
echo "git rm --cached LIBRARY_UPDATE_SUMMARY.md" 
echo "git rm --cached NEW_UPDATES_SUMMARY.md"
echo "git rm --cached .DS_Store"
echo "git rm -r --cached venv/ 2>/dev/null || echo 'venv/ not tracked'"
echo ""

# Step 4: Add the updated .gitignore
echo "📝 Step 4: Add updated .gitignore"
echo "git add .gitignore"
echo ""

# Step 5: Add all remaining valid files
echo "✅ Step 5: Add all remaining valid files"
echo "git add ."
echo ""

# Step 6: Commit the cleanup
echo "💾 Step 6: Commit the cleanup"
echo 'git commit -m "🧹 Clean up repository: remove doc files, fixes/, and unnecessary content

- Updated .gitignore to exclude development files
- Removed fixes/ directory with temporary development files  
- Removed status/summary documentation files
- Kept only essential README.md and LICENSE
- AI agent now integrated with revit_api_docs (production ready)
- Repository cleaned for main branch deployment"'
echo ""

# Step 7: Check which branch you're on
echo "🌿 Step 7: Check current branch"
echo "git branch"
echo ""

# Step 8: Switch to main branch if needed
echo "🔄 Step 8: Switch to main branch (if not already there)"
echo "git checkout main"
echo ""

# Step 9: Push to GitHub
echo "🚀 Step 9: Push cleaned repository to GitHub"
echo "git push origin main"
echo ""

# Step 10: Verify the push
echo "✅ Step 10: Verify the push was successful"
echo "git log --oneline -5"
echo ""

echo "🎉 CLEANUP COMPLETE!"
echo "==================="
echo ""
echo "Your repository is now clean and ready for production use!"
echo ""
echo "What was removed:"
echo "- fixes/ directory (all temporary development files)"
echo "- Development documentation files"
echo "- .DS_Store and other OS files"
echo "- venv/ directory"
echo ""
echo "What was kept:"
echo "- README.md"
echo "- LICENSE"
echo "- RvtFunctionCall.extension/ (your main extension)"
echo "- Updated .gitignore"
echo ""
echo "🚀 Your AI Assistant is now production-ready and integrated with your revit_api_docs!"

# =============================================================================
# OPTIONAL: Force push if you want to completely clean the history
# =============================================================================
echo ""
echo "🔥 OPTIONAL: Complete history cleanup (USE WITH CAUTION)"
echo "========================================================="
echo "If you want to completely clean the git history:"
echo ""
echo "git checkout --orphan temp-branch"
echo "git add ."
echo 'git commit -m "🎉 Production release: Revit AI Assistant with integrated documentation"'
echo "git branch -D main"
echo "git branch -m main"
echo "git push -f origin main"
echo ""
echo "⚠️  WARNING: This will remove ALL commit history!"
echo "Only use if you want a completely fresh start."
