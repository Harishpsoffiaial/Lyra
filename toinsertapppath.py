import os
import sqlite3

# Function to fetch all .exe paths
def fetch_all_exe_paths(directories, limit=500):
    """Fetch all .exe file paths from the specified directories."""
    exe_paths = []

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".exe"):
                    exe_paths.append(os.path.join(root, file))
                    if len(exe_paths) >= limit:  # Limit results to avoid overwhelming output
                        return exe_paths

    return exe_paths

# Directories to search
search_dirs = [
    r"C:\Program Files",
    r"C:\Program Files (x86)",
    r"C:\Windows\System32",
    os.path.expanduser(r"~\AppData\Local"),
    os.path.expanduser(r"~\AppData\Roaming")
]

# Fetch all .exe paths
all_exe_paths = fetch_all_exe_paths(search_dirs)  # Correctly initializing the variable

# Display the paths (optional)
for path in all_exe_paths[:10]:  # Display only the first 10 results
    print(path)

print(f"Found {len(all_exe_paths)} .exe files.")

# Database file path
DB_PATH = "lyra.db"

# Function to add .exe paths to the database
def add_exe_paths_to_db(exe_paths):
    """Insert all .exe paths into the sys_command table."""
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        for exe_path in exe_paths:
            # Extract app name from the path
            app_name = os.path.splitext(os.path.basename(exe_path))[0]

            # Insert into database
            cursor.execute("INSERT INTO sys_command (name, path) VALUES (?, ?)", (app_name, exe_path))

        conn.commit()
        print(f"Added {len(exe_paths)} applications to the database.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

# Add the fetched paths to the database
add_exe_paths_to_db(all_exe_paths)
