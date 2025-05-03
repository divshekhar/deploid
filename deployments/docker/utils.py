#!/usr/bin/env python3
"""
Docker utilities module for deployments.
Provides utility functions for Docker deployments.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import core modules
from core.colors import print_message, print_instruction, print_warning, print_error

def get_docker_info():
    """
    Get Docker system information.
    
    Returns:
        dict: Docker system information or None if Docker is not available
    """
    try:
        result = subprocess.run(
            ["docker", "info", "--format", "{{json .}}"],
            capture_output=True,
            text=True,
            check=True
        )
        
        return json.loads(result.stdout)
    except (subprocess.SubprocessError, json.JSONDecodeError, FileNotFoundError):
        return None

def list_docker_containers(all_containers=False):
    """
    List Docker containers.
    
    Args:
        all_containers (bool): Whether to list all containers or only running ones
        
    Returns:
        list: List of container information dictionaries
    """
    try:
        cmd = ["docker", "ps", "--format", "{{json .}}"]
        if all_containers:
            cmd.append("-a")
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        containers = []
        for line in result.stdout.splitlines():
            if line.strip():
                containers.append(json.loads(line))
        
        return containers
    except (subprocess.SubprocessError, json.JSONDecodeError, FileNotFoundError):
        return []

def list_docker_images():
    """
    List Docker images.
    
    Returns:
        list: List of image information dictionaries
    """
    try:
        result = subprocess.run(
            ["docker", "images", "--format", "{{json .}}"],
            capture_output=True,
            text=True,
            check=True
        )
        
        images = []
        for line in result.stdout.splitlines():
            if line.strip():
                images.append(json.loads(line))
        
        return images
    except (subprocess.SubprocessError, json.JSONDecodeError, FileNotFoundError):
        return []

def stop_docker_container(container_name):
    """
    Stop a Docker container.
    
    Args:
        container_name (str): Name or ID of the container to stop
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        subprocess.run(["docker", "stop", container_name], check=True)
        return True
    except subprocess.SubprocessError:
        return False

def start_docker_container(container_name):
    """
    Start a Docker container.
    
    Args:
        container_name (str): Name or ID of the container to start
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        subprocess.run(["docker", "start", container_name], check=True)
        return True
    except subprocess.SubprocessError:
        return False

def remove_docker_container(container_name, force=False):
    """
    Remove a Docker container.
    
    Args:
        container_name (str): Name or ID of the container to remove
        force (bool): Whether to force removal
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cmd = ["docker", "rm", container_name]
        if force:
            cmd.append("-f")
        
        subprocess.run(cmd, check=True)
        return True
    except subprocess.SubprocessError:
        return False

def docker_compose_up(repo_path, detach=True):
    """
    Start containers with Docker Compose.
    
    Args:
        repo_path (str): Path to the repository with docker-compose.yml
        detach (bool): Whether to run in detached mode
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cmd = ["docker-compose", "up"]
        if detach:
            cmd.append("-d")
        
        subprocess.run(cmd, cwd=repo_path, check=True)
        return True
    except subprocess.SubprocessError:
        return False

def docker_compose_down(repo_path, remove_volumes=False):
    """
    Stop and remove containers with Docker Compose.
    
    Args:
        repo_path (str): Path to the repository with docker-compose.yml
        remove_volumes (bool): Whether to remove volumes as well
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cmd = ["docker-compose", "down"]
        if remove_volumes:
            cmd.append("-v")
        
        subprocess.run(cmd, cwd=repo_path, check=True)
        return True
    except subprocess.SubprocessError:
        return False
