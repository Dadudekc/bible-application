#!/usr/bin/env python3
"""
🔐 GitHub Token Setup for Bible Project Upload
Simple script to set up GitHub token for automated upload
"""

import sys
from pathlib import Path

# Add agent_tools to path
sys.path.insert(0, '/home/dream/agent_tools')

try:
    from secrets.secrets_manager import SecretsManager
    HAS_SECRETS = True
except ImportError:
    HAS_SECRETS = False
    print("❌ Secrets manager not available")

def setup_github_token():
    """Set up GitHub token interactively"""
    print("🔐 GitHub Token Setup")
    print("=" * 30)
    print()
    
    if not HAS_SECRETS:
        print("❌ Secrets manager not available. Please check agent_tools installation.")
        return False
    
    # Create secrets manager
    secrets_manager = SecretsManager()
    
    # Check if token already exists
    existing_token = secrets_manager.get_secret('github')
    if existing_token:
        print("✅ GitHub token already exists!")
        print("🔧 Do you want to update it? (y/n): ", end="")
        choice = input().lower()
        if choice != 'y':
            print("✅ Keeping existing token")
            return True
    
    print("📝 Please enter your GitHub Personal Access Token:")
    print("   (Get one from: https://github.com/settings/tokens)")
    print("   Required permissions: repo, public_repo, workflow")
    print()
    
    token = input("GitHub Token: ").strip()
    
    if not token:
        print("❌ No token provided")
        return False
    
    # Save token
    try:
        secrets_manager.store_secret('github', token)
        print("✅ GitHub token saved successfully!")
        print()
        print("🧪 Testing token...")
        
        # Test the token
        import asyncio
        import aiohttp
        
        async def test_token():
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.github.com/user', headers=headers) as response:
                    if response.status == 200:
                        user_data = await response.json()
                        print(f"✅ Token valid! Connected as: {user_data.get('login', 'Unknown')}")
                        return True
                    else:
                        error_text = await response.text()
                        print(f"❌ Token invalid: {response.status} - {error_text}")
                        return False
        
        success = asyncio.run(test_token())
        return success
        
    except Exception as e:
        print(f"❌ Error saving token: {str(e)}")
        return False

def main():
    """Main function"""
    print("🚀 Bible Mathematical Discovery Suite")
    print("GitHub Token Setup")
    print("=" * 40)
    print()
    
    if setup_github_token():
        print()
        print("🎉 Setup Complete!")
        print("🚀 You can now run: python3 upload_to_github.py")
        print("   to automatically upload your project to GitHub")
    else:
        print()
        print("❌ Setup failed. Please check your token and try again.")
        print()
        print("📖 To get a GitHub token:")
        print("1. Go to https://github.com/settings/tokens")
        print("2. Click 'Generate new token'")
        print("3. Select scopes: repo, public_repo, workflow")
        print("4. Copy the generated token")
        print("5. Run this script again")

if __name__ == "__main__":
    main()

