# Deploid

Deploid is your AI Buddy for Quick and Easy Deployment! This Python-based tool helps you set up and manage deployments for various types of projects.

## Features

- Interactive menu with arrow key navigation
- Installation of essential tools (Git, Docker, OpenSSH, Sudo)
- Repository setup and configuration
- Deployment management for different project types (Docker, Node.js, etc.)
- SSH key generation and GitHub integration
- Submodule management

## Requirements

- Python 3.6 or higher
- pip (Python package manager)

## Installation

### Quick Installation (Recommended)

You can install Deploid with a single command:

```bash
curl -sSL https://github.com/yourusername/deploid/releases/latest/download/install.sh | bash
```

Or if you prefer wget:

```bash
wget -qO- https://github.com/yourusername/deploid/releases/latest/download/install.sh | bash
```

To install a specific version (e.g., v1.0.0):

```bash
curl -sSL https://github.com/yourusername/deploid/releases/download/v1.0.0/install.sh | bash -s -- --version v1.0.0
```

This will:

- Download Deploid
- Set up a virtual environment
- Install all dependencies
- Create an executable in your PATH

After installation, you can run Deploid from anywhere by typing:

```bash
deploid
```

#### Installation Options

The installer supports several options:

- `--version` or `-v`: Specify the version to install (default: latest)
- `--directory` or `-d`: Specify the installation directory
- `--yes` or `-y`: Automatic yes to prompts
- `--help` or `-h`: Show help message

Example with options:

```bash
bash install.sh --version v1.0.0 --directory ~/deploid-custom --yes
```

### Manual Installation

If you prefer to install manually:

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/deploid.git
   cd deploid
   ```

2. Set up the virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

   Or activate the virtual environment using one of these methods:

   **Method 1: Source the activation script** (recommended):

   ```bash
   # IMPORTANT: Use 'source' command to activate the environment
   source ./activate.sh   # or: . ./activate.sh
   ```

   **Method 2: Direct activation**:

   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

   > **⚠️ IMPORTANT**: Do NOT run `./activate.sh` directly. It must be sourced with the `source` command.
   >
   > - ✅ CORRECT: `source ./activate.sh`
   > - ❌ INCORRECT: `./activate.sh`
   >
   > The script now detects if it's being sourced and will show a warning if run incorrectly.

## Virtual Environment

This project uses a virtual environment to isolate dependencies. The `venv/` directory is included in `.gitignore` and should not be committed to the repository.

### Why use a virtual environment?

- Isolates project dependencies from your system Python
- Prevents conflicts between different projects' dependencies
- Makes it easier to reproduce the development environment
- Allows for clean installation and uninstallation of packages

### Working with the virtual environment

- **Activate** the environment before working on the project:

  ```bash
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

- **Deactivate** when you're done:

  ```bash
  deactivate
  ```

- **Install new dependencies**:

  ```bash
  pip install package-name
  ```

- **Update requirements.txt** after installing new packages:

  ```bash
  pip freeze > requirements.txt
  ```

## Usage

Run the main script:

```bash
python deploid.py
```

This will present you with a menu to:

- Install tools (Git, Docker, OpenSSH, Sudo)
- Set up repositories and deployments
- Update existing deployments

## Project Structure

- `core/`: Core functionality modules
- `deployments/`: Deployment-specific modules
- `install/`: Installation modules for various tools
- `setup/`: Setup modules for Git and SSH
- `utils/`: Utility functions

## Testing with Docker

To test these scripts in a clean environment, you can use Docker. This will allow you to test the setup process from scratch without affecting your local system.

### Prerequisites

- Docker installed on your system

### Option 1: Using the Docker Test Script

The easiest way to test Deploid in Docker is to use the provided test script:

```bash
./docker_test.sh
```

This script will:

1. Build the Docker image
2. Clean up any existing containers
3. Start a new container in interactive mode

### Option 2: Using the Python Test Script

You can also use the Python test script which supports both running inside and outside Docker:

```bash
# Outside Docker: builds and runs a Docker container
python test.py

# Inside Docker: runs the Python version in test mode
source venv/bin/activate && python test.py
```

### Option 3: Manual Docker Commands

If you prefer to run the Docker commands manually:

1. Build the Docker image:

   ```bash
   docker build -t deploid .
   ```

1. Run the container:

   ```bash
   docker run -it --privileged --name deploid-test deploid
   ```

The `--privileged` flag is required because the scripts will install and manage Docker inside the container.

### Inside the Container

Once inside the container, you can:

- Run the Python version in test mode:

   ```bash
   python3 run_test.py
   ```

- Run the Python version with root privileges:

   ```bash
   sudo python3 deploid.py
   ```

- Run the shell script version:

   ```bash
   ./deploid.sh
   ```

### Notes

- The container starts with a clean Ubuntu 22.04 installation
- All installation and configuration will be handled by the scripts
- The container has a non-root user (`testuser`) with sudo privileges
- All scripts are already made executable in the container
- Python packages are installed globally for easier usage
