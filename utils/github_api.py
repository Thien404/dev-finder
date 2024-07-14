import requests
import time
import datetime

GITHUB_API_URL = "https://api.github.com"
AUTHORIZATION_HEADER = {"Authorization": "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"}


# https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api?apiVersion=2022-11-28
# If you are making a large number of POST, PATCH, PUT, or DELETE requests, wait at least one second between each request. This will help you avoid secondary rate limits.


def get_org_members(org_name):
    print("Fetch members from:" + org_name)
    url = f"{GITHUB_API_URL}/orgs/{org_name}/members"
    response = send_request(url)
    return response.json()


def get_user_repos(username):
    print("Fetch repos from: " + username)
    url = f"{GITHUB_API_URL}/users/{username}/repos"
    response = send_request(url)
    return response.json()


def get_repo_languages(username, repo):
    print("Fetch languages from: " + username + "/" + repo)
    url = f"{GITHUB_API_URL}/repos/{username}/{repo}/languages"
    response = send_request(url)
    return response.json()


def send_request(url):
    response = requests.get(url, headers=AUTHORIZATION_HEADER)
    handle_api_rate_limit(response)
    response.raise_for_status()
    time.sleep(1)
    return response


def handle_api_rate_limit(response):
    rate_limit_remaining = response.headers.get("X-RateLimit-Remaining", None)
    if rate_limit_remaining is not None and int(rate_limit_remaining) < 10:
        reset_time = response.headers.get("X-RateLimit-Reset", None)
        dt = datetime.datetime.fromtimestamp(int(reset_time))
        print(f"Rate limit reached. Reset time: {dt}; {reset_time}")
        seconds_to_wait = int(reset_time) - int(time.time()) + 1
        print(f"Waiting {seconds_to_wait} seconds")
        time.sleep(seconds_to_wait)
        return True
    return False
