import os

def remove_migrations():
    base_dir = os.getcwd()  # Current working directory
    for root, dirs, files in os.walk(base_dir):
        if "migrations" in dirs:  # Check if a 'migrations' folder exists
            migration_path = os.path.join(root, "migrations")
            for file in os.listdir(migration_path):
                if file != "__init__.py":  # Skip __init__.py
                    file_path = os.path.join(migration_path, file)
                    os.remove(file_path)  # Remove the file
                    print(f"Deleted: {file_path}")

if __name__ == "__main__":
    remove_migrations()
