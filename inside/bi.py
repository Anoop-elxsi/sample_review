import os
import shutil
from urllib.parse import urlparse
from flask import Flask, request, jsonify
import git

app = Flask(__name__)

BASE_CLONE_DIR = "C:/repos"  # Persistent location to store repos
os.makedirs(BASE_CLONE_DIR, exist_ok=True)

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
        parsed_url = urlparse(github_url)
        repo_name = os.path.splitext(os.path.basename(parsed_url.path))[0]
        repo_path = os.path.join(BASE_CLONE_DIR, repo_name)

        # Remove if already exists
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)

        # Construct authenticated URL if needed
        auth_url = (
            f"https://{username}:{token}@{parsed_url.netloc}{parsed_url.path}"
            if username and token
            else github_url
        )

        git.Repo.clone_from(auth_url, repo_path, branch=branch, depth=1)

        return jsonify({"message": "Repository cloned successfully", "path": repo_path})

    except Exception as e:
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

    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    return jsonify({"content": content})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
