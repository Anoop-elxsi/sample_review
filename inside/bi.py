import os
import shutil
from urllib.parse import urlparse
import git
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

BASE_CLONE_DIR = "C:/repos"  # Persistent location to store repos
os.makedirs(BASE_CLONE_DIR, exist_ok=True)

def clone_repo(github_url, branch, username=None, token=None):
    """
    Clone a GitHub repository to a persistent local directory
    """
    repo_name = os.path.splitext(os.path.basename(urlparse(github_url).path))[0]
    repo_path = os.path.join(BASE_CLONE_DIR, repo_name)

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    auth_url = (
        f"https://{username}:{token}@{urlparse(github_url).netloc}{urlparse(github_url).path}"
        if username and token
        else github_url
    )

    try:
        git.Repo.clone_from(auth_url, repo_path, branch=branch, depth=1)
        logging.info(f"Repository cloned successfully to {repo_path}")
        return jsonify({"message": "Repository cloned successfully", "path": repo_path})
    except git.exc.GitCommandError as e:
        logging.error(f"Git command failed: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/clone', methods=['POST'])
def clone_repo():
    """
    Clone a GitHub repository to a persistent local directory
    """
    data = request.json
    github_url = data.get("github_url")
    branch = data.get("branch", "main")
    username = data.get("username")
    token = data.get("token")

    try:
        # Input validation - minimal for this example.  Expand as needed.
        if not isinstance(github_url, str) or not github_url:
            return jsonify({"error": "Invalid github_url"}), 400
        if not isinstance(branch, str) or not branch:
            return jsonify({"error": "Invalid branch"}), 400

        return clone_repo(github_url, branch, username, token)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/list-files', methods=['GET'])
def list_files():
    """
    List all files in the cloned repo
    """
    repo_path = request.args.get("repo_path")
    if not repo_path or not os.path.exists(repo_path):
        return jsonify({"error": "Repository path not found"}), 404

    file_list = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_list.append(os.path.relpath(os.path.join(root, file), repo_path))

    return jsonify({"files": file_list})


@app.route('/get-file', methods=['GET'])
def get_file():
    """
    Read a specific file from the cloned repo
    """
    repo_path = request.args.get("repo_path")
    file_name = request.args.get("file")

    if not repo_path or not os.path.exists(repo_path):
        return jsonify({"error": "Repository path not found"}), 404

    full_path = os.path.join(repo_path, file_name)
    if not os.path.exists(full_path):
        return jsonify({"error": "File not found"}), 404

    try:
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return jsonify({"content": content})
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)