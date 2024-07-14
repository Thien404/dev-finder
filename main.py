import json

import requests
from utils.file_utils import (
    get_repos_from_file, get_members_from_file, get_languages_from_file,
    write_org_members_to_file, write_user_repos_to_file, write_repo_languages_to_file
)
import utils.github_api as github_api
from utils.data_processor import query_by_language

ORG_NAME = "codecentric"


def get_org_members(org_name):
    # read content from user_data.json
    members_data = get_members_from_file()
    if members_data is None:
        members_data = {}
    # return members if exists in file
    if len(members_data) > 0 or members_data == {}:
        print("Load members from file")
        return members_data
    try:
        members_data = github_api.get_org_members(org_name)
        write_org_members_to_file(members_data)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to get members of {org_name}") from e

    return members_data


def get_user_repos(username):
    repos_data = get_repos_from_file(username)
    if repos_data is None:
        repos_data = {}
    # return data if exists in file
    if len(repos_data) > 0 or repos_data == {}:
        print("Load repos from file: " + username)
        return repos_data

    try:
        repos_data = github_api.get_user_repos(username)
        write_user_repos_to_file(username, repos_data)
    except requests.exceptions.RequestException as e:
        print(e)
        raise Exception(f"Failed to get repos of {username}") from e

    return repos_data


def get_repo_languages(username, repo):
    lang_data = get_languages_from_file(username, repo)
    if lang_data is None:
        lang_data = {}
    if len(lang_data) > 0 or lang_data == {}:
        print(f"Load languages from file: {username}/{repo}")
        return lang_data

    try:
        lang_data = github_api.get_repo_languages(username, repo)
        write_repo_languages_to_file(username, repo, lang_data)
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
        if counter > 2:
            break
        counter += 1
        username = member['login']
        try:
            repos = get_user_repos(username)
        except Exception as e:
            print("Failed to get repos of " + username)
            continue
        user_data = {'username': username, 'repos': []}

        repo_counter = 0
        for repo in repos:
            # if repo_counter > 3:
            #     break
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


def main():
    data = gather_data(ORG_NAME)
    matching_devs = query_by_language(data, 'javascript')

    print(matching_devs)


if __name__ == "__main__":
    main()
