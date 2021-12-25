from poetey import __version__
import pytest


@pytest.mark.dev
def test_version():
    assert __version__ == "0.1.0"
