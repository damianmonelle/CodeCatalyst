import os
import logging
from pathlib import Path
from github import Github
import subprocess
import re
import datetime
import openai

# Logging setup
logging.basicConfig(
    filename="main_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def sanitize_github_url(username, repo_name):
    """Construct and sanitize the GitHub repository URL."""
    if not username or not repo_name:
        raise ValueError("GitHub username and repository name are required.")
    
    base_url = "https://github.com"
    sanitized_url = f"{base_url}/{username}/{repo_name}.git"
    logging.info(f"Constructed GitHub URL: {sanitized_url}")
    return sanitized_url

def initialize_or_clone_repo(username, token, repo_name):
    """Create the GitHub repository if it doesn't exist, or clone it if it does."""
    try:
        github = Github(token)
        user = github.get_user()

        # Check if the repository already exists
        try:
            repo = user.get_repo(repo_name)
            logging.info(f"Repository '{repo_name}' exists. Cloning...")
            print(f"Repository '{repo_name}' exists. Cloning locally...")

        except:
            logging.info(f"Repository '{repo_name}' does not exist. Creating it...")
            print(f"Repository '{repo_name}' does not exist. Creating it...")
            repo = user.create_repo(repo_name)
            logging.info(f"Repository '{repo_name}' created successfully.")

        # Prepare the build directory
        build_dir = Path(os.getcwd(), "build")
        build_dir.mkdir(parents=True, exist_ok=True)
        repo_dir = build_dir / repo_name

        if not repo_dir.exists():
            clone_url = sanitize_github_url(username, repo_name)
            subprocess.run(["git", "clone", clone_url, str(repo_dir)], check=True)
            logging.info(f"Repository '{repo_name}' cloned to {repo_dir}.")
            print(f"Repository '{repo_name}' cloned to {repo_dir}.")
        else:
            logging.info(f"Repository '{repo_name}' already cloned locally at {repo_dir}.")
            print(f"Repository '{repo_name}' already exists locally at {repo_dir}.")

        return repo_dir

    except Exception as e:
        logging.error(f"Error handling repository '{repo_name}': {e}")
        print(f"Error: Failed to process repository '{repo_name}'. Check main_log.txt for details.")
        return None

def detect_changes(repo_dir):
    """Detect changes in the repository using Git."""
    try:
        os.chdir(repo_dir)
        changes = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
        return changes.stdout.strip() if changes.stdout.strip() else "No changes detected."
    except subprocess.CalledProcessError as e:
        logging.error(f"Error detecting changes: {e}")
        return "Error detecting changes."

def update_readme(repo_dir, changes_summary):
    """
    Update the README.md file with the AI-generated summary of changes.
    Args:
        repo_dir (str): The root directory of the repository.
        changes_summary (str): Summary of changes to include in the README.
    """
    try:
        readme_path = Path(repo_dir, "README.md")
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # Generate AI summary
        prompt = f"""
        Summarize the following changes for the project's README changelog:
        {changes_summary}

        Write it in markdown format with headings like "Changelog", and include the date and summary of features added or updated.
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=500
        )
        changelog_entry = response.choices[0].message["content"]

        if not changelog_entry.strip():
            logging.warning("AI response for changelog is empty. Skipping README update.")
            print("No AI summary generated for changelog. Skipping README update.")
            return

        with open(readme_path, "a") as readme_file:
            readme_file.write(f"\n## Changelog ({timestamp})\n")
            readme_file.write(changelog_entry)
            readme_file.write("\n")

        logging.info("README.md updated with changelog.")
        print("README.md updated successfully.")

    except Exception as e:
        logging.error(f"Error updating README.md: {e}")
        print(f"Error: Failed to update README.md. Check main_log.txt for details.")

def sync_repo(repo_dir):
    """Sync the local repository with the remote repository."""
    try:
        os.chdir(repo_dir)

        # Detect changes
        changes_summary = detect_changes(repo_dir)

        # Update README.md with AI-generated summary
        if "No changes detected" not in changes_summary:
            update_readme(repo_dir, changes_summary)

        # Add all changes
        subprocess.run(["git", "add", "."], check=True)

        # Check for changes
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if status.stdout.strip():  # Only commit if changes exist
            subprocess.run(["git", "commit", "-m", "Sync changes"], check=True)
            logging.info("Committed changes to local repository.")
        else:
            logging.info("No changes to commit. Skipping commit step.")
            print("No changes to commit. Skipping commit step.")

        # Push changes
        subprocess.run(["git", "push"], check=True)
        logging.info("Local changes pushed to remote repository.")
        print("Local changes synced with remote repository.")

    except subprocess.CalledProcessError as e:
        logging.error(f"Error syncing repository: {e}")
        print("Error: Failed to sync repository. Check main_log.txt for details.")
