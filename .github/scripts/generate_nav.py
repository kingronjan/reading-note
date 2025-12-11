
import yaml
import os

# Files or directories to exclude from the navigation
EXCLUDED_PATHS = [
    ".git",
    ".github",
    "site",
    "_site",
    "docs",
    "mkdocs.yml",
    "README.md",
    ".gitignore",
    "CNAME"
]

def create_nav_entry(path):
    """Create a navigation entry for a given path."""
    if os.path.isdir(path):
        # It's a directory, create a nested structure
        title = os.path.basename(path).replace('-', ' ').replace('_', ' ').title()
        
        # Get children, filter out excluded and non-markdown files
        children = [os.path.join(path, child) for child in sorted(os.listdir(path))]
        
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
    with open('mkdocs.yml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    root_items = sorted(os.listdir('.'))
    nav_structure = []

    # First, add top-level markdown files
    for item in root_items:
        if item.endswith('.md') and item not in EXCLUDED_PATHS:
            nav_structure.append(item)
            
    # Then, add directories
    for item in root_items:
        if os.path.isdir(item) and item not in EXCLUDED_PATHS:
            entry = create_nav_entry(item)
            if entry:
                nav_structure.append(entry)

    # Add the generated nav to the config under a single top-level key
    config['nav'] = [{'笔记': nav_structure}]

    with open('mkdocs.yml', 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print("Successfully generated and updated the navigation in mkdocs.yml")

if __name__ == "__main__":
    main()
