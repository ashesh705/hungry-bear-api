""" Dummy test case to test repository setup"""

from src.dummy import dummy


def test_dummy() -> None:
    """Dummy test case"""

    assert dummy() is True
