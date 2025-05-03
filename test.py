#!/usr/bin/env python3
"""
Test environment for Deploid.
Sets up a Docker container for testing Deploid.

This script can be run in two modes:
1. Outside Docker: It will build a Docker image and run a container for testing
2. Inside Docker: It will run the Python version of Deploid in test mode
"""

import os
import sys
import subprocess
import platform

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import core modules
from core.colors import print_message, print_instruction, print_warning, print_error

# Container name constant
CONTAINER_NAME = "deploid-test"

def is_running_in_docker():
    """
    Check if the script is running inside a Docker container.

    Returns:
        bool: True if running in Docker, False otherwise
    """
    # Check for .dockerenv file
    if os.path.exists('/.dockerenv'):
        return True

    # Check for cgroup
    try:
        with open('/proc/1/cgroup', 'r') as f:
            return 'docker' in f.read()
    except:
        pass

    return False

def check_docker():
    """
    Check if Docker is installed.
    Exits if Docker is not installed.
    """
    try:
        subprocess.run(['docker', '--version'], check=True, stdout=subprocess.PIPE)
    except (subprocess.SubprocessError, FileNotFoundError):
        print_error("Docker is not installed. Please install Docker first.")
        print_instruction("You can install Docker by running: python deploid.py and selecting 'Install' > 'Docker'")
        sys.exit(1)

def build_image():
    """
    Build Docker image for Deploid.
    Exits on failure.
    """
    print_message("Building Docker image 'deploid'...")

    try:
        # Using subprocess instead of docker-py to avoid dependency issues
        subprocess.run(["docker", "build", "-t", "deploid", "."], check=True)
        print_message("Docker image built successfully!")
    except subprocess.SubprocessError as e:
        print_error(f"Failed to build Docker image: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print_error(f"An error occurred while building the Docker image: {str(e)}")
        sys.exit(1)

def cleanup_containers():
    """Clean up existing containers using the Deploid image."""
    print_message("Cleaning up existing containers...")

    try:
        # Find containers by name (both running and stopped)
        result = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={CONTAINER_NAME}", "--format", "{{.ID}}"],
            capture_output=True,
            text=True,
            check=True
        )

        containers = result.stdout.strip().split('\n') if result.stdout.strip() else []

        if containers and containers[0]:
            # Stop and remove containers
            print_instruction("Stopping and removing containers...")
            for container_id in containers:
                subprocess.run(["docker", "stop", container_id], check=False)
                subprocess.run(["docker", "rm", "-f", container_id], check=False)

            print_message("Cleanup completed!")
        else:
            print_instruction(f"No existing containers found with name: {CONTAINER_NAME}")

        # Additional cleanup for any containers using the deploid image
        result = subprocess.run(
            ["docker", "ps", "-a", "--filter", "ancestor=deploid", "--format", "{{.ID}}"],
            capture_output=True,
            text=True,
            check=True
        )

        image_containers = result.stdout.strip().split('\n') if result.stdout.strip() else []

        if image_containers and image_containers[0]:
            print_instruction("Cleaning up additional containers using deploid image...")
            for container_id in image_containers:
                subprocess.run(["docker", "stop", container_id], check=False)
                subprocess.run(["docker", "rm", "-f", container_id], check=False)

    except subprocess.SubprocessError as e:
        print_error(f"Docker command error: {str(e)}")
    except Exception as e:
        print_error(f"An error occurred during container cleanup: {str(e)}")

def run_container():
    """Run the Deploid container in interactive mode."""
    print_message("Starting Docker container...")
    print_instruction("Container will start in interactive mode")
    print_instruction("You can test both the shell script and Python versions:")
    print_instruction("- Python: python3 deploid.py")
    print_instruction("- Python (test mode): python3 run_test.py")
    print_instruction("Use 'exit' to leave the container")
    print()

    try:
        # Using subprocess for interactive terminal
        welcome_message = "echo '=== Welcome to Deploid Test Environment ==='; "
        python_instructions = "echo '>>> To test the Python version, run:'; echo '>>> python3 run_test.py'; "
        shell_instructions = "echo '>>> To test the shell script version, run:'; echo '>>> ./deploid.sh'; "

        subprocess.run([
            "docker", "run", "-it", "--privileged",
            "--name", CONTAINER_NAME,
            "deploid",
            "/bin/bash", "-c", f"{welcome_message} echo; {python_instructions} echo; {shell_instructions} echo; bash"
        ], check=True)
    except subprocess.SubprocessError as e:
        print_error(f"Failed to run container: {str(e)}")
    except KeyboardInterrupt:
        print_instruction("\nContainer execution interrupted")

def run_inside_docker():
    """Run the Python version of Deploid in test mode when inside Docker."""
    print_message("Running Deploid in Docker Test Environment")
    print_instruction("This is the Python version of Deploid running in test mode")
    print()

    # Import and run the test version
    try:
        import run_test
        run_test.main()
    except ImportError:
        print_error("Could not import run_test.py")
        print_instruction("Make sure you're in the correct directory")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error running test mode: {str(e)}")
        sys.exit(1)

def main():
    """Main function to run the test environment."""
    print_message("=== Deploid Test Environment ===")
    print()

    # Check if running inside Docker
    if is_running_in_docker():
        run_inside_docker()
    else:
        # Running outside Docker, set up a container
        check_docker()
        build_image()
        cleanup_containers()
        run_container()

if __name__ == "__main__":
    main()
