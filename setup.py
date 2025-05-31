#!/usr/bin/env python3

import os
import sys
import subprocess

def install_dependencies():
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dependencies installed successfully.")

def run_game():
    print("Starting Tetris game...")
    # Set the Python path to include our src directory
    sys.path.append(os.path.join(os.getcwd(), "src"))
    os.chdir("src")
    subprocess.check_call([sys.executable, "game_modes.py"])
    print("Game exited.")

if __name__ == "__main__":
    install_dependencies()
    run_game()