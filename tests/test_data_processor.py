import pytest
from src.data_processor import query_by_language


@pytest.fixture
def test_data():
    return [
        {
            'username': 'user1',
            'repos': [
                {
                    'repo_name': 'repo1',
                    'languages': {'Python': 100, 'JavaScript': 200}
                },
                {
                    'repo_name': 'repo2',
                    'languages': {'Python': 50}
                }
            ]
        },
        {
            'username': 'user2',
            'repos': [
                {
                    'repo_name': 'repo1',
                    'languages': {'JavaScript': 300}
                },
                {
                    'repo_name': 'repo2',
                    'languages': {'Python': 100}
                }
            ]
        }
    ]


def test_query_by_language_javascript(test_data):
    assert (query_by_language(test_data, 'JavaScript') ==
            [{'language': 'JavaScript', 'lines': 300, 'username': 'user2'},
             {'language': 'JavaScript', 'lines': 200, 'username': 'user1'}])


def test_query_by_language_java(test_data):
    assert (query_by_language(test_data, 'Java') == [])


def test_query_by_language_python(test_data):
    assert (query_by_language(test_data, 'Python') ==
            [{'language': 'Python', 'lines': 150, 'username': 'user1'},
             {'language': 'Python', 'lines': 100, 'username': 'user2'}])
