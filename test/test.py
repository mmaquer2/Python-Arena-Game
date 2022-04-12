import pytest

# run test command: pytest test.py    
# install pytest: pip3 install pytest

def test_always_passes():
    assert True

def test_always_fails():
    assert False


def sum(a,b):
    return a + b
    
def test_sum():
    
    assert sum(1,1) == 2
    

def test_level_init():
    assert True

def test_player_int():
    assert True
    
def test_cpu_init():
    assert True




