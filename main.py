import json

import requests

GITHUB_API_URL = "https://api.github.com"
ORG_NAME = "codecentric"
AUTHORIZATION_HEADER = {"Authorization": "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"}

def get_org_members(org_name):
    # read content from user_data.json
    members_data = None
    with open('data/user_data.json', 'r') as file:
        file_content = file.read()
        members_data = json.loads(file_content)

    if members_data and len(members_data) > 0:
        print("Load members from file")
        return members_data
    try:
        url = f"{GITHUB_API_URL}/orgs/{org_name}/members"
        print("Fetch members from:" + url)
        response = requests.get(url, headers=AUTHORIZATION_HEADER)
        response.raise_for_status()
        members_data = response.json()
        with open('data/user_data.json', 'w') as file:
            print("Write members to file")
            file.write(json.dumps(members_data))
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to get members of {org_name}") from e

    return members_data


def get_user_repos(username):
    # check if directory exists
    import os
    if not os.path.exists("data/" + username):
        os.makedirs("data/" + username)

    # check if file in directory exists
    if not os.path.exists("data/" + username + "/repos.json"):
        file = open("data/" + username + "/repos.json", "w")
        file.write("[]")
        file.close()
        print("Create repo file for user: " + username)

    # read content from repos.json
    repos_data = None
    with open("data/" + username + "/repos.json", "r") as file:
        file_content = file.read()
        repos_data = json.loads(file_content)

    # return data if exists
    if len(repos_data) > 0 or repos_data == {}:
        print("Load repos from file: " + username)
        return repos_data

    try:
        print("Fetch repos from: " + username)
        url = f"{GITHUB_API_URL}/users/{username}/repos"
        response = requests.get(url, headers=AUTHORIZATION_HEADER)
        response.raise_for_status()
        print(response.headers())
        repos_data = response.json()
        with open("data/" + username + "/repos.json", "w") as file:
            file.write(json.dumps(repos_data))
    except requests.exceptions.RequestException as e:
        print(e)
        raise Exception(f"Failed to get repos of {username}") from e

    return repos_data


def get_repo_languages(username, repo):
    import os
    # check if file in directory exists
    if not os.path.exists(f"data/{username}/{repo}.json"):
        file = open(f"data/{username}/{repo}.json", "w")
        file.write("[]")
        file.close()
        print("Create languages file for user: " + username)

    lang_data = None
    with open(f"data/{username}/{repo}.json", "r") as file:
        file_content = file.read()
        lang_data = json.loads(file_content)

    if len(lang_data) > 0 or lang_data == {}:
        print(f"Load languages from file: {username}/{repo}")
        return lang_data

    try:
        print("Fetch languages from: " + username + "/" + repo)
        url = f"{GITHUB_API_URL}/repos/{username}/{repo}/languages"
        response = requests.get(url, headers=AUTHORIZATION_HEADER)
        print(response.headers)
        response.raise_for_status()

        lang_data = response.json()
        with open(f"data/{username}/{repo}.json", "w") as file:
            file.write(json.dumps(lang_data))
    except requests.exceptions.RequestException as e:
        print("LANGUAGE ERROR")
        print(e)
        raise Exception(f"Failed to get languages of {username}/{repo}")

    return lang_data


# main function
def gather_data(org_name):
    members = get_org_members(org_name)
    data = []
    print("Fetch data for " + str(len(members)) + " members")
    counter = 0
    for member in members:
        if counter > 10:
            break
        counter += 1
        username = member['login']
        try:
            repos = get_user_repos(username)
        except Exception as e:
            print("Failed to get repos of " + username)
            continue
        user_data = {'username': username, 'repos': []}
#1720977749
        repo_counter = 0
        for repo in repos:
            if repo_counter > 3:
                break
            repo_counter += 1
            repo_name = repo['name']

            try:
                languages = get_repo_languages(username, repo_name)
            except Exception as e:
                print("Failed to get languages of " + username + "/" + repo_name)
                print(e)
                continue

            if len(languages) <= 0:
                continue

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
            if language.lower() in [la.lower() for la in repo['languages']]:
                result.append(user['username'])
                break
    return result


# Daten sammeln
data = gather_data(ORG_NAME)

# Daten filtern
matching_devs = query_by_language(data, 'clojure')

print(matching_devs)