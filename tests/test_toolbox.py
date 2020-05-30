from foundry import Foundry
import pytest

def test_login():
    # Login works
    # Make sure Foundry can be reached
    f = Foundry()
    f.get_packages()
    assert True
