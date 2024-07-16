import unittest
from unittest.mock import MagicMock, patch
from src.github_api import get_org_members, get_user_repos, get_repo_languages, send_request, handle_api_rate_limit


class TestGitHubAPI(unittest.TestCase):

    @patch('requests.get')
    def test_get_org_members(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [{'login': 'user1'}, {'login': 'user2'}]
        mock_response.headers = {'X-RateLimit-Remaining': '100'}
        mock_get.return_value = mock_response

        members = get_org_members('codecentric')
        self.assertEquals(members, [{'login': 'user1'}, {'login': 'user2'}])
        mock_get.assert_called_with(
            'https://api.github.com/orgs/codecentric/members',
            headers={"Authorization": "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"})

    @patch('src.github_api.requests.get')
    def test_get_user_repos(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [{'name': 'repo1'}, {'name': 'repo2'}]
        mock_response.headers = {'X-RateLimit-Remaining': '100'}
        mock_get.return_value = mock_response

        repos = get_user_repos('user1')
        self.assertEqual(repos, [{'name': 'repo1'}, {'name': 'repo2'}])
        mock_get.assert_called_once_with(
            'https://api.github.com/users/user1/repos',
            headers={"Authorization": "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"}
        )

    @patch('src.github_api.requests.get')
    def test_get_repo_languages(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'Python': 100, 'JavaScript': 200}
        mock_response.headers = {'X-RateLimit-Remaining': '100'}
        mock_get.return_value = mock_response

        languages = get_repo_languages('user1', 'repo1')
        self.assertEqual(languages, {'Python': 100, 'JavaScript': 200})
        mock_get.assert_called_once_with(
            'https://api.github.com/repos/user1/repo1/languages',
            headers={"Authorization": "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"}
        )

    @patch('src.github_api.requests.get')
    def test_send_request(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'some': 'data'}
        mock_response.headers = {'X-RateLimit-Remaining': '100'}
        mock_get.return_value = mock_response

        response = send_request('https://api.github.com/some/endpoint')
        self.assertEqual(response.json(), {'some': 'data'})
        mock_get.assert_called_once_with(
            'https://api.github.com/some/endpoint',
            headers={"Authorization": "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"}
        )

    @patch('src.github_api.time.sleep', return_value=None)  # To avoid actually sleeping during tests
    def test_handle_api_rate_limit(self, mock_sleep):
        mock_response = MagicMock()
        import time
        mock_response.headers = {
            'X-RateLimit-Remaining': '1',
            'X-RateLimit-Reset': str(int(time.time()) + 10)  # Reset in 10 seconds
        }

        result = handle_api_rate_limit(mock_response)
        self.assertTrue(result)
        mock_sleep.assert_called_once()
