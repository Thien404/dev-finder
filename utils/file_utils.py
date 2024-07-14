import json
import os

def get_repos_from_file(username):
    if not os.path.exists("data/" + username):
        os.makedirs("data/" + username)

    # check if file in directory exists
    if not os.path.exists("data/" + username + "/repos.json"):
        with open("data/" + username + "/repos.json", "w") as file:
            file.write("[]")
            file.close()

    # read content from repos.json
    with open("data/" + username + "/repos.json", "r") as file:
        return json.loads(file.read())


def get_members_from_file():
    with open('data/user_data.json', 'r') as file:
        return json.loads(file.read())


def get_languages_from_file(username, repo):
    if not os.path.exists(f"data/{username}/{repo}.json"):
        file = open(f"data/{username}/{repo}.json", "w")
        file.write("[]")
        file.close()
        print("Create languages file for user: " + username)

    lang_data = None
    with open(f"data/{username}/{repo}.json", "r") as file:
        return json.loads(file.read())


def write_org_members_to_file(data):
    with open('data/user_data.json', 'w') as file:
        print("Write members to file")
        file.write(json.dumps(data))


def write_user_repos_to_file(username, data):
    with open("data/" + username + "/repos.json", "w") as file:
        file.write(json.dumps(data))


def write_repo_languages_to_file(username, repo, data):
    with open(f"data/{username}/{repo}.json", "w") as file:
        file.write(json.dumps(data))