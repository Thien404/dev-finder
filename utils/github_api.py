import requests
import time

GITHUB_API_URL = "https://api.github.com"
AUTHORIZATION_HEADER = {"Authorization": "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"}

# https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api?apiVersion=2022-11-28

# If you are making a large number of POST, PATCH, PUT, or DELETE requests, wait at least one second between each request. This will help you avoid secondary rate limits.
def get_org_members(org_name):
    url = f"{GITHUB_API_URL}/orgs/{org_name}/members"
    print("Fetch members from:" + url)
    response = requests.get(url, headers=AUTHORIZATION_HEADER)
    response.raise_for_status()
    time.sleep(1)
    return response.json()


def get_user_repos(username):
    print("Fetch repos from: " + username)
    url = f"{GITHUB_API_URL}/users/{username}/repos"
    response = requests.get(url, headers=AUTHORIZATION_HEADER)
    response.raise_for_status()
    # todo: get x-ratelimit-remaining from header
    print(response.headers)
    time.sleep(1)
    return response.json()


def get_repo_languages(username, repo):
    print("Fetch languages from: " + username + "/" + repo)
    url = f"{GITHUB_API_URL}/repos/{username}/{repo}/languages"
    response = requests.get(url, headers=AUTHORIZATION_HEADER)
    print(response.headers)
    response.raise_for_status()
    time.sleep(1)
    return response.json()
