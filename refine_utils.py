import os
import openai
import logging
import datetime

# Logging setup
logging.basicConfig(
    filename="refinement_session_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

SUPPORTED_EXTENSIONS = ('.py', '.java', '.html', '.js', '.css', '.md')


def remove_language_specifier(content: str) -> str:
    """
    Remove leading language specifiers (e.g., 'python', 'java') from content.

    Args:
        content (str): Raw content from OpenAI response.

    Returns:
        str: Cleaned content without language specifiers.
    """
    lines = content.splitlines()
    if lines and lines[0].strip().lower() in {"python", "java", "javascript", "html", "css", "markdown"}:
        lines.pop(0)  # Remove the first line if it's a language specifier
    return "\n".join(lines)


def parse_refined_content(response: str, file_extension: str) -> tuple:
    """
    Parse OpenAI response to extract refined content and summary.

    Args:
        response (str): Raw response from OpenAI.
        file_extension (str): File extension to determine content type.

    Returns:
        tuple: (refined_content, summary)
    """
    # Handle markdown and non-code files
    if file_extension in {".md"}:
        summary = "Summary not provided."
        if "Summary:" in response:
            summary_start = response.find("Summary:") + len("Summary:")
            summary = response[summary_start:].split("\n")[0].strip()
        return response.strip(), summary

    # Extract content for code files between triple backticks
    start = response.find("```") + 3
    end = response.rfind("```")
    refined_content = response[start:end].strip() if start > 3 and end > start else None

    # Remove language specifier if present
    if refined_content:
        refined_content = remove_language_specifier(refined_content)

    # Extract summary
    summary = "No summary provided."
    if "Summary:" in response:
        summary_start = response.find("Summary:") + len("Summary:")
        summary = response[summary_start:].split("\n")[0].strip()

    return refined_content, summary


def update_changelog(repo_dir, changes_summary):
    """
    Append detailed refinement updates to CHANGELOG.md.

    Args:
        repo_dir (str): Path to the repository.
        changes_summary (str): Detailed summary of changes made during the session.
    """
    changelog_path = os.path.join(repo_dir, "CHANGELOG.md")
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    entry = f"## {timestamp}\n{changes_summary}\n"
    with open(changelog_path, "a") as changelog:
        changelog.write(entry)
    print("CHANGELOG.md updated successfully.")


def update_readme(repo_dir, session_summary):
    """
    Update README.md with a high-level session summary and changelog link.

    Args:
        repo_dir (str): Path to the repository.
        session_summary (str): High-level summary of refinements.
    """
    readme_path = os.path.join(repo_dir, "README.md")

    new_content = f"""
    ## Last Updated

    **Latest Changes**: {session_summary}
    **See full details in** [CHANGELOG.md](./CHANGELOG.md).
    """

    with open(readme_path, "r") as readme:
        content = readme.readlines()

    # Update Last Updated section
    updated_content = []
    for line in content:
        if line.strip() == "## Last Updated":
            updated_content.append("## Last Updated\n" + new_content + "\n")
        else:
            updated_content.append(line)

    if "## Last Updated" not in content:
        updated_content.append("\n" + new_content)

    with open(readme_path, "w") as readme:
        readme.writelines(updated_content)
    print("README.md updated successfully.")


def refine_project(repo_dir, custom_instructions=None):
    """
    Refine project files using OpenAI.

    Args:
        repo_dir (str): Path to the repository directory to refine.
        custom_instructions (str): Optional custom instructions for refinement.
    """
    print("\n=== Refinement Process Started ===\n")
    logging.info(f"Starting refinement in directory: {repo_dir}")
    refined_files_count = 0
    skipped_files = []
    changes_summary = []

    for root, dirs, files in os.walk(repo_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1]

            if file_extension in SUPPORTED_EXTENSIONS:
                print(f"Processing: {file_path}")
                logging.info(f"Processing file: {file_path} with extension {file_extension}")

                try:
                    # Read file content
                    with open(file_path, "r") as f:
                        original_content = f.read()

                    # Construct prompt for OpenAI
                    prompt = f"""
                    Refactor the following file:
                    
                    Instructions: {custom_instructions or 'Ensure best practices, maintain functionality, and improve readability.'}
                    
                    Content:
                    ```{original_content}```

                    Provide only the refined content without language specifiers and a brief summary prefixed with "Summary:". 
                    """
                    # Send content to OpenAI
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.5,
                        max_tokens=1500
                    )
                    refined_content, summary = parse_refined_content(
                        response.choices[0].message["content"], file_extension)

                    if refined_content:
                        # Write the refined content back to the file
                        with open(file_path, "w") as f:
                            f.write(refined_content)
                        logging.info(f"Successfully refined and saved: {file_path}")
                        logging.info(f"Summary for {file_path}: {summary}")
                        print(f"✔ Successfully refined: {file_path}")
                        print(f"   ↳ Summary: {summary}")
                        changes_summary.append(f"- **{file}**: {summary}")
                        refined_files_count += 1
                    else:
                        logging.warning(f"Skipping file due to unexpected format: {file_path}")
                        print(f"✖ Skipped: {file_path} - Unexpected response format.")
                        skipped_files.append(file_path)

                except openai.error.OpenAIError as openai_error:
                    logging.error(f"OpenAI API error for {file_path}: {openai_error}")
                    print(f"✖ API error while processing: {file_path}. Skipping.")
                    skipped_files.append(file_path)
                except Exception as e:
                    logging.error(f"Error for {file_path}: {e}")
                    print(f"✖ Error processing: {file_path}. Skipping.")
                    skipped_files.append(file_path)

    # Update CHANGELOG.md and README.md
    if changes_summary:
        update_changelog(repo_dir, "\n".join(changes_summary))
        update_readme(repo_dir, f"Refined {refined_files_count} files.")

    # Log and print session results
    print("\n=== Refinement Process Completed ===\n")
    if refined_files_count > 0:
        print(f"✔ Total files refined: {refined_files_count}")
    else:
        print("✖ No files were successfully refined.")
    logging.info(f"Total files refined: {refined_files_count}")

    if skipped_files:
        print(f"✖ Skipped files: {len(skipped_files)}. Check logs for details.")
        logging.info(f"Skipped files: {skipped_files}")
