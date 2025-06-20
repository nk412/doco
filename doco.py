#!/usr/bin/env python

import os
import sys
import yaml
import subprocess
import argparse
import tempfile
from pathlib import Path

def load_config():
    """Load the doco.yaml config file from the current working directory."""
    config_path = Path("doco.yaml")

    if not config_path.exists():
        print("Error: doco.yaml not found in the current directory.")
        sys.exit(1)

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return config
    except yaml.YAMLError as e:
        print(f"Error parsing doco.yaml: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)

def check_dockerfile(dockerfile):
    """Check if a Dockerfile exists in the current working directory."""
    if not Path(dockerfile).exists():
        print(f"Error: Dockerfile not found at {dockerfile}")
        sys.exit(1)

def read_ssh_key_path(ssh_key_path):
    """Validate that the SSH key exists at the provided path."""
    key_path = os.path.expanduser(ssh_key_path)
    if not os.path.exists(key_path):
        print(f"Error: SSH key not found at {ssh_key_path}")
        sys.exit(1)
    return key_path

def build_image(config, dockerfile):
    """Build the Docker image using the {dockerfile} in the current directory."""
    image_name = config.get("image_name", "doco-workspace")
    platform = config.get("platform")
    ssh_key_path = config.get("ssh_key_path")

    print(f"Building Docker image: {image_name} for {platform} platform...")
    try:
        # Ensure we're using BuildKit
        build_env = os.environ.copy()
        build_env["DOCKER_BUILDKIT"] = "1"

        # Basic build command
        build_command = ["docker", "build", "-t", image_name]

        if platform:
            build_command.extend(["--platform", platform])

        # Handle SSH keys securely with BuildKit secrets if specified
        if ssh_key_path:
            ssh_key_abs_path = read_ssh_key_path(ssh_key_path)
            build_command.extend(["--secret", f"id=ssh_key,src={ssh_key_abs_path}"])
            print("Using SSH key with secure BuildKit secret mount")

        # Add dockerfile and context
        build_command.extend(["-f", dockerfile, "."])

        # Run the build
        print("Build command:", " ".join(build_command))
        subprocess.run(build_command, env=build_env, check=True)
        print("Build successful!")
        return image_name
    except subprocess.CalledProcessError as e:
        print(f"Error building Docker image: {e}")
        sys.exit(1)

def start_container(image_name, config):
    mount_path = config.get("mount_path", "/workspace")
    current_dir = os.getcwd()
    platform = config.get("platform")

    extra_options = config.get("docker_options", [])

    cmd = ["docker", "run", "-it", "--rm"]

    # Set platform from config (default is AMD64)
    if platform:
        cmd.extend(["--platform", platform])

    # Add volume mount for current directory
    cmd.extend(["-v", f"{current_dir}:{mount_path}"])

    # Add working directory specification
    cmd.extend(["-w", mount_path])

    # Add any extra options from config
    if extra_options:
        cmd.extend(extra_options)

    # Add image name
    cmd.append(image_name)

    # # Add bash (or specified shell)
    # shell = config.get("shell", "bash")
    # cmd.append(shell)

    print(f"Starting container with {current_dir} mounted at {mount_path} on {platform} platform...")
    print("Command:", " ".join(cmd))
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nExiting container...")
    except Exception as e:
        print(f"Error running container: {e}")
        sys.exit(1)

def init_wizard():
    """Initialize a new doco.yaml configuration file."""
    if os.path.exists("doco.yaml"):
        print("Error: doco.yaml already exists in the current directory.")
        sys.exit(1)
    else:
        print("Initializing new doco.yaml configuration...")
        config = {
            "image_name": "doco-workspace",
            "platform": "linux/amd64",
            "mount_path": "/workspace",
            "docker_options": [],
            "shell": "bash"
        }
        with open("doco.yaml", "w") as f:
            yaml.dump(config, f)
        print("Configuration file created. Edit it to customize your setup.")

def main():
    if len(sys.argv) > 1  and sys.argv[1] == "init":
        init_wizard()
        return
    parser = argparse.ArgumentParser(
        description="doco - run containers with your cwd mounted"
    )
    parser.add_argument("--no-build", action="store_true", help="Skip building the image and use the existing one")
    parser.add_argument("--dockerfile", type=str, default="Dockerfile", required=False, help="the path to the dockerfile")
    args = parser.parse_args()

    # Check for Dockerfile
    check_dockerfile(args.dockerfile)

    # Load configuration
    config = load_config()

    # Get image name from config
    image_name = config.get("image_name", "doco-workspace")

    # Build image (unless --no-build flag is used)
    if not args.no_build:
        image_name = build_image(config, args.dockerfile)

    # Start container with bash
    start_container(image_name, config)

if __name__ == "__main__":
    main()
