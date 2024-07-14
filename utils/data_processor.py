def query_by_language(data, language):
    result = []
    for user in data:
        for repo in user['repos']:
            if language.lower() in [la.lower() for la in repo['languages']]:
                result.append(user['username'])
                break
    return result