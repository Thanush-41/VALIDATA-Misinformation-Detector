#!/usr/bin/env python3
"""
Setup and deployment script for the Misinformation Detection System
This script helps set up the environment and run the demo
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60)

def print_step(step_num, text):
    """Print a formatted step"""
    print(f"\n📋 Step {step_num}: {text}")

def check_python_version():
    """Check if Python version is adequate"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_requirements():
    """Install required packages"""
    requirements = [
        "pandas>=1.5.0",
        "numpy>=1.21.0", 
        "streamlit>=1.25.0",
        "plotly>=5.10.0",
        "requests>=2.28.0",
        "python-dotenv>=0.19.0",
        "langdetect>=1.0.9"
    ]
    
    print("Installing required packages...")
    for req in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
            print(f"✅ Installed {req}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {req}")
            return False
    
    return True

def create_directories():
    """Create necessary directories"""
    directories = ["data", "logs", "src", "dashboard", "tests"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def run_demo():
    """Run the demonstration"""
    try:
        print("Running misinformation detection demo...")
        result = subprocess.run([sys.executable, "demo.py"], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Demo completed successfully!")
            print(result.stdout)
            return True
        else:
            print("❌ Demo failed:")
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("❌ Demo timed out")
        return False
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        return False

def check_database():
    """Check if demo database exists and has data"""
    db_path = "data/demo.db"
    
    if not os.path.exists(db_path):
        print("❌ Demo database not found")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM tweets")
        tweet_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM classifications")
        classification_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"✅ Database found with {tweet_count} tweets and {classification_count} classifications")
        return tweet_count > 0 and classification_count > 0
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

def launch_dashboard():
    """Launch the Streamlit dashboard"""
    try:
        print("Launching dashboard... (Press Ctrl+C to stop)")
        print("Dashboard will be available at: http://localhost:8501")
        
        subprocess.run([sys.executable, "-m", "streamlit", "run", "demo_dashboard.py"])
        
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")

def main():
    """Main setup function"""
    print_header("🔍 Misinformation Detection System Setup")
    
    print("Welcome to the Misinformation Detection System!")
    print("This script will help you set up and run the demo.")
    
    # Step 1: Check Python version
    print_step(1, "Checking Python version")
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Create directories
    print_step(2, "Creating directories")
    create_directories()
    
    # Step 3: Install requirements
    print_step(3, "Installing dependencies")
    if not install_requirements():
        print("❌ Failed to install some dependencies. Please install manually.")
        sys.exit(1)
    
    # Step 4: Run demo
    print_step(4, "Running demonstration")
    if not run_demo():
        print("❌ Demo failed. Please check the error messages above.")
        sys.exit(1)
    
    # Step 5: Check database
    print_step(5, "Verifying demo data")
    if not check_database():
        print("❌ Demo data not found. Please run demo.py manually.")
        sys.exit(1)
    
    # Step 6: Launch dashboard
    print_step(6, "Launching dashboard")
    
    choice = input("\n🚀 Launch the web dashboard? (y/n): ").lower().strip()
    if choice in ['y', 'yes']:
        launch_dashboard()
    else:
        print("\n✅ Setup completed successfully!")
        print("\nTo launch the dashboard manually, run:")
        print("   streamlit run demo_dashboard.py")
        print("\nTo run the demo again:")
        print("   python demo.py")
    
    print_header("Setup Complete! 🎉")
    
    print("📋 What you can do next:")
    print("1. View the dashboard at http://localhost:8501")
    print("2. Examine the source code in the src/ directory")
    print("3. Run tests with: python -m pytest tests/")
    print("4. Install additional dependencies for full functionality:")
    print("   - pip install snscrape (for real Twitter data collection)")
    print("   - pip install transformers torch (for LLM classification)")
    print("5. Customize the system by editing src/config.py")
    
    print("\n📚 Documentation:")
    print("- README.md: Complete system documentation")
    print("- src/: Source code for all components")
    print("- tests/: Unit tests for system components")
    
    print("\n⚠️  Important Notes:")
    print("- This demo uses rule-based classification")
    print("- For production use, consider using LLM-based classification")
    print("- Respect social media platforms' terms of service")
    print("- Always verify critical information through multiple sources")

if __name__ == "__main__":
    main()
