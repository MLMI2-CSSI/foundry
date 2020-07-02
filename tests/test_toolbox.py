from foundry import Foundry
import pytest

def test_login():
    # Login works
    # Make sure Foundry can be reached
    print('test running')
    print(open('~.globus-native-apps.cfg').read())
    f = Foundry()
    #f.get_packages()
    assert True
