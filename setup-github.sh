#!/bin/bash
# GitHub Setup Helper Script

echo "=== ML-KEM Prime Roots GitHub Setup ==="
echo ""

# Check if GitHub CLI is available
if command -v gh &> /dev/null; then
    echo "✓ GitHub CLI found"
    
    echo ""
    echo "To create and push to GitHub:"
    echo "1. Run: gh repo create mlkem-prime-roots --public --description 'ML-KEM Prime Roots Calculator with CI/CD testing'"
    echo "2. Run: git branch -M main"
    echo "3. Run: git remote add origin https://github.com/YOUR_USERNAME/mlkem-prime-roots.git"
    echo "4. Run: git push -u origin main"
    
else
    echo "GitHub CLI not found. Manual setup:"
    echo ""
    echo "1. Go to https://github.com/new"
    echo "2. Create repository named 'mlkem-prime-roots'"
    echo "3. Copy the repository URL"
    echo "4. Run these commands:"
    echo "   git branch -M main"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/mlkem-prime-roots.git"
    echo "   git push -u origin main"
fi

echo ""
echo "Repository structure:"
tree . -I '__pycache__|*.pyc|test_env'

echo ""
echo "After pushing to GitHub, the CI workflow will automatically:"
echo "- Test Python 3.8-3.12 compatibility"
echo "- Run comprehensive test suite"
echo "- Perform security scans"
echo "- Run performance benchmarks"
echo "- Execute daily regression tests"
echo ""
echo "GitHub Actions badge will be available at:"
echo "https://github.com/YOUR_USERNAME/mlkem-prime-roots/actions/workflows/ci.yml/badge.svg"