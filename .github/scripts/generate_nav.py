import yaml
import os

MKDOCS_YML_PATH = "mkdocs.yml"
TODO_MD_FILENAME = "todo.md"

# Files or directories to exclude from the navigation
EXCLUDED_PATHS = [
    ".git",
    ".github",
    "site",
    "_site",
    "docs",
    "README.md",
    ".gitignore",
    "CNAME",
    MKDOCS_YML_PATH,
]


def as_title(path):
    """Convert a file or directory path to a human-readable title."""
    title = os.path.basename(path)
    if title.endswith(".md"):
        title = title[:-3]  # Remove the .md extension
    return title.replace("_", " ")


def create_nav_entry(path):
    """Create a navigation entry for a given path."""
    if os.path.isdir(path):
        # It's a directory, create a nested structure
        title = as_title(path)

        # Get children, and separate them into dirs and files to ensure dirs come first
        child_items = sorted(os.listdir(path))
        dirs = []
        files = []
        for item in child_items:
            child_path = os.path.join(path, item)
            if os.path.isdir(child_path):
                dirs.append(child_path)
            elif item.endswith(".md"):
                files.append(child_path)

        children = dirs + files

        nav_children = []
        for child in children:
            if os.path.basename(child) in EXCLUDED_PATHS:
                continue
            if os.path.isdir(child) or child.endswith(".md"):
                child_entry = create_nav_entry(child)
                if child_entry:
                    nav_children.append(child_entry)

        if not nav_children:
            return None

        return {title: nav_children}
    elif path.endswith(".md"):
        # It's a markdown file, create a title from the filename
        title = as_title(path)
        return {title: path}
    return None


def generate_index_markdown(nav_structure, level=0):
    markdown = ""
    for entry in nav_structure:
        for title, value in entry.items():
            if isinstance(value, str):  # it's a file
                # Don't link to index.md itself
                if value == "index.md":
                    continue
                # Indentation for list level
                indent = "  " * level
                # Create markdown link, assuming it will be placed in the root of docs
                link_path = value[:-3] + "/"
                markdown += f"{indent}- [{title}]({link_path})\n"
            elif isinstance(value, list):  # it's a directory
                indent = "  " * level
                markdown += f"{indent}- {title}\n"
                markdown += generate_index_markdown(value, level + 1)
    return markdown


def main():
    """Main function to generate and update the navigation."""
    with open(MKDOCS_YML_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    docs_dir = "docs"
    if not os.path.isdir(docs_dir):
        print(
            f"Error: '{docs_dir}' directory not found. The workflow should have created it."
        )
        return

    # Change into docs directory to make path handling easier
    os.chdir(docs_dir)

    root_items = sorted(os.listdir("."))
    nav_structure = []

    # Separate directories and files to ensure dirs come first
    dirs = []
    files = []
    todo_files = []
    for item in root_items:
        if item in EXCLUDED_PATHS:
            continue
        if os.path.isdir(item):
            dirs.append(item)
        elif item == TODO_MD_FILENAME:
            todo_files.append(item)
        elif item.endswith(".md"):
            files.append(item)

    # Process directories, then files
    all_items = todo_files + dirs + files
    for item in all_items:
        entry = create_nav_entry(item)
        if entry:
            nav_structure.append(entry)

    # Change back to the project root to access mkdocs.yml
    os.chdir("..")

    # Add the generated nav to the config
    config["nav"] = nav_structure

    # Generate the content for index.md
    index_md_content = "# Home\n\n"
    index_md_content += generate_index_markdown(nav_structure)

    # Write the index.md file
    os.chdir(docs_dir)
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(index_md_content)
        
        print("Generated index.md with the following content:")
        print(index_md_content)

        print(f'Current dirs in {docs_dir}: {os.listdir(".")}')

    os.chdir("..")  # Change back to the project root

    with open(MKDOCS_YML_PATH, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print("Successfully generated and updated the navigation in mkdocs.yml")

    # Print the updated mkdocs.yml content for verification
    with open(MKDOCS_YML_PATH, "r", encoding="utf-8") as f:
        print(f.read())


if __name__ == "__main__":
    main()
