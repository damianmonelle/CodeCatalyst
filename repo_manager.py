import os
import github_utils

def get_repo_name():
    """
    Prompt the user for the repository name and validate the input.
    
    Returns:
        str: The sanitized repository name.
    Raises:
        ValueError: If the repository name is empty.
    """
    repo_name = input("Enter the repository name: ").strip()
    if not repo_name:
        raise ValueError("Repository name cannot be empty.")
    return repo_name

def handle_existing_repo(repo_dir):
    """
    Display options for handling an existing repository and return the user's choice.
    
    Args:
        repo_dir (str): The path to the existing repository.

    Returns:
        int: The user's selected action as an integer.
    """
    print(f"The repository '{os.path.basename(repo_dir)}' already exists locally.")
    options = [
        "Start a new project structure (existing files may be overwritten)",
        "Apply a predefined template",
        "Refine existing files",
        "Refactor with OpenAI",
        "Exit"
    ]
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
    
    while True:
        try:
            choice = int(input("Enter the number corresponding to your choice: ").strip())
            if 1 <= choice <= len(options):
                return choice
            else:
                print(f"Invalid choice. Please select a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
