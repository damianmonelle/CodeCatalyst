import openai
import os
import logging

# Configure logging
LOG_FILE = "openai_refactor_log.txt"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Retrieve OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError(
        "OPENAI_API_KEY is not set in the environment variables. Please set it to proceed."
)

# Initialize OpenAI API key
openai.api_key = OPENAI_API_KEY

SUPPORTED_FILE_EXTENSIONS = ('.py', '.js', '.html', '.css', '.java', '.md')


def log_and_print(message, level="info"):
    """
    Helper function to log and print messages.
    
    Args:
        message (str): The message to log and print.
        level (str): The logging level ('info', 'warning', 'error').
    """
    print(message)
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)


def process_file(file_path):
    """
    Process and refactor a single file using OpenAI.

    Args:
        file_path (str): Path to the file to refactor.
    """
    log_and_print(f"Processing file: {file_path}", "info")

    try:
        # Read file content
        with open(file_path, "r") as f:
            original_content = f.read()
    except Exception as e:
        log_and_print(f"Error reading file {file_path}: {e}. Skipping.", "error")
        return

    # Construct prompt for OpenAI API
    prompt = f"""
    Refactor the following code or content using best practices:
    {original_content}
    
    Include detailed comments and maintain original functionality.
    """
    try:
        log_and_print(f"Sending content of {os.path.basename(file_path)} to OpenAI for refactoring...")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500
        )
        refined_content = response.choices[0].message["content"]
        log_and_print(f"OpenAI refactoring completed for {os.path.basename(file_path)}.", "info")
    except Exception as e:
        log_and_print(f"OpenAI API call failed for {file_path}: {e}. Skipping.", "error")
        return

    # Write the refined content back to the file
    try:
        with open(file_path, "w") as f:
            f.write(refined_content)
        log_and_print(f"Refactored content saved for {file_path}.", "info")
    except Exception as e:
        log_and_print(f"Error saving refactored content for {file_path}: {e}.", "error")


def refactor_repo_with_openai(repo_dir):
    """
    Refactor all supported files in the repository using OpenAI's API.

    Args:
        repo_dir (str): Path to the repository directory.
    """
    log_and_print(f"Starting refactoring with OpenAI in repository: {repo_dir}")

    try:
        file_count = 0
        for root, _, files in os.walk(repo_dir):
            for file in files:
                if file.endswith(SUPPORTED_FILE_EXTENSIONS):
                    file_count += 1
                    process_file(os.path.join(root, file))

        if file_count == 0:
            log_and_print("No supported files found in the repository. Refactoring aborted.", "warning")
        else:
            log_and_print(f"Refactoring completed successfully. Total files processed: {file_count}", "info")
    except Exception as e:
        log_and_print(f"Unexpected error during refactoring: {e}", "error")
        raise RuntimeError(f"OpenAI refactoring failed: {e}")


if __name__ == "__main__":
    # Example usage
    repo_directory = input("Enter the path to the repository to refactor: ").strip()
    if os.path.isdir(repo_directory):
        try:
            refactor_repo_with_openai(repo_directory)
        except RuntimeError as e:
            log_and_print(f"Refactoring process failed: {e}", "error")
    else:
        log_and_print(f"Invalid directory: {repo_directory}", "error")
