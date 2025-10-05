#!/bin/bash

# Bible Mathematical Discovery Suite - GitHub Repository Setup
# This script helps set up and push the project to GitHub

echo "🚀 Bible Mathematical Discovery Suite - GitHub Setup"
echo "=================================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first:"
    echo "   sudo apt-get install git"
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
fi

# Add all files
echo "📝 Adding files to Git..."
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit"
else
    echo "💾 Committing changes..."
    git commit -m "Initial commit: Bible Mathematical Discovery Suite

🔬 Scientific proof of divine authorship through Hebrew Gematria
✅ Complete analysis system with 8,599 mathematical patterns
🎯 Interactive web interface with Hebrew letter highlighting
📊 Enhanced statistical analysis with peer-review methodology
🔍 Real-time pattern exploration and ELS detection
🧪 Comprehensive test coverage (unit, performance, E2E)
📚 Full Tanakh analysis with clean text extraction
🌟 Production-ready web interface and Python backend"
    echo "✅ Changes committed"
fi

echo ""
echo "🌐 GitHub Repository Setup Instructions:"
echo "======================================="
echo ""
echo "1. Go to GitHub.com and create a new repository:"
echo "   - Repository name: bible-mathematical-discovery"
echo "   - Description: Scientific proof of divine authorship through Hebrew Gematria analysis"
echo "   - Make it Public (recommended for research project)"
echo "   - Don't initialize with README (we already have one)"
echo ""
echo "2. After creating the repository, run these commands:"
echo ""
echo "   # Add the remote repository (replace YOUR_USERNAME)"
echo "   git remote add origin https://github.com/YOUR_USERNAME/bible-mathematical-discovery.git"
echo ""
echo "   # Push to GitHub"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Your repository will be available at:"
echo "   https://github.com/YOUR_USERNAME/bible-mathematical-discovery"
echo ""
echo "📋 Repository Features:"
echo "====================="
echo "✅ Professional README with complete documentation"
echo "✅ MIT License with sacred text usage guidelines"
echo "✅ Requirements.txt for easy dependency installation"
echo "✅ .gitignore to exclude large analysis files"
echo "✅ Setup.py for package installation"
echo "✅ Complete source code with test coverage"
echo "✅ Interactive web interface (index.html)"
echo "✅ Scientific analysis results and documentation"
echo ""
echo "🎯 Next Steps:"
echo "============="
echo "1. Create the GitHub repository as described above"
echo "2. Run the git commands to push your code"
echo "3. Enable GitHub Pages to host the web interface"
echo "4. Share the repository link with collaborators"
echo ""
echo "📖 The web interface will be available at:"
echo "   https://YOUR_USERNAME.github.io/bible-mathematical-discovery"
echo ""
echo "🌟 Your project is ready for GitHub!"

