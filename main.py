import os
import logging
import subprocess  # Import subprocess module
from config_utils import setup_logging, verify_environment_variables
from repo_manager import get_repo_name, handle_existing_repo
from template_manager import apply_template
import github_utils
import refine_utils
import openai_code_utils  # Import the OpenAI refactor module

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

def main():
    """
    Main function to handle repository initialization, refinement, synchronization, and more.
    """
    # Setup logging to a file
    setup_logging("main_log.txt")

    # Verify required environment variables
    required_vars = ["GITHUB_TOKEN", "GITHUB_USERNAME", "OPENAI_API_KEY"]
    valid_env, missing = verify_environment_variables(required_vars)
    if not valid_env:
        print(f"Missing environment variables: {', '.join(missing)}")
        logging.error(f"Missing environment variables: {', '.join(missing)}")
        return

    # Prompt the user for the repository name
    try:
        repo_name = get_repo_name()
    except ValueError as e:
        logging.error(f"Error getting repository name: {e}")
        print(f"Error: {e}")
        return

    # Initialize or clone the repository
    repo_dir = github_utils.initialize_or_clone_repo(
        os.getenv("GITHUB_USERNAME"), os.getenv("GITHUB_TOKEN"), repo_name
    )
    if not repo_dir:
        logging.error("Repository initialization or cloning failed.")
        print("Failed to initialize or clone repository. Check logs for details.")
        return

    # Handle an existing repository
    if os.path.exists(repo_dir):
        print("\nChoose an action:")
        print("1. Create a new project structure")
        print("2. Apply a predefined template")
        print("3. Refine existing files")
        print("4. Refactor with OpenAI")
        print("5. Sync repository with GitHub")
        print("6. Exit")

        try:
            action = int(input("Enter the number corresponding to your choice: ").strip())
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6.")
            return

        # Actions based on user's choice
        if action == 1:
            # Create a new project structure
            try:
                import ai_utils  # Import dynamically as needed
                app_type = ai_utils.select_app_type()
                app_description = ai_utils.get_app_description()
                file_structure = ai_utils.plan_file_structure(app_type, app_description)
                ai_utils.create_placeholders(file_structure, repo_dir)
                logging.info("New project structure created successfully.")
                print("New project structure created successfully.")
            except Exception as e:
                logging.error(f"Error creating project structure: {e}")
                print(f"Error: {e}")
        elif action == 2:
            # Apply a predefined template
            try:
                apply_template(repo_dir)
                logging.info("Template applied successfully.")
                print("Template applied successfully.")
            except Exception as e:
                logging.error(f"Error applying template: {e}")
                print(f"Error: {e}")
        elif action == 3:
            # Refine existing files
            try:
                refine_prompt = input("Enter custom instructions (or press Enter for default): ")
                refine_utils.refine_project(repo_dir, refine_prompt)
                logging.info("Project refined successfully.")
                print("Project refined successfully.")
            except Exception as e:
                logging.error(f"Error refining project: {e}")
                print(f"Error: {e}")
        elif action == 4:
            # Refactor with OpenAI
            try:
                print("Refactoring project using OpenAI...")
                openai_code_utils.refactor_repo_with_openai(repo_dir)
                logging.info("Project refactored using OpenAI successfully.")
                print("Project refactored using OpenAI successfully.")
            except Exception as e:
                logging.error(f"Error refactoring project with OpenAI: {e}")
                print(f"Error: {e}")
        elif action == 5:
            # Sync repository with GitHub
            try:
                sync_repo(repo_dir)
            except Exception as e:
                logging.error(f"Error syncing repository: {e}")
                print(f"Error: {e}")
        elif action == 6:
            print("Exiting application. No changes made.")
            logging.info("User exited the application without making changes.")
        else:
            print("Invalid action selected. Exiting.")
            logging.error("Invalid action selected.")

if __name__ == "__main__":
    main()
