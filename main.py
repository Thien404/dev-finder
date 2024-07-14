import json

import requests

GITHUB_API_URL = "https://api.github.com"
ORG_NAME = "codecentric"
AUTHORIZATION_HEADER = {"Authorization": "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"}

def get_org_members(org_name):
    # read content from user_data.json
    members_data = None
    with open('user_data.json', 'r') as file:
        members_data = file.read()

    if members_data:
        print("Load members from file")
        return json.loads(members_data)
    try:
        url = f"{GITHUB_API_URL}/orgs/{org_name}/members"
        print("Fetch members from:" + url)
        response = requests.get(url, headers=AUTHORIZATION_HEADER)
        response.raise_for_status()
        members_data = response.json()
        with open('user_data.json', 'w') as file:
            file.write(json.dumps(members_data))
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to get members of {org_name}") from e

    return members_data


def get_user_repos(username):
    try:
        url = f"{GITHUB_API_URL}/users/{username}/repos"
        response = requests.get(url, headers=AUTHORIZATION_HEADER)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to get repos of {username}") from e

    print(response.json())
    return response.json()


def get_repo_languages(owner, repo):
    try:
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/languages"
        response = requests.get(url, headers=AUTHORIZATION_HEADER)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to get languages of {owner}/{repo}") from e

    print(response.json())
    return response.json()


def gather_data(org_name):
    members = get_org_members(org_name)
    return members;
    data = []

    for member in members:
        username = member['login']
        repos = get_user_repos(username)
        user_data = {'username': username, 'repos': []}

        for repo in repos:
            repo_name = repo['name']
            languages = get_repo_languages(username, repo_name)
            user_data['repos'].append({
                'repo_name': repo_name,
                'languages': list(languages.keys())
            })

        data.append(user_data)

    return data


def query_by_language(data, language):
    result = []
    for user in data:
        for repo in user['repos']:
            if language in repo['languages']:
                result.append(user['username'])
                break
    return result


# Daten sammeln
data = gather_data(ORG_NAME)
print(data)
exit(1)
# Abfrage nach Scala Entwicklern
# scala_developers = query_by_language(data, 'Scala')
print(scala_developers)