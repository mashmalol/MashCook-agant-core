"""
Launcher script for the Streamlit UI
Run this script to start the web interface.
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit UI."""
    print("🚀 Starting Agent Chatbot UI...")
    print("📝 Make sure you have installed requirements: pip install -r requirements.txt")
    print("🌐 The UI will open in your default web browser")
    print("=" * 70)
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ui_file = os.path.join(script_dir, "ui.py")
    
    # Run streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", ui_file,
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n\n✨ UI stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure Streamlit is installed:")
        print("  pip install streamlit")

if __name__ == "__main__":
    main()

