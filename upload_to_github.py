#!/usr/bin/env python3
"""
🚀 Bible Mathematical Discovery Suite - GitHub Upload Automation
Automatically creates repository and uploads all project files
"""

import asyncio
import aiohttp
import json
import os
import sys
from pathlib import Path
import base64
import mimetypes

# Add agent_tools to path
sys.path.insert(0, '/home/dream/agent_tools')

try:
    from secrets.secrets_manager import SecretsManager
    from github.github_integration import GitHubIntegration
    HAS_GITHUB_TOOLS = True
except ImportError as e:
    print(f"❌ Could not import GitHub tools: {e}")
    HAS_GITHUB_TOOLS = False

class BibleProjectUploader:
    """🚀 Automated GitHub upload for Bible Mathematical Discovery Suite"""
    
    def __init__(self):
        self.secrets_manager = SecretsManager()
        self.github = None
        self.project_dir = Path("/home/dream/client_review")
        self.repository_name = "bible-mathematical-discovery"
        self.repository_description = "Scientific proof of divine authorship through Hebrew Gematria analysis"
        
    async def setup_github(self):
        """Set up GitHub connection"""
        print("🐙 Setting up GitHub connection...")
        
        # Load GitHub token
        token = self.secrets_manager.get_secret('github')
        if not token:
            print("❌ No GitHub token found!")
            print("🔧 Please set up your GitHub token first:")
            print("   1. Run: python3 /home/dream/agent_tools/gui/token_setup_gui.py")
            print("   2. Or manually add token to secrets manager")
            return False
        
        # Create GitHub integration
        self.github = GitHubIntegration(self.secrets_manager)
        
        # Connect to GitHub
        success, message = await self.github.connect()
        if not success:
            print(f"❌ Failed to connect to GitHub: {message}")
            return False
        
        print(f"✅ Connected to GitHub: {message}")
        return True
    
    async def create_repository(self):
        """Create the GitHub repository"""
        print(f"📁 Creating repository: {self.repository_name}")
        
        success, message = await self.github.create_repository(
            name=self.repository_name,
            description=self.repository_description,
            private=False  # Public repository
        )
        
        if not success:
            print(f"❌ Failed to create repository: {message}")
            return False
        
        print(f"✅ Repository created: {message}")
        print(f"🔗 Repository URL: {success.get('html_url', 'Unknown')}")
        return True
    
    def get_files_to_upload(self):
        """Get list of files to upload (excluding large/generated files)"""
        files_to_upload = []
        
        # Key files to upload
        key_files = [
            "README.md",
            "index.html", 
            "clean_bible_downloader.py",
            "requirements.txt",
            "LICENSE",
            "setup.py",
            ".gitignore",
            "github_setup.sh"
        ]
        
        # Python analysis files
        python_files = [
            "full_bible_analyzer.py",
            "hebrew_letter_highlighting.py", 
            "enhanced_statistical_analysis.py",
            "real_time_pattern_exploration.py",
            "els_pattern_detection.py",
            "pattern_significance_analyzer.py"
        ]
        
        # Test files
        test_files = [
            "test_bible_analyzer.py",
            "test_performance.py", 
            "test_e2e_integration.py",
            "test_hebrew_highlighting.py",
            "test_enhanced_statistical_analysis.py",
            "test_real_time_pattern_exploration.py",
            "test_els_pattern_detection.py"
        ]
        
        # Documentation files
        doc_files = [
            "WHAT_8599_PATTERNS_MEAN.md",
            "FEATURE_VALUE_ANALYSIS.md",
            "TEST_COVERAGE_REPORT.md"
        ]
        
        all_files = key_files + python_files + test_files + doc_files
        
        for filename in all_files:
            file_path = self.project_dir / filename
            if file_path.exists():
                files_to_upload.append(file_path)
        
        # Add small JSON files (skip large ones)
        for json_file in self.project_dir.glob("*.json"):
            if json_file.stat().st_size < 1024 * 1024:  # Less than 1MB
                files_to_upload.append(json_file)
        
        return files_to_upload
    
    async def upload_file(self, file_path, repo_owner, repo_name):
        """Upload a single file to GitHub"""
        try:
            # Read file content
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Encode as base64
            encoded_content = base64.b64encode(content).decode('utf-8')
            
            # Determine file path in repository
            relative_path = file_path.relative_to(self.project_dir)
            
            # Prepare API request
            headers = {
                'Authorization': f'token {self.secrets_manager.get_secret("github")}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            data = {
                'message': f'Add {relative_path}',
                'content': encoded_content,
                'branch': 'main'
            }
            
            # Check if file exists first
            url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{relative_path}'
            
            async with aiohttp.ClientSession() as session:
                # Check if file exists
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        # File exists, get SHA for update
                        file_data = await response.json()
                        data['sha'] = file_data['sha']
                
                # Upload/update file
                async with session.put(url, headers=headers, json=data) as response:
                    if response.status in [200, 201]:
                        return True, f"Uploaded {relative_path}"
                    else:
                        error_text = await response.text()
                        return False, f"Failed to upload {relative_path}: {response.status} - {error_text}"
        
        except Exception as e:
            return False, f"Error uploading {file_path}: {str(e)}"
    
    async def upload_all_files(self):
        """Upload all project files"""
        print("📤 Uploading project files...")
        
        # Get user info
        user_info, _ = await self.github.get_user_info()
        if not user_info:
            print("❌ Could not get user info")
            return False
        
        repo_owner = user_info['login']
        
        # Get files to upload
        files = self.get_files_to_upload()
        print(f"📁 Found {len(files)} files to upload")
        
        # Upload files
        successful_uploads = 0
        failed_uploads = 0
        
        for file_path in files:
            print(f"📤 Uploading {file_path.name}...")
            success, message = await self.upload_file(file_path, repo_owner, self.repository_name)
            
            if success:
                print(f"✅ {message}")
                successful_uploads += 1
            else:
                print(f"❌ {message}")
                failed_uploads += 1
        
        print(f"\n📊 Upload Summary:")
        print(f"✅ Successful: {successful_uploads}")
        print(f"❌ Failed: {failed_uploads}")
        print(f"📁 Total: {len(files)}")
        
        return failed_uploads == 0
    
    async def enable_github_pages(self):
        """Enable GitHub Pages for the repository"""
        print("🌐 Enabling GitHub Pages...")
        
        try:
            user_info, _ = await self.github.get_user_info()
            repo_owner = user_info['login']
            
            headers = {
                'Authorization': f'token {self.secrets_manager.get_secret("github")}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Enable Pages
            pages_data = {
                'source': {
                    'branch': 'main',
                    'path': '/'
                }
            }
            
            url = f'https://api.github.com/repos/{repo_owner}/{self.repository_name}/pages'
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=pages_data) as response:
                    if response.status == 201:
                        print("✅ GitHub Pages enabled successfully")
                        print(f"🌐 Live demo will be available at:")
                        print(f"   https://{repo_owner}.github.io/{self.repository_name}")
                        return True
                    else:
                        error_text = await response.text()
                        print(f"⚠️ GitHub Pages setup may need manual configuration: {error_text}")
                        return False
        
        except Exception as e:
            print(f"⚠️ GitHub Pages setup error: {str(e)}")
            return False
    
    async def run_full_upload(self):
        """Run the complete upload process"""
        print("🚀 Bible Mathematical Discovery Suite - GitHub Upload")
        print("=" * 60)
        print()
        
        # Step 1: Setup GitHub
        if not await self.setup_github():
            return False
        
        # Step 2: Create repository
        if not await self.create_repository():
            return False
        
        # Step 3: Upload files
        if not await self.upload_all_files():
            print("⚠️ Some files failed to upload, but continuing...")
        
        # Step 4: Enable GitHub Pages
        await self.enable_github_pages()
        
        print("\n🎉 GitHub Upload Complete!")
        print("=" * 40)
        print("🔗 Your repository is now live on GitHub!")
        print("🌐 Web interface will be available via GitHub Pages")
        print("📚 All source code and documentation uploaded")
        
        return True

async def main():
    """Main function"""
    if not HAS_GITHUB_TOOLS:
        print("❌ GitHub tools not available. Please check agent_tools installation.")
        return
    
    uploader = BibleProjectUploader()
    await uploader.run_full_upload()

if __name__ == "__main__":
    asyncio.run(main())

