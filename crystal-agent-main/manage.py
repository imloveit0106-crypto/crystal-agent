#!/usr/bin/env python3
"""
Crystal Agent - Cross-Platform Management Script

This script provides a unified entry point for running Crystal Agent across
different operating systems (Windows, macOS, Linux). It handles:
- Virtual environment creation and activation
- Dependency installation and verification
- Application launch with proper environment isolation

Usage:
    python manage.py           # Launch the application
    python manage.py --install # Force reinstall dependencies
    python manage.py --clean   # Clean virtual environment and reinstall
"""

import os
import sys
import platform
import subprocess
import venv
from pathlib import Path
import argparse


class CrystalAgentManager:
    """Cross-platform management system for Crystal Agent"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / ".venv"
        self.requirements_file = self.project_root / "requirements.txt"
        self.app_file = self.project_root / "app.py"
        self.os_type = platform.system()  # 'Windows', 'Darwin', 'Linux'

    def get_python_executable(self):
        """Get the path to the Python executable in virtual environment"""
        if self.os_type == "Windows":
            return self.venv_path / "Scripts" / "python.exe"
        else:  # macOS and Linux
            return self.venv_path / "bin" / "python"

    def get_pip_executable(self):
        """Get the path to the pip executable in virtual environment"""
        if self.os_type == "Windows":
            return self.venv_path / "Scripts" / "pip.exe"
        else:  # macOS and Linux
            return self.venv_path / "bin" / "pip"

    def print_status(self, message, status="INFO"):
        """Print colored status messages"""
        colors = {
            "INFO": "\033[94m",    # Blue
            "SUCCESS": "\033[92m", # Green
            "WARNING": "\033[93m", # Yellow
            "ERROR": "\033[91m",   # Red
            "RESET": "\033[0m"     # Reset
        }

        color = colors.get(status, colors["INFO"])
        reset = colors["RESET"]

        prefix = {
            "INFO": "ℹ️ ",
            "SUCCESS": "✅ ",
            "WARNING": "⚠️ ",
            "ERROR": "❌ "
        }.get(status, "")

        print(f"{color}{prefix}{message}{reset}")

    def check_venv_exists(self):
        """Check if virtual environment exists"""
        python_exe = self.get_python_executable()
        return python_exe.exists()

    def create_venv(self):
        """Create virtual environment"""
        self.print_status(f"Creating virtual environment at {self.venv_path}...", "INFO")

        try:
            venv.create(self.venv_path, with_pip=True)
            self.print_status("Virtual environment created successfully!", "SUCCESS")
            return True
        except Exception as e:
            self.print_status(f"Failed to create virtual environment: {e}", "ERROR")
            return False

    def upgrade_pip(self):
        """Upgrade pip to the latest version"""
        self.print_status("Upgrading pip to the latest version...", "INFO")

        pip_exe = self.get_pip_executable()

        try:
            subprocess.run(
                [str(pip_exe), "install", "--upgrade", "pip"],
                check=True,
                capture_output=True
            )
            self.print_status("Pip upgraded successfully!", "SUCCESS")
            return True
        except subprocess.CalledProcessError as e:
            self.print_status(f"Failed to upgrade pip: {e}", "WARNING")
            return False

    def install_dependencies(self, force=False):
        """Install dependencies from requirements.txt"""
        if not self.requirements_file.exists():
            self.print_status("requirements.txt not found!", "ERROR")
            return False

        pip_exe = self.get_pip_executable()

        # Check if dependencies are already installed
        if not force:
            self.print_status("Checking installed packages...", "INFO")
            try:
                result = subprocess.run(
                    [str(pip_exe), "freeze"],
                    check=True,
                    capture_output=True,
                    text=True
                )
                installed_packages = result.stdout.lower()

                # Read required packages
                with open(self.requirements_file, 'r') as f:
                    required = [line.strip().split('>=')[0].split('==')[0].lower()
                              for line in f if line.strip() and not line.startswith('#')]

                # Check if all required packages are installed
                all_installed = all(pkg in installed_packages for pkg in required)

                if all_installed:
                    self.print_status("All dependencies are already installed!", "SUCCESS")
                    return True

            except Exception as e:
                self.print_status(f"Could not verify packages: {e}", "WARNING")

        # Install dependencies
        self.print_status("Installing dependencies from requirements.txt...", "INFO")

        try:
            subprocess.run(
                [str(pip_exe), "install", "-r", str(self.requirements_file)],
                check=True
            )
            self.print_status("Dependencies installed successfully!", "SUCCESS")
            return True
        except subprocess.CalledProcessError as e:
            self.print_status(f"Failed to install dependencies: {e}", "ERROR")
            return False

    def launch_app(self):
        """Launch the Streamlit application"""
        if not self.app_file.exists():
            self.print_status(f"Application file not found: {self.app_file}", "ERROR")
            return False

        python_exe = self.get_python_executable()

        self.print_status("Launching Crystal Agent...", "INFO")
        self.print_status(f"OS: {self.os_type}", "INFO")
        self.print_status(f"Python: {python_exe}", "INFO")

        print("\n" + "="*60)
        print("🚀 Crystal Agent is starting...")
        print("="*60 + "\n")

        try:
            # Launch streamlit using the virtual environment's Python
            subprocess.run(
                [str(python_exe), "-m", "streamlit", "run", str(self.app_file)],
                check=True
            )
        except subprocess.CalledProcessError as e:
            self.print_status(f"Failed to launch application: {e}", "ERROR")
            return False
        except KeyboardInterrupt:
            self.print_status("\nApplication stopped by user.", "INFO")
            return True

        return True

    def clean_venv(self):
        """Remove virtual environment"""
        if self.venv_path.exists():
            self.print_status("Removing virtual environment...", "INFO")

            import shutil
            try:
                shutil.rmtree(self.venv_path)
                self.print_status("Virtual environment removed!", "SUCCESS")
                return True
            except Exception as e:
                self.print_status(f"Failed to remove virtual environment: {e}", "ERROR")
                return False
        else:
            self.print_status("Virtual environment does not exist.", "INFO")
            return True

    def run(self, clean=False, install_only=False):
        """Main execution flow"""
        print("\n" + "="*60)
        print("🔮 Crystal Agent - Cross-Platform Manager")
        print("="*60 + "\n")

        # Step 1: Clean if requested
        if clean:
            if not self.clean_venv():
                return False

        # Step 2: Check and create virtual environment
        if not self.check_venv_exists():
            self.print_status("Virtual environment not found.", "WARNING")
            if not self.create_venv():
                return False

            # Upgrade pip
            self.upgrade_pip()

            # Install dependencies
            if not self.install_dependencies(force=True):
                return False
        else:
            self.print_status("Virtual environment found!", "SUCCESS")

            # Check and install dependencies if needed
            if not self.install_dependencies(force=clean):
                return False

        # Step 3: Launch application (unless install-only mode)
        if install_only:
            self.print_status("Installation complete! Run 'python manage.py' to launch.", "SUCCESS")
            return True

        return self.launch_app()


def main():
    """Entry point for the script"""
    parser = argparse.ArgumentParser(
        description="Crystal Agent - Cross-Platform Management Script"
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="Install/reinstall dependencies only (don't launch app)"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean virtual environment and reinstall everything"
    )

    args = parser.parse_args()

    manager = CrystalAgentManager()

    try:
        success = manager.run(clean=args.clean, install_only=args.install)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
