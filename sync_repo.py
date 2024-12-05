import os
import logging
import subprocess
from pathlib import Path

logging.basicConfig(
    filename="sync_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def sync_repo(repo_dir):
    """
    Sync the local repository with the remote GitHub repository.

    Args:
        repo_dir (str): Path to the local repository directory.
    """
    try:
        os.chdir(repo_dir)

        # Detect changes
        changes = subprocess.run(["git", "status", "--short"], capture_output=True, text=True).stdout.strip()
        if not changes:
            logging.info("No changes to commit. Repository is up-to-date.")
            print("No changes to commit. Repository is already up-to-date.")
            return

        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)
        logging.info("All changes staged successfully.")

        # Commit changes
        commit_message = input("Enter a commit message (or press Enter for default): ").strip()
        commit_message = commit_message if commit_message else "Sync changes"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        logging.info(f"Changes committed with message: {commit_message}")

        # Push changes
        subprocess.run(["git", "push"], check=True)
        logging.info("Changes pushed to remote repository successfully.")
        print("Repository synced with GitHub successfully.")

    except subprocess.CalledProcessError as e:
        logging.error(f"Git command failed: {e}")
        print(f"Error syncing repository: {e}")
    except Exception as e:
        logging.error(f"Unexpected error during sync: {e}")
        print(f"Unexpected error occurred: {e}")
