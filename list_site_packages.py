import os

def print_tree(startpath):
    for root, dirs, files in os.walk(startpath):
        # Remove __pycache__ and *.dist-info folders from dirs list so they don't get walked
        dirs[:] = [d for d in dirs if not (d.endswith('.dist-info') or d == '__pycache__')]
        # Filter out .pyc files from files list
        files = [f for f in files if not f.endswith('.pyc')]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = '    ' * level
        print(f"{indent}{os.path.basename(root)}/")
        for f in files:
            print(f"{indent}    {f}")

if __name__ == "__main__":
    print_tree('.venv/Lib/site-packages')
