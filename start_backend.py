#!/usr/bin/env python3
"""
Smart Basket Recommender - Backend Startup Script
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def install_spacy_model():
    """Install spaCy English model"""
    print("🧠 Installing spaCy English model...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✅ spaCy model installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing spaCy model: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Smart Basket Recommender backend...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Change to backend directory
        os.chdir("backend")
        
        # Start the server
        subprocess.run([sys.executable, "main_basic.py"])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main startup function"""
    print("🛒 Smart Basket Recommender - Backend Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install dependencies. Please check your internet connection and try again.")
        sys.exit(1)
    
    # Install spaCy model
    # if not install_spacy_model():
    #     print("❌ Failed to install spaCy model. Please check your internet connection and try again.")
    #     sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main() 
 