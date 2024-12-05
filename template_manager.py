
import ai_utils
import template_utils

def apply_template(repo_dir):
    templates = template_utils.get_app_templates()

    print("Available Categories:")
    for idx, category in enumerate(templates.keys(), 1):
        print(f"{idx}. {category}")

    category_idx = int(input("Select a category: ")) - 1
    category_name = list(templates.keys())[category_idx]
    category_templates = templates[category_name]

    print(f"Templates in {category_name}:")
    for idx, template in enumerate(category_templates.keys(), 1):
        print(f"{idx}. {template}")

    template_idx = int(input("Select a template: ")) - 1
    template_name = list(category_templates.keys())[template_idx]

    file_structure = category_templates[template_name]
    ai_utils.create_placeholders(file_structure, repo_dir)
    print(f"Template {template_name} applied successfully.")
