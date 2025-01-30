import os

def remove_migrations():
    base_dir = os.getcwd()  # Current working directory
    for root, dirs, files in os.walk(base_dir):
        if "migrations" in dirs:  # Check if a 'migrations' folder exists
            migration_path = os.path.join(root, "migrations")
            for file in os.listdir(migration_path):
                file_path = os.path.join(migration_path, file)
                if file == "__init__.py":  # Skip __init__.py
                    continue
                if os.path.isfile(file_path):  # Ensure it's a file
                    os.remove(file_path)  # Remove the file
                    print(f"Deleted file: {file_path}")
                elif os.path.isdir(file_path):  # Skip directories like __pycache__
                    print(f"Skipped directory: {file_path}")

if __name__ == "__main__":
    remove_migrations()
