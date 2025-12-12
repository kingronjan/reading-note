
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

def find_first_md_path(nav_structure):
    """
    Recursively finds the path of the first markdown file in the nav_structure.
    The nav_structure is a list of dictionaries, where each dict can have:
    - {'Title': 'path/to/file.md'}
    - {'DirectoryTitle': [{'SubTitle': 'path/to/subfile.md'}, ...]}
    """
    if not nav_structure:
        return None

    first_entry = nav_structure[0]
    if isinstance(first_entry, dict):
        for key, value in first_entry.items():
            if isinstance(value, str) and value.endswith('.md'):
                return value
            elif isinstance(value, list):
                # Recurse into nested list (directory content)
                nested_path = find_first_md_path(value)
                if nested_path:
                    return nested_path
    return None

def redirect_path_to_url(md_path):
    """
    Converts a markdown file path (e.g., 'ai/gemini.md') to an MkDocs URL format
    (e.g., 'ai/gemini/').
    """
    if md_path.endswith('.md'):
        return md_path[:-3] + '/'
    return md_path

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
        # It's a markdown file, create a title from the filename
        title = os.path.basename(path)[:-3].replace('-', ' ').replace('_', ' ').title()
        return {title: path}
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

    # Process directories first, then files
    all_items = dirs + files
    for item in all_items:
        entry = create_nav_entry(item)
        if entry:
            nav_structure.append(entry)

    # Change back to the project root to access mkdocs.yml
    os.chdir('..')

    # Add the generated nav to the config
    config['nav'] = nav_structure

    # Find the first markdown file path for redirection
    first_md_path = find_first_md_path(nav_structure)
    if first_md_path:
        # Convert markdown path to a URL-friendly format for redirect
        redirect_url = redirect_path_to_url(first_md_path)
        
        # Create an index.md in the docs directory that redirects to the first item
        # Change back to the docs directory to write index.md
        os.chdir(docs_dir)
        with open('index.md', 'w', encoding='utf-8') as f:
            f.write(f'<!DOCTYPE html>\n<html>\n<head>\n<meta http-equiv="refresh" content="0; url=./{redirect_url}">\n</head>\n<body>\n<p>Redirecting to <a href="./{redirect_url}">{redirect_url}</a></p>\n</body>\n</html>')
        os.chdir('..') # Change back to the project root

    with open(MKDOCS_YML_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print("Successfully generated and updated the navigation in mkdocs.yml")

    # Print the updated mkdocs.yml content for verification
    with open(MKDOCS_YML_PATH, 'r', encoding='utf-8') as f:
        print(f.read())

if __name__ == "__main__":
    main()
