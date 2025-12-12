
import yaml
import os

MKDOCS_YML_PATH = 'mkdocs.yml'

# Files or directories to exclude from the navigation
EXCLUDED_PATHS = [
    ".git",
    ".github",
    "site",
    "_site",
    "docs",
    MKDOCS_YML_PATH,
    "README.md",
    ".gitignore",
    "CNAME"
]

def create_nav_entry(path):
    """Create a navigation entry for a given path."""
    if os.path.isdir(path):
        # It's a directory, create a nested structure
        title = os.path.basename(path).replace('-', ' ').replace('_', ' ').title()
        
        # Get children, and separate them into dirs and files to ensure dirs come first
        child_items = sorted(os.listdir(path))
        dirs = []
        files = []
        for item in child_items:
            child_path = os.path.join(path, item)
            if os.path.isdir(child_path):
                dirs.append(child_path)
            elif item.endswith('.md'):
                files.append(child_path)

        children = dirs + files
        
        nav_children = []
        for child in children:
            if os.path.basename(child) in EXCLUDED_PATHS:
                continue
            if os.path.isdir(child) or child.endswith('.md'):
                 child_entry = create_nav_entry(child)
                 if child_entry:
                    nav_children.append(child_entry)

        if not nav_children:
            return None
            
        return {title: nav_children}
    elif path.endswith('.md'):
        # It's a markdown file
        return path
    return None

def main():
    """Main function to generate and update the navigation."""
    with open(MKDOCS_YML_PATH, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    docs_dir = 'docs'
    if not os.path.isdir(docs_dir):
        print(f"Error: '{docs_dir}' directory not found. The workflow should have created it.")
        return

    # Change into docs directory to make path handling easier
    os.chdir(docs_dir)

    root_items = sorted(os.listdir('.'))
    nav_structure = []

    # Separate directories and files to ensure dirs come first
    dirs = []
    files = []
    for item in root_items:
        if item in EXCLUDED_PATHS:
            continue
        if os.path.isdir(item):
            dirs.append(item)
        elif item.endswith('.md'):
            files.append(item)

    # Process directories first
    for item in dirs:
        if item not in EXCLUDED_PATHS:
            entry = create_nav_entry(item)
            if entry:
                nav_structure.append(entry)

    # Then, add top-level markdown files
    for item in files:
        if item not in EXCLUDED_PATHS:
            nav_structure.append(item)

    # Change back to the project root to access mkdocs.yml
    os.chdir('..')

    # Add the generated nav to the config
    config['nav'] = nav_structure

    with open(MKDOCS_YML_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print("Successfully generated and updated the navigation in mkdocs.yml")

    with open(MKDOCS_YML_PATH, 'r', encoding='utf-8') as f:
        print(f.read())  # Print the updated mkdocs.yml content

if __name__ == "__main__":
    main()
