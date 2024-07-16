# Dev Finder
Find a developer to work on your project by language.
## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/dev-finder.git
    cd dev-finder
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Set up your GitHub token:

    To interact with the GitHub API, you need to set your personal access token. Replace `YOUR_GITHUB_TOKEN` with your actual token in the `AUTHORIZATION_HEADER` dictionary in `src/github_api.py`:

    ```python
    AUTHORIZATION_HEADER = {"Authorization": "YOUR_GITHUB_TOKEN"}
    ```
   
2. Run the script:

    You can run the main script to gather data and query developers by language:

    ```bash
    python main.py
    ```

3. Query developers by language:

    The script will output a list of developers who have experience with the specified language, sorted by the number of lines of code in that language.


## Testing
1. Run tests:

    ```bash
    pytest
    ```

## Further Development
- Add more test cases
- Create API endpoints for querying developers.
- Move the GitHub token to a configuration file
- Move generated data to a database
- Create virtual environment/container for the project
- Improve GitHub API rate limiting handling
- Improve error handling
- Add pipeline CI integration
- Parallelize data gathering with multiprocessing