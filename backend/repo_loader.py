import os
import shutil
import tempfile
import git
from pathlib import Path

# Common ignored directories and files
IGNORED_DIRS = {'.git', 'node_modules', 'venv', '__pycache__', 'dist', 'build', '.idea', '.vscode'}
IGNORED_FILES = {'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'poetry.lock', 'Pipfile.lock'}

# Valid source code extensions to ingest
VALID_EXTENSIONS = {
    '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', 
    '.java', '.cpp', '.c', '.h', '.cs', '.go', '.rs', 
    '.md', '.json', '.yml', '.yaml', '.toml', '.xml',
    '.sql', '.sh', '.bat', '.ps1'
}

def should_process_file(file_path: Path) -> bool:
    # Check filename
    if file_path.name in IGNORED_FILES:
        return False
    # Check extensions
    if file_path.suffix not in VALID_EXTENSIONS:
        return False
    # Check if any parent part is ignored
    for part in file_path.parts:
        if part in IGNORED_DIRS:
            return False
    if file_path.name.startswith('.'):
        return False
    return True

def clone_and_process_repo(repo_url: str) -> str:
    """
    Clones a git repo to a temp directory, reads all valid source files,
    concatenates them into a single string, and cleans up.
    """
    temp_dir = tempfile.mkdtemp()
    print(f"Cloning {repo_url} to {temp_dir}...")
    
    try:
        git.Repo.clone_from(repo_url, temp_dir, depth=1)
        
        all_content = []
        file_count = 0
        
        for root, dirs, files in os.walk(temp_dir):
            # Modify dirs in-place to skip ignored directories during walk
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith('.')]
            
            for file in files:
                file_path = Path(root) / file
                
                if should_process_file(file_path):
                    try:
                        # relatives path for display
                        rel_path = file_path.relative_to(temp_dir).as_posix()
                        
                        # Read content
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                        # Format entry
                        entry = f"--- START FILE: {rel_path} ---\n{content}\n--- END FILE: {rel_path} ---\n"
                        all_content.append(entry)
                        file_count += 1
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

        summary = f"Processed {file_count} files from {repo_url}.\n"
        print(summary)
        return summary + "\n".join(all_content)

    finally:
        try:
            # On Windows, readonly files sometimes cause rmtree to fail.
            # We can use a custom handler or just ignore errors for now given this is a hackathon/MVP.
            def on_rm_error(func, path, exc_info):
                os.chmod(path, 0o777)
                try:
                    func(path)
                except Exception:
                    pass

            shutil.rmtree(temp_dir, onerror=on_rm_error)
            print(f"Cleaned up {temp_dir}")
        except Exception as e:
            print(f"Cleanup error: {e}")
