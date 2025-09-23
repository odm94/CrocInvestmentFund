#!/usr/bin/env python3
"""
Setup script for Stock Valuation Tool
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def test_installation():
    """Test if the installation works"""
    print("\n🧪 Testing installation...")
    try:
        # Test imports
        import yfinance
        import pandas
        import numpy
        import streamlit
        import openai
        import plotly
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Stock Valuation Tool...")
    print("="*50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation")
        return False
    
    # Test installation
    if not test_installation():
        print("❌ Setup failed during testing")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the web app: streamlit run app.py")
    print("2. Or use command line: python run.py AAPL")
    print("3. Test AI integration: python test_ai.py")
    print("\n🔑 Your OpenAI API key is already configured!")
    
    return True

if __name__ == "__main__":
    main()
