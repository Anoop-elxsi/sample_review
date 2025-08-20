# Clone a GitHub repository to a persistent local directory
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


@app.route('/list_files', methods=['POST'])
def list_files():
    """
    Lists the files in a git repository.
    """
    data = request.get_json()
    repo_path = data.get('repo_path')

    if not repo_path:
        return jsonify({'error': 'repo_path is required'}), 400

    try:
        if not os.path.exists(repo_path):
            return jsonify({'error': 'repo_path does not exist'}), 404
        
        file_list = []
        for root, _, files in os.walk(repo_path):
            for file in files:
                file_list.append(os.path.relpath(os.path.join(root, file), repo_path))
        return jsonify({'files': file_list})
    except OSError as e:
        logging.error(f"Error walking directory: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/get_file', methods=['POST'])
def get_file():
    """
    Gets a specific file from a git repository.
    """
    data = request.get_json()
    repo_path = data.get('repo_path')
    file_path = data.get('file_path')

    if not repo_path or not file_path:
        return jsonify({'error': 'repo_path and file_path are required'}), 400

    try:
        if not os.path.exists(os.path.join(repo_path, file_path)):
            return jsonify({'error': 'file not found'}), 404
        
        with open(os.path.join(repo_path, file_path), 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({'content': content})
    except OSError as e:
        logging.error(f"Error reading file: {e}")
        return jsonify({'error': str(e)}), 500