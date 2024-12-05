import os
import logging
import openai
import json
import time

logging.basicConfig(
    filename="ai_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Retry configuration for API calls
MAX_RETRIES = 3
RETRY_DELAY = 10  # seconds


def call_openai(prompt, model="gpt-4", max_tokens=300, temperature=0.5):
    """
    Make a request to OpenAI's API with retries for robustness.

    Args:
        prompt (str): The prompt to send to OpenAI.
        model (str): The OpenAI model to use.
        max_tokens (int): Maximum tokens for the response.
        temperature (float): Sampling temperature.

    Returns:
        str: OpenAI response content.
    """
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            logging.info(f"Received OpenAI response: {response.choices[0].message['content']}")
            return response.choices[0].message["content"]
        except openai.error.OpenAIError as e:
            logging.error(f"OpenAI API error: {e}")
            retries += 1
            if retries < MAX_RETRIES:
                logging.info(f"Retrying OpenAI request ({retries}/{MAX_RETRIES}) after delay.")
                time.sleep(RETRY_DELAY)
            else:
                raise RuntimeError(f"OpenAI API request failed after {MAX_RETRIES} retries. Error: {e}")


def select_app_type():
    """
    Prompt the user to select the type of app they want to create.

    Returns:
        str: The selected app type.
    Raises:
        ValueError: If the selection is invalid.
    """
    app_types = ["web", "mobile", "backend", "frontend", "utility"]  # Example hardcoded list
    print("Select the type of app you want to create:")
    for idx, app_type in enumerate(app_types, 1):
        print(f"{idx}. {app_type.capitalize()}")

    selection = input("Enter the number corresponding to your choice: ").strip()
    try:
        app_type = app_types[int(selection) - 1]
        logging.info(f"User selected app type: {app_type}")
        return app_type
    except (IndexError, ValueError):
        raise ValueError("Invalid selection. Please enter a valid number.")


def get_app_description():
    """
    Prompt the user to describe the app they want to create.

    Returns:
        str: The app description provided by the user.
    Raises:
        ValueError: If the description is empty.
    """
    description = input("Describe the app you'd like to create: ").strip()
    if not description:
        raise ValueError("App description cannot be empty.")
    logging.info(f"User provided app description: {description}")
    return description


def plan_file_structure(app_type, description):
    """
    Generate a file structure dynamically based on the app type and description.

    Args:
        app_type (str): The selected app type.
        description (str): The app description.

    Returns:
        dict: The planned file structure.
    """
    prompt = f"""
    Based on the following app type and description, plan a file structure in JSON format:
    App Type: {app_type}
    Description: {description}

    Example Output:
    {{
        "project_root": "MyApp",
        "folders": ["src", "tests", "resources"],
        "files": {{
            "src": ["main.py", "utils.py"],
            "resources": ["image.png", "style.css"]
        }}
    }}
    """
    try:
        response = call_openai(prompt, max_tokens=500)
        file_structure = json.loads(response)
        logging.info(f"Generated file structure dynamically: {file_structure}")
        return file_structure
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing file structure response: {e}")
        raise ValueError("Invalid response format from AI. Ensure the AI returns JSON.")


def create_placeholders(file_structure, repo_dir):
    """
    Generate placeholder files in the repository directory.

    Args:
        file_structure (dict): The planned file structure.
        repo_dir (str): The root directory of the repository.
    """
    try:
        for folder in file_structure.get("folders", []):
            folder_path = os.path.join(repo_dir, folder)
            os.makedirs(folder_path, exist_ok=True)
            logging.info(f"Created folder: {folder_path}")

        for folder, files in file_structure.get("files", {}).items():
            folder_path = os.path.join(repo_dir, folder)
            os.makedirs(folder_path, exist_ok=True)
            for file in files:
                file_path = os.path.join(folder_path, file)
                if not os.path.exists(file_path):
                    placeholder_content = f"# Placeholder for {file}\n\n# Add your implementation here."
                    with open(file_path, "w") as f:
                        f.write(placeholder_content)
                    logging.info(f"Created placeholder file: {file_path}")
                else:
                    logging.info(f"Skipped placeholder creation for existing file: {file_path}")

        print("Placeholders created successfully.")
    except Exception as e:
        logging.error(f"Error creating placeholders: {e}")
        raise RuntimeError(f"Error creating placeholders: {e}")


def process_files(file_structure, repo_dir):
    """
    Iterate over files in the structure and code each one in the repository directory.

    Args:
        file_structure (dict): The planned file structure.
        repo_dir (str): The root directory of the repository.
    """
    try:
        for folder, files in file_structure.get("files", {}).items():
            for file in files:
                file_path = os.path.join(repo_dir, folder, file)
                refine_file(file_path)
        print("All files coded successfully.")
    except Exception as e:
        logging.error(f"Error processing files: {e}")
        raise RuntimeError(f"Error processing files: {e}")


def refine_file(file_path):
    """
    Generate and refine code for a file using OpenAI's API.

    Args:
        file_path (str): The path to the file to refine.
    """
    try:
        with open(file_path, "r") as f:
            content = f.read()

        prompt = f"Refactor the following content for clarity and optimization:\n```{content}```"
        refined_content = call_openai(prompt, max_tokens=500)

        with open(file_path, "w") as f:
            f.write(refined_content)
        logging.info(f"Refined file: {file_path}")
        print(f"Refined: {file_path}")

    except Exception as e:
        logging.error(f"Error refining file {file_path}: {e}")
        raise RuntimeError(f"Error refining file {file_path}: {e}")
