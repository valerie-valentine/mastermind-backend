import pytest

@pytest.fixture
def empty_list():
    return []


def test_len_of_empty_list(empty_list):
    assert isinstance(empty_list, list)
    assert len(empty_list) == 0
