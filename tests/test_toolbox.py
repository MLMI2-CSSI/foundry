from foundry import Foundry
import pytest
#Test Toolbox
def test_login():
    # Login works
    # Make sure Foundry can be reached
    f = Foundry()
    f.get_packages()
    assert True
